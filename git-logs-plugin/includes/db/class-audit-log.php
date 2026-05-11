<?php
/**
 * AuditLog — append-only audit trail.
 *
 * @package GitLogs\DB
 */

declare( strict_types = 1 );

namespace GitLogs\DB;

defined( 'ABSPATH' ) || exit;

if ( class_exists( __NAMESPACE__ . '\\AuditLog', false ) ) {
	return; // allow tests to pre-load an in-memory stub
}

require_once __DIR__ . '/class-database.php';

final class AuditLog {

	public const RESULT_OK     = 'ok';
	public const RESULT_DENIED = 'denied';
	public const RESULT_ERROR  = 'error';

	/**
	 * @param array{
	 *   action:string, result:string,
	 *   actor_user_id?:?int, actor_login?:?string,
	 *   auth_lane?:string,
	 *   target_type?:?string, target_id?:?string,
	 *   request_ip?:?string, request_id?:?string,
	 *   detail?:?array<mixed>
	 * } $args
	 */
	public static function record( array $args ): int {
		$pdo  = Database::root();
		$stmt = $pdo->prepare(
			'INSERT INTO audit
				(ts_utc, actor_user_id, actor_login, auth_lane, action, target_type, target_id, request_ip, request_id, result, detail_json)
			 VALUES
				(:ts, :uid, :login, :lane, :action, :ttype, :tid, :ip, :rid, :result, :detail)'
		);
		$stmt->execute( [
			':ts'     => gmdate( 'c' ),
			':uid'    => $args['actor_user_id'] ?? null,
			':login'  => $args['actor_login']   ?? null,
			':lane'   => $args['auth_lane']     ?? 'system',
			':action' => $args['action'],
			':ttype'  => $args['target_type']   ?? null,
			':tid'    => $args['target_id']     ?? null,
			':ip'     => $args['request_ip']    ?? null,
			':rid'    => $args['request_id']    ?? null,
			':result' => $args['result'],
			':detail' => isset( $args['detail'] ) ? wp_json_encode( $args['detail'] ) : null,
		] );
		return (int) $pdo->lastInsertId();
	}

	/**
	 * @return list<array<string,mixed>>
	 */
	public static function recent( int $limit = 100, ?string $action = null ): array {
		$pdo = Database::root();
		$sql = 'SELECT * FROM audit';
		$params = [];
		if ( null !== $action ) {
			$sql .= ' WHERE action = :a';
			$params[':a'] = $action;
		}
		$sql .= ' ORDER BY id DESC LIMIT :lim';

		$stmt = $pdo->prepare( $sql );
		foreach ( $params as $k => $v ) {
			$stmt->bindValue( $k, $v );
		}
		$stmt->bindValue( ':lim', $limit, \PDO::PARAM_INT );
		$stmt->execute();
		return $stmt->fetchAll();
	}
}
