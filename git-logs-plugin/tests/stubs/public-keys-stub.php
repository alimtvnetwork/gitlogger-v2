<?php
/**
 * In-memory PublicKeys stub for unit tests. Replaces the wpdb-backed
 * implementation so Ed25519Resolver can look up keys without a database
 * AND so the /keys REST controller can be exercised end-to-end.
 */

declare( strict_types = 1 );

namespace GitLogs\Auth;

defined( 'ABSPATH' ) || exit;

if ( ! class_exists( __NAMESPACE__ . '\\PublicKeys' ) ) {
	final class PublicKeys {
		/** @var array<string,array{user_id:int,pubkey:string,label:string,created_utc:string,last_used_utc:?string}> */
		public static array $keys    = [];
		public static array $touched = [];

		public static function reset(): void {
			self::$keys    = [];
			self::$touched = [];
		}

		// Test helper used by Ed25519Resolver tests.
		public static function register( string $key_id, string $pubkey, int $user_id = 7 ): void {
			self::$keys[ $key_id ] = [
				'id'            => $key_id,
				'user_id'       => $user_id,
				'pubkey'        => $pubkey,
				'pubkey_b64'    => base64_encode( $pubkey ),
				'label'         => 'preregistered',
				'created_utc'   => gmdate( 'c' ),
				'last_used_utc' => null,
			];
		}

		public static function find_by_key_id( string $key_id ): ?array {
			return self::$keys[ $key_id ] ?? null;
		}

		public static function touch_last_used( int $user_id, string $key_id ): void {
			self::$touched[] = [ $user_id, $key_id ];
			if ( isset( self::$keys[ $key_id ] ) ) {
				self::$keys[ $key_id ]['last_used_utc'] = gmdate( 'c' );
			}
		}

		// REST surface --------------------------------------------------

		public static function list_for_user( int $user_id ): array {
			$out = [];
			foreach ( self::$keys as $k ) {
				if ( (int) $k['user_id'] === $user_id ) $out[] = $k;
			}
			return $out;
		}

		public static function add( int $user_id, string $label, string $pubkey_b64 ): string {
			if ( '' === trim( $label ) ) {
				throw new \InvalidArgumentException( 'label required' );
			}
			$raw = base64_decode( $pubkey_b64, true );
			if ( false === $raw || 32 !== strlen( $raw ) ) {
				throw new \InvalidArgumentException( 'pubkey_b64 must decode to 32 bytes' );
			}
			$id = substr( hash( 'sha256', $raw ), 0, 8 );
			self::$keys[ $id ] = [
				'id'            => $id,
				'user_id'       => $user_id,
				'pubkey'        => $raw,
				'pubkey_b64'    => $pubkey_b64,
				'label'         => $label,
				'created_utc'   => gmdate( 'c' ),
				'last_used_utc' => null,
			];
			return $id;
		}

		public static function delete( int $user_id, string $key_id ): bool {
			if ( isset( self::$keys[ $key_id ] ) && (int) self::$keys[ $key_id ]['user_id'] === $user_id ) {
				unset( self::$keys[ $key_id ] );
				return true;
			}
			return false;
		}
	}
}
