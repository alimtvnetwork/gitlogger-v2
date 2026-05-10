#!/usr/bin/env python3
"""Mock server for T-28-48 (push deadline exceeded).

Sleeps 60 000 ms before responding to any request. The CLI's
push.request_timeout_ms (5000 ms) MUST abort each attempt, and
push.total_deadline_ms (15000 ms) MUST terminate the overall push with
GLCI-PUSH-DEADLINE-EXCEEDED.
"""
from __future__ import annotations
import sys, time
from http.server import BaseHTTPRequestHandler, HTTPServer


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):  # noqa: N802
        # Drain body so the client's send completes.
        length = int(self.headers.get("Content-Length") or 0)
        if length:
            _ = self.rfile.read(length)
        time.sleep(60)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'{"ok":true}')

    def log_message(self, *_args):
        pass


def main(port: int = 9932) -> int:
    HTTPServer(("127.0.0.1", port), Handler).serve_forever()
    return 0


if __name__ == "__main__":
    sys.exit(main(int(sys.argv[1]) if len(sys.argv) > 1 else 9932))
