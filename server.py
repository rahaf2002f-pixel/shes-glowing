"""Shopify-backed storefront API and static page server."""

import json
import os
import re
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit, urlunsplit, parse_qsl
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parent
PORT = 5000
API_VERSION = "2026-04"
CONNECTION_TTL = 60
PRODUCT_TTL = 60
BODY_LIMIT = 32 * 1024

_connection_cache = None
_connection_expiry = 0
_product_cache = None
_product_expiry = 0
_cache_lock = threading.Lock()

PRODUCTS_QUERY = """
query StoreProducts {
  products(first: 24, sortKey: TITLE) {
    nodes {
      id
      title
      handle
      description
      featuredImage { url altText }
      variants(first: 50) {
        nodes {
          id
          title
          availableForSale
          price { amount currencyCode }
        }
      }
    }
  }
}
"""

CART_FIELDS = """
id
totalQuantity
checkoutUrl
cost {
  subtotalAmount { amount currencyCode }
}
lines(first: 50) {
  nodes {
    id
    quantity
    merchandise {
      ... on ProductVariant {
        id
        title
        availableForSale
        price { amount currencyCode }
        image { url altText }
        product { title }
      }
    }
  }
}
"""

CART_QUERY = f"""
query StoreCart($cartId: ID!) {{
  cart(id: $cartId) {{ {CART_FIELDS} }}
}}
"""


class StorefrontError(Exception):
    def __init__(self, message, status=502):
        super().__init__(message)
        self.status = status


def _connector_auth():
    hostname = os.environ.get("REPLIT_CONNECTORS_HOSTNAME", "").strip()
    identity = os.environ.get("REPL_IDENTITY")
    renewal = os.environ.get("WEB_REPL_RENEWAL")
    token = f"repl {identity}" if identity else (
        f"depl {renewal}" if renewal else None
    )
    if not hostname or not token:
        raise StorefrontError(
            "Shopify is connected, but its storefront connection is not available to the server.",
            503,
        )
    protocol = "http" if hostname.startswith("localhost") else "https"
    return f"{protocol}://{hostname}", token


def _storefront_config(force_refresh=False):
    global _connection_cache, _connection_expiry
    now = time.monotonic()
    with _cache_lock:
        if not force_refresh and _connection_cache and now < _connection_expiry:
            return _connection_cache

    base_url, token = _connector_auth()
    query = urlencode({
        "include_secrets": "true",
        "connector_names": "shopify-store",
        "refresh_policy": "none",
    })
    request = Request(
        f"{base_url}/api/v2/connection?{query}",
        headers={"Accept": "application/json", "X_REPLIT_TOKEN": token},
    )
    try:
        with urlopen(request, timeout=15) as response:
            payload = json.loads(response.read())
    except (HTTPError, URLError, TimeoutError, ValueError) as exc:
        raise StorefrontError(
            "Could not load the connected Shopify storefront. Try again in a moment.",
            503,
        ) from exc

    items = payload.get("items") or []
    settings = items[0].get("settings") if items else None
    domain = settings.get("shop_domain") if settings else None
    storefront_token = settings.get("storefront_access_token") if settings else None
    if (
        not isinstance(domain, str)
        or not re.fullmatch(r"[A-Za-z0-9.-]+", domain)
        or not isinstance(storefront_token, str)
        or not storefront_token
    ):
        raise StorefrontError(
            "Shopify's Storefront API is not provisioned for this connection yet.",
            503,
        )

    config = (domain, storefront_token)
    with _cache_lock:
        _connection_cache = config
        _connection_expiry = time.monotonic() + CONNECTION_TTL
    return config


def _shopify_request(query, variables=None, retry_auth=True):
    domain, token = _storefront_config()
    request = Request(
        f"https://{domain}/api/{API_VERSION}/graphql.json",
        data=json.dumps({"query": query, "variables": variables or {}}).encode(),
        headers={
            "Content-Type": "application/json",
            "X-Shopify-Storefront-Access-Token": token,
        },
        method="POST",
    )
    try:
        with urlopen(request, timeout=20) as response:
            payload = json.loads(response.read())
    except HTTPError as exc:
        if exc.code in (401, 403) and retry_auth:
            _storefront_config(force_refresh=True)
            return _shopify_request(query, variables, retry_auth=False)
        raise StorefrontError(
            f"Shopify could not complete that request (HTTP {exc.code}).",
            502,
        ) from exc
    except (URLError, TimeoutError, ValueError) as exc:
        raise StorefrontError(
            "Shopify could not be reached. Please try again.",
            502,
        ) from exc

    if payload.get("errors"):
        raise StorefrontError("Shopify could not complete that request.", 502)
    return payload.get("data") or {}


def _user_errors(result):
    errors = (result or {}).get("userErrors") or []
    if errors:
        message = errors[0].get("message", "Shopify rejected the cart change.")
        raise StorefrontError(message, 400)
    return result


def _get_products(force_refresh=False):
    global _product_cache, _product_expiry
    now = time.monotonic()
    with _cache_lock:
        if not force_refresh and _product_cache is not None and now < _product_expiry:
            return _product_cache

    data = _shopify_request(PRODUCTS_QUERY)
    nodes = (data.get("products") or {}).get("nodes") or []
    products = []
    for product in nodes:
        variants = []
        for variant in (product.get("variants") or {}).get("nodes") or []:
            price = variant.get("price") or {}
            variants.append({
                "id": variant.get("id"),
                "title": variant.get("title") or "Default",
                "availableForSale": bool(variant.get("availableForSale")),
                "price": price,
            })
        image = product.get("featuredImage")
        products.append({
            "id": product.get("id"),
            "title": product.get("title") or "Product",
            "handle": product.get("handle"),
            "description": product.get("description") or "",
            "image": image,
            "variants": variants,
        })

    with _cache_lock:
        _product_cache = products
        _product_expiry = time.monotonic() + PRODUCT_TTL
    return products


def _normalize_cart(cart):
    if not cart:
        return None
    items = []
    for line in ((cart.get("lines") or {}).get("nodes") or []):
        variant = line.get("merchandise") or {}
        product = variant.get("product") or {}
        if not variant.get("id"):
            continue
        items.append({
            "lineId": line.get("id"),
            "variantId": variant.get("id"),
            "title": product.get("title") or "Product",
            "variantTitle": variant.get("title") or "",
            "quantity": int(line.get("quantity") or 0),
            "available": bool(variant.get("availableForSale")),
            "price": variant.get("price") or {},
            "image": variant.get("image"),
        })
    cost = cart.get("cost") or {}
    return {
        "id": cart.get("id"),
        "totalQuantity": int(cart.get("totalQuantity") or 0),
        "subtotal": cost.get("subtotalAmount") or {},
        "items": items,
    }


def _get_cart(cart_id):
    data = _shopify_request(CART_QUERY, {"cartId": cart_id})
    return (data.get("cart") or None)


def _cart_change(payload):
    action = payload.get("action")
    cart_id = payload.get("cartId")
    if cart_id is not None and (
        not isinstance(cart_id, str)
        or len(cart_id) > 500
        or not cart_id.startswith("gid://shopify/Cart/")
    ):
        raise StorefrontError("This cart could not be found. Please refresh and try again.", 400)

    if action == "get":
        return _normalize_cart(_get_cart(cart_id)) if cart_id else None

    if action == "add":
        variant_id = payload.get("variantId")
        quantity = payload.get("quantity", 1)
        if (
            not isinstance(variant_id, str)
            or len(variant_id) > 250
            or not variant_id.startswith("gid://shopify/ProductVariant/")
            or not isinstance(quantity, int)
            or isinstance(quantity, bool)
            or quantity < 1
            or quantity > 99
        ):
            raise StorefrontError("Choose an available product and quantity.", 400)
        if cart_id:
            data = _shopify_request(
                """
                mutation AddCartLine($cartId: ID!, $lines: [CartLineInput!]!) {
                  cartLinesAdd(cartId: $cartId, lines: $lines) {
                    cart { %s }
                    userErrors { message }
                  }
                }
                """ % CART_FIELDS,
                {"cartId": cart_id, "lines": [{"merchandiseId": variant_id, "quantity": quantity}]},
            )
            result = _user_errors(data.get("cartLinesAdd"))
            cart = result.get("cart")
        else:
            data = _shopify_request(
                """
                mutation CreateCart($lines: [CartLineInput!]!) {
                  cartCreate(input: { lines: $lines }) {
                    cart { %s }
                    userErrors { message }
                  }
                }
                """ % CART_FIELDS,
                {"lines": [{"merchandiseId": variant_id, "quantity": quantity}]},
            )
            result = _user_errors(data.get("cartCreate"))
            cart = result.get("cart")
        if not cart:
            raise StorefrontError("Shopify did not return a cart. Please try again.")
        return _normalize_cart(cart)

    if action in ("update", "remove"):
        if not cart_id:
            raise StorefrontError("Your bag is empty.", 400)
        line_id = payload.get("lineId")
        if not isinstance(line_id, str) or len(line_id) > 500:
            raise StorefrontError("That bag item could not be found.", 400)
        if action == "update":
            quantity = payload.get("quantity")
            if (
                not isinstance(quantity, int)
                or isinstance(quantity, bool)
                or quantity < 1
                or quantity > 99
            ):
                raise StorefrontError("Quantity must be between 1 and 99.", 400)
            mutation = """
            mutation UpdateCartLine($cartId: ID!, $lines: [CartLineUpdateInput!]!) {
              cartLinesUpdate(cartId: $cartId, lines: $lines) {
                cart { %s }
                userErrors { message }
              }
            }
            """ % CART_FIELDS
            variables = {"cartId": cart_id, "lines": [{"id": line_id, "quantity": quantity}]}
            key = "cartLinesUpdate"
        else:
            mutation = """
            mutation RemoveCartLine($cartId: ID!, $lineIds: [ID!]!) {
              cartLinesRemove(cartId: $cartId, lineIds: $lineIds) {
                cart { %s }
                userErrors { message }
              }
            }
            """ % CART_FIELDS
            variables = {"cartId": cart_id, "lineIds": [line_id]}
            key = "cartLinesRemove"
        data = _shopify_request(mutation, variables)
        result = _user_errors(data.get(key))
        return _normalize_cart(result.get("cart"))

    raise StorefrontError("Unknown bag action.", 400)


def _checkout_url(cart_id):
    if not isinstance(cart_id, str) or not cart_id.startswith("gid://shopify/Cart/"):
        raise StorefrontError("Your bag is empty.", 400)
    cart = _get_cart(cart_id)
    if not cart:
        raise StorefrontError("Your Shopify cart has expired. Add your products again.", 400)
    checkout_url = cart.get("checkoutUrl")
    domain, _ = _storefront_config()
    parsed = urlsplit(checkout_url or "")
    if parsed.scheme != "https" or parsed.hostname != domain or not parsed.path:
        raise StorefrontError("Shopify did not return a valid checkout link.")
    if os.environ.get("REPLIT_DEV_DOMAIN") and not os.environ.get("REPLIT_DEPLOYMENT"):
        query = dict(parse_qsl(parsed.query))
        query["channel"] = "online_store"
        parsed = parsed._replace(query=urlencode(query))
        checkout_url = urlunsplit(parsed)
    return checkout_url


class PageHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        # Do not log query strings, cart IDs, or Shopify/customer data.
        print(f"{self.command} {urlsplit(self.path).path}", flush=True)

    def do_GET(self):
        path = urlsplit(self.path).path
        try:
            if path == "/api/products":
                return self._json(200, {"products": _get_products()})
            if path in ("/", "/code.html"):
                return self._static_page()
            if path == "/storefront.js":
                return self._static_file("storefront.js", "text/javascript; charset=utf-8")
            if path == "/storefront.css":
                return self._static_file("storefront.css", "text/css; charset=utf-8")
            self.send_error(404)
        except StorefrontError as exc:
            self._json(exc.status, {"error": str(exc)})
        except Exception:
            self._json(502, {"error": "The store could not complete that request. Please try again."})

    def do_POST(self):
        path = urlsplit(self.path).path
        try:
            payload = self._read_json()
            if path == "/api/cart":
                return self._json(200, {"cart": _cart_change(payload)})
            if path == "/api/checkout":
                return self._json(200, {"checkoutUrl": _checkout_url(payload.get("cartId"))})
            self.send_error(404)
        except StorefrontError as exc:
            self._json(exc.status, {"error": str(exc)})
        except (ValueError, UnicodeDecodeError):
            self._json(400, {"error": "Please send a valid request."})
        except Exception:
            self._json(502, {"error": "The store could not complete that request. Please try again."})

    def _read_json(self):
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0 or length > BODY_LIMIT:
            raise ValueError("Invalid request size")
        payload = json.loads(self.rfile.read(length))
        if not isinstance(payload, dict):
            raise ValueError("Expected an object")
        return payload

    def _json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _static_file(self, filename, content_type):
        file_path = ROOT / filename
        try:
            body = file_path.read_bytes()
        except OSError:
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _static_page(self):
        try:
            html = (ROOT / "code.html").read_text(encoding="utf-8")
        except OSError:
            self.send_error(500, "The imported page could not be read")
            return
        injection = (
            '<link rel="stylesheet" href="/storefront.css">'
            '<script defer src="/storefront.js"></script>'
        )
        html = html.replace("</head>", injection + "</head>", 1)
        body = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    print("Serving the Shopify storefront on port 5000", flush=True)
    ThreadingHTTPServer(("0.0.0.0", PORT), PageHandler).serve_forever()
