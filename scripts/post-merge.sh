#!/usr/bin/env bash
set -euo pipefail

# Validate the files required by the Next.js app. Dependency installation is
# handled by the workspace package manager.
for required_file in package.json app/route.ts app/api/health/route.ts code.html; do
  if [[ ! -f "$required_file" ]]; then
    echo "Required application file is missing: $required_file" >&2
    exit 1
  fi
done

echo "Post-merge setup passed: Next.js storefront and API routes are present."
