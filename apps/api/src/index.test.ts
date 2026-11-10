import { describe, expect, it } from "vitest";

// Smoke test: the app module exports a valid Bun/Node serve config.
// Real route tests start in Phase 1.
describe("api stub", () => {
  it("exports a fetch handler", async () => {
    const mod = await import("../src/index.js");
    expect(typeof mod.default.fetch).toBe("function");
  });
});
