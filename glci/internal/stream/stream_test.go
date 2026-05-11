package stream

import (
	"context"
	"encoding/json"
	"io"
	"net/http"
	"net/http/httptest"
	"sync"
	"sync/atomic"
	"testing"
	"time"
)

func newTestServer(t *testing.T) (*httptest.Server, *atomic.Int32, *sync.Mutex, *[]Batch) {
	t.Helper()
	var count atomic.Int32
	var mu sync.Mutex
	var batches []Batch

	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		count.Add(1)
		body, _ := io.ReadAll(r.Body)
		var b Batch
		_ = json.Unmarshal(body, &b)
		mu.Lock()
		batches = append(batches, b)
		mu.Unlock()
		_, _ = w.Write([]byte(`{"RunId":"run-xyz"}`))
	}))
	t.Cleanup(srv.Close)
	return srv, &count, &mu, &batches
}

func TestStreamer_FlushOnLineThreshold(t *testing.T) {
	srv, count, mu, batches := newTestServer(t)
	s := New(Options{
		ServerURL:     srv.URL,
		RepoUrl:       "https://example.com/r",
		Branch:        "main",
		FlushLines:    3,
		FlushInterval: time.Hour, // ensure threshold is the trigger
	})
	for i := 0; i < 3; i++ {
		s.Append("info", "line")
	}
	// Wait briefly for async flush.
	deadline := time.Now().Add(2 * time.Second)
	for time.Now().Before(deadline) && count.Load() == 0 {
		time.Sleep(10 * time.Millisecond)
	}
	if count.Load() == 0 {
		t.Fatal("expected at least one POST after threshold")
	}
	if err := s.Close(context.Background()); err != nil {
		t.Fatal(err)
	}
	mu.Lock()
	defer mu.Unlock()
	// Last batch should be Final.
	if len(*batches) == 0 || !(*batches)[len(*batches)-1].Final {
		t.Fatalf("expected final batch, got %+v", *batches)
	}
}

func TestStreamer_RunIDPropagated(t *testing.T) {
	srv, _, mu, batches := newTestServer(t)
	s := New(Options{
		ServerURL:     srv.URL,
		FlushLines:    1,
		FlushInterval: time.Hour,
	})
	s.Append("info", "first")
	time.Sleep(150 * time.Millisecond)
	s.Append("info", "second")
	time.Sleep(150 * time.Millisecond)
	_ = s.Close(context.Background())

	mu.Lock()
	defer mu.Unlock()
	if len(*batches) < 2 {
		t.Fatalf("want >=2 batches, got %d", len(*batches))
	}
	// First post: RunId empty. Subsequent: server-assigned "run-xyz".
	if (*batches)[0].RunId != "" {
		t.Errorf("first batch should have empty RunId, got %q", (*batches)[0].RunId)
	}
	found := false
	for _, b := range (*batches)[1:] {
		if b.RunId == "run-xyz" {
			found = true
			break
		}
	}
	if !found {
		t.Errorf("RunId not propagated to subsequent batches")
	}
}

func TestStreamer_NoServerURLNoOp(t *testing.T) {
	s := New(Options{FlushLines: 1, FlushInterval: time.Hour})
	s.Append("info", "lonely")
	if err := s.Close(context.Background()); err != nil {
		t.Fatalf("Close should not error without server: %v", err)
	}
}
