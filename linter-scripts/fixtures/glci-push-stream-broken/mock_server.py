#!/usr/bin/env python3
"""Mock server for T-28-31 (stream-broken → batched fallback).

POST /stream: accept 3 NDJSON frames, then forcibly close the socket
              (no chunked terminator, no 200) to simulate mid-stream EOF.
POST /batch:  accept full payload, return 200, log every frame.

Logs all received frames to ./received.log so the test harness can verify
the CLI re-POSTed the un-acked frames in batched mode.
"""
from __future__ import annotations
import json, socket, sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

LOG = Path(__file__).parent / "received.log"


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):  # noqa: N802
        length = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(length) if length else b""
        if self.path == "/stream":
            # Read at most 3 NDJSON frames, log them, then slam the socket shut.
            frames = body.splitlines()[:3]
            with LOG.open("a") as f:
                for fr in frames:
                    f.write(f"stream\t{fr.decode('utf-8', 'replace')}\n")
            try:
                self.connection.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            self.connection.close()
            return
        if self.path == "/batch":
            with LOG.open("a") as f:
                for fr in body.splitlines():
                    f.write(f"batch\t{fr.decode('utf-8', 'replace')}\n")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"ok":true}')
            return
        self.send_response(404)
        self.end_headers()

    def log_message(self, *_args):  # silence default access log
        pass


def main(port: int = 9931) -> int:
    LOG.write_text("")
    HTTPServer(("127.0.0.1", port), Handler).serve_forever()
    return 0


if __name__ == "__main__":
    sys.exit(main(int(sys.argv[1]) if len(sys.argv) > 1 else 9931))
