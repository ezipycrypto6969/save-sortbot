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
  // The same slideshow as a vertical video (1080x1920) for YouTube Shorts, which only takes video:
  // each slide centred on the account's colour, sliding to the next with a soft whoosh.
  const { spawnSync } = require('child_process');
  const n = deck.slides.length, X = 0.3;
  const durs = deck.slides.map((s, i) => s.secs || (i === 0 ? 2.2 : 3.0));
  const bg = ((deck.theme.main || '#10121C') + '').replace('#', '0x');
  const args = ['-y', '-loglevel', 'error'];
  durs.forEach((d, i) => args.push('-loop', '1', '-t', String(d), '-i', path.join(out, `slide-${i + 1}.jpg`)));
  args.push('-f', 'lavfi', '-t', '0.45', '-i', 'anoisesrc=c=pink:a=0.6,highpass=f=900,lowpass=f=5000,afade=t=in:d=0.15,afade=t=out:st=0.15:d=0.3');
  let f = durs.map((_, i) => `[${i}:v]scale=1080:1350,pad=1080:1920:0:285:color=${bg},setsar=1,fps=30,format=yuv420p[v${i}]`).join(';');
  let last = 'v0', off = 0;
  for (let i = 1; i < n; i++) { off += durs[i - 1] - X; f += `;[${last}][v${i}]xfade=transition=slideleft:duration=${X}:offset=${off.toFixed(2)}[x${i}]`; last = `x${i}`; }
  const total = durs.reduce((a, b) => a + b, 0) - X * (n - 1);
  const sw = [...Array(n - 1).keys()].map(i => durs.slice(0, i + 1).reduce((a, b) => a + b, 0) - X * (i + 1) - 0.08);
  f += `;[${n}:a]volume=0.35,asplit=${n - 1}${sw.map((_, i) => `[s${i}]`).join('')}`;
  sw.forEach((t, i) => { const ms = Math.max(0, Math.round(t * 1000)); f += `;[s${i}]adelay=${ms}|${ms}[d${i}]`; });
  f += `;anullsrc=r=48000:cl=stereo,atrim=0:${total.toFixed(2)}[sil];[sil]${sw.map((_, i) => `[d${i}]`).join('')}amix=inputs=${n}:normalize=0,atrim=0:${total.toFixed(2)}[a]`;
  args.push('-filter_complex', f, '-map', `[${last}]`, '-map', '[a]', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20',
    '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '128k', '-ar', '48000', '-movflags', '+faststart', path.join(out, 'video.mp4'));
  const r = spawnSync('ffmpeg', args, { stdio: 'inherit' });
  if (r.status) { console.error('slideshow video failed'); process.exit(4); }
  console.log(`and video.mp4 (${total.toFixed(1)} s) for YouTube Shorts`);
})();
