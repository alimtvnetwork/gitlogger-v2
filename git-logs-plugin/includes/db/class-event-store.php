<?php
/**
 * EventStore — append events into per-SHA SQLite DBs and read them back.
 *
 * The per-SHA file is opened (and its `events` + `summary` tables created on
 * first touch) by Database::sha(). EventStore wraps that PDO with batched
 * inserts and summary recomputation.
 *
 * @package GitLogs\DB
 */

declare( strict_types = 1 );

namespace GitLogs\DB;

defined( 'ABSPATH' ) || exit;

require_once __DIR__ . '/class-database.php';
require_once __DIR__ . '/class-run-store.php';

final class EventStore {

	public const STREAMS    = [ 'stdout', 'stderr', 'meta' ];
	public const SEVERITIES = [ 'debug', 'info', 'warn', 'error', 'fatal' ];

	/**
	 * Append a batch of events for a single (sha, run_id).
	 *
	 * @param list<array{
	 *   seq:int, ts_utc:string, stream:string, phase:string,
	 *   severity:string, message:string, attrs?:?array<mixed>
	 * }> $events
	 *
	 * @return array{appended:int, errors:int, warns:int}
	 */
	public static function append( string $sha, string $run_id, array $events ): array {
		$pdo = Database::sha( $sha );

		$pdo->beginTransaction();
		try {
			$ins = $pdo->prepare(
				'INSERT OR IGNORE INTO events
					(run_id, seq, ts_utc, stream, phase, severity, message, attrs_json)
				 VALUES
					(:run, :seq, :ts, :stream, :phase, :sev, :msg, :attrs)'
			);

			$appended = 0;
			$errors   = 0;
			$warns    = 0;
			foreach ( $events as $e ) {
				self::validate( $e );
				$ins->execute( [
					':run'    => $run_id,
					':seq'    => $e['seq'],
					':ts'     => $e['ts_utc'],
					':stream' => $e['stream'],
					':phase'  => $e['phase'],
					':sev'    => $e['severity'],
					':msg'    => $e['message'],
					':attrs'  => isset( $e['attrs'] ) ? wp_json_encode( $e['attrs'] ) : null,
				] );
				if ( $ins->rowCount() > 0 ) {
					$appended++;
					if ( in_array( $e['severity'], [ 'error', 'fatal' ], true ) ) { $errors++; }
					if ( 'warn' === $e['severity'] )                              { $warns++;  }
				}
			}

			// Update per-SHA summary row (insert-or-update).
			$pdo->prepare(
				'INSERT INTO summary (run_id, started_utc, event_count, error_count, warn_count)
				 VALUES (:run, COALESCE((SELECT started_utc FROM summary WHERE run_id = :run), :now), :ec, :er, :wn)
				 ON CONFLICT(run_id) DO UPDATE SET
				   event_count = summary.event_count + :ec,
				   error_count = summary.error_count + :er,
				   warn_count  = summary.warn_count  + :wn'
			)->execute( [
				':run' => $run_id,
				':now' => gmdate( 'c' ),
				':ec'  => $appended,
				':er'  => $errors,
				':wn'  => $warns,
			] );

			$pdo->commit();
		} catch ( \Throwable $e ) {
			if ( $pdo->inTransaction() ) {
				$pdo->rollBack();
			}
			throw $e;
		}

		// Mirror counts onto the root `runs` row.
		$row = self::summary( $sha, $run_id );
		if ( null !== $row ) {
			RunStore::update_counts(
				$run_id,
				(int) $row['event_count'],
				(int) $row['error_count'],
				(int) $row['warn_count']
			);
		}

		return [ 'appended' => $appended, 'errors' => $errors, 'warns' => $warns ];
	}

	/** @return list<array<string,mixed>> */
	public static function read( string $sha, string $run_id, int $after_seq = 0, int $limit = 500 ): array {
		$pdo  = Database::sha( $sha );
		$stmt = $pdo->prepare(
			'SELECT seq, ts_utc, stream, phase, severity, message, attrs_json
			 FROM events
			 WHERE run_id = :run AND seq > :seq
			 ORDER BY seq ASC LIMIT :lim'
		);
		$stmt->bindValue( ':run', $run_id );
		$stmt->bindValue( ':seq', $after_seq, \PDO::PARAM_INT );
		$stmt->bindValue( ':lim', $limit,     \PDO::PARAM_INT );
		$stmt->execute();
		return $stmt->fetchAll();
	}

	/** @return array<string,mixed>|null */
	public static function summary( string $sha, string $run_id ): ?array {
		$pdo  = Database::sha( $sha );
		$stmt = $pdo->prepare( 'SELECT * FROM summary WHERE run_id = :run' );
		$stmt->execute( [ ':run' => $run_id ] );
		$row = $stmt->fetch();
		return false === $row ? null : $row;
	}

	public static function finalize( string $sha, string $run_id, ?string $finished_utc = null, ?int $exit_code = null ): void {
		$pdo  = Database::sha( $sha );
		$stmt = $pdo->prepare(
			'UPDATE summary SET finished_utc = :fin, exit_code = :ec WHERE run_id = :run'
		);
		$stmt->execute( [
			':fin' => $finished_utc ?? gmdate( 'c' ),
			':ec'  => $exit_code,
			':run' => $run_id,
		] );
	}

	private static function validate( array $e ): void {
		foreach ( [ 'seq', 'ts_utc', 'stream', 'phase', 'severity', 'message' ] as $k ) {
			if ( ! array_key_exists( $k, $e ) ) {
				throw new \InvalidArgumentException( "event missing required field: $k" );
			}
		}
		if ( ! in_array( $e['stream'], self::STREAMS, true ) ) {
			throw new \InvalidArgumentException( 'event.stream must be one of: ' . implode( ',', self::STREAMS ) );
		}
		if ( ! in_array( $e['severity'], self::SEVERITIES, true ) ) {
			throw new \InvalidArgumentException( 'event.severity must be one of: ' . implode( ',', self::SEVERITIES ) );
		}
		if ( ! is_int( $e['seq'] ) || $e['seq'] < 0 ) {
			throw new \InvalidArgumentException( 'event.seq must be non-negative integer' );
		}
	}
}
