<?php
/**
 * EventStore tests — append/read with summary roll-up, validation, and
 * unique (run_id, seq) handling.
 */

declare( strict_types = 1 );

use GitLogs\DB\RepoStore;
use GitLogs\DB\RunStore;
use GitLogs\DB\EventStore;

function _mk_run(): array {
	$repo_id = RepoStore::upsert( 'acme/api', 'Acme API' );
	$sha     = str_repeat( 'a', 40 );
	$run_id  = RunStore::create( [ 'repo_id' => $repo_id, 'branch' => 'main', 'sha' => $sha, 'ci_provider' => 'gh' ] );
	return [ $sha, $run_id ];
}

function _ev( int $seq, string $sev = 'info', string $msg = 'm' ): array {
	return [
		'seq'      => $seq,
		'ts_utc'   => '2025-01-01T00:00:00Z',
		'stream'   => 'stdout',
		'phase'    => 'build',
		'severity' => $sev,
		'message'  => $msg,
	];
}

function dbtest_events_append_then_read_roundtrip(): void {
	[ $sha, $run ] = _mk_run();
	$result = EventStore::append( $sha, $run, [
		_ev( 1, 'info'  ),
		_ev( 2, 'warn'  ),
		_ev( 3, 'error' ),
	] );
	assertSame( 3, $result['appended'] );
	assertSame( 1, $result['errors'] );
	assertSame( 1, $result['warns'] );

	$rows = EventStore::read( $sha, $run, 0, 100 );
	assertSame( 3, count( $rows ) );
	assertSame( 1, (int) $rows[0]['seq'] );
	assertSame( 'error', $rows[2]['severity'] );

	$tail = EventStore::read( $sha, $run, 1, 100 );
	assertSame( 2, count( $tail ) );
	assertSame( 2, (int) $tail[0]['seq'] );
}

function dbtest_events_summary_accumulates(): void {
	[ $sha, $run ] = _mk_run();
	EventStore::append( $sha, $run, [ _ev( 1, 'info' ) ] );
	EventStore::append( $sha, $run, [ _ev( 2, 'error' ), _ev( 3, 'warn' ) ] );
	$sum = EventStore::summary( $sha, $run );
	assertNotNull( $sum );
	assertSame( 3, (int) $sum['event_count'] );
	assertSame( 1, (int) $sum['error_count'] );
	assertSame( 1, (int) $sum['warn_count'] );

	// RunStore mirror must match.
	$row = RunStore::find( $run );
	assertSame( 3, (int) $row['event_count'] );
	assertSame( 1, (int) $row['error_count'] );
	assertSame( 1, (int) $row['warn_count'] );
}

function dbtest_events_duplicate_seq_is_ignored_idempotently(): void {
	[ $sha, $run ] = _mk_run();
	$first  = EventStore::append( $sha, $run, [ _ev( 1, 'info' ), _ev( 2, 'warn' ) ] );
	$second = EventStore::append( $sha, $run, [ _ev( 1, 'info' ), _ev( 2, 'warn' ), _ev( 3, 'error' ) ] );
	assertSame( 2, $first['appended'] );
	assertSame( 1, $second['appended'], 'duplicate (run_id,seq) rows must be skipped' );
	assertSame( 3, count( EventStore::read( $sha, $run, 0, 100 ) ) );
}

function dbtest_events_validate_rejects_bad_stream(): void {
	[ $sha, $run ] = _mk_run();
	$bad = _ev( 1 );
	$bad['stream'] = 'pipe';
	assertThrows( static function () use ( $sha, $run, $bad ) {
		EventStore::append( $sha, $run, [ $bad ] );
	}, 'event.stream must be' );
}

function dbtest_events_validate_rejects_bad_severity(): void {
	[ $sha, $run ] = _mk_run();
	$bad = _ev( 1 );
	$bad['severity'] = 'critical';
	assertThrows( static function () use ( $sha, $run, $bad ) {
		EventStore::append( $sha, $run, [ $bad ] );
	}, 'event.severity must be' );
}

function dbtest_events_validate_requires_all_keys(): void {
	[ $sha, $run ] = _mk_run();
	$bad = _ev( 1 );
	unset( $bad['phase'] );
	assertThrows( static function () use ( $sha, $run, $bad ) {
		EventStore::append( $sha, $run, [ $bad ] );
	}, 'missing required field: phase' );
}

function dbtest_events_finalize_writes_summary_columns(): void {
	[ $sha, $run ] = _mk_run();
	EventStore::append( $sha, $run, [ _ev( 1 ) ] );
	EventStore::finalize( $sha, $run, '2025-01-01T01:23:45Z', 0 );
	$sum = EventStore::summary( $sha, $run );
	assertSame( '2025-01-01T01:23:45Z', $sum['finished_utc'] );
	assertSame( 0, (int) $sum['exit_code'] );
}

function dbtest_events_isolated_per_run_id(): void {
	[ $sha, $run1 ] = _mk_run();
	$repo_id = RepoStore::upsert( 'acme/api', 'Acme API' ); // same slug = same repo
	$run2 = RunStore::create( [ 'repo_id' => $repo_id, 'branch' => 'main', 'sha' => $sha, 'ci_provider' => 'gh' ] );
	EventStore::append( $sha, $run1, [ _ev( 1 ) ] );
	EventStore::append( $sha, $run2, [ _ev( 1 ), _ev( 2 ) ] );
	assertSame( 1, count( EventStore::read( $sha, $run1, 0, 100 ) ) );
	assertSame( 2, count( EventStore::read( $sha, $run2, 0, 100 ) ) );
}

function dbtest_events_attrs_serialised_and_returned_as_json(): void {
	[ $sha, $run ] = _mk_run();
	$ev = _ev( 1 );
	$ev['attrs'] = [ 'k' => 'v', 'n' => 42 ];
	EventStore::append( $sha, $run, [ $ev ] );
	$row = EventStore::read( $sha, $run, 0, 1 )[0];
	assertSame( '{"k":"v","n":42}', $row['attrs_json'] );
}
