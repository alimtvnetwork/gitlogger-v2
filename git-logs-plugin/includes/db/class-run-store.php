<?php
/**
 * RunStore — CRUD for the `runs` table + sha_index linkage.
 *
 * Status state machine:
 *   queued → running → (succeeded|failed|cancelled|timed_out)
 *
 * @package GitLogs\DB
 */

declare( strict_types = 1 );

namespace GitLogs\DB;

defined( 'ABSPATH' ) || exit;

require_once __DIR__ . '/class-database.php';
require_once __DIR__ . '/class-sha-index.php';

final class RunStore {

	public const ALLOWED_STATUS = [ 'queued', 'running', 'succeeded', 'failed', 'cancelled', 'timed_out' ];

	/**
	 * Create a new run. Returns the generated UUIDv4 id.
	 *
	 * @param array{
	 *   repo_id:int, branch:string, sha:string, ci_provider:string,
	 *   ci_run_url?:?string, triggered_by?:?string, metadata?:?array<mixed>
	 * } $args
	 */
	public static function create( array $args ): string {
		$pdo = Database::root();
		$id  = self::uuid_v4();
		$now = gmdate( 'c' );

		$stmt = $pdo->prepare(
			'INSERT INTO runs
				(id, repo_id, branch, sha, ci_provider, ci_run_url, triggered_by, status, started_utc, metadata_json)
			 VALUES
				(:id, :repo, :branch, :sha, :prov, :url, :by, :status, :start, :meta)'
		);
		$stmt->execute( [
			':id'     => $id,
			':repo'   => $args['repo_id'],
			':branch' => $args['branch'],
			':sha'    => strtolower( $args['sha'] ),
			':prov'   => $args['ci_provider'],
			':url'    => $args['ci_run_url']    ?? null,
			':by'     => $args['triggered_by']  ?? null,
			':status' => 'queued',
			':start'  => $now,
			':meta'   => isset( $args['metadata'] ) ? wp_json_encode( $args['metadata'] ) : null,
		] );

		ShaIndex::add( $args['sha'], $id, (int) $args['repo_id'] );
		return $id;
	}

	public static function set_status( string $run_id, string $status, ?int $exit_code = null ): void {
		if ( ! in_array( $status, self::ALLOWED_STATUS, true ) ) {
			throw new \InvalidArgumentException( "invalid status: $status" );
		}
		$pdo  = Database::root();
		$now  = gmdate( 'c' );
		$is_terminal = in_array( $status, [ 'succeeded', 'failed', 'cancelled', 'timed_out' ], true );

		$sql = 'UPDATE runs SET status = :s';
		if ( null !== $exit_code ) {
			$sql .= ', exit_code = :ec';
		}
		if ( $is_terminal ) {
			$sql .= ", finished_utc = :fin, duration_ms = (CAST((julianday(:fin) - julianday(started_utc)) * 86400000 AS INTEGER))";
		}
		$sql .= ' WHERE id = :id';

		$params = [ ':s' => $status, ':id' => $run_id ];
		if ( null !== $exit_code )  { $params[':ec']  = $exit_code; }
		if ( $is_terminal )         { $params[':fin'] = $now; }

		$pdo->prepare( $sql )->execute( $params );
	}

	public static function update_counts( string $run_id, int $events, int $errors, int $warns ): void {
		$pdo  = Database::root();
		$stmt = $pdo->prepare(
			'UPDATE runs SET event_count = :e, error_count = :er, warn_count = :w WHERE id = :id'
		);
		$stmt->execute( [ ':e' => $events, ':er' => $errors, ':w' => $warns, ':id' => $run_id ] );
	}

	/** @return array<string,mixed>|null */
	public static function find( string $run_id ): ?array {
		$pdo  = Database::root();
		$stmt = $pdo->prepare( 'SELECT * FROM runs WHERE id = :id' );
		$stmt->execute( [ ':id' => $run_id ] );
		$row = $stmt->fetch();
		return false === $row ? null : $row;
	}

	/**
	 * @return list<array<string,mixed>>
	 */
	public static function list_recent( int $repo_id, int $limit = 50 ): array {
		$pdo  = Database::root();
		$stmt = $pdo->prepare(
			'SELECT * FROM runs WHERE repo_id = :r ORDER BY started_utc DESC LIMIT :lim'
		);
		$stmt->bindValue( ':r',   $repo_id, \PDO::PARAM_INT );
		$stmt->bindValue( ':lim', $limit,   \PDO::PARAM_INT );
		$stmt->execute();
		return $stmt->fetchAll();
	}

	private static function uuid_v4(): string {
		$d = random_bytes( 16 );
		$d[6] = chr( ( ord( $d[6] ) & 0x0f ) | 0x40 );
		$d[8] = chr( ( ord( $d[8] ) & 0x3f ) | 0x80 );
		return vsprintf( '%s%s-%s-%s-%s-%s%s%s', str_split( bin2hex( $d ), 4 ) );
	}
}
