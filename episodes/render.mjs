// Render an episode: node render.mjs ep01  ->  out/ep01.mp4
// Uses the episode's JSON script in this folder. Set CHROME=/path/to/chrome to use a local Chrome.
import fs from 'node:fs';
import path from 'node:path';
import {bundle} from '@remotion/bundler';
import {renderMedia, selectComposition} from '@remotion/renderer';

const id = process.argv[2] || 'ep01';
const here = path.dirname(new URL(import.meta.url).pathname);
const props = JSON.parse(fs.readFileSync(path.join(here, `${id}.json`), 'utf8'));
const browserExecutable = process.env.CHROME || (fs.existsSync('/usr/bin/google-chrome') ? '/usr/bin/google-chrome' : null);

const serveUrl = await bundle({entryPoint: path.join(here, 'src/index.ts')});
const composition = await selectComposition({serveUrl, id: 'Episode', inputProps: props, browserExecutable});
fs.mkdirSync(path.join(here, 'out'), {recursive: true});
const outputLocation = path.join(here, 'out', `${id}.mp4`);
await renderMedia({
	composition,
	serveUrl,
	codec: 'h264',
	crf: 20,
	inputProps: props,
	outputLocation,
	browserExecutable,
	onProgress: ({progress}) => { const p = Math.round(progress * 100); if (p % 10 === 0 && p !== globalThis.__last) { globalThis.__last = p; console.log(`${id}: ${p}%`); } },
});
console.log(`\nDone: ${outputLocation}`);
