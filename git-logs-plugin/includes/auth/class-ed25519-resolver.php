<?php
/**
 * Ed25519Resolver — verifies the X-GitLogs-Auth header and returns the user_id
 * (or WP_Error). Uses libsodium (`sodium_crypto_sign_verify_detached`).
 *
 * Header format (single line, comma-separated, order-insensitive):
 *
 *     X-GitLogs-Auth: GLCI1-ED25519 keyId=<id>,nonce=<n>,ts=<unix>,sig=<base64>
 *
 * Canonical signing string (LF-separated, no trailing LF):
 *
 *     GLCI1-ED25519
 *     <METHOD>
 *     <PATH-AND-QUERY>
 *     <SHA256_HEX_OF_BODY>
 *     <NONCE>
 *     <TIMESTAMP>
 *     <KEY_ID>
 *
 * Rules:
 *   - METHOD is uppercase (GET, POST, ...).
 *   - PATH-AND-QUERY is the request URI starting with '/', including query string if any.
 *   - SHA256_HEX_OF_BODY is sha256 of the raw request body (empty body → sha256 of "").
 *   - NONCE is opaque, ≤ 64 chars, [A-Za-z0-9_-].
 *   - TIMESTAMP is unix seconds, must be within ±300s of server time.
 *   - KEY_ID identifies which registered public key to use.
 *
 * @package GitLogs\Auth
 */

declare( strict_types = 1 );

namespace GitLogs\Auth;

defined( 'ABSPATH' ) || exit;

final class Ed25519Resolver {

	public const SCHEME           = 'GLCI1-ED25519';
	public const TIMESTAMP_WINDOW = 300; // ± seconds

	/**
	 * @return int|\WP_Error user_id on success, WP_Error on failure
	 */
	public static function resolve( \WP_REST_Request $request, string $header ) {
		if ( ! function_exists( 'sodium_crypto_sign_verify_detached' ) ) {
			return new \WP_Error( 'git_logs_auth_no_sodium', 'libsodium is required for Ed25519 auth', [ 'status' => 500 ] );
		}

		$parsed = self::parse_header( $header );
		if ( is_wp_error( $parsed ) ) {
			return $parsed;
		}
		[ 'key_id' => $key_id, 'nonce' => $nonce, 'ts' => $ts, 'sig' => $sig_b64 ] = $parsed;

		// Timestamp window.
		$now = time();
		if ( abs( $now - $ts ) > self::TIMESTAMP_WINDOW ) {
			return new \WP_Error( 'git_logs_auth_clock_skew', 'timestamp outside ±300s window', [ 'status' => 401 ] );
		}

		// Replay protection.
		if ( NonceStore::seen_or_remember( $key_id, $nonce ) ) {
			return new \WP_Error( 'git_logs_auth_replay', 'nonce already used', [ 'status' => 401 ] );
		}

		// Lookup key.
		$found = PublicKeys::find_by_key_id( $key_id );
		if ( null === $found ) {
			return new \WP_Error( 'git_logs_auth_unknown_key', 'unknown keyId', [ 'status' => 401 ] );
		}

		// Build canonical string.
		$method     = strtoupper( $request->get_method() );
		$path_query = self::request_path_and_query();
		$body_hash  = hash( 'sha256', (string) $request->get_body() );

		$canonical = implode(
			"\n",
			[
				self::SCHEME,
				$method,
				$path_query,
				$body_hash,
				$nonce,
				(string) $ts,
				$key_id,
			]
		);

		$sig = base64_decode( $sig_b64, true );
		if ( false === $sig || 64 !== strlen( $sig ) ) {
			return new \WP_Error( 'git_logs_auth_bad_sig', 'sig must decode to 64 bytes', [ 'status' => 401 ] );
		}

		$ok = sodium_crypto_sign_verify_detached( $sig, $canonical, $found['pubkey'] );
		if ( ! $ok ) {
			return new \WP_Error( 'git_logs_auth_invalid_sig', 'signature verification failed', [ 'status' => 401 ] );
		}

		PublicKeys::touch_last_used( $found['user_id'], $key_id );
		return $found['user_id'];
	}

	/**
	 * @return array{key_id:string,nonce:string,ts:int,sig:string}|\WP_Error
	 */
	private static function parse_header( string $header ) {
		$header = trim( $header );
		$prefix = self::SCHEME . ' ';
		if ( 0 !== strpos( $header, $prefix ) ) {
			return new \WP_Error( 'git_logs_auth_bad_scheme', 'expected scheme ' . self::SCHEME, [ 'status' => 401 ] );
		}
		$rest = substr( $header, strlen( $prefix ) );
		$out  = [ 'key_id' => '', 'nonce' => '', 'ts' => 0, 'sig' => '' ];
		foreach ( explode( ',', $rest ) as $part ) {
			$kv = explode( '=', trim( $part ), 2 );
			if ( 2 !== count( $kv ) ) {
				continue;
			}
			[ $k, $v ] = $kv;
			switch ( strtolower( trim( $k ) ) ) {
				case 'keyid': $out['key_id'] = trim( $v ); break;
				case 'nonce': $out['nonce']  = trim( $v ); break;
				case 'ts':    $out['ts']     = (int) trim( $v ); break;
				case 'sig':   $out['sig']    = trim( $v ); break;
			}
		}
		if ( '' === $out['key_id'] || '' === $out['nonce'] || 0 === $out['ts'] || '' === $out['sig'] ) {
			return new \WP_Error( 'git_logs_auth_bad_header', 'missing keyId/nonce/ts/sig', [ 'status' => 401 ] );
		}
		if ( ! preg_match( '/\A[A-Za-z0-9_-]{1,64}\z/', $out['nonce'] ) ) {
			return new \WP_Error( 'git_logs_auth_bad_nonce', 'nonce must match [A-Za-z0-9_-]{1,64}', [ 'status' => 401 ] );
		}
		return $out;
	}

	private static function request_path_and_query(): string {
		$uri = isset( $_SERVER['REQUEST_URI'] ) ? (string) wp_unslash( $_SERVER['REQUEST_URI'] ) : '/';
		// Normalise: strip scheme/host if a proxy passed it through.
		if ( false !== ( $p = strpos( $uri, '://' ) ) ) {
			$slash = strpos( $uri, '/', $p + 3 );
			$uri   = false === $slash ? '/' : substr( $uri, $slash );
		}
		return $uri;
	}
}
