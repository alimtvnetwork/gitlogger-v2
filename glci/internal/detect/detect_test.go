package detect

import (
	"errors"
	"os"
	"path/filepath"
	"testing"
)

func touch(t *testing.T, dir, name string) {
	t.Helper()
	if err := os.WriteFile(filepath.Join(dir, name), []byte("{}"), 0o600); err != nil {
		t.Fatal(err)
	}
}

func TestDetect_NoneReturnsError(t *testing.T) {
	dir := t.TempDir()
	_, err := Detect(dir)
	if !errors.Is(err, ErrNoRuntime) {
		t.Fatalf("want ErrNoRuntime, got %v", err)
	}
}

func TestDetect_TSWithBun(t *testing.T) {
	dir := t.TempDir()
	touch(t, dir, "package.json")
	touch(t, dir, "bun.lock")
	touch(t, dir, "tsconfig.json")
	res, err := Detect(dir)
	if err != nil {
		t.Fatal(err)
	}
	if len(res.Runtimes) != 1 || res.Runtimes[0].ID != "ts" {
		t.Fatalf("want one ts runtime, got %+v", res.Runtimes)
	}
	if res.Runtimes[0].Manager != "bun" {
		t.Errorf("manager: %q", res.Runtimes[0].Manager)
	}
	// tsc --noEmit path must be present in build phase.
	build := res.Runtimes[0].Phases[1]
	if build.Phase != "build" {
		t.Fatalf("phase order broken: %+v", build)
	}
	found := false
	for _, a := range build.Args {
		if a == "tsc" {
			found = true
		}
	}
	if !found {
		t.Errorf("tsc missing from build args: %v", build.Args)
	}
}

func TestDetect_AmbiguousJSLockfiles(t *testing.T) {
	dir := t.TempDir()
	touch(t, dir, "package.json")
	touch(t, dir, "bun.lock")
	touch(t, dir, "yarn.lock")
	_, err := Detect(dir)
	if !errors.Is(err, ErrAmbiguousLock) {
		t.Fatalf("want ErrAmbiguousLock, got %v", err)
	}
}

func TestDetect_GoOnly(t *testing.T) {
	dir := t.TempDir()
	touch(t, dir, "go.mod")
	res, err := Detect(dir)
	if err != nil {
		t.Fatal(err)
	}
	if len(res.Runtimes) != 1 || res.Runtimes[0].ID != "go" {
		t.Fatalf("want one go runtime, got %+v", res.Runtimes)
	}
	if res.Runtimes[0].Phases[2].Phase != "test" {
		t.Errorf("test phase missing")
	}
}

func TestDetect_PHPWithPHPCS(t *testing.T) {
	dir := t.TempDir()
	touch(t, dir, "composer.json")
	touch(t, dir, "phpcs.xml")
	res, _ := Detect(dir)
	php := res.Runtimes[0]
	if php.ID != "php" {
		t.Fatal("expected php runtime")
	}
	if php.Phases[0].Runner != "phpcs" {
		t.Errorf("lint runner: %q", php.Phases[0].Runner)
	}
}

func TestDetect_AllThreeRuntimes(t *testing.T) {
	dir := t.TempDir()
	touch(t, dir, "package.json")
	touch(t, dir, "package-lock.json")
	touch(t, dir, "go.mod")
	touch(t, dir, "composer.json")
	res, err := Detect(dir)
	if err != nil {
		t.Fatal(err)
	}
	if len(res.Runtimes) != 3 {
		t.Fatalf("want 3 runtimes, got %d: %+v", len(res.Runtimes), res.Runtimes)
	}
	// Order must be ts, go, php.
	want := []string{"ts", "go", "php"}
	for i, r := range res.Runtimes {
		if r.ID != want[i] {
			t.Errorf("order[%d]: want %s got %s", i, want[i], r.ID)
		}
	}
	if len(res.Skipped) != 0 {
		t.Errorf("nothing should be skipped, got %+v", res.Skipped)
	}
}

func TestResult_JSONStable(t *testing.T) {
	r := &Result{Cwd: "/x", Runtimes: []Runtime{goRuntime()}}
	b, err := r.JSON()
	if err != nil {
		t.Fatal(err)
	}
	if len(b) == 0 {
		t.Fatal("empty json")
	}
}
