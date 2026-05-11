<?php
/**
 * Tests for the /runs REST controller.
 *
 * Covers: create (validation + audit), list_runs (slug required, repo
 * lookup), fetch (404), append_events / read_events (round-trip,
 * severity validation), and finalize (status update + audit).
 */

declare( strict_types = 1 );

use GitLogs\Rest\Runs;
use GitLogs\DB\RepoStore;
use GitLogs\DB\RunStore;
use GitLogs\DB\EventStore;
use GitLogs\DB\BranchStore;
use GitLogs\DB\AuditLog;

function _runs_setup_repo(): int {
	wp_set_current_user( 9 );
	$GLOBALS['__current_user_login'] = 'bob';
	return RepoStore::upsert( 'acme/api', 'Acme API', null, 'main' );
}

const _RUN_SHA = '0123456789abcdef0123456789abcdef01234567';

function test_runs_create_succeeds_and_writes_audit(): void {
	_runs_setup_repo();
	$req = new WP_REST_Request_Ext( 'POST', [
		'repo_slug'   => 'acme/api',
		'branch'      => 'main',
		'sha'         => _RUN_SHA,
		'ci_provider' => 'github_actions',
		'ci_run_url'  => 'https://example.com/run/1',
	] );
	$res = Runs::create( $req );
	assertSame( 201, $res->get_status() );
	$id = $res->get_data()['id'];
	assertTrue( is_string( $id ) && 36 === strlen( $id ) );
	assertSame( 'running', RunStore::$rows[ $id ]['status'] );
	assertSame( 1, count( BranchStore::$touches ) );
	assertSame( 'run.create', AuditLog::$rows[0]['action'] );
}

function test_runs_create_unknown_slug_404s(): void {
	_runs_setup_repo();
	$res = Runs::create( new WP_REST_Request_Ext( 'POST', [
		'repo_slug'   => 'ghost/repo',
		'branch'      => 'main',
		'sha'         => _RUN_SHA,
		'ci_provider' => 'gh',
	] ) );
	assertSame( 404, $res->get_status() );
}

function test_runs_create_rejects_short_sha(): void {
	_runs_setup_repo();
	$res = Runs::create( new WP_REST_Request_Ext( 'POST', [
		'repo_slug'   => 'acme/api',
		'branch'      => 'main',
		'sha'         => 'deadbeef',
		'ci_provider' => 'gh',
	] ) );
	assertSame( 400, $res->get_status() );
	assertTrue( str_contains( $res->get_data()['error'], '40 lowercase hex' ) );
}

function test_runs_list_requires_slug_and_validates_repo(): void {
	_runs_setup_repo();
	$res = Runs::list_runs( new WP_REST_Request_Ext( 'GET' ) );
	assertSame( 400, $res->get_status() );

	$res2 = Runs::list_runs( new WP_REST_Request_Ext( 'GET', [ 'repo_slug' => 'ghost/repo' ] ) );
	assertSame( 404, $res2->get_status() );
}

function test_runs_list_returns_recent(): void {
	_runs_setup_repo();
	Runs::create( new WP_REST_Request_Ext( 'POST', [
		'repo_slug' => 'acme/api', 'branch' => 'main',
		'sha' => _RUN_SHA, 'ci_provider' => 'gh',
	] ) );
	$res = Runs::list_runs( new WP_REST_Request_Ext( 'GET', [ 'repo_slug' => 'acme/api' ] ) );
	assertSame( 200, $res->get_status() );
	assertSame( 1, count( $res->get_data()['runs'] ) );
}

function test_runs_fetch_unknown_404s(): void {
	_runs_setup_repo();
	$res = Runs::fetch( new WP_REST_Request_Ext( 'GET', [], '', [], [ 'id' => 'no-such-id' ] ) );
	assertSame( 404, $res->get_status() );
}

function test_runs_events_roundtrip(): void {
	_runs_setup_repo();
	$run_id = Runs::create( new WP_REST_Request_Ext( 'POST', [
		'repo_slug' => 'acme/api', 'branch' => 'main',
		'sha' => _RUN_SHA, 'ci_provider' => 'gh',
	] ) )->get_data()['id'];

	$body = json_encode( [ 'events' => [
		[ 'seq' => 1, 'ts_utc' => '2025-01-01T00:00:00Z', 'stream' => 'stdout', 'phase' => 'build', 'severity' => 'info',  'message' => 'hi' ],
		[ 'seq' => 2, 'ts_utc' => '2025-01-01T00:00:01Z', 'stream' => 'stderr', 'phase' => 'build', 'severity' => 'error', 'message' => 'boom' ],
	] ] );
	$append = Runs::append_events( new WP_REST_Request_Ext( 'POST', [], $body, [], [ 'id' => $run_id ] ) );
	assertSame( 202, $append->get_status() );
	assertSame( 2, $append->get_data()['appended'] );
	assertSame( 1, $append->get_data()['errors'] );

	$read = Runs::read_events( new WP_REST_Request_Ext( 'GET', [ 'after_seq' => 1 ], '', [], [ 'id' => $run_id ] ) );
	$events = $read->get_data()['events'];
	assertSame( 1, count( $events ) );
	assertSame( 2, $events[0]['seq'] );
}

function test_runs_append_events_rejects_bad_body(): void {
	_runs_setup_repo();
	$run_id = Runs::create( new WP_REST_Request_Ext( 'POST', [
		'repo_slug' => 'acme/api', 'branch' => 'main',
		'sha' => _RUN_SHA, 'ci_provider' => 'gh',
	] ) )->get_data()['id'];

	$res = Runs::append_events( new WP_REST_Request_Ext( 'POST', [], 'not json', [], [ 'id' => $run_id ] ) );
	assertSame( 400, $res->get_status() );
}

function test_runs_finalize_updates_status_and_audit(): void {
	_runs_setup_repo();
	$run_id = Runs::create( new WP_REST_Request_Ext( 'POST', [
		'repo_slug' => 'acme/api', 'branch' => 'main',
		'sha' => _RUN_SHA, 'ci_provider' => 'gh',
	] ) )->get_data()['id'];

	$res = Runs::finalize( new WP_REST_Request_Ext(
		'POST', [ 'status' => 'succeeded', 'exit_code' => 0 ], '', [], [ 'id' => $run_id ]
	) );
	assertSame( 200, $res->get_status() );
	assertSame( 'succeeded', RunStore::$rows[ $run_id ]['status'] );
	assertSame( 0, RunStore::$rows[ $run_id ]['exit_code'] );

	$last = end( AuditLog::$rows );
	assertSame( 'run.finalize', $last['action'] );
}

function test_runs_finalize_rejects_unknown_status(): void {
	_runs_setup_repo();
	$run_id = Runs::create( new WP_REST_Request_Ext( 'POST', [
		'repo_slug' => 'acme/api', 'branch' => 'main',
		'sha' => _RUN_SHA, 'ci_provider' => 'gh',
	] ) )->get_data()['id'];

	$res = Runs::finalize( new WP_REST_Request_Ext(
		'POST', [ 'status' => 'bogus' ], '', [], [ 'id' => $run_id ]
	) );
	assertSame( 400, $res->get_status() );
}
