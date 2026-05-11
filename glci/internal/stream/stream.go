// Package stream implements the §06 streaming mode: incremental
// POST <ServerURL>/events batches while a phase is still running.
//
// Streaming is opt-in via `glci run --stream`. Lines are buffered into
// chunks of up to FlushLines or FlushInterval, whichever fires first.
// On terminal flush, a final POST sets Final=true so the server can
// finalize the run row.
package stream

import (
	"bytes"
	"context"
	"encoding/json"
	"net/http"
	"strings"
	"sync"
	"time"
)

type Event struct {
	Ts    string `json:"Ts"`
	Level string `json:"Level"` // info|warn|error
	Line  string `json:"Line"`
}

type Batch struct {
	RunId     string  `json:"RunId,omitempty"`
	RepoUrl   string  `json:"RepoUrl"`
	Branch    string  `json:"Branch"`
	GitSha256 string  `json:"GitSha256"`
	TempToken string  `json:"TempToken,omitempty"`
	Token     string  `json:"Token,omitempty"`
	Events    []Event `json:"Events"`
	Final     bool    `json:"Final"`
}

type Options struct {
	ServerURL     string
	RepoUrl       string
	Branch        string
	GitSha256     string
	TempToken     string
	Token         string
	FlushLines    int           // default 100
	FlushInterval time.Duration // default 2s
	HTTPClient    *http.Client
}

type Streamer struct {
	opts   Options
	mu     sync.Mutex
	buf    []Event
	runID  string
	closed bool
	flushC chan struct{}
	doneC  chan struct{}
}

func New(opts Options) *Streamer {
	if opts.FlushLines <= 0 {
		opts.FlushLines = 100
	}
	if opts.FlushInterval <= 0 {
		opts.FlushInterval = 2 * time.Second
	}
	if opts.HTTPClient == nil {
		opts.HTTPClient = &http.Client{Timeout: 30 * time.Second}
	}
	s := &Streamer{
		opts:   opts,
		flushC: make(chan struct{}, 1),
		doneC:  make(chan struct{}),
	}
	go s.loop()
	return s
}

// Append enqueues a single event (non-blocking).
func (s *Streamer) Append(level, line string) {
	s.mu.Lock()
	s.buf = append(s.buf, Event{
		Ts:    time.Now().UTC().Format(time.RFC3339Nano),
		Level: level,
		Line:  line,
	})
	full := len(s.buf) >= s.opts.FlushLines
	s.mu.Unlock()
	if full {
		select {
		case s.flushC <- struct{}{}:
		default:
		}
	}
}

// Close flushes remaining events with Final=true and stops the loop.
func (s *Streamer) Close(ctx context.Context) error {
	s.mu.Lock()
	s.closed = true
	s.mu.Unlock()
	select {
	case s.flushC <- struct{}{}:
	default:
	}
	<-s.doneC
	return s.flush(ctx, true)
}

func (s *Streamer) loop() {
	t := time.NewTicker(s.opts.FlushInterval)
	defer t.Stop()
	for {
		select {
		case <-t.C:
			_ = s.flush(context.Background(), false)
		case <-s.flushC:
			s.mu.Lock()
			done := s.closed
			s.mu.Unlock()
			if done {
				close(s.doneC)
				return
			}
			_ = s.flush(context.Background(), false)
		}
	}
}

func (s *Streamer) flush(ctx context.Context, final bool) error {
	s.mu.Lock()
	if len(s.buf) == 0 && !final {
		s.mu.Unlock()
		return nil
	}
	evs := s.buf
	s.buf = nil
	runID := s.runID
	s.mu.Unlock()

	if s.opts.ServerURL == "" {
		return nil
	}
	body := Batch{
		RunId: runID, RepoUrl: s.opts.RepoUrl, Branch: s.opts.Branch,
		GitSha256: s.opts.GitSha256, TempToken: s.opts.TempToken,
		Token: s.opts.Token, Events: evs, Final: final,
	}
	payload, _ := json.Marshal(body)
	url := strings.TrimRight(s.opts.ServerURL, "/") + "/events"
	req, _ := http.NewRequestWithContext(ctx, http.MethodPost, url, bytes.NewReader(payload))
	req.Header.Set("Content-Type", "application/json")
	resp, err := s.opts.HTTPClient.Do(req)
	if err != nil {
		return err
	}
	var ack struct {
		RunId string `json:"RunId"`
	}
	_ = json.NewDecoder(resp.Body).Decode(&ack)
	_ = resp.Body.Close()
	if ack.RunId != "" {
		s.mu.Lock()
		s.runID = ack.RunId
		s.mu.Unlock()
	}
	return nil
}
