"""Serve the She's Glowing static landing page."""

import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parent
PORT = 5000

_CART_LINK = re.compile(
    r'<a\b(?=[^>]*\bdata-path=["\']cart["\'])[^>]*>.*?</a>',
    re.IGNORECASE | re.DOTALL,
)
_ADD_TO_BAG_BUTTON = re.compile(
    r'<button\b(?:(?!</button>)[\s\S])*?Add to Bag(?:(?!</button>)[\s\S])*?</button>',
    re.IGNORECASE | re.DOTALL,
)
_INERT_PRODUCT_BUTTON = re.compile(
    r'<button\b(?:(?!</button>)[\s\S])*?title=["\'](?:Save to Wishlist|Quick View)["\']'
    r'(?:(?!</button>)[\s\S])*?</button>',
    re.IGNORECASE | re.DOTALL,
)
_WISHLIST_LINK = re.compile(
    r'<a\b(?=[^>]*\bdata-path=["\']wishlist["\'])[^>]*>.*?</a>',
    re.IGNORECASE | re.DOTALL,
)
_PRODUCT_SHOP_BUTTON = re.compile(
    r'<button\b(?:(?!</button>)[\s\S])*?shopping_bag(?:(?!</button>)[\s\S])*?</button>',
    re.IGNORECASE | re.DOTALL,
)
_STATIC_PRICE = re.compile(
    r'<(?:p|span)\b[^>]*>\s*\$\d+(?:\.\d{2})?\s*</(?:p|span)>',
    re.IGNORECASE,
)


class PageHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print(f"{self.command} {urlsplit(self.path).path}", flush=True)

    def do_GET(self):
        path = urlsplit(self.path).path
        if path == "/favicon.ico":
            self.send_response(204)
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            return
        if path not in ("/", "/code.html"):
            self.send_error(404)
            return

        try:
            html = (ROOT / "code.html").read_text(encoding="utf-8")
        except OSError:
            self.send_error(500, "The page could not be read")
            return

        html = _CART_LINK.sub("", html)
        html = _ADD_TO_BAG_BUTTON.sub("", html)
        html = _WISHLIST_LINK.sub("", html)
        html = _INERT_PRODUCT_BUTTON.sub("", html)
        html = _PRODUCT_SHOP_BUTTON.sub("", html)
        html = _STATIC_PRICE.sub("", html)
        html = html.replace(
            'data-path="shop-all" href="#"',
            'data-path="shop-all" href="#products"',
        )
        html = html.replace(
            "✨ Free Glow Kit on orders over $50 • Worldwide Shipping • 100% Cruelty-Free ✨",
            "Discover your glow • Find your shade",
        )
        html = html.replace(
            "Tap any creator look to shop the exact high-impact glow formulation used in their routine.",
            "See how creators build their signature radiant look.",
        )
        html = html.replace(
            'data-path="shimmer-quiz" href="#"',
            'data-path="shimmer-quiz" href="#glow-quiz"',
        )
        body = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    print("Serving the She's Glowing page on port 5000", flush=True)
    ThreadingHTTPServer(("0.0.0.0", PORT), PageHandler).serve_forever()
