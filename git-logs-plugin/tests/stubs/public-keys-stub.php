<?php
/**
 * In-memory PublicKeys stub for unit tests. Replaces the wpdb-backed
 * implementation so Ed25519Resolver can look up keys without a database.
 */

declare( strict_types = 1 );

namespace GitLogs\Auth;

defined( 'ABSPATH' ) || exit;

if ( ! class_exists( __NAMESPACE__ . '\\PublicKeys' ) ) {
	final class PublicKeys {
		/** @var array<string,array{user_id:int,pubkey:string}> */
		public static array $keys    = [];
		public static array $touched = [];

		public static function reset(): void {
			self::$keys    = [];
			self::$touched = [];
		}
		public static function register( string $key_id, string $pubkey, int $user_id = 7 ): void {
			self::$keys[ $key_id ] = [ 'user_id' => $user_id, 'pubkey' => $pubkey ];
		}
		/** @return array{user_id:int,pubkey:string}|null */
		public static function find_by_key_id( string $key_id ): ?array {
			return self::$keys[ $key_id ] ?? null;
		}
		public static function touch_last_used( int $user_id, string $key_id ): void {
			self::$touched[] = [ $user_id, $key_id ];
		}
	}
}
