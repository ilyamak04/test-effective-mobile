import logging
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = int(os.environ.get("PORT", 8080))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("backend")


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self._respond(200, "ok")
            return
        self._respond(200, "Hello from Effective Mobile!")

    def _respond(self, code: int, body: str):
        payload = body.encode()
        self.send_response(code)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)
=
if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), Handler)
    logger.info("Listening on port %d", PORT)
    server.serve_forever()
