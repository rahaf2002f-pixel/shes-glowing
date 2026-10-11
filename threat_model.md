# Threat Model

## Project Overview

"She's Glowing" is a static cosmetics marketing landing page. A minimal Python
standard-library HTTP server (`server.py`, built on `http.server.ThreadingHTTPServer`)
serves a single pre-rendered HTML file (`code.html`) on `0.0.0.0:5000`. There is no
database, no authentication, no user accounts, and no server-side processing of user
input. The site explicitly does not take orders; cart/checkout/wishlist controls are
stripped out server-side before the page is served, and the shade quiz runs entirely
in the browser.

## Assets

- **Static content integrity** — the marketing page served to visitors. Low sensitivity;
  no PII or secrets are stored or transmitted.
- There are no credentials, tokens, API keys, payment data, or personal data handled by
  this application.

## Trust Boundaries

- **Browser to server** — the only boundary. Clients issue GET requests; the server
  replies with a fixed, transformed copy of `code.html`. No request-derived data (path
  beyond an exact allowlist, query, headers, body, cookies) influences server behavior
  in a security-relevant way.
- **Browser to third-party CDNs** — the page loads Tailwind, Google Fonts, and images
  from external hosts. These are standard public assets, not a trust boundary the app
  controls.

## Scan Anchors

- Production entry point: `server.py` (`PageHandler.do_GET`), serving only `/`,
  `/code.html`, and a 204 for `/favicon.ico`; all other paths return 404.
- Highest-risk code area (relative): the regex substitutions in `server.py` — but they
  operate exclusively on the server's own `code.html`, never attacker input.
- Public surface: entire site is public and read-only. No authenticated or admin surface.
- Client logic: inline `<script>` in `code.html` (shade quiz) uses `textContent`, not
  `innerHTML`; no attacker-controlled DOM sinks.
- Dev-only/no-op artifacts: `screen.png`, `zipFile.zip`, `DESIGN.md` are not served.

## Threat Categories

### Information Disclosure

The server reads only a fixed file and allowlists exactly two paths, returning 404 for
anything else, so internal workspace files (including `server.py`, `zipFile.zip`,
`screen.png`) are not exposed. Error handling returns generic messages without stack
traces. Guarantee: the path allowlist in `do_GET` must remain exact-match; no
user-supplied path segment may be joined onto the filesystem.

### Tampering / Elevation of Privilege

Not applicable in practice — there is no state to tamper with, no roles, and no
privileged actions. The server performs no writes and executes no user-derived code.

### Denial of Service

The server is single-purpose and reads a small file per request. Regexes use nested
quantifiers but run only against the trusted, fixed `code.html`, so there is no ReDoS
from attacker input. Platform-level protections apply if deployed. No rate limiting is
present, but there is no sensitive or expensive operation to protect.
