<?php
/**
 * REST: GET /admin/diagrams
 *
 * Lists shipped Mermaid + SVG diagrams under spec/26-gitlogs-diagrams/.
 * Returns:
 *   { items: [ { slug, title, href, source? } ] }
 *
 * - `href`   → public URL of the .svg (served as a static asset).
 * - `source` → public URL of the .mmd (when present), so the UI can link to it.
 *
 * Only readable to users with `manage_options` (admin-only consumption).
 *
 * @package GitLogs
 */

declare(strict_types=1);

namespace GitLogs\Rest;

class Admin_Diagrams {

	/** Plugin namespace, matches git-logs.php. */
	private const NS = 'git-logs/v1';

	/** Diagrams folder, relative to the plugin's parent (repo root). */
	private const DIAGRAM_DIR = 'spec/26-gitlogs-diagrams';

	/** Static entry — matches the convention used by other Rest\* classes. */
	public static function register(): void {
		( new self() )->routes();
	}



	public function routes(): void {
		register_rest_route( self::NS, '/admin/diagrams', [
			'methods'             => 'GET',
			'callback'            => [ $this, 'list' ],
			'permission_callback' => static fn () => current_user_can( 'manage_options' ),
		] );
	}

	public function list( \WP_REST_Request $req ): \WP_REST_Response {
		$root = $this->repo_root();
		$dir  = $root . DIRECTORY_SEPARATOR . self::DIAGRAM_DIR;

		if ( ! is_dir( $dir ) ) {
			return new \WP_REST_Response( [ 'items' => [] ], 200 );
		}

		$items = [];
		foreach ( glob( $dir . DIRECTORY_SEPARATOR . '*.svg' ) ?: [] as $svg ) {
			$slug   = basename( $svg, '.svg' );
			$mmd    = $dir . DIRECTORY_SEPARATOR . $slug . '.mmd';
			$items[] = [
				'slug'   => $slug,
				'title'  => $this->humanize( $slug ),
				'href'   => $this->public_url( self::DIAGRAM_DIR . '/' . basename( $svg ) ),
				'source' => is_file( $mmd ) ? $this->public_url( self::DIAGRAM_DIR . '/' . $slug . '.mmd' ) : null,
			];
		}
		usort( $items, static fn ( $a, $b ) => strcmp( $a['slug'], $b['slug'] ) );
		return new \WP_REST_Response( [ 'items' => $items ], 200 );
	}

	/** Best-effort repo root: parent of the plugin folder. */
	private function repo_root(): string {
		// git-logs-plugin/includes/rest/ → ../../../
		return dirname( __DIR__, 3 );
	}

	private function public_url( string $rel ): string {
		// Diagrams are static files; we expose them through the WP uploads
		// proxy when present, else a relative path the admin browser can hit
		// only if the WP host serves the repo root (dev setup). Production
		// installs SHOULD copy diagrams into wp-content/uploads/git-logs/.
		$uploads = wp_upload_dir();
		$copy    = trailingslashit( $uploads['basedir'] ) . 'git-logs/diagrams/' . basename( $rel );
		if ( is_file( $copy ) ) {
			return trailingslashit( $uploads['baseurl'] ) . 'git-logs/diagrams/' . basename( $rel );
		}
		return '/' . ltrim( $rel, '/' );
	}

	private function humanize( string $slug ): string {
		$slug = preg_replace( '/^\d+[-_]/', '', $slug ) ?? $slug;
		$slug = str_replace( [ '-', '_' ], ' ', $slug );
		return ucwords( $slug );
	}
}
