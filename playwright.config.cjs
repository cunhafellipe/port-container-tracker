const { defineConfig } = require("@playwright/test");
const { mkdtempSync } = require("node:fs");
const { tmpdir } = require("node:os");
const { join } = require("node:path");
const directory = mkdtempSync(join(tmpdir(), "port-container-tracker-e2e-"));
module.exports = defineConfig({
  testDir: "./tests/browser",
  workers: 1,
  retries: 0,
  timeout: 30000,
  use: {
    baseURL: "http://127.0.0.1:9112",
    browserName: "chromium",
    screenshot: "only-on-failure",
    trace: "retain-on-failure",
  },
  metadata: { demoTempDirectory: directory },
  globalTeardown: require.resolve("./tests/browser/cleanup.cjs"),
  webServer: [
    {
      command: `python3 -m demo.server --port 9112 --db "${join(directory, "demo.sqlite3")}"`,
      url: "http://127.0.0.1:9112/api/health",
      reuseExistingServer: false,
      timeout: 15000,
      stderr: "ignore",
    },
    {
      command: "python3 -m http.server 9212 --bind 127.0.0.1",
      url: "http://127.0.0.1:9212/index.html",
      reuseExistingServer: false,
      timeout: 15000,
      stderr: "ignore",
    },
  ],
});
