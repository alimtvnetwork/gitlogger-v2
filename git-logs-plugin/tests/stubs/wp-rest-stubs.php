<?php
/**
 * Minimal WP REST shims so the Git-Logs REST controllers can be invoked
 * directly (handler methods receive a WP_REST_Request, return a
 * WP_REST_Response) without spinning up the full WP_REST_Server.
 */

declare( strict_types = 1 );

namespace {
	defined( 'ABSPATH' ) || exit;

	// REST namespace constant the controllers reference. We must use define()
	// (not `const`) because `const` cannot live inside a conditional block.
	if ( ! defined( 'GitLogs\\GIT_LOGS_REST_NS' ) ) {
		define( 'GitLogs\\GIT_LOGS_REST_NS', 'git-logs/v1' );
	}

	if ( ! class_exists( 'WP_REST_Response' ) ) {
		class WP_REST_Response {
			private $data;
			private int $status;
			private array $headers;
			public function __construct( $data = null, int $status = 200, array $headers = [] ) {
				$this->data    = $data;
				$this->status  = $status;
				$this->headers = $headers;
			}
			public function get_status(): int { return $this->status; }
			public function get_data() { return $this->data; }
			public function get_headers(): array { return $this->headers; }
		}
	}

	// ParamBag-aware request: extends the auth bootstrap WP_REST_Request with
	// a params/body-json view that controllers rely on.
	if ( ! class_exists( 'WP_REST_Request_Ext' ) ) {
		class WP_REST_Request_Ext extends WP_REST_Request implements ArrayAccess {
			public array $params = [];
			public array $url_params = [];
			public function __construct( string $method = 'GET', array $params = [], string $body = '', array $headers = [], array $url_params = [] ) {
				parent::__construct( $method, $body, $headers );
				$this->params     = $params;
				$this->url_params = $url_params;
			}
			public function get_param( string $name ) {
				return $this->params[ $name ] ?? $this->url_params[ $name ] ?? null;
			}
			public function get_json_params() {
				$decoded = json_decode( $this->get_body(), true );
				return is_array( $decoded ) ? $decoded : null;
			}
			// ArrayAccess maps to URL params, mirroring WP_REST_Request behaviour
			// when controllers do `$r['id']`.
			public function offsetExists( $o ): bool { return isset( $this->url_params[ $o ] ); }
			public function offsetGet( $o ): mixed   { return $this->url_params[ $o ] ?? null; }
			public function offsetSet( $o, $v ): void { $this->url_params[ $o ] = $v; }
			public function offsetUnset( $o ): void  { unset( $this->url_params[ $o ] ); }
		}
	}

	if ( ! function_exists( 'register_rest_route' ) ) {
		$GLOBALS['__rest_routes'] = [];
		function register_rest_route( string $ns, string $route, array $args = [], bool $override = false ): bool {
			$GLOBALS['__rest_routes'][ "$ns|$route" ] = $args;
			return true;
		}
	}

	if ( ! function_exists( 'sanitize_key' ) ) {
		function sanitize_key( $key ) {
			$key = strtolower( (string) $key );
			return preg_replace( '/[^a-z0-9_\-\/.]/', '', $key );
		}
	}

	if ( ! function_exists( 'current_user_can' ) ) {
		function current_user_can( string $cap ): bool {
			$caps = $GLOBALS['__user_caps'] ?? [];
			return in_array( $cap, $caps, true );
		}
	}

	if ( ! function_exists( 'wp_get_current_user' ) ) {
		function wp_get_current_user() {
			$id = (int) ( $GLOBALS['__current_user_id'] ?? 0 );
			$u  = (object) [
				'ID'           => $id,
				'user_login'   => $id > 0 ? ( $GLOBALS['__current_user_login'] ?? 'tester' ) : '',
				'display_name' => $id > 0 ? ( $GLOBALS['__current_user_display'] ?? 'Tester' ) : '',
				'roles'        => $GLOBALS['__current_user_roles'] ?? [],
			];
			return $u;
		}
	}
}
