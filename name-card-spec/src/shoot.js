// Renders build/*.html to ../figures/*.png at 2x. Run from this folder: node shoot.js
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
(async () => {
  const build = path.join(__dirname, 'build');
  const out = path.join(__dirname, '..', 'figures');
  fs.mkdirSync(out, { recursive: true });
  const only = process.argv[2] ? process.argv[2].split(',') : null;
  const b = await chromium.launch();
  for (const f of fs.readdirSync(build).filter(f => f.endsWith('.html')).sort()) {
    const name = f.replace(/\.html$/, '');
    if (only && !only.includes(name)) continue;
    const p = await b.newPage({ viewport: { width: 1100, height: 900 }, deviceScaleFactor: 2 });
    await p.goto('file://' + path.join(build, f), { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(250);
    const el = await p.$('#fig');
    await el.screenshot({ path: path.join(out, name + '.png') });
    const box = await el.boundingBox();
    console.log(name, Math.round(box.width) + 'x' + Math.round(box.height));
    await p.close();
  }
  await b.close();
})();
