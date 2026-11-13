import React from 'react';
import {
	AbsoluteFill,
	Audio,
	Img,
	OffthreadVideo,
	Sequence,
	interpolate,
	random,
	spring,
	staticFile,
	useCurrentFrame,
	useVideoConfig,
} from 'remotion';
import {loadFont} from '@remotion/fonts';

loadFont({family: 'Bricolage', url: staticFile('fonts/bricolage-grotesque.woff2'), weight: '200 800'});
const FONT = 'Bricolage, Inter, sans-serif';

export type Sfx = string | {k: string; at?: number};
export type Shot = {
	n: number;
	start: number;
	end: number;
	kind?: 'black';
	src?: string | null; // public/ path to a .png/.jpg frame or .mp4 clip; empty = storyboard card
	text?: string; // big text on a black shot
	big?: string; // big joke text over the picture (e.g. a joke number)
	camera?: 'push' | 'crash' | 'shake' | 'whip' | 'pan' | 'tilt' | 'wobble' | 'none';
	line?: string; // Sorty's line; *words* are highlighted
	voice?: string; // public/ path to the voice line audio
	card?: string; // a saved-reel card shown over the shot
	stamp?: 'do' | 'watch' | 'skip' | 'locked';
	stampAt?: number;
	sfx?: Sfx[];
	make?: string;
	picture?: string;
	real?: boolean;
};
export type EpisodeProps = {
	id: string;
	title: string;
	fps: number;
	music?: {src: string; volume?: number; duck?: number};
	hits?: number[];
	shots: Shot[];
	end: {start: number; end: number; line: string; url: string; sub: string; voice?: string};
};

// The four real SaveSort labels (site names, owner 11 Nov 2026).
const STAMPS = {
	do: {text: 'DO IT', color: '#2BD18B'},
	watch: {text: 'WATCH IT', color: '#5B9BFF'},
	skip: {text: 'SKIP IT', color: '#FF5A4E'},
	locked: {text: 'LOCKED', color: '#F2C45B'},
};

const Highlight: React.FC<{text: string}> = ({text}) => (
	<>
		{text.split(/(\*[^*]+\*)/g).map((part, i) =>
			part.startsWith('*') ? (
				<span key={i} style={{color: '#FFD23F'}}>
					{part.slice(1, -1)}
				</span>
			) : (
				<span key={i}>{part}</span>
			),
		)}
	</>
);

const Camera: React.FC<{mode: Shot['camera']; seed: number; children: React.ReactNode}> = ({mode, seed, children}) => {
	const f = useCurrentFrame();
	const {fps, durationInFrames} = useVideoConfig();
	const p = f / Math.max(1, durationInFrames - 1);
	let scale = 1.04;
	let x = 0;
	let y = 0;
	let rot = 0;
	if (mode === 'push') scale = interpolate(p, [0, 1], [1.02, 1.14]);
	if (mode === 'crash') scale = interpolate(f, [0, 5], [1.6, 1.08], {extrapolateRight: 'clamp'}) + p * 0.04;
	if (mode === 'pan') x = interpolate(p, [0, 1], [-50, 50]);
	if (mode === 'tilt') y = interpolate(p, [0, 1], [70, -40]);
	if (mode === 'whip') x = interpolate(f, [0, 5], [1080, 0], {extrapolateRight: 'clamp'});
	if (mode === 'wobble') rot = Math.sin(f / 3) * 1.6;
	if (mode === 'shake' || mode === 'crash') {
		const amp = interpolate(f, [0, 0.35 * fps], [26, 0], {extrapolateRight: 'clamp'});
		x += (random(`x${seed}${f}`) - 0.5) * amp;
		y += (random(`y${seed}${f}`) - 0.5) * amp;
	}
	return (
		<AbsoluteFill style={{transform: `translate(${x}px, ${y}px) scale(${scale}) rotate(${rot}deg)`}}>{children}</AbsoluteFill>
	);
};

const StoryboardCard: React.FC<{shot: Shot}> = ({shot}) => (
	<AbsoluteFill
		style={{
			background: shot.real ? '#0E1F17' : '#16193A',
			color: '#E9ECFF',
			fontFamily: FONT,
			padding: 90,
			justifyContent: 'center',
			gap: 30,
		}}
	>
		<div style={{fontSize: 34, letterSpacing: 4, opacity: 0.6, fontWeight: 700}}>
			SHOT {shot.n} · {shot.make?.toUpperCase()}
		</div>
		<div style={{fontSize: 64, fontWeight: 700, lineHeight: 1.15}}>{shot.picture}</div>
		{shot.real ? <div style={{fontSize: 34, color: '#2BD18B', fontWeight: 700}}>REAL SCREEN (proof)</div> : null}
	</AbsoluteFill>
);

const Picture: React.FC<{shot: Shot}> = ({shot}) => {
	if (shot.kind === 'black')
		return (
			<AbsoluteFill style={{background: '#000', alignItems: 'center', justifyContent: 'center'}}>
				<div style={{color: '#fff', fontFamily: FONT, fontSize: 230, fontWeight: 300}}>{shot.text}</div>
			</AbsoluteFill>
		);
	if (!shot.src) return <StoryboardCard shot={shot} />;
	const src = staticFile(shot.src);
	return /\.(mp4|mov|webm)$/i.test(shot.src) ? (
		<OffthreadVideo src={src} muted style={{width: '100%', height: '100%', objectFit: 'cover'}} />
	) : (
		<Img src={src} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
	);
};

const Line: React.FC<{text: string; y?: number}> = ({text, y = 1260}) => {
	const f = useCurrentFrame();
	const {fps} = useVideoConfig();
	const s = spring({frame: f, fps, config: {damping: 12, mass: 0.6}});
	return (
		<div
			style={{
				position: 'absolute',
				left: 70,
				right: 70,
				top: y,
				textAlign: 'center',
				fontFamily: FONT,
				fontWeight: 800,
				fontSize: 84,
				lineHeight: 1.08,
				color: '#fff',
				WebkitTextStroke: '10px #000',
				paintOrder: 'stroke fill',
				textShadow: '0 8px 0 rgba(0,0,0,.45)',
				transform: `scale(${interpolate(s, [0, 1], [0.6, 1])})`,
				opacity: s,
			}}
		>
			<Highlight text={text} />
		</div>
	);
};

const Card: React.FC<{text: string}> = ({text}) => {
	const f = useCurrentFrame();
	const {fps} = useVideoConfig();
	const s = spring({frame: f, fps, config: {damping: 14}});
	return (
		<div
			style={{
				position: 'absolute',
				left: 110,
				right: 110,
				top: 470,
				background: '#fff',
				borderRadius: 36,
				padding: '46px 50px',
				fontFamily: FONT,
				boxShadow: '0 30px 80px rgba(0,0,0,.45)',
				transform: `translateY(${interpolate(s, [0, 1], [500, 0])}px) rotate(-2deg)`,
			}}
		>
			<div style={{fontSize: 30, letterSpacing: 3, color: '#888', fontWeight: 700}}>SAVED REEL SAYS</div>
			<div style={{fontSize: 70, color: '#111', fontWeight: 800, lineHeight: 1.1, marginTop: 14}}>{text}</div>
		</div>
	);
};

const Stamp: React.FC<{kind: keyof typeof STAMPS}> = ({kind}) => {
	const f = useCurrentFrame();
	const {fps} = useVideoConfig();
	const p = interpolate(f, [0, 0.18 * fps], [0, 1], {extrapolateRight: 'clamp'});
	const st = STAMPS[kind];
	return (
		<div style={{position: 'absolute', top: 760, left: 0, right: 0, textAlign: 'center'}}>
			<span
				style={{
					display: 'inline-block',
					fontFamily: FONT,
					fontWeight: 800,
					fontSize: 150,
					color: st.color,
					border: `16px solid ${st.color}`,
					borderRadius: 30,
					padding: '4px 44px',
					background: 'rgba(0,0,0,.25)',
					transform: `rotate(-8deg) scale(${interpolate(p, [0, 1], [2.6, 1])})`,
					opacity: p > 0 ? 1 : 0,
				}}
			>
				{st.text}
			</span>
		</div>
	);
};

const BigText: React.FC<{text: string}> = ({text}) => {
	const f = useCurrentFrame();
	const {fps} = useVideoConfig();
	const s = spring({frame: f - 4, fps, config: {damping: 8}});
	return (
		<div
			style={{
				position: 'absolute',
				top: 640,
				left: 0,
				right: 0,
				textAlign: 'center',
				fontFamily: FONT,
				fontWeight: 800,
				fontSize: 120,
				color: '#FF5A4E',
				WebkitTextStroke: '12px #fff',
				paintOrder: 'stroke fill',
				transform: `scale(${s}) rotate(-4deg)`,
			}}
		>
			{text}
		</div>
	);
};

const EndCard: React.FC<{end: EpisodeProps['end']}> = ({end}) => {
	const f = useCurrentFrame();
	const {fps} = useVideoConfig();
	const s = spring({frame: f, fps, config: {damping: 10}});
	return (
		<AbsoluteFill style={{background: '#2433E8', alignItems: 'center', justifyContent: 'center', fontFamily: FONT, color: '#fff'}}>
			<div style={{fontSize: 92, fontWeight: 800, textAlign: 'center', transform: `scale(${s})`, padding: '0 60px'}}>
				<Highlight text={end.line} />
			</div>
			<div style={{fontSize: 110, fontWeight: 800, marginTop: 70}}>{end.url}</div>
			<div style={{fontSize: 48, fontWeight: 600, marginTop: 16, opacity: 0.85}}>{end.sub}</div>
		</AbsoluteFill>
	);
};

const sfxFile = (k: string, i: number) => staticFile(`sfx/${k.replace(':', '-')}-${(i % 3) + 1}.wav`);

export const Episode: React.FC<EpisodeProps> = ({shots, end, music}) => {
	const {fps} = useVideoConfig();
	const sec = (s: number) => Math.round(s * fps);
	const talking = shots.filter((s) => s.line).map((s) => [s.start, s.end]).concat([[end.start, end.end]]);
	return (
		<AbsoluteFill style={{background: '#000'}}>
			{music ? (
				<Audio
					src={staticFile(music.src)}
					volume={(f) => {
						const t = f / fps;
						const duck = talking.some(([a, b]) => t >= a && t < b);
						return duck ? music.duck ?? 0.2 : music.volume ?? 0.5;
					}}
				/>
			) : null}
			{shots.map((shot, i) => (
				<Sequence key={shot.n} name={`Shot ${shot.n}`} from={sec(shot.start)} durationInFrames={sec(shot.end) - sec(shot.start)}>
					<Camera mode={shot.camera} seed={shot.n}>
						<Picture shot={shot} />
						{shot.big ? <BigText text={shot.big} /> : null}
						{shot.card ? <Card text={shot.card} /> : null}
					</Camera>
					{shot.stamp ? (
						<Sequence from={sec(shot.stampAt ?? 0)}>
							<Stamp kind={shot.stamp} />
						</Sequence>
					) : null}
					{shot.line ? <Line text={shot.line} /> : null}
					{shot.voice ? <Audio src={staticFile(shot.voice)} /> : null}
					{(shot.sfx ?? []).map((s, j) => {
						const k = typeof s === 'string' ? s : s.k;
						const at = typeof s === 'string' ? 0 : s.at ?? 0;
						return (
							<Sequence key={j} from={sec(at)}>
								<Audio src={sfxFile(k, i + j)} volume={0.8} />
							</Sequence>
						);
					})}
				</Sequence>
			))}
			<Sequence name="End card" from={sec(end.start)} durationInFrames={sec(end.end) - sec(end.start)}>
				<EndCard end={end} />
				<Audio src={sfxFile('end', 0)} volume={0.8} />
				{end.voice ? <Audio src={staticFile(end.voice)} /> : null}
			</Sequence>
		</AbsoluteFill>
	);
};
