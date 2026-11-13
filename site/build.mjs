// SaveSort site builder. No dependencies: run `node site/build.mjs` from the repo root.
// It wraps every file in site/src/pages and site/src/blog in the shared header/footer and writes the
// finished pages to site/public (which is what Cloudflare serves). It also writes the blog index,
// sitemap.xml and feed.xml from the blog posts' details, so those never go out of date.
// The built files are committed: after changing anything in site/src, run the build and commit both.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.dirname(fileURLToPath(import.meta.url));
const SRC = path.join(ROOT, "src"), OUT = path.join(ROOT, "public");
const SITE = "https://savesortai.com";
const EMAIL = "eddieleafe3@gmail.com";
const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const niceDate = d => new Date(d + "T00:00:00Z").toLocaleDateString("en-AU", { day: "numeric", month: "long", year: "numeric", timeZone: "UTC" });

// Each source file starts with one comment holding its details as JSON: <!--{ "path": "/about", "title": "…", … }-->
function load(file) {
  const raw = fs.readFileSync(file, "utf8");
  const m = raw.match(/^<!--(\{[\s\S]*?\})-->\s*/);
  if (!m) throw new Error(file + ": missing the <!--{…}--> details comment on the first line");
  let meta; try { meta = JSON.parse(m[1]); } catch (e) { throw new Error(file + ": details comment isn't valid JSON (" + e.message + ")"); }
  let body = raw.slice(m[0].length), head = "";
  body = body.replace(/<!--head-->([\s\S]*?)<!--\/head-->\s*/, (_, h) => { head = h.trim(); return ""; });
  for (const k of ["title", "description"]) if (!meta[k]) throw new Error(file + ": needs \"" + k + "\"");
  // SEO rules the build enforces (search results cut off anything longer)
  if (!meta.noindex && meta.title.length > 60) throw new Error(file + ": title is " + meta.title.length + " characters; keep it to 60 or fewer");
  if (!meta.noindex && (meta.description.length < 70 || meta.description.length > 160)) throw new Error(file + ": description is " + meta.description.length + " characters; keep it between 70 and 160");
  if (!meta.noindex && (body.match(/<h1[\s>]/g) || []).length > 1) throw new Error(file + ": more than one <h1>");
  if (/<img(?![^>]*\balt=)/.test(body)) throw new Error(file + ": every <img> needs alt text");
  return { meta, body, head, file };
}

const ICONS = `<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <symbol id="i-ribbon" viewBox="0 0 22 26"><path d="M2 4a2 2 0 012-2h14a2 2 0 012 2v20l-9-6.5L2 24z" fill="currentColor"/></symbol>
  <symbol id="i-check" viewBox="0 0 20 20"><path d="M4 10.5l4 4 8-9" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></symbol>
  <symbol id="i-x" viewBox="0 0 20 20"><path d="M5 5l10 10M15 5L5 15" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></symbol>
  <symbol id="i-lock" viewBox="0 0 20 20"><rect x="4" y="9" width="12" height="9" rx="2" fill="currentColor"/><path d="M7 9V6.5a3 3 0 016 0V9" fill="none" stroke="currentColor" stroke-width="2"/></symbol>
  <symbol id="i-shield" viewBox="0 0 20 20"><path d="M10 2l7 3v5c0 4-3 7-7 8-4-1-7-4-7-8V5z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M7 10l2 2 4-4" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></symbol>
  <symbol id="i-menu" viewBox="0 0 20 20"><path d="M3 6h14M3 10h14M3 14h14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></symbol>
</svg>`;

// Sorty, the mascot from the reels (same shapes as engine/mascot.js, drawn still).
export const SORTY = `<svg class="sorty" viewBox="-40 -10 280 290" role="img" aria-label="Sorty, the SaveSort bookmark mascot">
  <defs><linearGradient id="sortyBody" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4C5CFF"/><stop offset="1" stop-color="#2433D0"/></linearGradient></defs>
  <path d="M30 150 Q0 165 -14 196" stroke="#1C27A8" stroke-width="13" fill="none" stroke-linecap="round"/><circle cx="-14" cy="198" r="13" fill="#FFE14A" stroke="#1C27A8" stroke-width="5"/>
  <g class="arm-wave"><path d="M170 150 Q204 140 216 108" stroke="#1C27A8" stroke-width="13" fill="none" stroke-linecap="round"/><circle cx="217" cy="104" r="13" fill="#FFE14A" stroke="#1C27A8" stroke-width="5"/></g>
  <path d="M24 22 Q24 6 40 6 H160 Q176 6 176 22 V252 L100 204 L24 252 Z" fill="url(#sortyBody)" stroke="#1C27A8" stroke-width="6" stroke-linejoin="round"/>
  <ellipse cx="58" cy="36" rx="20" ry="9" fill="#fff" opacity=".22" transform="rotate(-18 58 36)"/>
  <circle cx="50" cy="130" r="12" fill="#FF8FA3" opacity=".45"/><circle cx="150" cy="130" r="12" fill="#FF8FA3" opacity=".45"/>
  <g class="eyes"><ellipse cx="72" cy="92" rx="23" ry="27" fill="#fff" stroke="#10121C" stroke-width="4"/><circle cx="74" cy="96" r="11" fill="#10121C"/><circle cx="78" cy="91" r="3.5" fill="#fff"/>
  <ellipse cx="128" cy="92" rx="23" ry="27" fill="#fff" stroke="#10121C" stroke-width="4"/><circle cx="130" cy="96" r="11" fill="#10121C"/><circle cx="134" cy="91" r="3.5" fill="#fff"/></g>
  <path d="M54 54 Q72 45 90 52M110 52 Q128 45 146 54" stroke="#10121C" stroke-width="8" stroke-linecap="round" fill="none"/>
  <path d="M78 150 Q100 174 122 150" stroke="#10121C" stroke-width="7" stroke-linecap="round" fill="none"/>
</svg>`;

const NAV = [["/#how", "How it works"], ["/#pricing", "Pricing"], ["/blog/", "Blog"], ["/about", "About"]];

function layout({ meta, body, head }, posts) {
  const url = SITE + meta.path;
  const og = meta.ogTitle || meta.title;
  const cur = href => (href === meta.path || (href === "/blog/" && meta.path.startsWith("/blog/")) ? ' aria-current="page"' : "");
  const links = NAV.map(([h, t]) => `<li><a href="${h}"${cur(h)}>${t}</a></li>`).join("");
  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>${esc(meta.title)}</title>
<meta name="description" content="${esc(meta.description)}">
<link rel="canonical" href="${url}">
<meta name="robots" content="${meta.noindex ? "noindex" : "index, follow, max-image-preview:large"}">
<meta name="theme-color" content="#FFFFFF">
<meta name="color-scheme" content="light">
<meta property="og:type" content="${meta.type === "post" ? "article" : "website"}">
<meta property="og:site_name" content="SaveSort">
<meta property="og:url" content="${url}">
<meta property="og:title" content="${esc(og)}">
<meta property="og:description" content="${esc(meta.ogDescription || meta.description)}">
<meta property="og:image" content="${SITE}/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="SaveSort: You saved 156 reels. Here are the 30 worth doing.">
<meta property="og:locale" content="en_AU">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="${esc(og)}">
<meta name="twitter:description" content="${esc(meta.ogDescription || meta.description)}">
<meta name="twitter:image" content="${SITE}/og.png">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 22 26'%3E%3Cpath d='M2 4a2 2 0 012-2h14a2 2 0 012 2v20l-9-6.5L2 24z' fill='%234C5CFF'/%3E%3C/svg%3E">
<link rel="alternate" type="application/rss+xml" title="SaveSort blog" href="/feed.xml">
<link rel="preload" href="/fonts/bricolage-grotesque.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/figtree.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/site.css">
${head}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
${ICONS}
<header class="nav">
  <div class="wrap">
    <a class="logo" href="/" aria-label="SaveSort home"><svg aria-hidden="true"><use href="#i-ribbon"/></svg>SaveSort</a>
    <ul class="nav-links">${links}</ul>
    <a class="btn btn-primary btn-s" href="/#try">Sort my saves<span class="sr"> free</span></a>
    <details class="menu">
      <summary aria-label="Menu"><svg aria-hidden="true"><use href="#i-menu"/></svg></summary>
      <ul>${links}<li><a href="/#faq">FAQ</a></li></ul>
    </details>
  </div>
</header>
<main id="main">
${body.trim()}
</main>
<footer class="foot">
  <div class="wrap">
    <div class="cols">
      <div class="brand">
        <a class="logo" href="/"><svg aria-hidden="true"><use href="#i-ribbon"/></svg>SaveSort</a>
        <p>Sorts your saved Instagram reels in your browser. Your file is never uploaded.</p>
      </div>
      <div>
        <h2>Product</h2>
        <ul><li><a href="/#try">Sort my saves</a></li><li><a href="/#how">How it works</a></li><li><a href="/#breakdowns">Pro breakdowns</a></li><li><a href="/#pricing">Pricing</a></li><li><a href="/#faq">FAQ</a></li></ul>
      </div>
      <div>
        <h2>Guides</h2>
        <ul>${posts.slice(0, 4).map(p => `<li><a href="${p.meta.path}">${esc(p.meta.short || p.meta.h1)}</a></li>`).join("")}<li><a href="/blog/">All guides</a></li></ul>
      </div>
      <div>
        <h2>Company</h2>
        <ul><li><a href="/about">About</a></li><li><a href="mailto:${EMAIL}">Contact</a></li><li><a href="/privacy">Privacy</a></li><li><a href="/terms">Terms</a></li><li><a href="/refunds">Refunds</a></li></ul>
      </div>
    </div>
    <div class="base"><span>© 2026 SaveSort. All rights reserved.</span><span>Not affiliated with Instagram or Meta.</span></div>
  </div>
</footer>
${(meta.scripts || []).map(s => `<script src="${s}"></script>`).join("\n")}
<script>
document.addEventListener("click",e=>{const m=document.querySelector(".menu");if(m&&m.open&&(!m.contains(e.target)||e.target.closest("a")))m.open=false});
// Numbers count up once when they come into view. Skipped for people who ask for reduced motion.
(function(){
  if(!("IntersectionObserver" in window)||matchMedia("(prefers-reduced-motion: reduce)").matches)return;
  const count=el=>{const to=+el.dataset.count,t0=performance.now(),d=1100;const tick=t=>{const k=Math.min(1,(t-t0)/d);el.textContent=Math.round(to*(1-Math.pow(1-k,3)));if(k<1)requestAnimationFrame(tick)};requestAnimationFrame(tick)};
  const io=new IntersectionObserver(es=>es.forEach(e=>{if(!e.isIntersecting)return;io.unobserve(e.target);count(e.target)}),{rootMargin:"0px 0px -8% 0px"});
  document.querySelectorAll("[data-count]").forEach(el=>io.observe(el));
})();
</script>
</body>
</html>
`;
}

const ld = o => `<script type="application/ld+json">${JSON.stringify(o)}</script>`;
const ORG = { "@type": "Organization", "@id": SITE + "/#org", name: "SaveSort", url: SITE + "/", logo: SITE + "/og.png" };

function postCard(p) {
  return `<li><a class="post-card" href="${p.meta.path}"><h3>${esc(p.meta.h1)}</h3><p>${esc(p.meta.description)}</p><span class="meta">${niceDate(p.meta.date)}, ${p.meta.readMins} min read</span></a></li>`;
}

function postPage(p) {
  const m = p.meta, url = SITE + m.path;
  p.head = ld({ "@context": "https://schema.org", "@graph": [
    { "@type": "BlogPosting", "@id": url + "#post", headline: m.h1, description: m.description, datePublished: m.date, dateModified: m.updated || m.date,
      mainEntityOfPage: url, image: SITE + "/og.png", inLanguage: "en", author: ORG, publisher: ORG },
    { "@type": "BreadcrumbList", itemListElement: [
      { "@type": "ListItem", position: 1, name: "SaveSort", item: SITE + "/" },
      { "@type": "ListItem", position: 2, name: "Blog", item: SITE + "/blog/" },
      { "@type": "ListItem", position: 3, name: m.h1, item: url } ] },
    // Optional "faq": [[question, answer], ...] in a post's details. It's shown on the page AND sent as FAQ data,
    // from the same text, so what search engines and AI tools read always matches what people see.
    ...(m.faq && m.faq.length ? [{ "@type": "FAQPage", "@id": url + "#faq", mainEntity: m.faq.map(([q, a]) =>
      ({ "@type": "Question", name: q, acceptedAnswer: { "@type": "Answer", text: a } })) }] : []) ] });
  // Optional "answer": one or two plain sentences that answer the post's question directly, shown first.
  // Search engines and AI assistants quote this kind of short, self-contained answer.
  const answer = m.answer ? `<p class="note answer"><strong>Short answer:</strong> ${esc(m.answer)}</p>\n` : "";
  const faq = m.faq && m.faq.length ? `<h2 id="faq">Questions</h2>\n<div class="faq">${m.faq.map(([q, a]) =>
    `<details><summary>${esc(q)}</summary><p>${esc(a)}</p></details>`).join("")}</div>\n` : "";
  p.body = `<article>
  <header class="page-head"><div class="wrap narrow">
    <ol class="crumbs"><li><a href="/">SaveSort</a></li><li><a href="/blog/">Blog</a></li></ol>
    <h1>${esc(m.h1)}</h1>
    <p class="lede">${esc(m.description)}</p>
    <p class="byline">By the SaveSort team. ${m.updated && m.updated !== m.date ? "Updated " + niceDate(m.updated) : niceDate(m.date)}, ${m.readMins} min read.</p>
  </div></header>
  <div class="wrap narrow prose">
${answer}${p.body.trim()}
${faq}    <aside class="cta-box"><div><h2>Sort your own saves, free</h2><p>Drop in the file Instagram emails you. It's sorted in your browser and never uploaded.</p></div><a class="btn btn-light" href="/#try">Sort my saves free</a></aside>
  </div>
</article>`;
  return p;
}

function build() {
  const read = dir => fs.readdirSync(path.join(SRC, dir)).filter(f => f.endsWith(".html")).sort().map(f => load(path.join(SRC, dir, f)));
  const posts = read("blog").map(p => {
    const slug = path.basename(p.file, ".html");
    for (const k of ["h1", "date", "readMins"]) if (!p.meta[k]) throw new Error(p.file + ": needs \"" + k + "\"");
    Object.assign(p.meta, { path: "/blog/" + slug, type: "post" });
    return p;
  }).sort((a, b) => b.meta.date.localeCompare(a.meta.date) || a.meta.path.localeCompare(b.meta.path));
  const pages = read("pages");
  const latest = posts.map(p => (p.meta.updated || p.meta.date)).sort().pop();

  // blog index
  pages.push({ meta: { path: "/blog/", title: "SaveSort blog: guides for your Instagram saved posts", updated: latest,
      description: "Plain guides on organising your Instagram saved posts, downloading your saves, and telling useful reels from hype." },
    head: ld({ "@context": "https://schema.org", "@type": "Blog", "@id": SITE + "/blog/#blog", name: "SaveSort blog", url: SITE + "/blog/", publisher: ORG,
      blogPost: posts.map(p => ({ "@type": "BlogPosting", headline: p.meta.h1, url: SITE + p.meta.path, datePublished: p.meta.date })) }),
    body: `<header class="page-head"><div class="wrap">
    <h1>Guides for people with a full Saved tab</h1>
    <p class="lede">How to organise your Instagram saves, get them out of the app, and tell a useful reel from a hyped one. Written from what we found sorting our sample report: 156 real saved reels.</p>
  </div></header>
  <section class="band tight"><div class="wrap"><ul class="posts two">${posts.map(postCard).join("")}</ul></div></section>` });

  const titles = new Map();
  for (const p of [...pages, ...posts]) { if (titles.has(p.meta.title)) throw new Error(`${p.file || p.meta.path}: same title as ${titles.get(p.meta.title)}; every page needs its own`); titles.set(p.meta.title, p.file || p.meta.path); }
  for (const p of posts) {
    if (!/href="\/#try"/.test(p.body) && !/href="\/"/.test(p.body)) throw new Error(p.file + ": link to the sorter (/#try) somewhere in the post");
    if (!/href="\/blog\/[a-z0-9-]+"/.test(p.body)) throw new Error(p.file + ": link to at least one other blog post");
  }
  const all = [...pages, ...posts.map(postPage)];
  for (const p of all) {
    p.body = p.body.replace("<!--POSTS-->", posts.slice(0, 3).map(postCard).join("")).replaceAll("<!--SORTY-->", SORTY).replaceAll("{{EMAIL}}", EMAIL);
    if (p.meta.updated) p.body = p.body.replaceAll("{{UPDATED}}", niceDate(p.meta.updated));
    const rel = p.meta.path === "/" ? "index.html" : p.meta.path.endsWith("/") ? p.meta.path.slice(1) + "index.html" : p.meta.path.slice(1) + ".html";
    const out = path.join(OUT, rel);
    fs.mkdirSync(path.dirname(out), { recursive: true });
    fs.writeFileSync(out, layout(p, posts));
  }

  // sitemap: every public page, short addresses (/terms not /terms.html)
  const listed = all.filter(p => !p.meta.noindex).sort((a, b) => a.meta.path.localeCompare(b.meta.path));
  for (const p of listed) if (!p.meta.updated && !p.meta.date) throw new Error(p.file + ": needs \"updated\" (YYYY-MM-DD) for the sitemap");
  fs.writeFileSync(path.join(OUT, "sitemap.xml"), `<?xml version="1.0" encoding="UTF-8"?>
<!-- Written by site/build.mjs. Don't edit by hand. -->
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${listed.map(p => `  <url><loc>${SITE}${p.meta.path}</loc><lastmod>${p.meta.updated || p.meta.date}</lastmod></url>`).join("\n")}
</urlset>
`);

  // RSS feed of the blog
  fs.writeFileSync(path.join(OUT, "feed.xml"), `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel>
<title>SaveSort blog</title><link>${SITE}/blog/</link><description>Guides for your Instagram saved posts.</description><language>en</language>
<atom:link href="${SITE}/feed.xml" rel="self" type="application/rss+xml"/>
${posts.map(p => `<item><title>${esc(p.meta.h1)}</title><link>${SITE}${p.meta.path}</link><guid>${SITE}${p.meta.path}</guid><pubDate>${new Date(p.meta.date + "T00:00:00Z").toUTCString()}</pubDate><description>${esc(p.meta.description)}</description></item>`).join("\n")}
</channel></rss>
`);
  console.log(`Built ${all.length} pages (${posts.length} blog posts) into site/public`);
}
build();
