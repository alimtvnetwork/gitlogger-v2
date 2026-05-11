<?php
/**
 * NonceStore tests.
 */

declare( strict_types = 1 );

use GitLogs\Auth\NonceStore;

function test_nonce_first_use_not_seen(): void {
	assertFalse( NonceStore::seen_or_remember( 'k1', 'n1' ), 'first use should not be seen' );
}

function test_nonce_replay_detected(): void {
	assertFalse( NonceStore::seen_or_remember( 'k1', 'n2' ) );
	assertTrue(  NonceStore::seen_or_remember( 'k1', 'n2' ), 'replay must be detected' );
}

function test_nonce_scoped_per_key_id(): void {
	NonceStore::seen_or_remember( 'k1', 'shared' );
	// Different key_id with same nonce string → not a replay.
	assertFalse( NonceStore::seen_or_remember( 'k2', 'shared' ), 'nonce store must scope by key_id' );
}
