package ship

import (
	"context"
	"crypto/ed25519"
	"crypto/rand"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
)

func TestShip_PreflightNoURL(t *testing.T) {
	r := Ship(context.Background(), Options{}, Body{GitSha256: "x"})
	if r.OurCode != CodeNoURL || r.ExitCode != 2 {
		t.Fatalf("want NO-URL/exit=2, got %s/%d", r.OurCode, r.ExitCode)
	}
}

func TestShip_PreflightNoSHA(t *testing.T) {
	r := Ship(context.Background(), Options{ServerURL: "http://x"}, Body{})
	if r.OurCode != CodeNoSHA || r.ExitCode != 2 {
		t.Fatalf("want NO-SHA/exit=2, got %s/%d", r.OurCode, r.ExitCode)
	}
}

func TestShip_Success(t *testing.T) {
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, _ *http.Request) {
		_ = json.NewEncoder(w).Encode(Ack{Accepted: true, RunId: "r1"})
	}))
	defer srv.Close()
	r := Ship(context.Background(), Options{ServerURL: srv.URL, MaxRetries: 1},
		Body{GitSha256: "abc", RepoUrl: "u", Branch: "main"})
	if r.ExitCode != 0 || r.Ack == nil || r.Ack.RunId != "r1" {
		t.Fatalf("unexpected result: %+v", r)
	}
}

func TestShip_PermanentRejection(t *testing.T) {
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, _ *http.Request) {
		w.WriteHeader(400)
		_ = json.NewEncoder(w).Encode(Ack{ErrorCode: "GL-VALIDATION"})
	}))
	defer srv.Close()
	r := Ship(context.Background(), Options{ServerURL: srv.URL}, Body{GitSha256: "abc"})
	if r.ExitCode != 3 || r.ServerCode != "GL-VALIDATION" {
		t.Fatalf("want exit=3 GL-VALIDATION, got %d %s", r.ExitCode, r.ServerCode)
	}
}

func TestSignVerify_Roundtrip(t *testing.T) {
	pub, priv, err := ed25519.GenerateKey(rand.Reader)
	if err != nil {
		t.Fatal(err)
	}
	body := []byte(`{"x":1}`)
	h, err := Sign(priv, "kid", "POST", "/append-log", "n0", body)
	if err != nil {
		t.Fatal(err)
	}
	if err := Verify(pub, h, "POST", "/append-log", body); err != nil {
		t.Fatalf("verify: %v", err)
	}
	// tamper
	if err := Verify(pub, h, "POST", "/append-log", []byte(`{"x":2}`)); err == nil ||
		!strings.Contains(err.Error(), "GL-SSH-SIG-INVALID") {
		t.Fatalf("expected SIG-INVALID, got %v", err)
	}
}
