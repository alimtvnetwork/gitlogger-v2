<?php
/**
 * DB-layer test runner. Mirrors tests/run.php but loads bootstrap-db.php
 * and discovers tests under tests/db/test-*.php so they exercise the
 * REAL PDO/SQLite-backed stores.
 */

declare( strict_types = 1 );

require_once __DIR__ . '/bootstrap-db.php';

$assertions = 0;
$failures   = [];

function _fail( string $msg ): void { throw new \RuntimeException( $msg ); }
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
function assertNotNull( $v, string $msg = 'expected non-null' ): void {
	global $assertions; $assertions++;
	if ( null === $v ) { _fail( $msg ); }
}
function assertThrows( callable $fn, ?string $expect_substr = null ): void {
	global $assertions; $assertions++;
	try {
		$fn();
	} catch ( \Throwable $e ) {
		if ( null === $expect_substr || str_contains( $e->getMessage(), $expect_substr ) ) {
			return;
		}
		_fail( "expected exception containing '$expect_substr', got: " . $e->getMessage() );
	}
	_fail( 'expected exception, none thrown' );
}

$files = glob( __DIR__ . '/db/test-*.php' ) ?: [];
sort( $files );
foreach ( $files as $f ) { require_once $f; }

$tests = array_values( array_filter(
	get_defined_functions()['user'],
	static fn( string $fn ): bool => str_starts_with( $fn, 'dbtest_' )
) );
sort( $tests );

$pass = 0;
foreach ( $tests as $fn ) {
	migrate_fresh();
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
echo "\nDB tests: $total | Passed: $pass | Failed: " . count( $failures ) . " | Assertions: $assertions\n";

exit( empty( $failures ) ? 0 : 1 );
