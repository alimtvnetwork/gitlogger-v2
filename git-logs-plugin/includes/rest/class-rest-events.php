<?php
/**
 * REST: POST /wp-json/git-logs/v1/events
 * Streaming-mode incremental event ingest (§06).
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
		$branch   = (string) ( $body['Branch'] ?? 'main' );
		$sha      = strtolower( (string) ( $body['GitSha256'] ?? '' ) );
		$run_id   = (string) ( $body['RunId'] ?? '' );
		$events   = is_array( $body['Events'] ?? null ) ? $body['Events'] : [];
		$final    = ! empty( $body['Final'] );

		if ( '' === $repo_url || '' === $sha ) {
			return new \WP_REST_Response( [ 'ErrorCode' => 'GL-EVENTS-MISSING-FIELDS' ], 400 );
		}

		// Resolve / create the run row on first call.
		if ( '' === $run_id ) {
			$slug    = self::slug_from_url( $repo_url );
			$repo_id = \GitLogs\DB\RepoStore::upsert( $slug, $slug, $repo_url, $branch );
			$run_id  = \GitLogs\DB\RunStore::create( [
				'repo_id'      => $repo_id,
				'branch'       => $branch,
				'sha'          => $sha,
				'ci_provider'  => 'glci-stream',
				'triggered_by' => 'glci',
			] );
			\GitLogs\DB\RunStore::set_status( $run_id, 'running' );
		}

		// Translate streaming envelope → EventStore::append shape.
		$batch   = [];
		$seq     = 0;
		$has_err = false;
		foreach ( $events as $ev ) {
			if ( ! is_array( $ev ) ) {
				continue;
			}
			$lvl = (string) ( $ev['Level'] ?? 'info' );
			if ( ! in_array( $lvl, \GitLogs\DB\EventStore::SEVERITIES, true ) ) {
				$lvl = 'info';
			}
			$batch[] = [
				'seq'      => ++$seq,
				'ts_utc'   => (string) ( $ev['Ts'] ?? gmdate( 'c' ) ),
				'stream'   => 'stdout',
				'phase'    => (string) ( $body['PipelineName'] ?? 'stream' ),
				'severity' => $lvl,
				'message'  => (string) ( $ev['Line'] ?? '' ),
			];
			if ( 'error' === $lvl || 'fatal' === $lvl ) {
				$has_err = true;
			}
		}
		$result = $batch ? \GitLogs\DB\EventStore::append( $sha, $run_id, $batch )
		                 : [ 'appended' => 0, 'errors' => 0, 'warns' => 0 ];

		if ( $final ) {
			\GitLogs\DB\RunStore::set_status( $run_id, $has_err ? 'failed' : 'succeeded', $has_err ? 1 : 0 );
		}

		return new \WP_REST_Response( [
			'Accepted' => true,
			'RunId'    => $run_id,
			'Inserted' => $result['appended'],
			'Final'    => $final,
		], 200 );
	}

	private static function slug_from_url( string $url ): string {
		$path = parse_url( $url, PHP_URL_PATH ) ?: $url;
		$slug = trim( (string) $path, '/' );
		$slug = preg_replace( '/\.git$/', '', $slug );
		$slug = preg_replace( '/[^A-Za-z0-9._\/-]/', '-', $slug );
		return $slug ?: 'unknown';
	}
}
