<?php
/**
 * DB-layer test bootstrap.
 *
 * Unlike tests/bootstrap.php (which pre-loads in-memory stubs to exercise
 * the auth + REST layers), this bootstrap installs only the WordPress
 * helper shims the production DB classes actually call, then loads the
 * REAL Database / RepoStore / RunStore / EventStore / BranchStore /
 * ShaIndex / AuditLog / MigrationRunner against a per-process scratch
 * directory under `/tmp`.
 */

declare( strict_types = 1 );

if ( ! defined( 'ABSPATH' ) ) {
	define( 'ABSPATH', __DIR__ . '/' );
}

// Per-process upload directory under /tmp. Each test resets it via
// reset_db_state() so DBs start empty.
$GLOBALS['__upload_basedir'] = sys_get_temp_dir() . '/git-logs-tests-' . getmypid();

if ( ! function_exists( 'wp_get_upload_dir' ) ) {
	function wp_get_upload_dir(): array {
		return [ 'basedir' => $GLOBALS['__upload_basedir'] ];
	}
}
if ( ! function_exists( 'wp_mkdir_p' ) ) {
	function wp_mkdir_p( string $dir ): bool {
		return is_dir( $dir ) || mkdir( $dir, 0o755, true );
	}
}
if ( ! function_exists( 'wp_json_encode' ) ) {
	function wp_json_encode( $data, int $opts = 0, int $depth = 512 ): string {
		return json_encode( $data, $opts, $depth );
	}
}
if ( ! function_exists( '__' ) ) {
	function __( string $s, string $domain = '' ): string { return $s; }
}

// --- Load production DB classes (no stubs) ----------------------------
require_once __DIR__ . '/../includes/db/class-database.php';
require_once __DIR__ . '/../includes/db/class-sha-index.php';
require_once __DIR__ . '/../includes/db/class-repo-store.php';
require_once __DIR__ . '/../includes/db/class-run-store.php';
require_once __DIR__ . '/../includes/db/class-branch-store.php';
require_once __DIR__ . '/../includes/db/class-event-store.php';
require_once __DIR__ . '/../includes/db/class-audit-log.php';
require_once __DIR__ . '/../includes/db/class-migration-runner.php';

/**
 * Wipe and re-create the scratch upload dir, then close all PDO handles
 * so the next root()/sha() call re-opens against the empty filesystem.
 */
function reset_db_state(): void {
	$base = $GLOBALS['__upload_basedir'];
	if ( is_dir( $base ) ) {
		$it = new RecursiveIteratorIterator(
			new RecursiveDirectoryIterator( $base, FilesystemIterator::SKIP_DOTS ),
			RecursiveIteratorIterator::CHILD_FIRST
		);
		foreach ( $it as $f ) {
			$f->isDir() ? rmdir( $f->getPathname() ) : unlink( $f->getPathname() );
		}
		rmdir( $base );
	}
	\GitLogs\DB\Database::reset_for_tests();
}

/** Apply all migrations against a fresh root DB. */
function migrate_fresh(): void {
	reset_db_state();
	$result = \GitLogs\DB\MigrationRunner::migrate();
	if ( null !== $result['failed'] ) {
		throw new \RuntimeException( 'migrate_fresh: ' . $result['failed'] );
	}
}

register_shutdown_function( static function (): void {
	if ( is_dir( $GLOBALS['__upload_basedir'] ) ) {
		$it = new RecursiveIteratorIterator(
			new RecursiveDirectoryIterator( $GLOBALS['__upload_basedir'], FilesystemIterator::SKIP_DOTS ),
			RecursiveIteratorIterator::CHILD_FIRST
		);
		foreach ( $it as $f ) {
			$f->isDir() ? @rmdir( $f->getPathname() ) : @unlink( $f->getPathname() );
		}
		@rmdir( $GLOBALS['__upload_basedir'] );
	}
} );
