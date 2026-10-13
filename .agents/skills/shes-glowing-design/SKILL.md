---
name: shes-glowing-design
description: Designs, updates, and reviews the She’s Glowing beauty storefront. Use for brand styling, responsive page improvements, beauty-shopping UX, or storefront feature work in this project.
---

# She’s Glowing Design

Use this project skill when working on the She’s Glowing website. Inspect the current implementation before changing it; the guidance below is not proof that a described feature or brand claim is currently implemented.

## Brand identity

- Keep the brand name exactly **She’s Glowing**.
- Aim for an elegant, feminine, modern beauty-store identity.
- Use blush pink, ivory, cream, white, and restrained champagne-gold accents.
- Keep typography readable and elegant, with consistent spacing and clear hierarchy.
- Prefer a polished, inviting, product-focused experience with generous whitespace.
- Use available high-quality beauty and product imagery. Do not replace working assets unnecessarily.
- The suggested homepage headline is “Your Glow, Your Rules.”
- Use subtle transitions and hover states; avoid distracting animation.

## Storefront design

- Use clear navigation and consistent, touch-friendly buttons.
- When supported by the current catalog, present New Arrivals, Best Sellers, and Glow Picks.
- Use relevant categories such as Makeup, Skincare, Perfumes, and Beauty Tools only when they match real catalog data.
- Show product images, names, prices, ratings, details, and galleries only when they come from a real, verified source. Never invent current prices, ratings, reviews, product claims, or inventory.
- Add search, category filters, sorting, product details, or other shopping interactions only when they work end-to-end with the current data source.
- Include footer and social links only when their destinations are configured.
- Optional features such as Find Your Glow discovery or Glow Rewards must not be presented as working unless implemented.

## Commerce and feature integrity

- Treat the running code and connected services as the source of truth. Preserve working authentication, product data, cart behavior, and database configuration when they exist.
- The current project was intentionally changed to stop using Shopify; product cards are display-only and there is no live cart, wishlist, or checkout.
- Do not reconnect Shopify or restore cart, wishlist, or checkout UI unless the user explicitly requests it. If live commerce is requested, clarify the desired commerce provider when needed and connect the UI to a real catalog and checkout flow.
- Do not show fake success states. Add clear feedback and loading, empty, or error states for any real interactions you implement.

## Accessibility and responsive behavior

- Make the site work at mobile, tablet, and desktop sizes.
- Prevent horizontal scrolling, overlapping, and clipped content.
- Maintain readable contrast and semantic heading structure.
- Label form controls, support keyboard use, and keep interactive targets touch-friendly.
- Use descriptive alternative text for meaningful imagery.

## Implementation workflow

1. Inspect the relevant pages, components, server routes, data sources, integrations, and workflows before editing.
2. Identify useful existing design and behavior; make the smallest changes that meet the request.
3. Reuse existing components, tokens, and patterns where possible.
4. Connect new behavior to the real backend or service. Do not substitute a static mockup for a requested working feature.
5. Keep credentials and secrets out of source code, logs, and screenshots.
6. Verify the changed page and key interactions at relevant screen sizes; check workflow and browser logs for regressions.
7. Summarize what changed and call out anything that still needs configuration or user input.
