<?php
/**
 * NonceStore — replay protection for Ed25519 signed requests.
 *
 * Backed by WP transients. Each (keyId, nonce) pair is stored for 600s
 * (twice the timestamp window). Re-presenting the same nonce within the TTL
 * is rejected as a replay.
 *
 * @package GitLogs\Auth
 */

declare( strict_types = 1 );

namespace GitLogs\Auth;

defined( 'ABSPATH' ) || exit;

final class NonceStore {

	private const PREFIX = 'gl_nonce_';
	private const TTL    = 600; // seconds

	public static function seen_or_remember( string $key_id, string $nonce ): bool {
		$cache_key = self::PREFIX . md5( $key_id . '|' . $nonce );
		if ( false !== get_transient( $cache_key ) ) {
			return true; // already seen → replay
		}
		set_transient( $cache_key, 1, self::TTL );
		return false;
	}
}
