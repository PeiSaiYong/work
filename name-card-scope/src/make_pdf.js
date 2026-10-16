// Prints the scope and the build notes to PDF with Chromium (Playwright), in two sizes:
// -phone.pdf: narrow pages laid out like the page on a phone, for reading in the Drive app;
// -a4.pdf: A4 pages laid out like the page on a computer, for printing.
// Run: NODE_PATH=$(npm root -g) node name-card-scope/src/make_pdf.js
const path = require('path');
const { chromium } = require('playwright');

const DIR = path.resolve(__dirname, '..');
const DOCS = [
  ['minmed-name-card-scope', 'Minmed Digital Name Cards · Product scope'],
  ['minmed-name-card-build-notes', 'Minmed Digital Name Cards · Build notes'],
];
// width: layout width in CSS px (page width minus side margins, divided by scale)
const SIZES = [
  { tag: 'phone', width: 400, scale: 1, page: { width: '118mm', height: '256mm' }, side: '6mm', top: '7mm', bottom: '11mm', foot: 9 },
  { tag: 'a4', width: 976, scale: 0.72, page: { format: 'A4' }, side: '12mm', top: '12mm', bottom: '16mm', foot: 8 },
];

(async () => {
  const browser = await chromium.launch();
  for (const [name, title] of DOCS) {
    for (const z of SIZES) {
      const page = await browser.newPage({ viewport: { width: z.width, height: 1400 } });
      await page.goto('file://' + path.join(DIR, name + '.html'), { waitUntil: 'networkidle' });
      await page.evaluate(() => document.fonts.ready);
      await page.evaluate(() => { if (typeof fitShots === 'function') fitShots(); });
      const out = `${name}-${z.tag}.pdf`;
      await page.pdf({
        path: path.join(DIR, out),
        ...z.page,
        printBackground: true,
        scale: z.scale,
        margin: { top: z.top, right: z.side, bottom: z.bottom, left: z.side },
        displayHeaderFooter: true,
        headerTemplate: '<span></span>',
        footerTemplate:
          `<div style="width:100%;padding:0 ${z.side};display:flex;justify-content:space-between;` +
          `font:${z.foot}px Arial,Helvetica,sans-serif;color:#8a8f99">` +
          `<span>${title}</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>`,
      });
      await page.close();
      console.log('wrote', out);
    }
  }
  await browser.close();
})();
