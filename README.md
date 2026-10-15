# She’s Glowing

The storefront is served by Next.js, with its backend API routes in the same
application.

## Run locally

```sh
npm run dev
```

The Replit preview uses port 5000. For a production build, run `npm run build`
and then `npm run start`.

The home page is served from `code.html` through the Next.js Node.js route at
`app/route.ts`. Backend endpoints belong under `app/api/`; `/api/health` is a
basic availability check.

For Vercel, use the repository root (`./`) and let Vercel detect Next.js. No
custom output directory is required.
