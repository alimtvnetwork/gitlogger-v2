<?php
/**
 * AuthContext — resolves the WP user behind a REST request via either lane:
 *   1. WP App Password (HTTP Basic; WP core handles validation, we just check current_user)
 *   2. Ed25519 signed request (custom, see class-ed25519-resolver.php)
 *
 * Used as `permission_callback` for protected routes.
 *
 * @package GitLogs\Auth
 */

declare( strict_types = 1 );

namespace GitLogs\Auth;

defined( 'ABSPATH' ) || exit;

require_once __DIR__ . '/class-nonce-store.php';
require_once __DIR__ . '/class-public-keys.php';
require_once __DIR__ . '/class-ed25519-resolver.php';

final class AuthContext {

	/**
	 * REST permission_callback. Returns true if either lane authenticates the request,
	 * or a WP_Error otherwise.
	 *
	 * @return bool|\WP_Error
	 */
	public static function require_authenticated( \WP_REST_Request $request ) {
		// Lane 1: App Password / cookie / any WP-core auth that already populated current_user.
		if ( is_user_logged_in() ) {
			return true;
		}

		// Lane 2: Ed25519 signed request via X-GitLogs-Auth header.
		$header = (string) $request->get_header( 'x_gitlogs_auth' );
		if ( '' !== $header ) {
			$user_id = Ed25519Resolver::resolve( $request, $header );
			if ( is_wp_error( $user_id ) ) {
				return $user_id;
			}
			wp_set_current_user( (int) $user_id );
			return true;
		}

		return new \WP_Error(
			'git_logs_unauthorized',
			__( 'Authentication required: provide WP App Password (Basic) or X-GitLogs-Auth signed header.', 'git-logs' ),
			[ 'status' => 401 ]
		);
	}
}
