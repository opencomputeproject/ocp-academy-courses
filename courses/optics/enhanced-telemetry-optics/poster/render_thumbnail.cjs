const path = require('path');
const { pathToFileURL } = require('url');
const { chromium } = require('playwright');

async function render() {
  const browser = await chromium.launch({ headless: true, channel: 'chrome' });
  try {
    const page = await browser.newPage({
      viewport: { width: 800, height: 400 },
      deviceScaleFactor: 1,
    });
    await page.goto(pathToFileURL(path.join(__dirname, 'thumbnail.html')).href);
    await page.evaluate(async () => {
      await document.fonts.ready;
      await Promise.all(Array.from(document.images, image => image.decode()));
      if (!document.fonts.check('700 42px PosterLato')) {
        throw new Error('The Academy Lato font did not load.');
      }
      const emblemLeft = 530;
      for (const element of document.querySelectorAll('h1 span, .badge, .support')) {
        const range = document.createRange();
        range.selectNodeContents(element);
        for (const rect of range.getClientRects()) {
          if (rect.left < 0 || rect.right >= emblemLeft || rect.bottom > 400) {
            throw new Error('Poster text is clipped or collides with the emblem.');
          }
        }
      }
    });
    const output = path.join(__dirname, '..', 'thumbnail.png');
    await page.screenshot({ path: output, type: 'png' });
    console.log(`Rendered 800 x 400 LMS poster: ${output}`);
  } finally {
    await browser.close();
  }
}

render().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
