import canvaPlugin from "@canva/app-eslint-plugin";

export default [
  { ignores: ["**/node_modules/", "**/dist", "**/*.d.ts"] },
  ...canvaPlugin.configs.apps_no_i18n,
  // The Canva plugin bundles eslint-plugin-jest; this app has no jest, so pin the version.
  { settings: { jest: { version: 30 } } },
];
