<?php
/**
 * REST: POST /wp-json/git-logs/v1/events
 * Streaming-mode incremental event ingest (§06).
 *
 * Accepts batches of {Ts, Level, Line} events. Creates a Run row on
 * first call (RunId omitted), then upserts events keyed by (run_id, ts, line).
 * When Final=true, the run row's status transitions queued|running → passed
 * (or failed if any error events were seen).
 *
 * @package GitLogs\Rest
 */

declare( strict_types = 1 );

namespace GitLogs\Rest;

defined( 'ABSPATH' ) || exit;

require_once __DIR__ . '/../auth/class-auth-context.php';
require_once __DIR__ . '/../db/class-event-store.php';
require_once __DIR__ . '/../db/class-run-store.php';
require_once __DIR__ . '/../db/class-repo-store.php';

final class Events {

	public static function register(): void {
		register_rest_route(
			\GitLogs\GIT_LOGS_REST_NS,
			'/events',
			[
				'methods'             => 'POST',
				'callback'            => [ self::class, 'handle' ],
				'permission_callback' => [ \GitLogs\Auth\AuthContext::class, 'require_authenticated' ],
			]
		);
	}

	public static function handle( \WP_REST_Request $r ): \WP_REST_Response {
		$body = $r->get_json_params();
		if ( ! is_array( $body ) ) {
			return new \WP_REST_Response( [ 'ErrorCode' => 'GL-EVENTS-BAD-JSON' ], 400 );
		}

		$repo_url = (string) ( $body['RepoUrl'] ?? '' );
		$branch   = (string) ( $body['Branch'] ?? '' );
		$sha      = (string) ( $body['GitSha256'] ?? '' );
		$run_id   = (string) ( $body['RunId'] ?? '' );
		$events   = is_array( $body['Events'] ?? null ) ? $body['Events'] : [];
		$final    = ! empty( $body['Final'] );

		if ( '' === $repo_url || '' === $sha ) {
			return new \WP_REST_Response( [ 'ErrorCode' => 'GL-EVENTS-MISSING-FIELDS' ], 400 );
		}

		// Resolve / create the run row on first call.
		if ( '' === $run_id ) {
			$repo_id = \GitLogs\DB\RepoStore::ensure( $repo_url );
			$run_id  = \GitLogs\DB\RunStore::create_streaming( [
				'repo_id'   => $repo_id,
				'branch'    => $branch,
				'git_sha'   => $sha,
				'pipeline'  => (string) ( $body['PipelineName'] ?? 'stream' ),
			] );
		}

		$inserted = 0;
		$has_err  = false;
		foreach ( $events as $ev ) {
			if ( ! is_array( $ev ) ) {
				continue;
			}
			$level = (string) ( $ev['Level'] ?? 'info' );
			$line  = (string) ( $ev['Line'] ?? '' );
			$ts    = (string) ( $ev['Ts'] ?? gmdate( 'c' ) );
			\GitLogs\DB\EventStore::append( $run_id, $ts, $level, $line );
			$inserted++;
			if ( 'error' === $level ) {
				$has_err = true;
			}
		}

		if ( $final ) {
			\GitLogs\DB\RunStore::finalize( $run_id, $has_err ? 'failed' : 'passed' );
		}

		return new \WP_REST_Response( [
			'Accepted'  => true,
			'RunId'     => $run_id,
			'Inserted'  => $inserted,
			'Final'     => $final,
		], 200 );
	}
}
