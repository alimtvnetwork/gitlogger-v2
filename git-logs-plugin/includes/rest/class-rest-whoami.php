<?php
/**
 * REST: GET /wp-json/git-logs/v1/whoami
 *
 * Authenticated. Returns the current user's id, login, display_name, and which
 * auth lane resolved the request. Used by `glci whoami` and the admin UI.
 *
 * @package GitLogs\Rest
 */

declare( strict_types = 1 );

namespace GitLogs\Rest;

defined( 'ABSPATH' ) || exit;

require_once __DIR__ . '/../auth/class-auth-context.php';

final class Whoami {

	public static function register(): void {
		register_rest_route(
			\GitLogs\GIT_LOGS_REST_NS,
			'/whoami',
			[
				'methods'             => 'GET',
				'callback'            => [ self::class, 'handle' ],
				'permission_callback' => [ \GitLogs\Auth\AuthContext::class, 'require_authenticated' ],
			]
		);
	}

	public static function handle( \WP_REST_Request $request ): \WP_REST_Response {
		$user = wp_get_current_user();
		$lane = '' !== (string) $request->get_header( 'x_gitlogs_auth' ) ? 'ed25519' : 'wp_session';

		return new \WP_REST_Response(
			[
				'user_id'         => (int) $user->ID,
				'user_login'      => $user->user_login,
				'display_name'    => $user->display_name,
				'roles'           => array_values( (array) $user->roles ),
				'auth_lane'       => $lane,
				'server_time_utc' => gmdate( 'c' ),
			],
			200
		);
	}
}
