<?php
/**
 * REST: /wp-json/git-logs/v1/repos
 *
 *   GET  /repos                      list (query: include_archived=0|1)
 *   POST /repos                      upsert by slug
 *
 * @package GitLogs\Rest
 */

declare( strict_types = 1 );

namespace GitLogs\Rest;

defined( 'ABSPATH' ) || exit;

require_once __DIR__ . '/../auth/class-auth-context.php';
require_once __DIR__ . '/../db/class-repo-store.php';
require_once __DIR__ . '/../db/class-audit-log.php';

final class Repos {

	public static function register(): void {
		$ns   = \GitLogs\GIT_LOGS_REST_NS;
		$auth = [ \GitLogs\Auth\AuthContext::class, 'require_authenticated' ];

		register_rest_route( $ns, '/repos', [
			[
				'methods'             => 'GET',
				'callback'            => [ self::class, 'list_repos' ],
				'permission_callback' => $auth,
			],
			[
				'methods'             => 'POST',
				'callback'            => [ self::class, 'upsert' ],
				'permission_callback' => $auth,
				'args'                => [
					'slug'           => [ 'required' => true,  'type' => 'string' ],
					'display_name'   => [ 'required' => true,  'type' => 'string' ],
					'remote_url'     => [ 'required' => false, 'type' => 'string' ],
					'default_branch' => [ 'required' => false, 'type' => 'string' ],
				],
			],
		] );
	}

	public static function list_repos( \WP_REST_Request $r ): \WP_REST_Response {
		$include = '1' === (string) $r->get_param( 'include_archived' );
		return new \WP_REST_Response( [
			'repos' => \GitLogs\DB\RepoStore::list_all( $include ),
		], 200 );
	}

	public static function upsert( \WP_REST_Request $r ): \WP_REST_Response {
		$slug = sanitize_key( (string) $r->get_param( 'slug' ) );
		if ( '' === $slug || ! preg_match( '#\A[a-z0-9][a-z0-9._/-]{0,127}\z#', $slug ) ) {
			return new \WP_REST_Response( [ 'error' => 'invalid slug (allowed: [a-z0-9._/-], 1..128)' ], 400 );
		}
		$id = \GitLogs\DB\RepoStore::upsert(
			$slug,
			(string) $r->get_param( 'display_name' ),
			$r->get_param( 'remote_url' ),
			(string) ( $r->get_param( 'default_branch' ) ?: 'main' )
		);
		\GitLogs\DB\AuditLog::record( [
			'action'        => 'repo.upsert',
			'result'        => 'ok',
			'target_type'   => 'repo',
			'target_id'     => (string) $id,
			'actor_user_id' => get_current_user_id(),
			'actor_login'   => wp_get_current_user()->user_login ?: null,
			'auth_lane'     => '' !== (string) $r->get_header( 'x_gitlogs_auth' ) ? 'ed25519' : 'wp_session',
			'detail'        => [ 'slug' => $slug ],
		] );
		return new \WP_REST_Response( [ 'id' => $id, 'slug' => $slug ], 201 );
	}
}
