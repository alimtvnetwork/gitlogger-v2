<?php
/**
 * ShaIndex — links a commit SHA to the runs that recorded events for it.
 *
 * @package GitLogs\DB
 */

declare( strict_types = 1 );

namespace GitLogs\DB;

defined( 'ABSPATH' ) || exit;

require_once __DIR__ . '/class-database.php';

final class ShaIndex {

	public static function add( string $sha, string $run_id, int $repo_id ): void {
		$pdo  = Database::root();
		$stmt = $pdo->prepare(
			'INSERT OR IGNORE INTO sha_index (sha, run_id, repo_id, created_utc)
			 VALUES (:sha, :run, :repo, :now)'
		);
		$stmt->execute( [
			':sha'  => strtolower( $sha ),
			':run'  => $run_id,
			':repo' => $repo_id,
			':now'  => gmdate( 'c' ),
		] );
	}

	/** @return list<string> run ids ordered by created_utc DESC */
	public static function runs_for_sha( string $sha ): array {
		$pdo  = Database::root();
		$stmt = $pdo->prepare(
			'SELECT run_id FROM sha_index WHERE sha = :sha ORDER BY created_utc DESC'
		);
		$stmt->execute( [ ':sha' => strtolower( $sha ) ] );
		return array_map( static fn( $r ) => (string) $r['run_id'], $stmt->fetchAll() );
	}
}
