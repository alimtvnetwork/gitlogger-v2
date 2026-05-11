<?php
/**
 * Tests for the /events streaming REST controller.
 *
 * Verifies first-call run materialisation, severity normalisation,
 * Final flag drives RunStore::set_status, and validation errors.
 */

declare( strict_types = 1 );

use GitLogs\Rest\Events;
use GitLogs\DB\RunStore;
use GitLogs\DB\RepoStore;
use GitLogs\DB\EventStore;

function test_events_first_call_creates_run_and_appends(): void {
	wp_set_current_user( 1 );
	$body = json_encode( [
		'RepoUrl'      => 'https://github.com/acme/api.git',
		'Branch'       => 'main',
		'GitSha256'    => 'abc1234567890abcdef1234567890abcdef12345',
		'PipelineName' => 'ci',
		'Events'       => [
			[ 'Ts' => '2025-01-01T00:00:00Z', 'Level' => 'info', 'Line' => 'starting' ],
			[ 'Ts' => '2025-01-01T00:00:01Z', 'Level' => 'unknown_level', 'Line' => 'normalised' ],
		],
	] );
	$res = Events::handle( new WP_REST_Request_Ext( 'POST', [], $body ) );
	assertSame( 200, $res->get_status() );
	$d = $res->get_data();
	assertTrue( $d['Accepted'] );
	assertSame( 2, $d['Inserted'] );
	assertFalse( $d['Final'] );
	assertSame( 'running', RunStore::$rows[ $d['RunId'] ]['status'] );
	// Repo slug derived from URL path (.git stripped).
	$slugs = array_column( RepoStore::$rows, 'slug' );
	assertTrue( in_array( 'acme/api', $slugs, true ) );
}

function test_events_final_with_error_marks_failed(): void {
	wp_set_current_user( 1 );
	$body = json_encode( [
		'RepoUrl'   => 'https://github.com/acme/api',
		'GitSha256' => 'abc1234567890abcdef1234567890abcdef12345',
		'Final'     => true,
		'Events'    => [ [ 'Ts' => '2025-01-01T00:00:00Z', 'Level' => 'fatal', 'Line' => 'kaboom' ] ],
	] );
	$res = Events::handle( new WP_REST_Request_Ext( 'POST', [], $body ) );
	assertSame( 200, $res->get_status() );
	$d = $res->get_data();
	assertTrue( $d['Final'] );
	assertSame( 'failed', RunStore::$rows[ $d['RunId'] ]['status'] );
	assertSame( 1, RunStore::$rows[ $d['RunId'] ]['exit_code'] );
}

function test_events_final_without_errors_marks_succeeded(): void {
	wp_set_current_user( 1 );
	$body = json_encode( [
		'RepoUrl'   => 'https://github.com/acme/api',
		'GitSha256' => 'abc1234567890abcdef1234567890abcdef12345',
		'Final'     => true,
		'Events'    => [ [ 'Level' => 'info', 'Line' => 'done' ] ],
	] );
	$res = Events::handle( new WP_REST_Request_Ext( 'POST', [], $body ) );
	assertSame( 'succeeded', RunStore::$rows[ $res->get_data()['RunId'] ]['status'] );
}

function test_events_rejects_bad_json(): void {
	wp_set_current_user( 1 );
	$res = Events::handle( new WP_REST_Request_Ext( 'POST', [], 'definitely not json' ) );
	assertSame( 400, $res->get_status() );
	assertSame( 'GL-EVENTS-BAD-JSON', $res->get_data()['ErrorCode'] );
}

function test_events_rejects_missing_fields(): void {
	wp_set_current_user( 1 );
	$body = json_encode( [ 'RepoUrl' => '', 'GitSha256' => '' ] );
	$res = Events::handle( new WP_REST_Request_Ext( 'POST', [], $body ) );
	assertSame( 400, $res->get_status() );
	assertSame( 'GL-EVENTS-MISSING-FIELDS', $res->get_data()['ErrorCode'] );
}

function test_events_existing_run_id_skips_repo_creation(): void {
	wp_set_current_user( 1 );
	$repo_id = RepoStore::upsert( 'acme/preexisting', 'Pre' );
	$run_id  = RunStore::create( [
		'repo_id' => $repo_id, 'branch' => 'main',
		'sha' => 'fff1234567890abcdef1234567890abcdef12345',
		'ci_provider' => 'glci-stream',
	] );
	$body = json_encode( [
		'RepoUrl'   => 'https://github.com/acme/preexisting',
		'GitSha256' => 'fff1234567890abcdef1234567890abcdef12345',
		'RunId'     => $run_id,
		'Events'    => [ [ 'Level' => 'info', 'Line' => 'continuing' ] ],
	] );
	$res = Events::handle( new WP_REST_Request_Ext( 'POST', [], $body ) );
	assertSame( $run_id, $res->get_data()['RunId'] );
	// No additional repo created beyond the one we seeded.
	assertSame( 1, count( RepoStore::$rows ) );
}
