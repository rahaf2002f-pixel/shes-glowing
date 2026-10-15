export const runtime = "nodejs";

export function GET() {
  return Response.json(
    { status: "ok", service: "shes-glowing" },
    { headers: { "Cache-Control": "no-store" } },
  );
}
