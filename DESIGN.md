---
name: Luminous Editorial
colors:
  surface: '#f9f9f9'
  surface-dim: '#dadada'
  surface-bright: '#f9f9f9'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f3f3f3'
  surface-container: '#eeeeee'
  surface-container-high: '#e8e8e8'
  surface-container-highest: '#e2e2e2'
  on-surface: '#1a1c1c'
  on-surface-variant: '#47464b'
  inverse-surface: '#2f3131'
  inverse-on-surface: '#f0f1f1'
  outline: '#77767b'
  outline-variant: '#c8c5cb'
  surface-tint: '#5f5e61'
  primary: '#000000'
  on-primary: '#ffffff'
  primary-container: '#1b1b1e'
  on-primary-container: '#858387'
  inverse-primary: '#c8c5ca'
  secondary: '#a43073'
  on-secondary: '#ffffff'
  secondary-container: '#fc79bd'
  on-secondary-container: '#76014e'
  tertiary: '#000000'
  on-tertiary: '#ffffff'
  tertiary-container: '#26171c'
  on-tertiary-container: '#947e84'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#e4e1e6'
  primary-fixed-dim: '#c8c5ca'
  on-primary-fixed: '#1b1b1e'
  on-primary-fixed-variant: '#47464a'
  secondary-fixed: '#ffd8e7'
  secondary-fixed-dim: '#ffafd3'
  on-secondary-fixed: '#3d0026'
  on-secondary-fixed-variant: '#85145a'
  tertiary-fixed: '#f7dce2'
  tertiary-fixed-dim: '#dac0c6'
  on-tertiary-fixed: '#26171c'
  on-tertiary-fixed-variant: '#544247'
  background: '#f9f9f9'
  on-background: '#1a1c1c'
  surface-variant: '#e2e2e2'
typography:
  display:
    fontFamily: Playfair Display
    fontSize: 56px
    fontWeight: '600'
    lineHeight: 64px
    letterSpacing: -0.02em
  display-mobile:
    fontFamily: Playfair Display
    fontSize: 36px
    fontWeight: '600'
    lineHeight: 44px
    letterSpacing: -0.01em
  headline-lg:
    fontFamily: Playfair Display
    fontSize: 40px
    fontWeight: '600'
    lineHeight: 48px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Playfair Display
    fontSize: 28px
    fontWeight: '600'
    lineHeight: 36px
    letterSpacing: 0em
  headline-md:
    fontFamily: Playfair Display
    fontSize: 28px
    fontWeight: '500'
    lineHeight: 36px
  headline-sm:
    fontFamily: Playfair Display
    fontSize: 22px
    fontWeight: '500'
    lineHeight: 30px
  body-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 15px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 20px
  label-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.04em
  label-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.06em
  label-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 10px
    fontWeight: '700'
    lineHeight: 14px
    letterSpacing: 0.08em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1.5rem
  gutter-mobile: 1rem
  margin: 3rem
  margin-mobile: 1.25rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.75rem
  space-xl: 3rem
---

## Brand & Style

The design system embodies a modern, ultra-chic luxury beauty ethos. Built for a digitally native audience of young women and beauty aficionados, the visual experience strikes a balance between hyper-feminine softness and bold, editorial confidence.

The design philosophy unites:
- **Luminous Editorial:** High-fashion editorial layouts driven by high-contrast serif typography paired with hyper-refined, luminous white spaces.
- **Glass & Gloss Accents:** Subtle surface gloss, soft radiant glows, and frosted blurs that evoke dewy, glass-skin cosmetics and highlighter shimmer.
- **Modern Minimal Structure:** Grounded structural geometry prevents the brand from feeling overly ornate, keeping the digital store intuitive, sleek, and conversion-focused.

The interface should evoke a sense of empowerment, radiant self-care, and aspirational beauty that feels accessible yet elevated.

## Colors

The palette leverages high-contrast editorial drama with soft, romantic cosmetic undertones:

- **Primary (`#18181B`):** Deep carbon black. Anchors the brand with decisive readability, crisp borders, and authoritative high-fashion framing.
- **Secondary (`#F472B6`):** Vibrant rose quartz. Used strategically for promotional callouts, active state indicators, hover highlights, and radiant accents.
- **Tertiary (`#FDE2E8`):** Ballet slipper blush. Provides warm, soft tinted surface fills, chip backings, and subtle glow gradients.
- **Neutral (`#FAFAFA`):** Luminous pearl white. Serves as the canvas base to deliver pristine clarity, letting product imagery and packaging take center stage.

### Application Rules
- Canvas backgrounds stay strictly clean on pure pearl neutral tones (`#FFFFFF` to `#FAFAFA`).
- Heavy primary black is reserved for primary CTAs, headlines, and thin geometric borders to prevent the interface from drifting into overly childish pastel territory.
- Pink tones serve as ambient light and warmth; avoid full-screen pink washes.

## Typography

The type system blends classic editorial sophistication with clean geometric legibility.

- **Headlines (`Playfair Display`):** Conveys luxury beauty editorial credibility. Display and large headings should use italic styling selectively for key accent words (e.g., "*Glow*", "*Rules*") to accentuate movement and editorial charm.
- **Body & Controls (`Plus Jakarta Sans`):** Delivers welcoming, open curves that pair naturally with cosmetic themes while maintaining sharp readability across small UI elements, product specifications, and pricing tables.
- **Labels & Microcopy:** Capitalized, tracked-out styling (`0.04em` to `0.08em`) is used for collection tags, category chips, and luxury badges to mirror perfume and high-end packaging standards.

## Layout & Spacing

The layout embraces generous breathing room to communicate premium tier status. Clutter conveys bargain; spaciousness conveys curated luxury.

### Grid & Layout Rules
- **Desktop (1024px+):** 12-column fluid grid within a `1360px` max container width. Gutter spacing sits at `1.5rem` with page margins scaling up to `3rem`.
- **Tablet (768px - 1023px):** 8-column grid with `1.25rem` gutters and `2rem` margins.
- **Mobile (320px - 767px):** 4-column layout with `1rem` gutters and `1.25rem` screen edge margins.

### Vertical Rhythm
Section blocks adhere to generous vertical separation (`space-xl` scaled to double on desktop breakpoints) to give product hero features, shade finders, and beauty tutorials room to unfold sequentially without visual collision.

## Elevation & Depth

Elevation moves away from heavy grey shadows in favor of ambient luminescence and glassmorphism.

- **Dewy Ambient Shadows:** Drop shadows use tinted blush and warm undertones (`rgba(244, 114, 182, 0.12)` to `rgba(24, 24, 27, 0.05)`) with broad diffusion radiuses (16px to 32px). This creates a floating, sun-kissed lift.
- **Gloss Surfaces:** Modal sheets, quick-shop overlays, and floating headers use a semi-translucent backdrop (`rgba(255, 255, 255, 0.85)`) coupled with a `16px` backdrop blur and a `1px` crisp inner highlight line (`rgba(255, 255, 255, 0.6)`).
- **Luminous Rim Effects:** Key featured product cards use a hairline border (`1px solid rgba(244, 114, 182, 0.2)`) that amplifies on hover to simulate an iridescent reflection.

## Shapes

The geometric framework balances soft, approachable cosmetics contours with structural balance:

- **Base Radius (0.5rem / 8px):** Applied to form inputs, thumbnails, review cards, and subtle interactive panels.
- **Large Radius (1rem / 16px):** Standard for product cards, modal containers, and curated editorial carousels.
- **Full Pill Radius (9999px):** Applied exclusively to call-to-action buttons, filter pills, formula badges, and floating navigation bars to preserve a friendly, soft-touch cosmetic aesthetic.

## Components

### Buttons
- **Primary Action:** Solid carbon black background (`#18181B`), crisp white text, fully pill-shaped. Hover introduces an ambient rose shadow (`0 8px 24px rgba(244, 114, 182, 0.35)`) and micro-scale lift.
- **Secondary Action:** Ghost pill with a `1.5px` carbon black border (`#18181B`) and translucent ivory interior. Hover shifts background to ballet slipper blush (`#FDE2E8`).
- **Glow Accent Button:** Gradient fill spanning `#F472B6` to delicate coral-blush, white bold text; reserved for "Add to Bag" instant buy or shade matching tools.

### Product Cards
- **Structure:** Encased in a `1rem` radius white pearl card (`#FFFFFF`) framed by a low-opacity border (`rgba(24, 24, 27, 0.06)`).
- **Imagery:** Aspect ratio 4:5 with soft pastel-tinted studio backdrops.
- **Interaction:** On hover, image transitions to an application or swatch preview, while the card lifts with a dewy ambient blur. A quick-add pill fades up from the bottom edge.

### Chips & Badges
- **Status Badges ("Clean", "Vegan", "New"):** Uppercase `label-sm` tracking with semi-translucent blush background (`rgba(253, 226, 232, 0.7)`), deep black text, and full pill curves.
- **Filter Chips:** Inactive state features pearl white background and delicate gray contour; selected state switches to solid carbon black fill with white text.

### Form Inputs
- **Text Inputs:** Generous height (`48px`), gentle `0.5rem` radius, light neutral fill (`#FAFAFA`), and `1px` subtle border. 
- **Focus State:** Transitions to a clean black border accompanied by a soft pink aura ring (`box-shadow: 0 0 0 3px rgba(244, 114, 182, 0.25)`).

### Checkboxes & Radios
- Circular and rounded square selectors that fill with solid `#18181B` upon selection, showing an inner white check or pearl dot.

### Specialized Beauty Components
- **Shade Swatch Selector:** Clustered `28px` circular swatches with realistic formula sheen. Active selection shows an outer concentric ring offset by `2px`.
- **Luminous Banner:** Soft gradient background fusing `#FAFAFA`, `#FDE2E8`, and radial shimmers of `#FCE7F3`, pairing dramatic Playfair Display typography with high-contrast pill CTAs.