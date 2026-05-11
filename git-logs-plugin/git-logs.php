<?php
/**
 * Plugin Name:       Git Logs
 * Plugin URI:        https://example.com/git-logs
 * Description:       Git Logs v2 — CI run ingestion, audit, and diagram surfaces (spec/22..26).
 * Version:           0.4.0
 * Requires at least: 6.5
 * Requires PHP:      8.1
 * Author:            Git Logs Contributors
 * License:           GPL-2.0-or-later
 * Text Domain:       git-logs
 *
 * @package GitLogs
 */

declare( strict_types = 1 );

namespace GitLogs;

defined( 'ABSPATH' ) || exit;

const GIT_LOGS_VERSION    = '0.4.0';
const GIT_LOGS_REST_NS    = 'git-logs/v1';
const GIT_LOGS_PLUGIN_DIR = __DIR__;

require_once __DIR__ . '/includes/class-rest-health.php';
require_once __DIR__ . '/includes/class-admin-page.php';
require_once __DIR__ . '/includes/rest/class-rest-whoami.php';
require_once __DIR__ . '/includes/rest/class-rest-keys.php';
require_once __DIR__ . '/includes/rest/class-rest-admin-migrate.php';
require_once __DIR__ . '/includes/rest/class-rest-admin-gc.php';
require_once __DIR__ . '/includes/rest/class-rest-repos.php';
require_once __DIR__ . '/includes/rest/class-rest-runs.php';
require_once __DIR__ . '/includes/rest/class-rest-audit.php';
require_once __DIR__ . '/includes/rest/class-rest-admin-diagrams.php';
require_once __DIR__ . '/includes/db/class-migration-runner.php';

add_action( 'rest_api_init', [ Rest\Health::class,        'register' ] );
add_action( 'rest_api_init', [ Rest\Whoami::class,        'register' ] );
add_action( 'rest_api_init', [ Rest\Keys::class,          'register' ] );
add_action( 'rest_api_init', [ Rest\AdminMigrate::class,  'register' ] );
add_action( 'rest_api_init', [ Rest\AdminGc::class,       'register' ] );
add_action( 'rest_api_init', [ Rest\Repos::class,         'register' ] );
add_action( 'rest_api_init', [ Rest\Runs::class,          'register' ] );
add_action( 'rest_api_init', [ Rest\Audit::class,         'register' ] );
add_action( 'rest_api_init', [ Rest\Admin_Diagrams::class, 'register' ] );
add_action( 'admin_menu',           [ Admin\Page::class, 'register' ] );
add_action( 'admin_enqueue_scripts', [ Admin\Page::class, 'enqueue'  ] );

register_activation_hook( __FILE__, static function (): void {
	DB\MigrationRunner::migrate();
} );

add_action( 'upgrader_process_complete', static function ( $upgrader, array $hook_extra ): void {
	if ( 'plugin' !== ( $hook_extra['type'] ?? '' ) ) {
		return;
	}
	$plugins = $hook_extra['plugins'] ?? [];
	$me      = plugin_basename( __FILE__ );
	if ( in_array( $me, (array) $plugins, true ) ) {
		DB\MigrationRunner::migrate();
	}
}, 10, 2 );
