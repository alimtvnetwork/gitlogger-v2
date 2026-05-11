// Package ship implements the §06 log shipping contract (batched mode,
// Lane A / TempToken).
//
// Wire shape: POST <ServerURL>/append-log with the §06 batched-body JSON.
// Bounded by two independent timeouts: PUSH_REQUEST_TIMEOUT_MS (per-attempt)
// and PUSH_TOTAL_DEADLINE_MS (total ship-cycle).
//
// Retry classification per §06 R1–R5 table (first match wins):
//
//	R1 transient (5xx without Retry-After, network) → backoff + jitter, count + budget bound
//	R2 rate-limited (429 / 503 with Retry-After)    → server hint dominates floor
//	R3 permanent client (other 4xx)                 → no retry, exit 3
//	R4 signature invalid (401 GL-SSH-SIG-INVALID)   → ONE conditional retry (Lane B; not exercised here)
//	R5 pre-flight (no SHA / no config / no URL)     → no retry, exit 2
package ship

import (
	"bytes"
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"math/rand"
	"net/http"
	"strconv"
	"strings"
	"time"
)

// Body is the §06 batched payload.
type Body struct {
	RepoUrl      string   `json:"RepoUrl"`
	RootRepo     string   `json:"RootRepo"`
	Branch       string   `json:"Branch"`
	TempToken    string   `json:"TempToken,omitempty"`
	Token        string   `json:"Token,omitempty"`
	PipelineName string   `json:"PipelineName"`
	GitSha256    string   `json:"GitSha256"`
	Logs         []string `json:"Logs"`
	ErrorLogs    []string `json:"ErrorLogs"`
	FilePaths    []string `json:"FilePaths"`
	HasError     bool     `json:"HasError"`
}

// Ack is the v2 server's success envelope (subset; §06 mentions optional
// PreviousHasError used for /fixed-log auto-detection — GAP-22-04).
type Ack struct {
	Accepted         bool   `json:"Accepted"`
	RunId            string `json:"RunId,omitempty"`
	PreviousHasError bool   `json:"PreviousHasError,omitempty"`
	ErrorCode        string `json:"ErrorCode,omitempty"`
}

// Options pin the §06 timeout/retry envelope.
type Options struct {
	ServerURL         string
	RequestTimeoutMS  int      // PUSH_REQUEST_TIMEOUT_MS, default 30000
	TotalDeadlineMS   int      // PUSH_TOTAL_DEADLINE_MS,  default 180000
	BackoffBaseMS     int      // push.backoff_ms,         default 1000
	MaxRetries        int      // push.max_retries,        default 5
	HTTPClient        *http.Client
	Now               func() time.Time
	Sleep             func(time.Duration)
	Rand              func() float64 // returns [0,1); allow deterministic tests
}

// ErrorCode classifies the terminal outcome.
type ErrorCode string

const (
	CodeOK              ErrorCode = ""
	CodeRetriesExhausted ErrorCode = "GLCI-PUSH-RETRIES-EXHAUSTED"  // R1 termination 3
	CodeRateLimited     ErrorCode = "GLCI-PUSH-RATE-LIMIT-EXHAUSTED" // R2 termination
	CodeDeadline        ErrorCode = "GLCI-PUSH-DEADLINE-EXCEEDED"    // R1/R2 termination 4
	CodePermanent       ErrorCode = ""                               // R3: surface server's ErrorCode verbatim
	CodeNoSHA           ErrorCode = "GLCI-PUSH-NO-SHA"               // R5
	CodeNoURL           ErrorCode = "GLCI-PUSH-NO-URL"               // R5
)

// Result is the outcome of a single Ship() call.
type Result struct {
	Ack         *Ack
	ServerCode  string    // verbatim ErrorCode from server (R3)
	OurCode     ErrorCode // CLI-side classification when applicable
	Attempts    int
	StatusCode  int
	ExitCode    int       // §01 exit code matrix
	Err         error
	StartedAt   time.Time
	EndedAt     time.Time
}

// Ship POSTs the body to <ServerURL>/append-log with §06 retry discipline.
//
// Pre-flight (R5):
//   - opts.ServerURL non-empty     → else GLCI-PUSH-NO-URL  (exit 2)
//   - body.GitSha256 non-empty     → else GLCI-PUSH-NO-SHA  (exit 2)
func Ship(ctx context.Context, opts Options, body Body) *Result {
	o := withDefaults(opts)
	res := &Result{StartedAt: o.Now()}
	defer func() { res.EndedAt = o.Now() }()

	// R5 pre-flight.
	if o.ServerURL == "" {
		res.OurCode = CodeNoURL
		res.ExitCode = 2
		res.Err = errors.New(string(CodeNoURL))
		return res
	}
	if strings.TrimSpace(body.GitSha256) == "" {
		res.OurCode = CodeNoSHA
		res.ExitCode = 2
		res.Err = errors.New(string(CodeNoSHA))
		return res
	}

	url := strings.TrimRight(o.ServerURL, "/") + "/append-log"
	payload, err := json.Marshal(body)
	if err != nil {
		res.ExitCode = 4
		res.Err = err
		return res
	}

	deadline := o.Now().Add(time.Duration(o.TotalDeadlineMS) * time.Millisecond)

	for attempt := 0; ; attempt++ {
		res.Attempts = attempt + 1

		// Total-deadline check before each attempt (rule 4).
		if !o.Now().Before(deadline) {
			res.OurCode = CodeDeadline
			res.ExitCode = 4
			res.Err = errors.New(string(CodeDeadline))
			return res
		}

		attemptCtx, cancel := context.WithTimeout(ctx,
			time.Duration(o.RequestTimeoutMS)*time.Millisecond)
		req, _ := http.NewRequestWithContext(attemptCtx, http.MethodPost, url, bytes.NewReader(payload))
		req.Header.Set("Content-Type", "application/json")

		resp, herr := o.HTTPClient.Do(req)
		if herr != nil {
			cancel()
			// Network/timeout → R1 transient.
			if attempt+1 >= o.MaxRetries {
				res.OurCode = CodeRetriesExhausted
				res.ExitCode = 4
				res.Err = fmt.Errorf("%s: %w", CodeRetriesExhausted, herr)
				return res
			}
			waitJittered(o, attempt, 0, deadline)
			if !o.Now().Before(deadline) {
				res.OurCode = CodeDeadline
				res.ExitCode = 4
				res.Err = errors.New(string(CodeDeadline))
				return res
			}
			continue
		}

		bodyBytes, _ := io.ReadAll(resp.Body)
		_ = resp.Body.Close()
		cancel()
		res.StatusCode = resp.StatusCode

		// 2xx → success (rule 1).
		if resp.StatusCode >= 200 && resp.StatusCode < 300 {
			ack := &Ack{}
			_ = json.Unmarshal(bodyBytes, ack)
			res.Ack = ack
			res.ExitCode = 0
			return res
		}

		// R2 — 429 or 503-with-Retry-After.
		if resp.StatusCode == 429 || (resp.StatusCode == 503 && resp.Header.Get("Retry-After") != "") {
			if attempt+1 >= o.MaxRetries {
				res.OurCode = CodeRateLimited
				res.ExitCode = 4
				res.Err = errors.New(string(CodeRateLimited))
				return res
			}
			hint := parseRetryAfter(resp.Header.Get("Retry-After"), o.Now())
			waitJittered(o, attempt, hint, deadline)
			if !o.Now().Before(deadline) {
				res.OurCode = CodeDeadline
				res.ExitCode = 4
				res.Err = errors.New(string(CodeDeadline))
				return res
			}
			continue
		}

		// R1 — generic 5xx.
		if resp.StatusCode >= 500 {
			if attempt+1 >= o.MaxRetries {
				res.OurCode = CodeRetriesExhausted
				res.ExitCode = 4
				res.Err = fmt.Errorf("%s: HTTP %d", CodeRetriesExhausted, resp.StatusCode)
				return res
			}
			waitJittered(o, attempt, 0, deadline)
			continue
		}

		// R3 — any other 4xx → no retry, exit 3, surface server ErrorCode verbatim.
		ack := &Ack{}
		_ = json.Unmarshal(bodyBytes, ack)
		res.Ack = ack
		res.ServerCode = ack.ErrorCode
		if res.ServerCode == "" {
			res.ServerCode = fmt.Sprintf("HTTP-%d", resp.StatusCode)
		}
		res.ExitCode = 3
		res.Err = fmt.Errorf("server rejected (HTTP %d): %s", resp.StatusCode, res.ServerCode)
		return res
	}
}

// Reach implements the §06 doctor reachability ping:
// GET <ServerURL>/get-logs?q=<repo>&limit=0 with current credentials.
// Returns (statusCode, error).
func Reach(ctx context.Context, opts Options, repoUrl, tempToken, token string) (int, error) {
	o := withDefaults(opts)
	if o.ServerURL == "" {
		return 0, errors.New(string(CodeNoURL))
	}
	url := fmt.Sprintf("%s/get-logs?q=%s&limit=0",
		strings.TrimRight(o.ServerURL, "/"), repoUrl)
	cctx, cancel := context.WithTimeout(ctx,
		time.Duration(o.RequestTimeoutMS)*time.Millisecond)
	defer cancel()
	req, _ := http.NewRequestWithContext(cctx, http.MethodGet, url, nil)
	if tempToken != "" {
		req.Header.Set("X-GL-TempToken", tempToken)
	}
	if token != "" {
		req.Header.Set("X-GL-Token", token)
	}
	resp, err := o.HTTPClient.Do(req)
	if err != nil {
		return 0, err
	}
	defer resp.Body.Close()
	return resp.StatusCode, nil
}

// --- helpers ---

func withDefaults(o Options) Options {
	if o.RequestTimeoutMS <= 0 {
		o.RequestTimeoutMS = 30000
	}
	if o.TotalDeadlineMS <= 0 {
		o.TotalDeadlineMS = 180000
	}
	if o.BackoffBaseMS <= 0 {
		o.BackoffBaseMS = 1000
	}
	if o.MaxRetries <= 0 {
		o.MaxRetries = 5
	}
	if o.HTTPClient == nil {
		o.HTTPClient = &http.Client{
			Timeout: time.Duration(o.RequestTimeoutMS+5000) * time.Millisecond,
		}
	}
	if o.Now == nil {
		o.Now = time.Now
	}
	if o.Sleep == nil {
		o.Sleep = time.Sleep
	}
	if o.Rand == nil {
		r := rand.New(rand.NewSource(time.Now().UnixNano()))
		o.Rand = r.Float64
	}
	return o
}

// waitJittered computes delay = max(floorMs, backoff_ms * 2^attempt) * (0.75 + rand*0.5),
// clamped so we never sleep past the total deadline.
func waitJittered(o Options, attempt int, floorMS int64, deadline time.Time) {
	base := int64(o.BackoffBaseMS) << attempt
	if floorMS > base {
		base = floorMS
	}
	jitter := 0.75 + o.Rand()*0.5
	delay := time.Duration(float64(base)*jitter) * time.Millisecond
	if remaining := time.Until(deadline); delay > remaining && remaining > 0 {
		delay = remaining
	}
	if delay < 0 {
		return
	}
	o.Sleep(delay)
}

// parseRetryAfter accepts integer seconds or HTTP-date; returns ms hint.
func parseRetryAfter(h string, now time.Time) int64 {
	h = strings.TrimSpace(h)
	if h == "" {
		return 0
	}
	if n, err := strconv.Atoi(h); err == nil {
		return int64(n) * 1000
	}
	if t, err := http.ParseTime(h); err == nil {
		d := t.Sub(now)
		if d < 0 {
			return 0
		}
		return d.Milliseconds()
	}
	return 0
}
