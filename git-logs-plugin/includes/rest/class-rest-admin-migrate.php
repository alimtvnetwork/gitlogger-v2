<?php
/**
 * REST: POST /wp-json/git-logs/v1/admin/migrate
 *      GET  /wp-json/git-logs/v1/admin/migrate (status only)
 *
 * Admin-only. Idempotent. Useful for ops + plugin-update flows where the
 * activation hook didn't fire (e.g. WP-CLI deploys, multisite network admin).
 *
 * @package GitLogs\Rest
 */

declare( strict_types = 1 );

namespace GitLogs\Rest;

defined( 'ABSPATH' ) || exit;

require_once __DIR__ . '/../auth/class-auth-context.php';
require_once __DIR__ . '/../db/class-migration-runner.php';
require_once __DIR__ . '/../db/class-audit-log.php';

final class AdminMigrate {

	public static function register(): void {
		register_rest_route(
			\GitLogs\GIT_LOGS_REST_NS,
			'/admin/migrate',
			[
				[
					'methods'             => 'GET',
					'callback'            => [ self::class, 'status' ],
					'permission_callback' => [ self::class, 'require_admin' ],
				],
				[
					'methods'             => 'POST',
					'callback'            => [ self::class, 'run' ],
					'permission_callback' => [ self::class, 'require_admin' ],
				],
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

	public static function status( \WP_REST_Request $r ): \WP_REST_Response {
		return new \WP_REST_Response( [
			'applied' => \GitLogs\DB\MigrationRunner::applied_versions(),
		], 200 );
	}

	public static function run( \WP_REST_Request $r ): \WP_REST_Response {
		$result = \GitLogs\DB\MigrationRunner::migrate();
		\GitLogs\DB\AuditLog::record( [
			'action'        => 'admin.migrate',
			'result'        => null === $result['failed'] ? 'ok' : 'error',
			'actor_user_id' => get_current_user_id(),
			'actor_login'   => wp_get_current_user()->user_login ?: null,
			'auth_lane'     => '' !== (string) $r->get_header( 'x_gitlogs_auth' ) ? 'ed25519' : 'wp_session',
			'detail'        => $result,
		] );
		$status = null === $result['failed'] ? 200 : 500;
		return new \WP_REST_Response( $result, $status );
	}
}
