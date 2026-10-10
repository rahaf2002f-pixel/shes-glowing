# Imported She's Glowing page

## Run

Use the **Start application** workflow, or run:

```sh
python3 server.py
```

The server binds to `0.0.0.0:5000`. Both `/` and `/code.html` serve the
original `code.html` unchanged. Other paths return 404 so the uploaded archive
and internal workspace files are not publicly served.

No third-party Python packages, secrets, or backend services are required.
The page uses externally hosted Tailwind CSS, Google Fonts, and images, so
those resources require an internet connection.

## Scope

This is the imported static storefront, not a complete ecommerce backend.
Keep the existing HTML and design guide; do not migrate or restructure the
project as part of setup.
