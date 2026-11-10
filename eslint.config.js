// @ts-check
import eslint from "@eslint/js";
import tseslint from "typescript-eslint";

export default tseslint.config(
  eslint.configs.recommended,
  ...tseslint.configs.strictTypeChecked,
  ...tseslint.configs.stylisticTypeChecked,
  {
    languageOptions: {
      parserOptions: {
        projectService: true,
        tsconfigRootDir: import.meta.dirname,
      },
    },
  },
  {
    // Relax rules for config and test files that run outside TS project references
    files: ["**/*.config.{js,ts,mjs,mts}", "eslint.config.js"],
    extends: [tseslint.configs.disableTypeChecked],
  },
  {
    ignores: [
      "**/node_modules/**",
      "**/dist/**",
      "python/**",
      "graphify-out/**",
      "**/*.d.ts",
      "**/*.js.map",
    ],
  },
);
