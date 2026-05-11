<?php
/**
 * Tiny PHPUnit-free runner.
 *
 * Discovers files matching tests/test-*.php, includes them, then invokes
 * every global function whose name starts with "test_". Each test may
 * throw or call assert*() helpers; non-zero exit means at least one failed.
 *
 * Usage:  php tests/run.php
 */

declare( strict_types = 1 );

require_once __DIR__ . '/bootstrap.php';

$assertions = 0;
$failures   = [];

function _fail( string $msg ): void {
	throw new \RuntimeException( $msg );
}
function assertTrue( bool $v, string $msg = 'assertTrue failed' ): void {
	global $assertions; $assertions++;
	if ( ! $v ) { _fail( $msg ); }
}
function assertFalse( bool $v, string $msg = 'assertFalse failed' ): void {
	global $assertions; $assertions++;
	if ( $v ) { _fail( $msg ); }
}
function assertSame( $expected, $actual, string $msg = '' ): void {
	global $assertions; $assertions++;
	if ( $expected !== $actual ) {
		_fail( $msg ?: sprintf( 'assertSame: expected %s got %s', var_export( $expected, true ), var_export( $actual, true ) ) );
	}
}
function assertEquals( $expected, $actual, string $msg = '' ): void {
	global $assertions; $assertions++;
	if ( $expected != $actual ) {
		_fail( $msg ?: sprintf( 'assertEquals: %s != %s', var_export( $expected, true ), var_export( $actual, true ) ) );
	}
}
function assertWPError( $thing, ?string $code = null, string $msg = '' ): void {
	global $assertions; $assertions++;
	if ( ! ( $thing instanceof \WP_Error ) ) {
		_fail( $msg ?: 'expected WP_Error, got ' . var_export( $thing, true ) );
	}
	if ( null !== $code && $thing->get_error_code() !== $code ) {
		_fail( sprintf( 'expected WP_Error code %s, got %s', $code, $thing->get_error_code() ) );
	}
}

// Discover test files.
$files = glob( __DIR__ . '/test-*.php' ) ?: [];
sort( $files );
foreach ( $files as $f ) {
	require_once $f;
}

// Find every global test_* function.
$tests = array_values( array_filter(
	get_defined_functions()['user'],
	static fn( string $fn ): bool => str_starts_with( $fn, 'test_' )
) );
sort( $tests );

$pass = 0;
foreach ( $tests as $fn ) {
	// reset between tests
	$GLOBALS['__transients']            = [];
	$GLOBALS['__current_user_id']       = 0;
	$GLOBALS['__current_user_login']    = null;
	$GLOBALS['__current_user_display']  = null;
	$GLOBALS['__current_user_roles']    = [];
	$GLOBALS['__user_caps']             = [];
	if ( class_exists( '\\GitLogs\\Auth\\PublicKeys' ) ) {
		\GitLogs\Auth\PublicKeys::reset();
	}
	foreach ( [ 'RepoStore', 'RunStore', 'EventStore', 'BranchStore', 'AuditLog' ] as $cls ) {
		$fq = "\\GitLogs\\DB\\$cls";
		if ( class_exists( $fq ) ) { $fq::reset(); }
	}
	try {
		$fn();
		echo "  ok   $fn\n";
		$pass++;
	} catch ( \Throwable $e ) {
		echo "  FAIL $fn — " . $e->getMessage() . "\n";
		$failures[] = $fn;
	}
}

$total = count( $tests );
echo "\n";
echo "Tests: $total | Passed: $pass | Failed: " . count( $failures ) . " | Assertions: $assertions\n";

exit( empty( $failures ) ? 0 : 1 );
