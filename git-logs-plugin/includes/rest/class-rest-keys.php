<?php
/**
 * REST: /wp-json/git-logs/v1/keys
 *
 *   GET    /keys             list current user's keys (no pubkey bytes — id+label+timestamps only)
 *   POST   /keys             body: { label, pubkey_b64 } → { id }
 *   DELETE /keys/<id>        delete a key
 *
 * All routes authenticated via AuthContext.
 *
 * @package GitLogs\Rest
 */

declare( strict_types = 1 );

namespace GitLogs\Rest;

defined( 'ABSPATH' ) || exit;

require_once __DIR__ . '/../auth/class-auth-context.php';
require_once __DIR__ . '/../auth/class-public-keys.php';

final class Keys {

	public static function register(): void {
		$ns   = \GitLogs\GIT_LOGS_REST_NS;
		$auth = [ \GitLogs\Auth\AuthContext::class, 'require_authenticated' ];

		register_rest_route( $ns, '/keys', [
			[
				'methods'             => 'GET',
				'callback'            => [ self::class, 'list_keys' ],
				'permission_callback' => $auth,
			],
			[
				'methods'             => 'POST',
				'callback'            => [ self::class, 'add_key' ],
				'permission_callback' => $auth,
				'args'                => [
					'label'      => [ 'required' => true, 'type' => 'string' ],
					'pubkey_b64' => [ 'required' => true, 'type' => 'string' ],
				],
			],
		] );

		register_rest_route( $ns, '/keys/(?P<id>[A-Fa-f0-9]{8})', [
			'methods'             => 'DELETE',
			'callback'            => [ self::class, 'delete_key' ],
			'permission_callback' => $auth,
		] );
	}

	public static function list_keys( \WP_REST_Request $r ): \WP_REST_Response {
		$rows = \GitLogs\Auth\PublicKeys::list_for_user( get_current_user_id() );
		// Strip pubkey_b64 from listing — clients only need the id/label/timestamps.
		$out = array_map( static fn( $k ) => [
			'id'            => $k['id'] ?? '',
			'label'         => $k['label'] ?? '',
			'created_utc'   => $k['created_utc'] ?? null,
			'last_used_utc' => $k['last_used_utc'] ?? null,
		], $rows );
		return new \WP_REST_Response( [ 'keys' => $out ], 200 );
	}

	public static function add_key( \WP_REST_Request $r ): \WP_REST_Response {
		try {
			$id = \GitLogs\Auth\PublicKeys::add(
				get_current_user_id(),
				(string) $r->get_param( 'label' ),
				(string) $r->get_param( 'pubkey_b64' )
			);
		} catch ( \InvalidArgumentException $e ) {
			return new \WP_REST_Response( [ 'error' => $e->getMessage() ], 400 );
		}
		return new \WP_REST_Response( [ 'id' => $id ], 201 );
	}

	public static function delete_key( \WP_REST_Request $r ): \WP_REST_Response {
		$ok = \GitLogs\Auth\PublicKeys::delete( get_current_user_id(), (string) $r['id'] );
		return new \WP_REST_Response( [ 'deleted' => $ok ], $ok ? 200 : 404 );
	}
}
