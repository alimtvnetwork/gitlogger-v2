<?php
/**
 * Plugin Name:       Git Logs
 * Plugin URI:        https://example.com/git-logs
 * Description:       Git Logs v2 — CI run ingestion, audit, and diagram surfaces (spec/22..26).
 * Version:           0.1.0
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

const GIT_LOGS_VERSION    = '0.1.0';
const GIT_LOGS_REST_NS    = 'git-logs/v1';
const GIT_LOGS_PLUGIN_DIR = __DIR__;

require_once __DIR__ . '/includes/class-rest-health.php';
require_once __DIR__ . '/includes/class-admin-page.php';

add_action( 'rest_api_init', [ Rest\Health::class, 'register' ] );
add_action( 'admin_menu',    [ Admin\Page::class, 'register' ] );
add_action( 'admin_enqueue_scripts', [ Admin\Page::class, 'enqueue' ] );
