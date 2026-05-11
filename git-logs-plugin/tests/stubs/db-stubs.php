<?php
/**
 * In-memory stand-ins for the wpdb-backed and PDO-backed DB stores used
 * by the Git-Logs REST controllers. Loaded BEFORE the controllers so the
 * `require_once` calls inside class-rest-*.php become no-ops.
 *
 * These stubs intentionally mirror only the methods actually called from
 * the REST layer. Persistence is global-array based and reset between
 * tests by run.php.
 */

declare( strict_types = 1 );

namespace GitLogs\DB;

defined( 'ABSPATH' ) || exit;

if ( ! class_exists( __NAMESPACE__ . '\\RepoStore' ) ) {
	final class RepoStore {
		/** @var array<int,array{id:int,slug:string,display_name:string,remote_url:?string,default_branch:string,archived:int}> */
		public static array $rows = [];
		private static int $seq = 0;

		public static function reset(): void { self::$rows = []; self::$seq = 0; }

		public static function upsert( string $slug, string $display_name, ?string $remote_url = null, string $default_branch = 'main' ): int {
			foreach ( self::$rows as &$r ) {
				if ( $r['slug'] === $slug ) {
					$r['display_name']   = $display_name;
					$r['remote_url']     = $remote_url;
					$r['default_branch'] = $default_branch;
					return $r['id'];
				}
			}
			$id = ++self::$seq;
			self::$rows[ $id ] = [
				'id'             => $id,
				'slug'           => $slug,
				'display_name'   => $display_name,
				'remote_url'     => $remote_url,
				'default_branch' => $default_branch,
				'archived'       => 0,
			];
			return $id;
		}
		public static function find_by_slug( string $slug ): ?array {
			foreach ( self::$rows as $r ) {
				if ( $r['slug'] === $slug ) return $r;
			}
			return null;
		}
		public static function list_all( bool $include_archived = false ): array {
			return array_values( array_filter(
				self::$rows,
				static fn( $r ) => $include_archived || 0 === (int) $r['archived']
			) );
		}
	}
}

if ( ! class_exists( __NAMESPACE__ . '\\RunStore' ) ) {
	final class RunStore {
		/** @var array<string,array<string,mixed>> */
		public static array $rows = [];

		public static function reset(): void { self::$rows = []; }

		public static function create( array $args ): string {
			$sha = strtolower( (string) ( $args['sha'] ?? '' ) );
			if ( ! preg_match( '/\A[0-9a-f]{40}\z/', $sha ) ) {
				throw new \InvalidArgumentException( 'sha must be 40 lowercase hex chars' );
			}
			$id = sprintf(
				'%08x-%04x-%04x-%04x-%012x',
				random_int( 0, 0xffffffff ), random_int( 0, 0xffff ),
				random_int( 0, 0xffff ),     random_int( 0, 0xffff ),
				random_int( 0, 0xffffffffffff )
			);
			self::$rows[ $id ] = array_merge( $args, [ 'id' => $id, 'sha' => $sha, 'status' => 'queued' ] );
			return $id;
		}
		public static function set_status( string $run_id, string $status, ?int $exit_code = null ): void {
			$allowed = [ 'queued', 'running', 'succeeded', 'failed', 'cancelled', 'errored' ];
			if ( ! in_array( $status, $allowed, true ) ) {
				throw new \InvalidArgumentException( "invalid status: $status" );
			}
			if ( ! isset( self::$rows[ $run_id ] ) ) {
				throw new \InvalidArgumentException( "unknown run: $run_id" );
			}
			self::$rows[ $run_id ]['status']    = $status;
			self::$rows[ $run_id ]['exit_code'] = $exit_code;
		}
		public static function find( string $run_id ): ?array {
			return self::$rows[ $run_id ] ?? null;
		}
		public static function list_recent( int $repo_id, int $limit = 50 ): array {
			$out = [];
			foreach ( self::$rows as $r ) {
				if ( (int) ( $r['repo_id'] ?? 0 ) === $repo_id ) $out[] = $r;
			}
			return array_slice( array_reverse( $out ), 0, $limit );
		}
	}
}

if ( ! class_exists( __NAMESPACE__ . '\\EventStore' ) ) {
	final class EventStore {
		public const SEVERITIES = [ 'debug', 'info', 'warn', 'error', 'fatal' ];
		/** @var array<string,array<int,array<string,mixed>>> */
		public static array $events = [];

		public static function reset(): void { self::$events = []; }

		public static function append( string $sha, string $run_id, array $events ): array {
			$key = "$sha:$run_id";
			$errors = $warns = 0;
			foreach ( $events as $e ) {
				if ( ! isset( $e['severity'] ) || ! in_array( $e['severity'], self::SEVERITIES, true ) ) {
					throw new \InvalidArgumentException( 'invalid severity' );
				}
				self::$events[ $key ][] = $e;
				if ( 'error' === $e['severity'] || 'fatal' === $e['severity'] ) $errors++;
				if ( 'warn' === $e['severity'] ) $warns++;
			}
			return [ 'appended' => count( $events ), 'errors' => $errors, 'warns' => $warns ];
		}
		public static function read( string $sha, string $run_id, int $after_seq = 0, int $limit = 500 ): array {
			$key = "$sha:$run_id";
			$rows = self::$events[ $key ] ?? [];
			$out = array_values( array_filter( $rows, static fn( $r ) => (int) ( $r['seq'] ?? 0 ) > $after_seq ) );
			return array_slice( $out, 0, $limit );
		}
		public static function finalize( string $sha, string $run_id, ?string $finished_utc = null, ?int $exit_code = null ): void {
			// no-op for tests
		}
	}
}

if ( ! class_exists( __NAMESPACE__ . '\\BranchStore' ) ) {
	final class BranchStore {
		public static array $touches = [];
		public static function reset(): void { self::$touches = []; }
		public static function touch( int $repo_id, string $name, ?string $head_sha = null ): int {
			self::$touches[] = [ $repo_id, $name, $head_sha ];
			return count( self::$touches );
		}
	}
}

if ( ! class_exists( __NAMESPACE__ . '\\AuditLog' ) ) {
	final class AuditLog {
		public static array $rows = [];
		public static function reset(): void { self::$rows = []; }
		public static function record( array $args ): int {
			self::$rows[] = $args;
			return count( self::$rows );
		}
		public static function recent( int $limit = 100, ?string $action = null ): array {
			$rows = $action
				? array_values( array_filter( self::$rows, static fn( $r ) => ( $r['action'] ?? '' ) === $action ) )
				: self::$rows;
			return array_slice( array_reverse( $rows ), 0, $limit );
		}
	}
}
