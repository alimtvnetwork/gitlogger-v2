package ship

import (
	"context"
	"net/http"
	"net/http/httptest"
	"sync/atomic"
	"testing"
	"time"
)

func fixedNow() time.Time { return time.Unix(1_700_000_000, 0).UTC() }

func baseOpts(url string) Options {
	return Options{
		ServerURL:        url,
		RequestTimeoutMS: 1000,
		TotalDeadlineMS:  5000,
		BackoffBaseMS:    1, // fast retries for tests
		MaxRetries:       3,
		Now:              time.Now, // real clock so deadline math works
		Sleep:            func(d time.Duration) {},
		Rand:             func() float64 { return 0.5 },
	}
}

func goodBody() Body {
	return Body{
		RepoUrl:   "https://example.com/r",
		Branch:    "main",
		GitSha256: "deadbeef",
	}
}

func TestShip_PreflightNoURL(t *testing.T) {
	r := Ship(context.Background(), Options{Now: fixedNow}, goodBody())
	if r.OurCode != CodeNoURL || r.ExitCode != 2 {
		t.Fatalf("want CodeNoURL/exit2, got %+v", r)
	}
}

func TestShip_PreflightNoSHA(t *testing.T) {
	b := goodBody()
	b.GitSha256 = ""
	r := Ship(context.Background(), Options{ServerURL: "https://x", Now: fixedNow}, b)
	if r.OurCode != CodeNoSHA || r.ExitCode != 2 {
		t.Fatalf("want CodeNoSHA/exit2, got %+v", r)
	}
}

func TestShip_Success200(t *testing.T) {
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/append-log" {
			t.Errorf("unexpected path %s", r.URL.Path)
		}
		w.Header().Set("Content-Type", "application/json")
		_, _ = w.Write([]byte(`{"Accepted":true,"RunId":"r-1"}`))
	}))
	defer srv.Close()

	r := Ship(context.Background(), baseOpts(srv.URL), goodBody())
	if r.ExitCode != 0 {
		t.Fatalf("want exit 0, got %+v", r)
	}
	if r.Ack == nil || r.Ack.RunId != "r-1" {
		t.Errorf("ack: %+v", r.Ack)
	}
	if r.Attempts != 1 {
		t.Errorf("want 1 attempt, got %d", r.Attempts)
	}
}

func TestShip_RetryThenSuccess(t *testing.T) {
	var n atomic.Int32
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if n.Add(1) < 3 {
			w.WriteHeader(500)
			return
		}
		_, _ = w.Write([]byte(`{"Accepted":true}`))
	}))
	defer srv.Close()

	r := Ship(context.Background(), baseOpts(srv.URL), goodBody())
	if r.ExitCode != 0 {
		t.Fatalf("want eventual success, got %+v", r)
	}
	if r.Attempts != 3 {
		t.Errorf("want 3 attempts, got %d", r.Attempts)
	}
}

func TestShip_5xxRetriesExhausted(t *testing.T) {
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(503) // no Retry-After → R1 path
	}))
	defer srv.Close()

	o := baseOpts(srv.URL)
	o.MaxRetries = 2
	r := Ship(context.Background(), o, goodBody())
	if r.OurCode != CodeRetriesExhausted || r.ExitCode != 4 {
		t.Fatalf("want retries-exhausted/exit4, got %+v", r)
	}
	if r.Attempts != 2 {
		t.Errorf("want 2 attempts, got %d", r.Attempts)
	}
}

func TestShip_429RateLimited(t *testing.T) {
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Retry-After", "1")
		w.WriteHeader(429)
	}))
	defer srv.Close()

	o := baseOpts(srv.URL)
	o.MaxRetries = 2
	r := Ship(context.Background(), o, goodBody())
	if r.OurCode != CodeRateLimited || r.ExitCode != 4 {
		t.Fatalf("want rate-limited/exit4, got %+v", r)
	}
}

func TestShip_4xxPermanentSurfaces(t *testing.T) {
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(400)
		_, _ = w.Write([]byte(`{"ErrorCode":"GL-VALIDATION-FAIL"}`))
	}))
	defer srv.Close()

	r := Ship(context.Background(), baseOpts(srv.URL), goodBody())
	if r.ExitCode != 3 {
		t.Fatalf("want exit 3, got %+v", r)
	}
	if r.ServerCode != "GL-VALIDATION-FAIL" {
		t.Errorf("server code: %q", r.ServerCode)
	}
	if r.Attempts != 1 {
		t.Errorf("4xx must not retry, attempts=%d", r.Attempts)
	}
}

func TestShip_4xxFallbackHTTPCode(t *testing.T) {
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(403)
	}))
	defer srv.Close()

	r := Ship(context.Background(), baseOpts(srv.URL), goodBody())
	if r.ServerCode != "HTTP-403" {
		t.Errorf("fallback code: %q", r.ServerCode)
	}
}

func TestReach_Success(t *testing.T) {
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/get-logs" {
			t.Errorf("path: %s", r.URL.Path)
		}
		if r.Header.Get("X-GL-TempToken") != "tt" {
			t.Errorf("temp token header missing")
		}
		w.WriteHeader(204)
	}))
	defer srv.Close()

	code, err := Reach(context.Background(), baseOpts(srv.URL), "https://r", "tt", "")
	if err != nil {
		t.Fatal(err)
	}
	if code != 204 {
		t.Errorf("status: %d", code)
	}
}

func TestReach_NoURL(t *testing.T) {
	if _, err := Reach(context.Background(), Options{}, "r", "", ""); err == nil {
		t.Fatal("expected error for empty server url")
	}
}

func TestParseRetryAfter(t *testing.T) {
	now := fixedNow()
	if parseRetryAfter("5", now) != 5000 {
		t.Errorf("seconds form")
	}
	if parseRetryAfter("", now) != 0 {
		t.Errorf("empty form")
	}
	if parseRetryAfter("garbage", now) != 0 {
		t.Errorf("garbage form")
	}
	// HTTP-date in the past → 0.
	if parseRetryAfter("Wed, 21 Oct 2015 07:28:00 GMT", now) != 0 {
		t.Errorf("past date should be 0")
	}
}
