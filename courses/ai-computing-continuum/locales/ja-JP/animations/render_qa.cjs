const fs = require("fs");
const path = require("path");
const { pathToFileURL } = require("url");
const { chromium } = require("playwright");

const jobs = [
  ["m1_inference_placement.html", "m1"],
  ["m2_inference_request.html", "m2"],
  ["m3_sync_across.html", "m3"],
  ["m4_aicc_research_park.html", "m4"],
];
const selectedJobs = process.env.ANIMATION_FILTER
  ? jobs.filter(([, slug]) => slug === process.env.ANIMATION_FILTER)
  : jobs;
const out = "/tmp/aicc-animation-qa";

(async () => {
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  for (const [source, slug] of selectedJobs) {
    await page.goto(pathToFileURL(path.join(__dirname, source)).href);
    await page.waitForFunction(() => typeof window.setFrame === "function");
    for (const [label, progress] of [["first", 0.03], ["middle", 0.52], ["final", 0.98]]) {
      await page.evaluate((p) => window.setFrame(p), progress);
      await page.screenshot({ path: path.join(out, `${slug}_${label}.png`) });
    }
  }
  await browser.close();
  process.stdout.write(`${out}\n`);
})();
