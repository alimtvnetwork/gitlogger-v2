<?php
/**
 * AuthContext tests — verifies the permission_callback dispatches correctly
 * between Lane 1 (logged-in WP user) and Lane 2 (Ed25519 header).
 */

declare( strict_types = 1 );

use GitLogs\Auth\AuthContext;
use GitLogs\Auth\PublicKeys;

function test_authctx_logged_in_user_passes(): void {
	wp_set_current_user( 99 );
	$_SERVER['REQUEST_URI'] = '/x';
	$req = new WP_REST_Request( 'GET', '', [] );
	assertSame( true, AuthContext::require_authenticated( $req ) );
}

function test_authctx_no_creds_returns_unauthorized(): void {
	$_SERVER['REQUEST_URI'] = '/x';
	$req = new WP_REST_Request( 'GET', '', [] );
	$res = AuthContext::require_authenticated( $req );
	assertWPError( $res, 'git_logs_unauthorized' );
}

function test_authctx_ed25519_header_routes_to_resolver(): void {
	$kp   = sodium_crypto_sign_keypair();
	$priv = sodium_crypto_sign_secretkey( $kp );
	$pub  = sodium_crypto_sign_publickey( $kp );
	PublicKeys::register( 'kid-ctx', $pub, 11 );

	$ts    = time();
	$nonce = 'authctx-nonce';
	$path  = '/wp-json/git-logs/v1/whoami';
	$canon = implode( "\n", [ 'GLCI1-ED25519', 'GET', $path, hash( 'sha256', '' ), $nonce, (string) $ts, 'kid-ctx' ] );
	$sig   = sodium_crypto_sign_detached( $canon, $priv );
	$hdr   = sprintf( 'GLCI1-ED25519 keyId=kid-ctx,nonce=%s,ts=%d,sig=%s', $nonce, $ts, base64_encode( $sig ) );

	$_SERVER['REQUEST_URI'] = $path;
	$req = new WP_REST_Request( 'GET', '', [ 'X-GitLogs-Auth' => $hdr ] );

	assertSame( true, AuthContext::require_authenticated( $req ) );
	assertSame( 11, get_current_user_id(), 'wp_set_current_user must be called with resolver result' );
}

function test_authctx_ed25519_bad_sig_propagates_wp_error(): void {
	$kp   = sodium_crypto_sign_keypair();
	$pub  = sodium_crypto_sign_publickey( $kp );
	PublicKeys::register( 'kid-badsig', $pub, 12 );

	$ts  = time();
	$hdr = sprintf( 'GLCI1-ED25519 keyId=kid-badsig,nonce=n,ts=%d,sig=%s', $ts, base64_encode( str_repeat( 'A', 64 ) ) );
	$_SERVER['REQUEST_URI'] = '/x';
	$req = new WP_REST_Request( 'GET', '', [ 'X-GitLogs-Auth' => $hdr ] );

	$res = AuthContext::require_authenticated( $req );
	assertWPError( $res, 'git_logs_auth_invalid_sig' );
}
