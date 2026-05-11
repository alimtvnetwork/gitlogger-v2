// Streaming mode: emit per-line events to POST <ServerURL>/events with
// periodic flush, then POST /finalize when the runner exits.
//
// Wire shape (§06 streaming, GAP-22-04):
//   POST /events   { RunId?, RepoUrl, Branch, PipelineName, GitSha256, Events:[{ts,level,line,file?}] }
//   POST /finalize { RunId, HasError, ExitCode }
//
// The same R1–R5 retry classification from Ship() applies per request; we
// reuse waitJittered/parseRetryAfter through a thin wrapper.

package ship

import (
	"bytes"
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net/http"
	"strings"
	"sync"
	"time"
)

// Event is one classified runner line (§09 classification mapping).
type Event struct {
	Ts    string `json:"ts"`
	Level string `json:"level"` // info|warn|error
	Line  string `json:"line"`
	File  string `json:"file,omitempty"`
}

// StreamHeader is the per-batch envelope sent to /events.
type StreamHeader struct {
	RunId        string  `json:"RunId,omitempty"`
	RepoUrl      string  `json:"RepoUrl"`
	RootRepo     string  `json:"RootRepo,omitempty"`
	Branch       string  `json:"Branch"`
	TempToken    string  `json:"TempToken,omitempty"`
	Token        string  `json:"Token,omitempty"`
	PipelineName string  `json:"PipelineName"`
	GitSha256    string  `json:"GitSha256"`
	Events       []Event `json:"Events"`
}

// FinalizeBody closes the run.
type FinalizeBody struct {
	RunId     string `json:"RunId"`
	TempToken string `json:"TempToken,omitempty"`
	Token     string `json:"Token,omitempty"`
	HasError  bool   `json:"HasError"`
	ExitCode  int    `json:"ExitCode"`
}

// Streamer batches Events and flushes them on size or interval.
type Streamer struct {
	Opts       Options
	Header     StreamHeader  // RunId is filled after the first ack
	FlushEvery time.Duration // default 1s
	BatchMax   int           // default 200

	mu     sync.Mutex
	buf    []Event
	runId  string
	closed bool
}

// NewStreamer constructs a streamer with sane defaults.
func NewStreamer(opts Options, h StreamHeader) *Streamer {
	o := withDefaults(opts)
	return &Streamer{Opts: o, Header: h, FlushEvery: time.Second, BatchMax: 200}
}

// Push enqueues an event; if the buffer reaches BatchMax it auto-flushes.
func (s *Streamer) Push(ctx context.Context, e Event) error {
	s.mu.Lock()
	s.buf = append(s.buf, e)
	full := len(s.buf) >= s.BatchMax
	s.mu.Unlock()
	if full {
		return s.Flush(ctx)
	}
	return nil
}

// Flush sends the current buffer to /events. Empty buffers are no-ops.
func (s *Streamer) Flush(ctx context.Context) error {
	s.mu.Lock()
	if len(s.buf) == 0 {
		s.mu.Unlock()
		return nil
	}
	batch := s.buf
	s.buf = nil
	hdr := s.Header
	hdr.RunId = s.runId
	hdr.Events = batch
	s.mu.Unlock()

	url := strings.TrimRight(s.Opts.ServerURL, "/") + "/events"
	ack, err := s.postJSON(ctx, url, hdr)
	if err != nil {
		return err
	}
	if ack != nil && ack.RunId != "" && s.runId == "" {
		s.mu.Lock()
		s.runId = ack.RunId
		s.mu.Unlock()
	}
	return nil
}

// Finalize closes the run server-side. Idempotent.
func (s *Streamer) Finalize(ctx context.Context, hasError bool, exitCode int) error {
	if err := s.Flush(ctx); err != nil {
		return err
	}
	s.mu.Lock()
	rid := s.runId
	s.closed = true
	s.mu.Unlock()
	if rid == "" {
		return errors.New("GLCI-PUSH-NO-RUN-ID")
	}
	url := strings.TrimRight(s.Opts.ServerURL, "/") + "/finalize"
	_, err := s.postJSON(ctx, url, FinalizeBody{
		RunId:     rid,
		TempToken: s.Header.TempToken,
		Token:     s.Header.Token,
		HasError:  hasError,
		ExitCode:  exitCode,
	})
	return err
}

// postJSON applies the §06 retry envelope to a single endpoint.
func (s *Streamer) postJSON(ctx context.Context, url string, body any) (*Ack, error) {
	payload, err := json.Marshal(body)
	if err != nil {
		return nil, err
	}
	deadline := s.Opts.Now().Add(time.Duration(s.Opts.TotalDeadlineMS) * time.Millisecond)
	for attempt := 0; ; attempt++ {
		if !s.Opts.Now().Before(deadline) {
			return nil, errors.New(string(CodeDeadline))
		}
		actx, cancel := context.WithTimeout(ctx,
			time.Duration(s.Opts.RequestTimeoutMS)*time.Millisecond)
		req, _ := http.NewRequestWithContext(actx, http.MethodPost, url, bytes.NewReader(payload))
		req.Header.Set("Content-Type", "application/json")
		if s.Header.TempToken != "" {
			req.Header.Set("X-GL-TempToken", s.Header.TempToken)
		}
		if s.Header.Token != "" {
			req.Header.Set("X-GL-Token", s.Header.Token)
		}
		resp, herr := s.Opts.HTTPClient.Do(req)
		if herr != nil {
			cancel()
			if attempt+1 >= s.Opts.MaxRetries {
				return nil, fmt.Errorf("%s: %w", CodeRetriesExhausted, herr)
			}
			waitJittered(s.Opts, attempt, 0, deadline)
			continue
		}
		bb, _ := io.ReadAll(resp.Body)
		_ = resp.Body.Close()
		cancel()
		if resp.StatusCode >= 200 && resp.StatusCode < 300 {
			ack := &Ack{}
			_ = json.Unmarshal(bb, ack)
			return ack, nil
		}
		if resp.StatusCode == 429 || (resp.StatusCode == 503 && resp.Header.Get("Retry-After") != "") {
			if attempt+1 >= s.Opts.MaxRetries {
				return nil, errors.New(string(CodeRateLimited))
			}
			hint := parseRetryAfter(resp.Header.Get("Retry-After"), s.Opts.Now())
			waitJittered(s.Opts, attempt, hint, deadline)
			continue
		}
		if resp.StatusCode >= 500 {
			if attempt+1 >= s.Opts.MaxRetries {
				return nil, fmt.Errorf("%s: HTTP %d", CodeRetriesExhausted, resp.StatusCode)
			}
			waitJittered(s.Opts, attempt, 0, deadline)
			continue
		}
		ack := &Ack{}
		_ = json.Unmarshal(bb, ack)
		code := ack.ErrorCode
		if code == "" {
			code = fmt.Sprintf("HTTP-%d", resp.StatusCode)
		}
		return ack, fmt.Errorf("server rejected (HTTP %d): %s", resp.StatusCode, code)
	}
}
