<?php
/**
 * AuditLog tests — append-only insert + filtered listing.
 */

declare( strict_types = 1 );

use GitLogs\DB\AuditLog;

function dbtest_audit_record_inserts_and_returns_pk(): void {
	$id = AuditLog::record( [
		'action'        => 'run.create',
		'result'        => AuditLog::RESULT_OK,
		'actor_user_id' => 7,
		'actor_login'   => 'alice',
		'auth_lane'     => 'wp_session',
		'target_type'   => 'run',
		'target_id'     => 'rid-1',
		'detail'        => [ 'a' => 1 ],
	] );
	assertSame( 1, $id );

	$rows = AuditLog::recent( 10 );
	assertSame( 1, count( $rows ) );
	assertSame( 'run.create',  $rows[0]['action'] );
	assertSame( 'wp_session',  $rows[0]['auth_lane'] );
	assertSame( '{"a":1}',     $rows[0]['detail_json'] );
	assertSame( 7,             (int) $rows[0]['actor_user_id'] );
}

function dbtest_audit_default_lane_is_system(): void {
	AuditLog::record( [ 'action' => 'gc.run', 'result' => 'ok' ] );
	$rows = AuditLog::recent( 1 );
	assertSame( 'system', $rows[0]['auth_lane'] );
}

function dbtest_audit_invalid_lane_rejected_by_check_constraint(): void {
	assertThrows( static function () {
		AuditLog::record( [ 'action' => 'x', 'result' => 'ok', 'auth_lane' => 'bogus' ] );
	}, 'CHECK' );
}

function dbtest_audit_invalid_result_rejected(): void {
	assertThrows( static function () {
		AuditLog::record( [ 'action' => 'x', 'result' => 'partial' ] );
	}, 'CHECK' );
}

function dbtest_audit_recent_orders_desc_and_limits(): void {
	for ( $i = 1; $i <= 5; $i++ ) {
		AuditLog::record( [ 'action' => 'a' . $i, 'result' => 'ok' ] );
	}
	$rows = AuditLog::recent( 3 );
	assertSame( 3, count( $rows ) );
	assertSame( 'a5', $rows[0]['action'] );
	assertSame( 'a4', $rows[1]['action'] );
	assertSame( 'a3', $rows[2]['action'] );
}

function dbtest_audit_filter_by_action(): void {
	AuditLog::record( [ 'action' => 'run.create',   'result' => 'ok' ] );
	AuditLog::record( [ 'action' => 'run.finalize', 'result' => 'ok' ] );
	AuditLog::record( [ 'action' => 'run.create',   'result' => 'ok' ] );
	$rows = AuditLog::recent( 50, 'run.create' );
	assertSame( 2, count( $rows ) );
	foreach ( $rows as $r ) { assertSame( 'run.create', $r['action'] ); }
}
