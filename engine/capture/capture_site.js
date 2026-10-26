// node capture_site.js <site.html> <fontsDir> <outDir>
// Phone-size screenshots of the real SaveSort site for "screen" scenes: hero, drop zone, and the sorted report
// under each filter (tall images the stage pans through like a screen recording). Caption text from other
// creators' reels is blurred so only SaveSort's own labels are readable.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const [site, fontsDir, out, savedFile] = process.argv.slice(2);
  fs.mkdirSync(out, { recursive: true });
  const f = n => 'file://' + path.resolve(fontsDir, n);
  const css = `@font-face{font-family:Archivo;src:url("${f('Archivo[wdth,wght].ttf')}");font-weight:100 900;font-stretch:62% 125%}
@font-face{font-family:"Instrument Sans";src:url("${f('InstrumentSans[wdth,wght].ttf')}");font-weight:400 700;font-stretch:75% 100%}
@font-face{font-family:"JetBrains Mono";src:url("${f('JetBrainsMono[wght].ttf')}");font-weight:100 800}`;
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, reducedMotion: 'reduce' });
  const p = await ctx.newPage();
  await p.route('https://fonts.googleapis.com/**', r => r.fulfill({ contentType: 'text/css', body: css }));
  await p.route('https://fonts.gstatic.com/**', r => r.abort());
  await p.route('https://cdnjs.cloudflare.com/**', r => r.fulfill({ contentType: 'text/javascript', body: '' }));
  await p.goto('file://' + path.resolve(site));
  await p.evaluate(() => document.fonts.ready);
  await p.addStyleTag({ content: '#r-items .item p{filter:blur(5px)} .nav{position:static!important} *{scroll-behavior:auto!important}' });
  await p.waitForTimeout(800);
  const shot = async (name, opts = {}) => { await p.screenshot({ path: path.join(out, name), ...opts }); console.log('shot', name); };
  await shot('hero.png');
  // drop zone
  await p.evaluate(() => { const e = document.getElementById('try'); window.scrollTo(0, e.offsetTop - 10); });
  await p.waitForTimeout(300);
  await shot('drop.png');
  const dz = await p.evaluate(() => { const r = document.getElementById('drop').getBoundingClientRect(); return { x: r.x, y: r.y, w: r.width, h: r.height }; });
  // sorted report
  if (savedFile) await p.setInputFiles('#file', savedFile);  // the real flow: choose your own saved-posts file
  else await p.evaluate(() => { buildReport(SAMPLE.map(([caption, url]) => ({ caption, url, user: '' })), false); });
  await p.waitForSelector('#report:not([hidden])'); await p.waitForTimeout(600);
  const tall = async (name) => {
    const top = await p.evaluate(() => document.getElementById('report').getBoundingClientRect().top + window.scrollY - 12);
    const h = await p.evaluate(() => document.getElementById('report').offsetHeight + 24);
    await shot(name, { fullPage: true, clip: { x: 0, y: top, width: 390, height: Math.min(h, 6000) } });
    return { top, h };
  };
  const meta = { dropzone: dz };
  meta.report = await tall('report-all.png');
  const pos = await p.evaluate(() => {
    const top = document.getElementById('report').getBoundingClientRect().top + window.scrollY - 12;
    const q = s => { const r = document.querySelector(s).getBoundingClientRect(); return { x: r.x + r.width / 2, y: r.y + window.scrollY - top + r.height / 2 }; };
    return { stats: q('#r-stats'), topics: q('#r-topics'), go: q('.chip[data-l="go"]'), warn: q('.chip[data-l="warn"]'), gate: q('.chip[data-l="gate"]'), items: q('#r-items') };
  });
  meta.pos = pos;
  for (const k of ['go', 'warn', 'gate']) {
    await p.click(`.chip[data-l="${k}"]`);
    await p.waitForTimeout(250);
    meta['report_' + k] = await tall(`report-${k}.png`);
  }
  // stats numbers for the narration
  meta.stats = await p.evaluate(() => [...document.querySelectorAll('#r-stats .rstat')].map(e => e.innerText.replace(/\n/g, ' ')));
  meta.chips = await p.evaluate(() => [...document.querySelectorAll('#r-filters .chip')].map(e => e.innerText));
  fs.writeFileSync(path.join(out, 'meta.json'), JSON.stringify(meta, null, 1));
  await b.close();
})();
