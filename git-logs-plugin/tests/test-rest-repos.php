<?php
/**
 * Tests for the /repos REST controller.
 *
 * Exercises Repos::list_repos and Repos::upsert directly with crafted
 * WP_REST_Request_Ext objects and the in-memory RepoStore stub.
 */

declare( strict_types = 1 );

use GitLogs\Rest\Repos;
use GitLogs\DB\RepoStore;
use GitLogs\DB\AuditLog;

function _repos_logged_in(): void {
	wp_set_current_user( 7 );
	$GLOBALS['__current_user_login'] = 'alice';
}

function test_repos_upsert_creates_row_and_audit(): void {
	_repos_logged_in();
	$req = new WP_REST_Request_Ext( 'POST', [
		'slug'           => 'acme/api',
		'display_name'   => 'Acme API',
		'remote_url'     => 'https://github.com/acme/api',
		'default_branch' => 'main',
	] );
	$res = Repos::upsert( $req );
	assertSame( 201, $res->get_status() );
	$data = $res->get_data();
	assertSame( 'acme/api', $data['slug'] );
	assertSame( 1, $data['id'] );
	assertSame( 1, count( AuditLog::$rows ) );
	assertSame( 'repo.upsert', AuditLog::$rows[0]['action'] );
	assertSame( 'wp_session', AuditLog::$rows[0]['auth_lane'] );
}

function test_repos_upsert_with_signed_header_marks_ed25519_lane(): void {
	_repos_logged_in();
	$req = new WP_REST_Request_Ext(
		'POST',
		[ 'slug' => 'acme/api', 'display_name' => 'Acme API' ],
		'',
		[ 'X-GitLogs-Auth' => 'glci-ed25519 1' ]
	);
	$res = Repos::upsert( $req );
	assertSame( 201, $res->get_status() );
	assertSame( 'ed25519', AuditLog::$rows[0]['auth_lane'] );
}

function test_repos_upsert_rejects_invalid_slug(): void {
	_repos_logged_in();
	// After sanitize_key, leading "_" survives but fails the [a-z0-9] anchor.
	$req = new WP_REST_Request_Ext( 'POST', [
		'slug'         => '___',
		'display_name' => 'x',
	] );
	$res = Repos::upsert( $req );
	assertSame( 400, $res->get_status() );
	assertTrue( str_contains( $res->get_data()['error'], 'invalid slug' ) );
	assertSame( 0, count( RepoStore::$rows ) );
}

function test_repos_upsert_idempotent_on_same_slug(): void {
	_repos_logged_in();
	$mk = static fn( string $name ) => new WP_REST_Request_Ext(
		'POST', [ 'slug' => 'acme/api', 'display_name' => $name ]
	);
	$id1 = Repos::upsert( $mk( 'First' ) )->get_data()['id'];
	$id2 = Repos::upsert( $mk( 'Second' ) )->get_data()['id'];
	assertSame( $id1, $id2 );
	assertSame( 1, count( RepoStore::$rows ) );
	assertSame( 'Second', RepoStore::$rows[ $id1 ]['display_name'] );
}

function test_repos_list_filters_archived_by_default(): void {
	_repos_logged_in();
	$id1 = RepoStore::upsert( 'a/keep', 'Keep' );
	$id2 = RepoStore::upsert( 'a/archive', 'Archived' );
	RepoStore::$rows[ $id2 ]['archived'] = 1;

	$res = Repos::list_repos( new WP_REST_Request_Ext( 'GET' ) );
	assertSame( 200, $res->get_status() );
	$slugs = array_column( $res->get_data()['repos'], 'slug' );
	assertSame( [ 'a/keep' ], $slugs );

	$res2 = Repos::list_repos( new WP_REST_Request_Ext( 'GET', [ 'include_archived' => '1' ] ) );
	$slugs2 = array_column( $res2->get_data()['repos'], 'slug' );
	assertSame( [ 'a/keep', 'a/archive' ], $slugs2 );
}
