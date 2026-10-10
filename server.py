"""Serve the imported page without exposing workspace files."""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit


PAGE = Path(__file__).resolve().parent / "code.html"


class PageHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.serve_page()

    def do_HEAD(self):
        self.serve_page(head_only=True)

    def serve_page(self, head_only=False):
        if urlsplit(self.path).path not in ("/", "/code.html"):
            self.send_error(404)
            return
        try:
            content = PAGE.read_bytes()
        except OSError:
            self.send_error(500, "The imported page could not be read")
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if not head_only:
            self.wfile.write(content)


if __name__ == "__main__":
    print("Serving the imported page on port 5000", flush=True)
    ThreadingHTTPServer(("0.0.0.0", 5000), PageHandler).serve_forever()
