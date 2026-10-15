# She's Glowing website

## Run

Use the **Start application** workflow, or run:

```sh
npm run dev
```

Next.js binds to `0.0.0.0:5000`. The storefront at `/` is served by the Node.js
route in `app/route.ts`; backend endpoints belong in `app/api/`. The `/api/health`
endpoint is a basic availability check.

The source storefront is `code.html`. Tailwind CSS, Google Fonts, and page
images load from external hosts, so the page needs an internet connection.

## Page behavior

- The collection cards are a visual showcase; this site does not take orders.
- The shade quiz runs in the browser and does not use an external service.
