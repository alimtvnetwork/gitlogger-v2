<?php
/**
 * BranchStore — CRUD for the `branches` table.
 *
 * @package GitLogs\DB
 */

declare( strict_types = 1 );

namespace GitLogs\DB;

defined( 'ABSPATH' ) || exit;

if ( class_exists( __NAMESPACE__ . '\\BranchStore', false ) ) {
	return; // allow tests to pre-load an in-memory stub
}

require_once __DIR__ . '/class-database.php';

final class BranchStore {

	public static function touch( int $repo_id, string $name, ?string $head_sha = null ): int {
		$pdo  = Database::root();
		$now  = gmdate( 'c' );
		$stmt = $pdo->prepare(
			'INSERT INTO branches (repo_id, name, head_sha, last_run_utc)
			 VALUES (:r, :n, :h, :t)
			 ON CONFLICT(repo_id, name) DO UPDATE SET
			   head_sha     = COALESCE(excluded.head_sha, branches.head_sha),
			   last_run_utc = excluded.last_run_utc'
		);
		$stmt->execute( [ ':r' => $repo_id, ':n' => $name, ':h' => $head_sha, ':t' => $now ] );

		$id = $pdo->prepare( 'SELECT id FROM branches WHERE repo_id = :r AND name = :n' );
		$id->execute( [ ':r' => $repo_id, ':n' => $name ] );
		return (int) $id->fetchColumn();
	}

	/** @return list<array<string,mixed>> */
	public static function list_for_repo( int $repo_id ): array {
		$pdo  = Database::root();
		$stmt = $pdo->prepare( 'SELECT * FROM branches WHERE repo_id = :r ORDER BY name' );
		$stmt->execute( [ ':r' => $repo_id ] );
		return $stmt->fetchAll();
	}
}
