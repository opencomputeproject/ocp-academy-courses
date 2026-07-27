const fs = require("fs");
const os = require("os");
const path = require("path");
const { pathToFileURL } = require("url");
const { spawnSync } = require("child_process");
const { chromium } = require("playwright");

const root = __dirname;
const output = path.resolve(root, "../figures");
const ffmpeg = process.env.FFMPEG_BIN || "ffmpeg";
const fps = 15;
const jobs = [
  ["m1_inference_placement.html", "m1_inference_placement", 12],
  ["m2_inference_request.html", "m2_inference_request", 12],
  ["m3_sync_across.html", "m3_sync_across", 12],
  ["m4_aicc_research_park.html", "m4_aicc_research_park", 24],
];
const selectedJobs = process.env.ANIMATION_FILTER
  ? jobs.filter(([, outputName]) => outputName === process.env.ANIMATION_FILTER)
  : jobs;

function run(command, args) {
  const result = spawnSync(command, args, { stdio: "inherit" });
  if (result.status !== 0) {
    throw new Error(`${command} failed with exit code ${result.status}`);
  }
}

(async () => {
  fs.mkdirSync(output, { recursive: true });
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({
    viewport: { width: 1280, height: 720 },
    deviceScaleFactor: 1,
  });

  for (const [sourceName, outputName, duration] of selectedJobs) {
    const framesDir = fs.mkdtempSync(path.join(os.tmpdir(), `${outputName}-`));
    await page.goto(pathToFileURL(path.join(root, sourceName)).href);
    await page.waitForFunction(() => typeof window.setFrame === "function");
    const frameCount = fps * duration;
    const posterFrame = Math.floor(frameCount * 0.72);

    for (let i = 0; i < frameCount; i += 1) {
      const progress = i / (frameCount - 1);
      await page.evaluate((p) => window.setFrame(p), progress);
      const framePath = path.join(framesDir, `frame_${String(i).padStart(4, "0")}.png`);
      await page.screenshot({ path: framePath });
      if (i === posterFrame) {
        fs.copyFileSync(
          framePath,
          path.join(output, `${outputName}_poster.png`)
        );
      }
    }

    run(ffmpeg, [
      "-y",
      "-framerate", String(fps),
      "-i", path.join(framesDir, "frame_%04d.png"),
      "-c:v", "libx264",
      "-preset", "medium",
      "-crf", "20",
      "-pix_fmt", "yuv420p",
      "-movflags", "+faststart",
      path.join(output, `${outputName}.mp4`),
    ]);
    fs.rmSync(framesDir, { recursive: true, force: true });
    process.stdout.write(`rendered ${outputName}.mp4\n`);
  }

  await browser.close();
})();
