<?php
/**
 * RepoStore + BranchStore + ShaIndex tests.
 */

declare( strict_types = 1 );

use GitLogs\DB\RepoStore;
use GitLogs\DB\BranchStore;
use GitLogs\DB\ShaIndex;
use GitLogs\DB\RunStore;

function dbtest_repo_upsert_then_find(): void {
	$id = RepoStore::upsert( 'acme/api', 'Acme API', 'https://example.com/repo', 'develop' );
	assertSame( 1, $id );
	$row = RepoStore::find_by_slug( 'acme/api' );
	assertNotNull( $row );
	assertSame( 'Acme API', $row['display_name'] );
	assertSame( 'develop', $row['default_branch'] );
	assertSame( $id, RepoStore::id_for_slug( 'acme/api' ) );
}

function dbtest_repo_upsert_updates_existing_row(): void {
	$id1 = RepoStore::upsert( 'acme/api', 'First', null, 'main' );
	$id2 = RepoStore::upsert( 'acme/api', 'Second', 'u', 'develop' );
	assertSame( $id1, $id2 );
	$row = RepoStore::find_by_slug( 'acme/api' );
	assertSame( 'Second',  $row['display_name'] );
	assertSame( 'develop', $row['default_branch'] );
	assertSame( 'u',       $row['remote_url'] );
}

function dbtest_repo_id_for_slug_throws_on_missing(): void {
	assertThrows( static function () { RepoStore::id_for_slug( 'ghost' ); }, 'repo not found' );
}

function dbtest_repo_list_filters_archived(): void {
	$a = RepoStore::upsert( 'a/keep',    'Keep' );
	$b = RepoStore::upsert( 'b/archive', 'Archived' );
	RepoStore::archive( $b, true );

	$active   = RepoStore::list_all( false );
	$slugs    = array_column( $active, 'slug' );
	assertSame( [ 'a/keep' ], $slugs );

	$all = RepoStore::list_all( true );
	assertSame( 2, count( $all ) );
}

function dbtest_repo_find_returns_null_for_unknown(): void {
	assertSame( null, RepoStore::find_by_slug( 'no/such-repo' ) );
}

// --- BranchStore -----------------------------------------------------

function dbtest_branch_touch_creates_and_updates(): void {
	$repo_id = RepoStore::upsert( 'acme/api', 'Acme API' );
	$id1 = BranchStore::touch( $repo_id, 'main', 'a' . str_repeat( '0', 39 ) );
	$id2 = BranchStore::touch( $repo_id, 'main', 'b' . str_repeat( '0', 39 ) );
	assertSame( $id1, $id2, 'second touch must return same branch row id' );
	$rows = BranchStore::list_for_repo( $repo_id );
	assertSame( 1, count( $rows ) );
	assertSame( 'b' . str_repeat( '0', 39 ), $rows[0]['head_sha'] );
}

function dbtest_branch_touch_preserves_head_when_null(): void {
	$repo_id = RepoStore::upsert( 'acme/api', 'Acme API' );
	BranchStore::touch( $repo_id, 'main', str_repeat( 'a', 40 ) );
	BranchStore::touch( $repo_id, 'main', null );
	$rows = BranchStore::list_for_repo( $repo_id );
	assertSame( str_repeat( 'a', 40 ), $rows[0]['head_sha'], 'null head_sha must NOT clobber existing value' );
}

function dbtest_branch_isolated_per_repo(): void {
	$r1 = RepoStore::upsert( 'one/a', 'One' );
	$r2 = RepoStore::upsert( 'two/b', 'Two' );
	BranchStore::touch( $r1, 'main' );
	BranchStore::touch( $r2, 'main' );
	BranchStore::touch( $r2, 'feature' );
	assertSame( 1, count( BranchStore::list_for_repo( $r1 ) ) );
	assertSame( 2, count( BranchStore::list_for_repo( $r2 ) ) );
}

// --- ShaIndex --------------------------------------------------------

function dbtest_sha_index_links_runs_and_normalises_case(): void {
	$repo_id = RepoStore::upsert( 'acme/api', 'Acme API' );
	$sha     = str_repeat( 'a', 40 );
	$run1 = RunStore::create( [ 'repo_id' => $repo_id, 'branch' => 'main', 'sha' => $sha,            'ci_provider' => 'github' ] );
	$run2 = RunStore::create( [ 'repo_id' => $repo_id, 'branch' => 'main', 'sha' => strtoupper( $sha ), 'ci_provider' => 'github' ] );
	$ids = ShaIndex::runs_for_sha( strtoupper( $sha ) );
	assertSame( 2, count( $ids ) );
	assertTrue( in_array( $run1, $ids, true ) );
	assertTrue( in_array( $run2, $ids, true ) );
}

function dbtest_sha_index_dedupes_same_run(): void {
	$repo_id = RepoStore::upsert( 'acme/api', 'Acme API' );
	$sha     = str_repeat( 'b', 40 );
	$run     = RunStore::create( [ 'repo_id' => $repo_id, 'branch' => 'main', 'sha' => $sha, 'ci_provider' => 'github' ] );
	// Re-add manually — INSERT OR IGNORE means the second call is a no-op.
	ShaIndex::add( $sha, $run, $repo_id );
	assertSame( 1, count( ShaIndex::runs_for_sha( $sha ) ) );
}
