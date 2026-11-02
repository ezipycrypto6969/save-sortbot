// node slides.js <queue/id.json> <outDir>  — renders a slideshow (carousel) spec into slide-1.jpg … slide-N.jpg (1080x1350, 4:5).
// 4:5 is the tallest shape Instagram carousels accept, and TikTok photo posts show it full width.
// The account's look (colours, handle) comes from accounts.json, matched by the spec's "account".
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const [specPath, out] = process.argv.slice(2);
  const spec = JSON.parse(fs.readFileSync(specPath, 'utf8'));
  if (!Array.isArray(spec.slides) || spec.slides.length < 2) { console.error('slideshow needs at least 2 slides'); process.exit(1); }
  if (spec.slides.length > 10) { console.error('slideshow has more than 10 slides (Instagram limit)'); process.exit(1); }
  const accounts = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'accounts.json'), 'utf8')).accounts;
  const acct = accounts.find(a => a.id === (spec.account || 'main')) || {};
  const deck = { slides: spec.slides, theme: { ...(acct.theme || {}), ...(spec.theme || {}) } };
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('file://' + path.join(__dirname, 'slides.html'));
  for (let i = 0; i < deck.slides.length; i++) {
    await p.evaluate(([d, i]) => window.show(d, i), [deck, i]);
    await p.waitForFunction(() => [...document.images].every(im => im.complete && im.naturalWidth > 0), null, { timeout: 30000 });
    // overflow check: nothing may spill outside the slide
    const over = await p.evaluate(() => { const s = document.querySelector('.slide'); return s.scrollHeight > s.clientHeight + 2 || s.scrollWidth > s.clientWidth + 2; });
    if (over) errs.push(`slide ${i + 1}: text overflows the slide; shorten it`);
    await p.screenshot({ path: path.join(out, `slide-${i + 1}.jpg`), type: 'jpeg', quality: 92 });
  }
  await b.close();
  if (errs.length) { console.error(errs.join('\n')); process.exit(3); }
  console.log(`rendered ${deck.slides.length} slides to ${out}`);
})();
