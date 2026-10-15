import { readFile } from "node:fs/promises";
import path from "node:path";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

function prepareStorefront(html: string) {
  return html
    .replace(
      /<a\b(?=[^>]*\bdata-path=["']cart["'])[^>]*>[\s\S]*?<\/a>/gi,
      "",
    )
    .replace(
      /<button\b(?:(?!<\/button>)[\s\S])*?Add to Bag(?:(?!<\/button>)[\s\S])*?<\/button>/gi,
      "",
    )
    .replace(
      /<button\b(?:(?!<\/button>)[\s\S])*?title=["'](?:Save to Wishlist|Quick View)["'](?:(?!<\/button>)[\s\S])*?<\/button>/gi,
      "",
    )
    .replace(
      /<a\b(?=[^>]*\bdata-path=["']wishlist["'])[^>]*>[\s\S]*?<\/a>/gi,
      "",
    )
    .replace(
      /<button\b(?:(?!<\/button>)[\s\S])*?shopping_bag(?:(?!<\/button>)[\s\S])*?<\/button>/gi,
      "",
    )
    .replace(
      /<(?:p|span)\b[^>]*>\s*\$\d+(?:\.\d{2})?\s*<\/(?:p|span)>/gi,
      "",
    )
    .replace(
      'data-path="shop-all" href="#"',
      'data-path="shop-all" href="#products"',
    )
    .replace(
      "✨ Free Glow Kit on orders over $50 • Worldwide Shipping • 100% Cruelty-Free ✨",
      "Discover your glow • Find your shade",
    )
    .replace(
      "Tap any creator look to shop the exact high-impact glow formulation used in their routine.",
      "See how creators build their signature radiant look.",
    )
    .replace(
      'data-path="shimmer-quiz" href="#"',
      'data-path="shimmer-quiz" href="#glow-quiz"',
    );
}

export async function GET() {
  try {
    const source = await readFile(path.join(process.cwd(), "code.html"), "utf8");
    return new Response(prepareStorefront(source), {
      headers: {
        "Content-Type": "text/html; charset=utf-8",
        "Cache-Control": "no-store",
      },
    });
  } catch (error) {
    console.error("Unable to load the storefront page.", error);
    return new Response("The storefront page could not be loaded.", {
      status: 500,
      headers: { "Content-Type": "text/plain; charset=utf-8" },
    });
  }
}
