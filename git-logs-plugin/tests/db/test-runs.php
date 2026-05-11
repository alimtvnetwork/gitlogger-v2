<?php
/**
 * RunStore tests — UUID generation, status transitions, terminal-state
 * timestamping, count updates, and listing.
 */

declare( strict_types = 1 );

use GitLogs\DB\RepoStore;
use GitLogs\DB\RunStore;

function _mk_repo(): int { return RepoStore::upsert( 'acme/api', 'Acme API' ); }

function dbtest_run_create_returns_uuid_and_sets_queued(): void {
	$repo = _mk_repo();
	$id = RunStore::create( [
		'repo_id' => $repo, 'branch' => 'main',
		'sha' => str_repeat( 'a', 40 ),
		'ci_provider' => 'github_actions',
		'metadata' => [ 'pipeline' => 'ci' ],
	] );
	assertSame( 36, strlen( $id ) );
	assertTrue( (bool) preg_match( '/\A[0-9a-f-]{36}\z/', $id ) );

	$row = RunStore::find( $id );
	assertNotNull( $row );
	assertSame( 'queued', $row['status'] );
	assertSame( str_repeat( 'a', 40 ), $row['sha'] );
	assertSame( '{"pipeline":"ci"}', $row['metadata_json'] );
}

function dbtest_run_create_lowercases_sha(): void {
	$repo = _mk_repo();
	$id = RunStore::create( [
		'repo_id' => $repo, 'branch' => 'main',
		'sha' => str_repeat( 'A', 40 ), 'ci_provider' => 'gh',
	] );
	assertSame( str_repeat( 'a', 40 ), RunStore::find( $id )['sha'] );
}

function dbtest_run_set_status_running_does_not_finalize(): void {
	$repo = _mk_repo();
	$id = RunStore::create( [ 'repo_id' => $repo, 'branch' => 'main', 'sha' => str_repeat( 'a', 40 ), 'ci_provider' => 'gh' ] );
	RunStore::set_status( $id, 'running' );
	$row = RunStore::find( $id );
	assertSame( 'running', $row['status'] );
	assertSame( null, $row['finished_utc'] );
	assertSame( null, $row['duration_ms'] );
}

function dbtest_run_set_status_terminal_writes_finished_and_duration(): void {
	$repo = _mk_repo();
	$id = RunStore::create( [ 'repo_id' => $repo, 'branch' => 'main', 'sha' => str_repeat( 'a', 40 ), 'ci_provider' => 'gh' ] );
	RunStore::set_status( $id, 'running' );
	usleep( 5000 ); // ensure non-zero duration_ms (julianday is ms-precise)
	RunStore::set_status( $id, 'succeeded', 0 );
	$row = RunStore::find( $id );
	assertSame( 'succeeded', $row['status'] );
	assertSame( 0, (int) $row['exit_code'] );
	assertNotNull( $row['finished_utc'] );
	assertNotNull( $row['duration_ms'] );
	assertTrue( (int) $row['duration_ms'] >= 0 );
}

function dbtest_run_set_status_rejects_unknown_state(): void {
	$repo = _mk_repo();
	$id = RunStore::create( [ 'repo_id' => $repo, 'branch' => 'main', 'sha' => str_repeat( 'a', 40 ), 'ci_provider' => 'gh' ] );
	assertThrows( static function () use ( $id ) { RunStore::set_status( $id, 'bogus' ); }, 'invalid status' );
}

function dbtest_run_update_counts_writes_through(): void {
	$repo = _mk_repo();
	$id = RunStore::create( [ 'repo_id' => $repo, 'branch' => 'main', 'sha' => str_repeat( 'a', 40 ), 'ci_provider' => 'gh' ] );
	RunStore::update_counts( $id, 42, 3, 7 );
	$row = RunStore::find( $id );
	assertSame( 42, (int) $row['event_count'] );
	assertSame( 3,  (int) $row['error_count'] );
	assertSame( 7,  (int) $row['warn_count'] );
}

function dbtest_run_find_returns_null_for_unknown(): void {
	assertSame( null, RunStore::find( '00000000-0000-4000-8000-000000000000' ) );
}

function dbtest_run_list_recent_limits_and_returns_all_for_repo(): void {
	$repo = _mk_repo();
	$ids = [];
	for ( $i = 0; $i < 5; $i++ ) {
		$ids[] = RunStore::create( [
			'repo_id' => $repo, 'branch' => 'main',
			'sha' => str_repeat( dechex( $i ), 40 ),
			'ci_provider' => 'gh',
		] );
	}
	// Limit honoured.
	$top3 = RunStore::list_recent( $repo, 3 );
	assertSame( 3, count( $top3 ) );

	// Full set returned at higher limit and contains every inserted id.
	$all = RunStore::list_recent( $repo, 50 );
	assertSame( 5, count( $all ) );
	$got_ids = array_column( $all, 'id' );
	foreach ( $ids as $expected ) {
		assertTrue( in_array( $expected, $got_ids, true ), "missing id: $expected" );
	}
}

function dbtest_run_list_recent_isolates_repos(): void {
	$r1 = RepoStore::upsert( 'one/a', 'One' );
	$r2 = RepoStore::upsert( 'two/b', 'Two' );
	RunStore::create( [ 'repo_id' => $r1, 'branch' => 'main', 'sha' => str_repeat( 'a', 40 ), 'ci_provider' => 'gh' ] );
	RunStore::create( [ 'repo_id' => $r2, 'branch' => 'main', 'sha' => str_repeat( 'b', 40 ), 'ci_provider' => 'gh' ] );
	assertSame( 1, count( RunStore::list_recent( $r1 ) ) );
	assertSame( 1, count( RunStore::list_recent( $r2 ) ) );
}
