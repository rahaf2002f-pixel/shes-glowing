---
name: Clerk app naming after ZIP imports
description: Avoid Clerk provisioning failures when the Replit project name comes from an uploaded ZIP filename.
---

If Clerk setup rejects a project name derived from an imported ZIP filename, rename the project display name in Project Editor to remove the `.zip` suffix and URL-like punctuation before retrying.

**Why:** Clerk provisioning rejected the ZIP-derived name as URL-like.

**How to apply:** Before provisioning Clerk on a ZIP-imported project, check the Replit display name and simplify it if it contains a filename extension or URL-like characters.
