<?php
/**
 * Database / MigrationRunner — schema bootstrap and idempotency.
 */

declare( strict_types = 1 );

use GitLogs\DB\Database;
use GitLogs\DB\MigrationRunner;

function dbtest_migrate_creates_root_schema_and_records_version(): void {
	$pdo = Database::root();
	$tables = $pdo->query(
		"SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
	)->fetchAll( PDO::FETCH_COLUMN );
	foreach ( [ 'audit', 'branches', 'repos', 'runs', 'schema_migrations', 'sha_index' ] as $t ) {
		assertTrue( in_array( $t, $tables, true ), "missing table: $t" );
	}
	assertSame( [ '0001_root_schema' ], MigrationRunner::applied_versions() );
}

function dbtest_migrate_is_idempotent(): void {
	$first = MigrationRunner::migrate();
	assertSame( null, $first['failed'] );
	assertSame( 0, count( $first['applied'] ) );
	assertSame( 1, count( $first['skipped'] ) );
}

function dbtest_migrate_detects_tampered_migration(): void {
	$pdo = Database::root();
	$pdo->prepare( 'UPDATE schema_migrations SET checksum = :c WHERE version = :v' )
	    ->execute( [ ':c' => 'tampered', ':v' => '0001_root_schema' ] );
	$result = MigrationRunner::migrate();
	assertNotNull( $result['failed'] );
	assertTrue( str_contains( $result['failed'], 'checksum mismatch' ) );
}

function dbtest_database_pragmas_applied(): void {
	$pdo = Database::root();
	$jm = (string) $pdo->query( 'PRAGMA journal_mode' )->fetchColumn();
	assertSame( 'wal', strtolower( $jm ) );
	$fk = (string) $pdo->query( 'PRAGMA foreign_keys' )->fetchColumn();
	assertSame( '1', $fk );
}

function dbtest_sha_normalisation_rejects_garbage(): void {
	assertThrows( static function () { Database::sha( 'not-a-sha' ); }, '40 lowercase hex' );
	assertThrows( static function () { Database::sha( str_repeat( 'g', 40 ) ); }, '40 lowercase hex' );
}

function dbtest_sha_db_creates_per_commit_schema(): void {
	$sha = str_repeat( 'a', 40 );
	$pdo = Database::sha( $sha );
	$tables = $pdo->query(
		"SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
	)->fetchAll( PDO::FETCH_COLUMN );
	assertTrue( in_array( 'events',  $tables, true ) );
	assertTrue( in_array( 'summary', $tables, true ) );
	assertTrue( file_exists( Database::sha_path( $sha ) ) );
}

function dbtest_ensure_dirs_writes_htaccess(): void {
	Database::ensure_dirs();
	$ht = Database::base_dir() . '/db/.htaccess';
	assertTrue( file_exists( $ht ) );
	assertTrue( str_contains( (string) file_get_contents( $ht ), 'Require all denied' ) );
}
