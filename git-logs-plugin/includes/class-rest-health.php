<?php
/**
 * REST: GET /wp-json/git-logs/v1/health
 *
 * Phase 1 walking-skeleton endpoint. No auth required (public health probe).
 * Future phases will add authenticated endpoints behind WP App Password
 * + SSH-key signed-request middleware (spec/22 §auth).
 *
 * @package GitLogs\Rest
 */

declare( strict_types = 1 );

namespace GitLogs\Rest;

defined( 'ABSPATH' ) || exit;

final class Health {

	public static function register(): void {
		register_rest_route(
			\GitLogs\GIT_LOGS_REST_NS,
			'/health',
			[
				'methods'             => 'GET',
				'callback'            => [ self::class, 'handle' ],
				'permission_callback' => '__return_true',
			]
		);
	}

	public static function handle( \WP_REST_Request $request ): \WP_REST_Response {
		return new \WP_REST_Response(
			[
				'status'           => 'ok',
				'plugin'           => 'git-logs',
				'plugin_version'   => \GitLogs\GIT_LOGS_VERSION,
				'wp_version'       => get_bloginfo( 'version' ),
				'php_version'      => PHP_VERSION,
				'rest_namespace'   => \GitLogs\GIT_LOGS_REST_NS,
				'server_time_utc'  => gmdate( 'c' ),
			],
			200
		);
	}
}
