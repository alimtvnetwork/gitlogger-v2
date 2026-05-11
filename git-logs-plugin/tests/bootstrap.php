<?php
/**
 * PHPUnit-free WordPress shim for the plugin's auth/REST unit tests.
 *
 * Provides just enough of the WP runtime (WP_Error, WP_REST_Request,
 * transients, helpers) so that the auth classes can be exercised in
 * isolation under plain `php`. No database, no HTTP, no plugins loaded.
 */

declare( strict_types = 1 );

if ( ! defined( 'ABSPATH' ) ) {
	define( 'ABSPATH', __DIR__ . '/' );
}

// --- WP_Error -------------------------------------------------------------
if ( ! class_exists( 'WP_Error' ) ) {
	class WP_Error {
		public string $code;
		public string $message;
		public array  $data;
		public function __construct( string $code = '', string $message = '', $data = [] ) {
			$this->code    = $code;
			$this->message = $message;
			$this->data    = is_array( $data ) ? $data : [ 'data' => $data ];
		}
		public function get_error_code(): string    { return $this->code; }
		public function get_error_message(): string { return $this->message; }
		public function get_error_data() { return $this->data; }
	}
}
if ( ! function_exists( 'is_wp_error' ) ) {
	function is_wp_error( $thing ): bool { return $thing instanceof WP_Error; }
}

// --- WP_REST_Request ------------------------------------------------------
if ( ! class_exists( 'WP_REST_Request' ) ) {
	class WP_REST_Request {
		private string $method;
		private string $body;
		private array  $headers;
		public function __construct( string $method = 'GET', string $body = '', array $headers = [] ) {
			$this->method = $method;
			$this->body   = $body;
			// Normalise to lower-snake (matches WP_REST_Request::get_header behaviour).
			$norm = [];
			foreach ( $headers as $k => $v ) {
				$norm[ strtolower( str_replace( '-', '_', (string) $k ) ) ] = (string) $v;
			}
			$this->headers = $norm;
		}
		public function get_method(): string { return $this->method; }
		public function get_body(): string   { return $this->body; }
		public function get_header( string $name ): string {
			$key = strtolower( str_replace( '-', '_', $name ) );
			return $this->headers[ $key ] ?? '';
		}
	}
}

// --- transients (in-memory) ----------------------------------------------
$GLOBALS['__transients'] = [];
if ( ! function_exists( 'get_transient' ) ) {
	function get_transient( string $k ) {
		$store = $GLOBALS['__transients'] ?? [];
		if ( ! isset( $store[ $k ] ) ) {
			return false;
		}
		[ $val, $expires ] = $store[ $k ];
		if ( $expires > 0 && $expires < time() ) {
			unset( $GLOBALS['__transients'][ $k ] );
			return false;
		}
		return $val;
	}
}
if ( ! function_exists( 'set_transient' ) ) {
	function set_transient( string $k, $v, int $ttl = 0 ): bool {
		$GLOBALS['__transients'][ $k ] = [ $v, $ttl > 0 ? time() + $ttl : 0 ];
		return true;
	}
}

// --- misc WP helpers ------------------------------------------------------
if ( ! function_exists( 'wp_unslash' ) ) {
	function wp_unslash( $v ) {
		return is_string( $v ) ? stripslashes( $v ) : $v;
	}
}
if ( ! function_exists( '__' ) ) {
	function __( string $s, string $domain = '' ): string { return $s; }
}
if ( ! function_exists( 'is_user_logged_in' ) ) {
	function is_user_logged_in(): bool { return ( $GLOBALS['__current_user_id'] ?? 0 ) > 0; }
}
if ( ! function_exists( 'wp_set_current_user' ) ) {
	function wp_set_current_user( int $id ): void { $GLOBALS['__current_user_id'] = $id; }
}
if ( ! function_exists( 'get_current_user_id' ) ) {
	function get_current_user_id(): int { return (int) ( $GLOBALS['__current_user_id'] ?? 0 ); }
}

// --- Stub for PublicKeys (auth classes require it) -----------------------
// We pre-load an in-memory key registry under \GitLogs\Auth\PublicKeys so
// the resolver doesn't try to touch wpdb. Loaded BEFORE the auth classes.
require_once __DIR__ . '/stubs/public-keys-stub.php';

// --- Load the system under test ------------------------------------------
require_once __DIR__ . '/../includes/auth/class-nonce-store.php';
require_once __DIR__ . '/../includes/auth/class-ed25519-resolver.php';
require_once __DIR__ . '/../includes/auth/class-auth-context.php';
