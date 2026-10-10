# She's Glowing Shopify storefront

## Run

Use the **Start application** workflow, or run:

```sh
python3 server.py
```

The server binds to `0.0.0.0:5000`. Both `/` and `/code.html` serve the
imported `code.html` with the Shopify storefront client injected. Other paths
return 404 so the uploaded archive and internal workspace files are not served.

The bag uses the connected Shopify Storefront API for products, cart changes,
and Shopify-hosted checkout. The server reads the Storefront settings from the
Replit Shopify connection; never put its token in browser code or ask a buyer
to provide it. Shopify must have published products for them to appear in the
store. Add and publish products in Shopify; this app does not create sample
products or inventory.

No third-party Python packages are required. Tailwind CSS, Google Fonts, and
product images load from external hosts, so the page needs an internet
connection.

## Storefront behavior

- Add published, available Shopify variants to the bag.
- Keep the Shopify cart ID in the visitor's browser storage so the bag survives
  refreshes on that browser.
- Change item quantities or remove items; Shopify remains the source of truth
  for prices, product availability, and totals.
- Continue checkout on Shopify. Payment collection, shipping, and taxes happen
  there, not in this app.
