// Hono API stub — Phase 0 skeleton only.
// No routes or business logic yet; that starts in Phase 1.
import { Hono } from "hono";
import { logger } from "hono/logger";

const app = new Hono();

app.use(logger());

app.get("/", (c) =>
  c.json({
    app: "marghire",
    status: "ok",
    phase: 0,
    message: "Setup in progress. See docs/ for the build plan.",
  }),
);

app.get("/health", (c) => c.json({ status: "ok" }));

const host = process.env.API_HOST ?? "127.0.0.1";
const port = Number(process.env.API_PORT ?? 3000);

console.log(`MargHire API listening on http://${host}:${String(port)}`);

export default {
  port,
  hostname: host,
  fetch: app.fetch,
};
