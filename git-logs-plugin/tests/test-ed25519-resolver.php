<?php
/**
 * Ed25519Resolver tests — exercises canonical signing string, header parser,
 * timestamp window, replay store integration, key lookup, and signature
 * verification (via libsodium).
 */

declare( strict_types = 1 );

use GitLogs\Auth\Ed25519Resolver;
use GitLogs\Auth\PublicKeys;

/** Build a signed request and matching X-GitLogs-Auth header. */
function _sign( string $method, string $path_and_query, string $body, string $key_id, string $priv, string $pub, ?int $ts = null, ?string $nonce = null ): array {
	$ts    = $ts    ?? time();
	$nonce = $nonce ?? rtrim( strtr( base64_encode( random_bytes( 12 ) ), '+/', '-_' ), '=' );
	$canonical = implode(
		"\n",
		[ 'GLCI1-ED25519', strtoupper( $method ), $path_and_query, hash( 'sha256', $body ), $nonce, (string) $ts, $key_id ]
	);
	$sig    = sodium_crypto_sign_detached( $canonical, $priv );
	$header = sprintf( 'GLCI1-ED25519 keyId=%s,nonce=%s,ts=%d,sig=%s', $key_id, $nonce, $ts, base64_encode( $sig ) );

	$_SERVER['REQUEST_URI'] = $path_and_query;
	$req = new WP_REST_Request( $method, $body, [ 'X-GitLogs-Auth' => $header ] );
	return [ $req, $header, $nonce ];
}

function _fresh_keypair(): array {
	$kp = sodium_crypto_sign_keypair();
	return [ sodium_crypto_sign_secretkey( $kp ), sodium_crypto_sign_publickey( $kp ) ];
}

// ------------------ Happy path ------------------

function test_ed25519_resolve_success_returns_user_id(): void {
	[ $priv, $pub ] = _fresh_keypair();
	PublicKeys::register( 'kid-1', $pub, 42 );

	[ $req ] = _sign( 'POST', '/wp-json/git-logs/v1/append-log?repo=acme%2Fwidget', '{"hello":"world"}', 'kid-1', $priv, $pub );
	$res = Ed25519Resolver::resolve( $req, $req->get_header( 'X-GitLogs-Auth' ) );

	assertSame( 42, $res, 'should return the registered user_id' );
	assertSame( 1, count( PublicKeys::$touched ), 'last_used must be touched on success' );
}

function test_ed25519_resolve_empty_body_uses_sha256_of_empty(): void {
	[ $priv, $pub ] = _fresh_keypair();
	PublicKeys::register( 'kid-empty', $pub, 7 );
	[ $req ] = _sign( 'GET', '/wp-json/git-logs/v1/whoami', '', 'kid-empty', $priv, $pub );
	assertSame( 7, Ed25519Resolver::resolve( $req, $req->get_header( 'X-GitLogs-Auth' ) ) );
}

// ------------------ Header parsing failures ------------------

function test_ed25519_bad_scheme(): void {
	$_SERVER['REQUEST_URI'] = '/x';
	$req = new WP_REST_Request( 'GET', '', [ 'X-GitLogs-Auth' => 'BEARER abc' ] );
	$res = Ed25519Resolver::resolve( $req, 'BEARER abc' );
	assertWPError( $res, 'git_logs_auth_bad_scheme' );
}

function test_ed25519_missing_field(): void {
	$_SERVER['REQUEST_URI'] = '/x';
	$req = new WP_REST_Request( 'GET', '', [] );
	$res = Ed25519Resolver::resolve( $req, 'GLCI1-ED25519 keyId=k,nonce=n,ts=1' ); // no sig
	assertWPError( $res, 'git_logs_auth_bad_header' );
}

function test_ed25519_bad_nonce_chars(): void {
	$_SERVER['REQUEST_URI'] = '/x';
	$req = new WP_REST_Request( 'GET', '', [] );
	$header = 'GLCI1-ED25519 keyId=k,nonce=bad space,ts=' . time() . ',sig=' . base64_encode( str_repeat( 'A', 64 ) );
	assertWPError( Ed25519Resolver::resolve( $req, $header ), 'git_logs_auth_bad_nonce' );
}

// ------------------ Time / replay / key lookup ------------------

function test_ed25519_clock_skew(): void {
	[ $priv, $pub ] = _fresh_keypair();
	PublicKeys::register( 'kid-skew', $pub, 1 );
	[ $req ] = _sign( 'GET', '/x', '', 'kid-skew', $priv, $pub, time() - 1000 );
	assertWPError( Ed25519Resolver::resolve( $req, $req->get_header( 'X-GitLogs-Auth' ) ), 'git_logs_auth_clock_skew' );
}

function test_ed25519_replay_rejected(): void {
	[ $priv, $pub ] = _fresh_keypair();
	PublicKeys::register( 'kid-replay', $pub, 5 );
	[ $req, , $nonce ] = _sign( 'POST', '/x', 'b', 'kid-replay', $priv, $pub );

	$first = Ed25519Resolver::resolve( $req, $req->get_header( 'X-GitLogs-Auth' ) );
	assertSame( 5, $first );

	// Re-issue exact same signed request → replay (nonce already remembered).
	$second = Ed25519Resolver::resolve( $req, $req->get_header( 'X-GitLogs-Auth' ) );
	assertWPError( $second, 'git_logs_auth_replay' );
}

function test_ed25519_unknown_key(): void {
	[ $priv, $pub ] = _fresh_keypair();
	// NOT registered.
	[ $req ] = _sign( 'GET', '/x', '', 'kid-missing', $priv, $pub );
	assertWPError( Ed25519Resolver::resolve( $req, $req->get_header( 'X-GitLogs-Auth' ) ), 'git_logs_auth_unknown_key' );
}

// ------------------ Signature failures ------------------

function test_ed25519_bad_sig_length(): void {
	[ , $pub ] = _fresh_keypair();
	PublicKeys::register( 'kid-len', $pub, 1 );
	$_SERVER['REQUEST_URI'] = '/x';
	$req = new WP_REST_Request( 'GET', '', [] );
	$header = sprintf( 'GLCI1-ED25519 keyId=kid-len,nonce=n,ts=%d,sig=%s', time(), base64_encode( 'short' ) );
	assertWPError( Ed25519Resolver::resolve( $req, $header ), 'git_logs_auth_bad_sig' );
}

function test_ed25519_invalid_sig_when_body_tampered(): void {
	[ $priv, $pub ] = _fresh_keypair();
	PublicKeys::register( 'kid-tamper', $pub, 9 );
	[ $req ] = _sign( 'POST', '/x', 'original', 'kid-tamper', $priv, $pub );
	// Replace the request body with a different one; sig was computed over "original".
	$bad_req = new WP_REST_Request( 'POST', 'tampered', [ 'X-GitLogs-Auth' => $req->get_header( 'X-GitLogs-Auth' ) ] );
	assertWPError( Ed25519Resolver::resolve( $bad_req, $req->get_header( 'X-GitLogs-Auth' ) ), 'git_logs_auth_invalid_sig' );
}

function test_ed25519_invalid_sig_when_path_tampered(): void {
	[ $priv, $pub ] = _fresh_keypair();
	PublicKeys::register( 'kid-path', $pub, 9 );
	[ $req ] = _sign( 'GET', '/wp-json/git-logs/v1/runs', '', 'kid-path', $priv, $pub );
	// Server now sees a different REQUEST_URI than the client signed.
	$_SERVER['REQUEST_URI'] = '/wp-json/git-logs/v1/admin/diagrams';
	assertWPError( Ed25519Resolver::resolve( $req, $req->get_header( 'X-GitLogs-Auth' ) ), 'git_logs_auth_invalid_sig' );
}
