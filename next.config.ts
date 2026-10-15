import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  allowedDevOrigins: ["*.replit.dev", "*.repl.co"],
  outputFileTracingIncludes: {
    "/*": ["./code.html"],
  },
};

export default nextConfig;
