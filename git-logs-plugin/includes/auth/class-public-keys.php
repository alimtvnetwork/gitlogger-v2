<?php
/**
 * PublicKeys — per-user Ed25519 public-key registry, stored in user_meta.
 *
 * Each user has a list of keys: [ { id, label, pubkey_b64, created_utc, last_used_utc } ].
 * The keyId is a short random string (8 chars) used to look up the right key
 * during signature verification, scoped to the user.
 *
 * Format of the wire pubkey: base64 of 32-byte raw Ed25519 public key.
 *
 * @package GitLogs\Auth
 */

declare( strict_types = 1 );

namespace GitLogs\Auth;

defined( 'ABSPATH' ) || exit;

final class PublicKeys {

	private const META_KEY = 'git_logs_public_keys';

	/** @return array<int,array<string,mixed>> */
	public static function list_for_user( int $user_id ): array {
		$raw = get_user_meta( $user_id, self::META_KEY, true );
		return is_array( $raw ) ? array_values( $raw ) : [];
	}

	/**
	 * Look up a (user_id, raw_pubkey_bytes) pair by key_id.
	 * Searches across all users. Returns null if not found.
	 *
	 * @return array{user_id:int, pubkey:string}|null
	 */
	public static function find_by_key_id( string $key_id ): ?array {
		global $wpdb;
		// Bounded scan: only users who have at least one key registered.
		$rows = $wpdb->get_results(
			$wpdb->prepare(
				"SELECT user_id, meta_value FROM {$wpdb->usermeta} WHERE meta_key = %s",
				self::META_KEY
			)
		);
		if ( ! $rows ) {
			return null;
		}
		foreach ( $rows as $row ) {
			$keys = maybe_unserialize( $row->meta_value );
			if ( ! is_array( $keys ) ) {
				continue;
			}
			foreach ( $keys as $k ) {
				if ( ! is_array( $k ) || ( $k['id'] ?? '' ) !== $key_id ) {
					continue;
				}
				$bytes = base64_decode( (string) ( $k['pubkey_b64'] ?? '' ), true );
				if ( false === $bytes || 32 !== strlen( $bytes ) ) {
					continue;
				}
				return [ 'user_id' => (int) $row->user_id, 'pubkey' => $bytes ];
			}
		}
		return null;
	}

	/**
	 * Add a new key for the given user. Returns the assigned keyId.
	 *
	 * @throws \InvalidArgumentException on malformed pubkey.
	 */
	public static function add( int $user_id, string $label, string $pubkey_b64 ): string {
		$bytes = base64_decode( $pubkey_b64, true );
		if ( false === $bytes || 32 !== strlen( $bytes ) ) {
			throw new \InvalidArgumentException( 'pubkey_b64 must decode to exactly 32 bytes (Ed25519 public key)' );
		}
		$key_id  = substr( bin2hex( random_bytes( 6 ) ), 0, 8 );
		$current = self::list_for_user( $user_id );
		$current[] = [
			'id'            => $key_id,
			'label'         => sanitize_text_field( $label ),
			'pubkey_b64'    => $pubkey_b64,
			'created_utc'   => gmdate( 'c' ),
			'last_used_utc' => null,
		];
		update_user_meta( $user_id, self::META_KEY, $current );
		return $key_id;
	}

	public static function delete( int $user_id, string $key_id ): bool {
		$current = self::list_for_user( $user_id );
		$kept    = array_values( array_filter( $current, static fn( $k ) => ( $k['id'] ?? '' ) !== $key_id ) );
		if ( count( $kept ) === count( $current ) ) {
			return false;
		}
		update_user_meta( $user_id, self::META_KEY, $kept );
		return true;
	}

	public static function touch_last_used( int $user_id, string $key_id ): void {
		$current = self::list_for_user( $user_id );
		foreach ( $current as &$k ) {
			if ( ( $k['id'] ?? '' ) === $key_id ) {
				$k['last_used_utc'] = gmdate( 'c' );
				break;
			}
		}
		unset( $k );
		update_user_meta( $user_id, self::META_KEY, $current );
	}
}
