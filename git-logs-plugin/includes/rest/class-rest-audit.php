<?php
/**
 * REST: GET /wp-json/git-logs/v1/audit
 *
 * Admin-only. Filters: action, limit (≤500).
 *
 * @package GitLogs\Rest
 */

declare( strict_types = 1 );

namespace GitLogs\Rest;

defined( 'ABSPATH' ) || exit;

require_once __DIR__ . '/../auth/class-auth-context.php';
require_once __DIR__ . '/../db/class-audit-log.php';

final class Audit {

	public static function register(): void {
		register_rest_route(
			\GitLogs\GIT_LOGS_REST_NS,
			'/audit',
			[
				'methods'             => 'GET',
				'callback'            => [ self::class, 'list_entries' ],
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

	public static function list_entries( \WP_REST_Request $r ): \WP_REST_Response {
		$action = $r->get_param( 'action' );
		$limit  = max( 1, min( 500, (int) ( $r->get_param( 'limit' ) ?? 100 ) ) );
		return new \WP_REST_Response( [
			'entries' => \GitLogs\DB\AuditLog::recent( $limit, $action ? (string) $action : null ),
		], 200 );
	}
}
