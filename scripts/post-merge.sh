#!/usr/bin/env bash
set -euo pipefail

# This project has no package manifest or database migrations. Validate the
# files needed to serve the static page without installing unnecessary packages.
python3 - <<'PY'
import ast
from pathlib import Path

server = Path("server.py")
page = Path("code.html")

for required_file in (server, page):
    if not required_file.is_file():
        raise SystemExit(f"Required application file is missing: {required_file}")

ast.parse(server.read_text(encoding="utf-8"), filename=str(server))
print("Post-merge setup passed: application files are present and server.py parses.")
PY
