package cmd

import (
	"context"
	"time"

	"github.com/example/glci/internal/classify"
	"github.com/example/glci/internal/config"
	"github.com/example/glci/internal/runner"
	"github.com/example/glci/internal/ship"
)

// shipStream walks res.Lines and feeds them to a ship.Streamer in batches,
// then calls Finalize. Used by `glci run --stream`.
//
// This is a post-run replay (not true line-by-line live emission); the runner
// already buffers Lines deterministically. The wire shape exercised here is
// identical to a live emitter — POST /events batches + POST /finalize.
func shipStream(cfg *config.Config, body ship.Body, res *runner.Result) error {
	hdr := ship.StreamHeader{
		RepoUrl:      body.RepoUrl,
		RootRepo:     body.RootRepo,
		Branch:       body.Branch,
		TempToken:    body.TempToken,
		Token:        body.Token,
		PipelineName: body.PipelineName,
		GitSha256:    body.GitSha256,
	}
	st := ship.NewStreamer(ship.Options{
		ServerURL:  cfg.ServerURL,
		MaxRetries: cfg.MaxRetries,
	}, hdr)

	ctx := context.Background()
	for _, ln := range res.Lines {
		level := "info"
		switch classify.Classify(ln.Text, nil, nil) {
		case classify.Error:
			level = "error"
		case classify.Warn:
			level = "warn"
		}
		if err := st.Push(ctx, ship.Event{
			Ts:    ln.TS.UTC().Format(time.RFC3339Nano),
			Level: level,
			Line:  ln.Text,
		}); err != nil {
			return err
		}
	}
	return st.Finalize(ctx, body.HasError, res.ExitCode)
}
