<?php
/**
 * Tests for /whoami, /keys, and /audit REST controllers.
 */

declare( strict_types = 1 );

use GitLogs\Rest\Whoami;
use GitLogs\Rest\Keys;
use GitLogs\Rest\Audit;
use GitLogs\Auth\PublicKeys;
use GitLogs\DB\AuditLog;

// --- whoami --------------------------------------------------------------

function test_whoami_reports_wp_session_lane(): void {
	wp_set_current_user( 5 );
	$GLOBALS['__current_user_login']   = 'carol';
	$GLOBALS['__current_user_display'] = 'Carol';
	$GLOBALS['__current_user_roles']   = [ 'editor' ];

	$res = Whoami::handle( new WP_REST_Request_Ext( 'GET' ) );
	assertSame( 200, $res->get_status() );
	$d = $res->get_data();
	assertSame( 5, $d['user_id'] );
	assertSame( 'carol', $d['user_login'] );
	assertSame( [ 'editor' ], $d['roles'] );
	assertSame( 'wp_session', $d['auth_lane'] );
}

function test_whoami_reports_ed25519_lane_when_header_present(): void {
	wp_set_current_user( 5 );
	$res = Whoami::handle( new WP_REST_Request_Ext( 'GET', [], '', [ 'X-GitLogs-Auth' => 'glci-ed25519 1' ] ) );
	assertSame( 'ed25519', $res->get_data()['auth_lane'] );
}

// --- /keys ---------------------------------------------------------------

function _keys_pubkey_b64(): string {
	return base64_encode( str_repeat( "\x01", 32 ) );
}

function test_keys_add_then_list_then_delete(): void {
	wp_set_current_user( 11 );

	$add = Keys::add_key( new WP_REST_Request_Ext( 'POST', [
		'label'      => 'laptop',
		'pubkey_b64' => _keys_pubkey_b64(),
	] ) );
	assertSame( 201, $add->get_status() );
	$id = $add->get_data()['id'];
	assertTrue( is_string( $id ) && 8 === strlen( $id ) );

	$list = Keys::list_keys( new WP_REST_Request_Ext( 'GET' ) );
	assertSame( 200, $list->get_status() );
	$keys = $list->get_data()['keys'];
	assertSame( 1, count( $keys ) );
	assertSame( 'laptop', $keys[0]['label'] );
	// Pubkey bytes MUST NOT leak in the listing response.
	assertFalse( array_key_exists( 'pubkey_b64', $keys[0] ) );
	assertFalse( array_key_exists( 'pubkey', $keys[0] ) );

	$del = Keys::delete_key( new WP_REST_Request_Ext( 'DELETE', [], '', [], [ 'id' => $id ] ) );
	assertSame( 200, $del->get_status() );
	assertTrue( $del->get_data()['deleted'] );
}

function test_keys_delete_unknown_returns_404(): void {
	wp_set_current_user( 11 );
	$del = Keys::delete_key( new WP_REST_Request_Ext( 'DELETE', [], '', [], [ 'id' => 'deadbeef' ] ) );
	assertSame( 404, $del->get_status() );
	assertFalse( $del->get_data()['deleted'] );
}

function test_keys_add_rejects_bad_pubkey_length(): void {
	wp_set_current_user( 11 );
	$res = Keys::add_key( new WP_REST_Request_Ext( 'POST', [
		'label'      => 'short',
		'pubkey_b64' => base64_encode( 'too-short' ),
	] ) );
	assertSame( 400, $res->get_status() );
	assertTrue( str_contains( $res->get_data()['error'], '32 bytes' ) );
}

function test_keys_isolated_per_user(): void {
	wp_set_current_user( 11 );
	Keys::add_key( new WP_REST_Request_Ext( 'POST', [ 'label' => 'a', 'pubkey_b64' => _keys_pubkey_b64() ] ) );

	wp_set_current_user( 22 );
	$list = Keys::list_keys( new WP_REST_Request_Ext( 'GET' ) );
	assertSame( 0, count( $list->get_data()['keys'] ) );
}

// --- /audit (admin only) -------------------------------------------------

function test_audit_requires_manage_options(): void {
	wp_set_current_user( 7 );
	$GLOBALS['__user_caps'] = []; // not an admin
	$gate = Audit::require_admin( new WP_REST_Request_Ext( 'GET' ) );
	assertWPError( $gate, 'git_logs_forbidden' );
}

function test_audit_admin_can_list_filtered_by_action(): void {
	wp_set_current_user( 7 );
	$GLOBALS['__user_caps'] = [ 'manage_options' ];

	AuditLog::record( [ 'action' => 'repo.upsert', 'result' => 'ok' ] );
	AuditLog::record( [ 'action' => 'run.create',  'result' => 'ok' ] );
	AuditLog::record( [ 'action' => 'run.create',  'result' => 'ok' ] );

	$gate = Audit::require_admin( new WP_REST_Request_Ext( 'GET' ) );
	assertSame( true, $gate );

	$res = Audit::list_entries( new WP_REST_Request_Ext( 'GET', [ 'action' => 'run.create' ] ) );
	$entries = $res->get_data()['entries'];
	assertSame( 2, count( $entries ) );
	foreach ( $entries as $e ) { assertSame( 'run.create', $e['action'] ); }
}

function test_audit_clamps_limit(): void {
	wp_set_current_user( 7 );
	$GLOBALS['__user_caps'] = [ 'manage_options' ];
	for ( $i = 0; $i < 10; $i++ ) {
		AuditLog::record( [ 'action' => 'x', 'result' => 'ok' ] );
	}
	$res = Audit::list_entries( new WP_REST_Request_Ext( 'GET', [ 'limit' => 3 ] ) );
	assertSame( 3, count( $res->get_data()['entries'] ) );
}
