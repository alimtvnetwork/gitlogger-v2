<?php
/**
 * MigrationRunner — applies SQL files from includes/db/migrations/ in order.
 *
 * Each file is named NNNN_<slug>.sql (e.g. 0001_root_schema.sql). Applied
 * versions and their SHA-256 checksums are recorded in schema_migrations.
 * If a previously-applied file has changed on disk, the runner aborts
 * (developer must add a new migration, never edit historical ones).
 *
 * @package GitLogs\DB
 */

declare( strict_types = 1 );

namespace GitLogs\DB;

defined( 'ABSPATH' ) || exit;

require_once __DIR__ . '/class-database.php';

final class MigrationRunner {

	public const MIGRATIONS_DIR = __DIR__ . '/migrations';

	/**
	 * @return array{applied: list<string>, skipped: list<string>, failed: ?string}
	 */
	public static function migrate(): array {
		$pdo = Database::root();

		// Bootstrap schema_migrations so we can record the very first migration.
		$pdo->exec(
			'CREATE TABLE IF NOT EXISTS schema_migrations (
				version     TEXT PRIMARY KEY,
				applied_utc TEXT NOT NULL,
				checksum    TEXT NOT NULL
			)'
		);

		$files = glob( self::MIGRATIONS_DIR . '/[0-9]*.sql' ) ?: [];
		sort( $files, SORT_STRING );

		$applied = [];
		$skipped = [];

		foreach ( $files as $file ) {
			$version  = basename( $file, '.sql' );
			$contents = (string) file_get_contents( $file );
			$checksum = hash( 'sha256', $contents );

			$row = $pdo->prepare( 'SELECT checksum FROM schema_migrations WHERE version = :v' );
			$row->execute( [ ':v' => $version ] );
			$existing = $row->fetchColumn();

			if ( false !== $existing ) {
				if ( $existing !== $checksum ) {
					return [
						'applied' => $applied,
						'skipped' => $skipped,
						'failed'  => sprintf(
							'migration %s has been edited after being applied (checksum mismatch). Add a new migration instead of modifying %s.',
							$version,
							basename( $file )
						),
					];
				}
				$skipped[] = $version;
				continue;
			}

			try {
				$pdo->beginTransaction();
				$pdo->exec( $contents );
				$ins = $pdo->prepare(
					'INSERT INTO schema_migrations (version, applied_utc, checksum) VALUES (:v, :t, :c)'
				);
				$ins->execute( [
					':v' => $version,
					':t' => gmdate( 'c' ),
					':c' => $checksum,
				] );
				$pdo->commit();
				$applied[] = $version;
			} catch ( \Throwable $e ) {
				if ( $pdo->inTransaction() ) {
					$pdo->rollBack();
				}
				return [
					'applied' => $applied,
					'skipped' => $skipped,
					'failed'  => sprintf( 'migration %s failed: %s', $version, $e->getMessage() ),
				];
			}
		}

		return [ 'applied' => $applied, 'skipped' => $skipped, 'failed' => null ];
	}

	/** @return list<string> versions currently recorded as applied */
	public static function applied_versions(): array {
		$pdo = Database::root();
		$pdo->exec(
			'CREATE TABLE IF NOT EXISTS schema_migrations (
				version     TEXT PRIMARY KEY,
				applied_utc TEXT NOT NULL,
				checksum    TEXT NOT NULL
			)'
		);
		$rows = $pdo->query( 'SELECT version FROM schema_migrations ORDER BY version' )->fetchAll();
		return array_map( static fn( $r ) => (string) $r['version'], $rows );
	}
}
