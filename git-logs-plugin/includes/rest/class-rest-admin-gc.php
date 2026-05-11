<?php
/**
 * REST: POST /wp-json/git-logs/v1/admin/gc
 *
 * Admin-only. Garbage-collects per-SHA SQLite files older than `older_than_days`
 * (default 90) **and** not referenced by any non-archived run within the cutoff.
 *
 * Body (JSON, optional):
 *   { "older_than_days": 90, "dry_run": true }
 *
 * @package GitLogs\Rest
 */

declare( strict_types = 1 );

namespace GitLogs\Rest;

defined( 'ABSPATH' ) || exit;

require_once __DIR__ . '/../auth/class-auth-context.php';
require_once __DIR__ . '/../db/class-database.php';
require_once __DIR__ . '/../db/class-audit-log.php';

final class AdminGc {

	public static function register(): void {
		register_rest_route(
			\GitLogs\GIT_LOGS_REST_NS,
			'/admin/gc',
			[
				'methods'             => 'POST',
				'callback'            => [ self::class, 'run' ],
				'permission_callback' => [ self::class, 'require_admin' ],
			]
		);
	}

	public static function require_admin( \WP_REST_Request $r ) {
		$ok = \GitLogs\Auth\AuthContext::require_authenticated( $r );
		if ( true !== $ok ) {
			return $ok;
		}
		if ( ! current_user_can( 'manage_options' ) ) {
			return new \WP_Error( 'git_logs_forbidden', 'manage_options capability required', [ 'status' => 403 ] );
		}
		return true;
	}

	public static function run( \WP_REST_Request $r ): \WP_REST_Response {
		$body    = json_decode( (string) $r->get_body(), true );
		$days    = (int) ( $body['older_than_days'] ?? 90 );
		$dry_run = (bool) ( $body['dry_run'] ?? true );
		$days    = max( 1, min( 3650, $days ) );

		$cutoff_ts = time() - ( $days * 86400 );
		$root      = \GitLogs\DB\Database::root();

		// Active SHAs = anything in sha_index whose run is from a non-archived repo
		// and whose run was created within the cutoff. Everything else is GC-eligible.
		$keep = $root->prepare(
			'SELECT DISTINCT si.sha
			   FROM sha_index si
			   JOIN runs  r ON r.id      = si.run_id
			   JOIN repos p ON p.id      = r.repo_id
			  WHERE p.archived = 0
			    AND ( r.started_utc >= :cutoff OR r.status IN ("queued","running") )'
		);
		$keep->execute( [ ':cutoff' => gmdate( 'c', $cutoff_ts ) ] );
		$keep_set = array_fill_keys( array_map( static fn( $r ) => (string) $r['sha'], $keep->fetchAll() ), true );

		$sha_dir   = \GitLogs\DB\Database::base_dir() . '/db/sha';
		$files     = is_dir( $sha_dir ) ? glob( $sha_dir . '/*.sqlite' ) : [];
		$candidates = [];
		$bytes      = 0;

		foreach ( (array) $files as $path ) {
			$sha = strtolower( basename( $path, '.sqlite' ) );
			if ( ! preg_match( '/\A[0-9a-f]{40}\z/', $sha ) ) {
				continue;
			}
			if ( isset( $keep_set[ $sha ] ) ) {
				continue;
			}
			$mtime = (int) filemtime( $path );
			if ( $mtime > $cutoff_ts ) {
				continue;
			}
			$candidates[] = $sha;
			$bytes       += (int) filesize( $path );
			if ( ! $dry_run ) {
				@unlink( $path );
				// Companion WAL/SHM files.
				@unlink( $path . '-wal' );
				@unlink( $path . '-shm' );
				$root->prepare( 'DELETE FROM sha_index WHERE sha = :s' )->execute( [ ':s' => $sha ] );
			}
		}

		\GitLogs\DB\AuditLog::record( [
			'action'        => 'admin.gc',
			'result'        => 'ok',
			'actor_user_id' => get_current_user_id(),
			'actor_login'   => wp_get_current_user()->user_login ?: null,
			'auth_lane'     => '' !== (string) $r->get_header( 'x_gitlogs_auth' ) ? 'ed25519' : 'wp_session',
			'detail'        => [ 'older_than_days' => $days, 'dry_run' => $dry_run, 'count' => count( $candidates ), 'bytes' => $bytes ],
		] );

		return new \WP_REST_Response( [
			'dry_run'        => $dry_run,
			'older_than_days'=> $days,
			'count'          => count( $candidates ),
			'bytes_freed'    => $bytes,
			'shas'           => $candidates,
		], 200 );
	}
}
