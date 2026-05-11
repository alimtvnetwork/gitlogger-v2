<?php
/**
 * Database — SQLite connection factory + storage paths.
 *
 * Layout under wp-content/uploads/git-logs/:
 *
 *   db/
 *     root.sqlite              — repos, branches, runs, sha_index, audit, schema_migrations
 *     sha/<sha40>.sqlite       — per-commit DB: events, summary
 *
 * All connections use PDO with PRAGMAs:
 *   journal_mode = WAL    (concurrent readers + 1 writer)
 *   synchronous  = NORMAL (WAL-safe, faster than FULL)
 *   foreign_keys = ON
 *   busy_timeout = 5000   (5s lock-retry window)
 *
 * @package GitLogs\DB
 */

declare( strict_types = 1 );

namespace GitLogs\DB;

defined( 'ABSPATH' ) || exit;

final class Database {

	private static ?\PDO $root = null;
	/** @var array<string,\PDO> */
	private static array $sha_conns = [];

	public static function root(): \PDO {
		if ( null === self::$root ) {
			self::ensure_dirs();
			self::$root = self::open( self::root_path() );
		}
		return self::$root;
	}

	public static function sha( string $sha ): \PDO {
		$sha = self::normalize_sha( $sha );
		if ( ! isset( self::$sha_conns[ $sha ] ) ) {
			self::ensure_dirs();
			$pdo = self::open( self::sha_path( $sha ) );
			self::ensure_sha_schema( $pdo );
			self::$sha_conns[ $sha ] = $pdo;
		}
		return self::$sha_conns[ $sha ];
	}

	public static function root_path(): string {
		return self::base_dir() . '/db/root.sqlite';
	}

	public static function sha_path( string $sha ): string {
		$sha = self::normalize_sha( $sha );
		return self::base_dir() . '/db/sha/' . $sha . '.sqlite';
	}

	public static function base_dir(): string {
		$uploads = wp_get_upload_dir();
		return rtrim( (string) $uploads['basedir'], '/' ) . '/git-logs';
	}

	public static function ensure_dirs(): void {
		$base = self::base_dir();
		foreach ( [ $base, $base . '/db', $base . '/db/sha' ] as $d ) {
			if ( ! is_dir( $d ) ) {
				wp_mkdir_p( $d );
			}
		}
		// Deny direct HTTP access to the DB dir.
		$ht = $base . '/db/.htaccess';
		if ( ! file_exists( $ht ) ) {
			file_put_contents( $ht, "Require all denied\n" );
		}
		$idx = $base . '/db/index.html';
		if ( ! file_exists( $idx ) ) {
			file_put_contents( $idx, '' );
		}
	}

	public static function reset_for_tests(): void {
		self::$root      = null;
		self::$sha_conns = [];
	}

	private static function open( string $path ): \PDO {
		$pdo = new \PDO( 'sqlite:' . $path );
		$pdo->setAttribute( \PDO::ATTR_ERRMODE, \PDO::ERRMODE_EXCEPTION );
		$pdo->setAttribute( \PDO::ATTR_DEFAULT_FETCH_MODE, \PDO::FETCH_ASSOC );
		$pdo->exec( 'PRAGMA journal_mode = WAL' );
		$pdo->exec( 'PRAGMA synchronous  = NORMAL' );
		$pdo->exec( 'PRAGMA foreign_keys = ON' );
		$pdo->exec( 'PRAGMA busy_timeout = 5000' );
		return $pdo;
	}

	private static function ensure_sha_schema( \PDO $pdo ): void {
		// Per-SHA schema is fixed (single migration), created on first open.
		$pdo->exec(
			"CREATE TABLE IF NOT EXISTS events (
				id              INTEGER PRIMARY KEY AUTOINCREMENT,
				run_id          TEXT    NOT NULL,
				seq             INTEGER NOT NULL,
				ts_utc          TEXT    NOT NULL,
				stream          TEXT    NOT NULL CHECK (stream IN ('stdout','stderr','meta')),
				phase           TEXT    NOT NULL,
				severity        TEXT    NOT NULL CHECK (severity IN ('debug','info','warn','error','fatal')),
				message         TEXT    NOT NULL,
				attrs_json      TEXT,
				UNIQUE (run_id, seq)
			);
			CREATE INDEX IF NOT EXISTS idx_events_run ON events(run_id, seq);
			CREATE INDEX IF NOT EXISTS idx_events_sev ON events(run_id, severity);

			CREATE TABLE IF NOT EXISTS summary (
				run_id          TEXT PRIMARY KEY,
				started_utc     TEXT NOT NULL,
				finished_utc    TEXT,
				exit_code       INTEGER,
				event_count     INTEGER NOT NULL DEFAULT 0,
				error_count     INTEGER NOT NULL DEFAULT 0,
				warn_count      INTEGER NOT NULL DEFAULT 0
			);"
		);
	}

	private static function normalize_sha( string $sha ): string {
		$sha = strtolower( trim( $sha ) );
		if ( ! preg_match( '/\A[0-9a-f]{40}\z/', $sha ) ) {
			throw new \InvalidArgumentException( 'sha must be 40 lowercase hex chars' );
		}
		return $sha;
	}
}
