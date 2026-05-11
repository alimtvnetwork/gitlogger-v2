<?php
/**
 * Admin page registration + asset enqueue for the React/TS admin UI bundle.
 *
 * @package GitLogs\Admin
 */

declare( strict_types = 1 );

namespace GitLogs\Admin;

defined( 'ABSPATH' ) || exit;

final class Page {

	public const SLUG       = 'git-logs';
	public const SCRIPT_ID  = 'git-logs-admin-ui';
	public const STYLE_ID   = 'git-logs-admin-ui';

	public static function register(): void {
		add_menu_page(
			__( 'Git Logs', 'git-logs' ),
			__( 'Git Logs', 'git-logs' ),
			'manage_options',
			self::SLUG,
			[ self::class, 'render' ],
			'dashicons-chart-line',
			58
		);
	}

	public static function render(): void {
		echo '<div class="wrap"><div id="git-logs-admin-root"></div></div>';
	}

	public static function enqueue( string $hook ): void {
		if ( 'toplevel_page_' . self::SLUG !== $hook ) {
			return;
		}

		$asset_file = \GitLogs\GIT_LOGS_PLUGIN_DIR . '/admin-ui/dist/index.js';
		$style_file = \GitLogs\GIT_LOGS_PLUGIN_DIR . '/admin-ui/dist/index.css';

		if ( file_exists( $asset_file ) ) {
			wp_enqueue_script(
				self::SCRIPT_ID,
				plugins_url( 'admin-ui/dist/index.js', \GitLogs\GIT_LOGS_PLUGIN_DIR . '/git-logs.php' ),
				[],
				\GitLogs\GIT_LOGS_VERSION,
				true
			);
			wp_localize_script(
				self::SCRIPT_ID,
				'GitLogsBoot',
				[
					'restRoot'  => esc_url_raw( rest_url( \GitLogs\GIT_LOGS_REST_NS ) ),
					'nonce'     => wp_create_nonce( 'wp_rest' ),
					'version'   => \GitLogs\GIT_LOGS_VERSION,
				]
			);
		}

		if ( file_exists( $style_file ) ) {
			wp_enqueue_style(
				self::STYLE_ID,
				plugins_url( 'admin-ui/dist/index.css', \GitLogs\GIT_LOGS_PLUGIN_DIR . '/git-logs.php' ),
				[],
				\GitLogs\GIT_LOGS_VERSION
			);
		}
	}
}
