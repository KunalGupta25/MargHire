import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    projects: [
      "apps/api/vitest.config.ts",
      "packages/core/vitest.config.ts",
      "packages/providers/vitest.config.ts",
      "packages/sources/vitest.config.ts",
      "packages/db/vitest.config.ts",
    ],
  },
});
