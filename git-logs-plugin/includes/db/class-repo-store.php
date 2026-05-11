<?php
/**
 * RepoStore — CRUD for the `repos` table.
 *
 * @package GitLogs\DB
 */

declare( strict_types = 1 );

namespace GitLogs\DB;

defined( 'ABSPATH' ) || exit;

if ( class_exists( __NAMESPACE__ . '\\RepoStore', false ) ) {
	return; // allow tests to pre-load an in-memory stub
}

require_once __DIR__ . '/class-database.php';

final class RepoStore {

	public static function upsert( string $slug, string $display_name, ?string $remote_url = null, string $default_branch = 'main' ): int {
		$pdo  = Database::root();
		$now  = gmdate( 'c' );
		$stmt = $pdo->prepare(
			'INSERT INTO repos (slug, display_name, remote_url, default_branch, created_utc)
			 VALUES (:slug, :name, :url, :db, :now)
			 ON CONFLICT(slug) DO UPDATE SET
			   display_name   = excluded.display_name,
			   remote_url     = excluded.remote_url,
			   default_branch = excluded.default_branch'
		);
		$stmt->execute( [
			':slug' => $slug,
			':name' => $display_name,
			':url'  => $remote_url,
			':db'   => $default_branch,
			':now'  => $now,
		] );
		return self::id_for_slug( $slug );
	}

	public static function id_for_slug( string $slug ): int {
		$pdo  = Database::root();
		$stmt = $pdo->prepare( 'SELECT id FROM repos WHERE slug = :s' );
		$stmt->execute( [ ':s' => $slug ] );
		$id = $stmt->fetchColumn();
		if ( false === $id ) {
			throw new \RuntimeException( "repo not found: $slug" );
		}
		return (int) $id;
	}

	/** @return array<string,mixed>|null */
	public static function find_by_slug( string $slug ): ?array {
		$pdo  = Database::root();
		$stmt = $pdo->prepare( 'SELECT * FROM repos WHERE slug = :s' );
		$stmt->execute( [ ':s' => $slug ] );
		$row = $stmt->fetch();
		return false === $row ? null : $row;
	}

	/** @return list<array<string,mixed>> */
	public static function list_all( bool $include_archived = false ): array {
		$pdo = Database::root();
		$sql = 'SELECT * FROM repos';
		if ( ! $include_archived ) {
			$sql .= ' WHERE archived = 0';
		}
		$sql .= ' ORDER BY slug';
		return $pdo->query( $sql )->fetchAll();
	}

	public static function archive( int $repo_id, bool $archived = true ): void {
		$pdo  = Database::root();
		$stmt = $pdo->prepare( 'UPDATE repos SET archived = :a WHERE id = :id' );
		$stmt->execute( [ ':a' => $archived ? 1 : 0, ':id' => $repo_id ] );
	}
}
