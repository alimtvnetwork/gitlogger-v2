<?php
/**
 * REST: /wp-json/git-logs/v1/runs
 *
 *   POST /runs                       create a run
 *   GET  /runs                       list (query: repo_slug, limit≤200)
 *   GET  /runs/{id}                  fetch single run
 *   POST /runs/{id}/events           append events batch
 *   GET  /runs/{id}/events           read events (after_seq, limit≤500)
 *   POST /runs/{id}/finalize         set terminal status + exit code, finalize summary
 *
 * @package GitLogs\Rest
 */

declare( strict_types = 1 );

namespace GitLogs\Rest;

defined( 'ABSPATH' ) || exit;

require_once __DIR__ . '/../auth/class-auth-context.php';
require_once __DIR__ . '/../db/class-repo-store.php';
require_once __DIR__ . '/../db/class-run-store.php';
require_once __DIR__ . '/../db/class-event-store.php';
require_once __DIR__ . '/../db/class-branch-store.php';
require_once __DIR__ . '/../db/class-audit-log.php';

final class Runs {

	public static function register(): void {
		$ns   = \GitLogs\GIT_LOGS_REST_NS;
		$auth = [ \GitLogs\Auth\AuthContext::class, 'require_authenticated' ];

		register_rest_route( $ns, '/runs', [
			[
				'methods'             => 'GET',
				'callback'            => [ self::class, 'list_runs' ],
				'permission_callback' => $auth,
			],
			[
				'methods'             => 'POST',
				'callback'            => [ self::class, 'create' ],
				'permission_callback' => $auth,
				'args'                => [
					'repo_slug'    => [ 'required' => true,  'type' => 'string' ],
					'branch'       => [ 'required' => true,  'type' => 'string' ],
					'sha'          => [ 'required' => true,  'type' => 'string' ],
					'ci_provider'  => [ 'required' => true,  'type' => 'string' ],
					'ci_run_url'   => [ 'required' => false, 'type' => 'string' ],
					'metadata'     => [ 'required' => false, 'type' => 'object' ],
				],
			],
		] );

		register_rest_route( $ns, '/runs/(?P<id>[A-Fa-f0-9-]{36})', [
			'methods'             => 'GET',
			'callback'            => [ self::class, 'fetch' ],
			'permission_callback' => $auth,
		] );

		register_rest_route( $ns, '/runs/(?P<id>[A-Fa-f0-9-]{36})/events', [
			[
				'methods'             => 'POST',
				'callback'            => [ self::class, 'append_events' ],
				'permission_callback' => $auth,
			],
			[
				'methods'             => 'GET',
				'callback'            => [ self::class, 'read_events' ],
				'permission_callback' => $auth,
			],
		] );

		register_rest_route( $ns, '/runs/(?P<id>[A-Fa-f0-9-]{36})/finalize', [
			'methods'             => 'POST',
			'callback'            => [ self::class, 'finalize' ],
			'permission_callback' => $auth,
			'args'                => [
				'status'    => [ 'required' => true,  'type' => 'string' ],
				'exit_code' => [ 'required' => false, 'type' => 'integer' ],
			],
		] );
	}

	public static function list_runs( \WP_REST_Request $r ): \WP_REST_Response {
		$slug  = (string) ( $r->get_param( 'repo_slug' ) ?? '' );
		$limit = max( 1, min( 200, (int) ( $r->get_param( 'limit' ) ?? 50 ) ) );
		if ( '' === $slug ) {
			return new \WP_REST_Response( [ 'error' => 'repo_slug is required' ], 400 );
		}
		$repo = \GitLogs\DB\RepoStore::find_by_slug( $slug );
		if ( null === $repo ) {
			return new \WP_REST_Response( [ 'error' => 'unknown repo_slug' ], 404 );
		}
		return new \WP_REST_Response( [
			'runs' => \GitLogs\DB\RunStore::list_recent( (int) $repo['id'], $limit ),
		], 200 );
	}

	public static function create( \WP_REST_Request $r ): \WP_REST_Response {
		$slug = (string) $r->get_param( 'repo_slug' );
		$repo = \GitLogs\DB\RepoStore::find_by_slug( $slug );
		if ( null === $repo ) {
			return new \WP_REST_Response( [ 'error' => 'unknown repo_slug' ], 404 );
		}
		$sha = strtolower( (string) $r->get_param( 'sha' ) );
		if ( ! preg_match( '/\A[0-9a-f]{40}\z/', $sha ) ) {
			return new \WP_REST_Response( [ 'error' => 'sha must be 40 lowercase hex chars' ], 400 );
		}

		$user_login = wp_get_current_user()->user_login ?: null;
		try {
			$id = \GitLogs\DB\RunStore::create( [
				'repo_id'      => (int) $repo['id'],
				'branch'       => (string) $r->get_param( 'branch' ),
				'sha'          => $sha,
				'ci_provider'  => (string) $r->get_param( 'ci_provider' ),
				'ci_run_url'   => $r->get_param( 'ci_run_url' ),
				'triggered_by' => $user_login,
				'metadata'     => $r->get_param( 'metadata' ),
			] );
		} catch ( \Throwable $e ) {
			return new \WP_REST_Response( [ 'error' => $e->getMessage() ], 400 );
		}

		\GitLogs\DB\BranchStore::touch( (int) $repo['id'], (string) $r->get_param( 'branch' ), $sha );
		\GitLogs\DB\RunStore::set_status( $id, 'running' );

		\GitLogs\DB\AuditLog::record( [
			'action'        => 'run.create',
			'result'        => 'ok',
			'target_type'   => 'run',
			'target_id'     => $id,
			'actor_user_id' => get_current_user_id(),
			'actor_login'   => $user_login,
			'auth_lane'     => '' !== (string) $r->get_header( 'x_gitlogs_auth' ) ? 'ed25519' : 'wp_session',
			'detail'        => [ 'repo_slug' => $slug, 'sha' => $sha ],
		] );

		return new \WP_REST_Response( [ 'id' => $id ], 201 );
	}

	public static function fetch( \WP_REST_Request $r ): \WP_REST_Response {
		$row = \GitLogs\DB\RunStore::find( (string) $r['id'] );
		if ( null === $row ) {
			return new \WP_REST_Response( [ 'error' => 'unknown run' ], 404 );
		}
		return new \WP_REST_Response( [ 'run' => $row ], 200 );
	}

	public static function append_events( \WP_REST_Request $r ): \WP_REST_Response {
		$run = \GitLogs\DB\RunStore::find( (string) $r['id'] );
		if ( null === $run ) {
			return new \WP_REST_Response( [ 'error' => 'unknown run' ], 404 );
		}
		$body   = json_decode( (string) $r->get_body(), true );
		$events = is_array( $body ) ? ( $body['events'] ?? null ) : null;
		if ( ! is_array( $events ) ) {
			return new \WP_REST_Response( [ 'error' => 'body must be {"events":[...]}' ], 400 );
		}
		try {
			$result = \GitLogs\DB\EventStore::append( (string) $run['sha'], (string) $run['id'], $events );
		} catch ( \Throwable $e ) {
			return new \WP_REST_Response( [ 'error' => $e->getMessage() ], 400 );
		}
		return new \WP_REST_Response( $result, 202 );
	}

	public static function read_events( \WP_REST_Request $r ): \WP_REST_Response {
		$run = \GitLogs\DB\RunStore::find( (string) $r['id'] );
		if ( null === $run ) {
			return new \WP_REST_Response( [ 'error' => 'unknown run' ], 404 );
		}
		$after = max( 0, (int) ( $r->get_param( 'after_seq' ) ?? 0 ) );
		$limit = max( 1, min( 500, (int) ( $r->get_param( 'limit' ) ?? 200 ) ) );
		return new \WP_REST_Response( [
			'events' => \GitLogs\DB\EventStore::read( (string) $run['sha'], (string) $run['id'], $after, $limit ),
		], 200 );
	}

	public static function finalize( \WP_REST_Request $r ): \WP_REST_Response {
		$run = \GitLogs\DB\RunStore::find( (string) $r['id'] );
		if ( null === $run ) {
			return new \WP_REST_Response( [ 'error' => 'unknown run' ], 404 );
		}
		$status    = (string) $r->get_param( 'status' );
		$exit_code = $r->get_param( 'exit_code' );
		$exit_code = ( null === $exit_code ) ? null : (int) $exit_code;

		try {
			\GitLogs\DB\RunStore::set_status( (string) $run['id'], $status, $exit_code );
			\GitLogs\DB\EventStore::finalize( (string) $run['sha'], (string) $run['id'], null, $exit_code );
		} catch ( \Throwable $e ) {
			return new \WP_REST_Response( [ 'error' => $e->getMessage() ], 400 );
		}

		\GitLogs\DB\AuditLog::record( [
			'action'        => 'run.finalize',
			'result'        => 'ok',
			'target_type'   => 'run',
			'target_id'     => (string) $run['id'],
			'actor_user_id' => get_current_user_id(),
			'actor_login'   => wp_get_current_user()->user_login ?: null,
			'auth_lane'     => '' !== (string) $r->get_header( 'x_gitlogs_auth' ) ? 'ed25519' : 'wp_session',
			'detail'        => [ 'status' => $status, 'exit_code' => $exit_code ],
		] );

		return new \WP_REST_Response( [
			'run' => \GitLogs\DB\RunStore::find( (string) $run['id'] ),
		], 200 );
	}
}
