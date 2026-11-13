import React from 'react';
import {Composition} from 'remotion';
import {Episode, EpisodeProps} from './Episode';
import ep01 from '../ep01.json';

// One template for every episode: the episode's JSON script decides the shots, timing and length.
// Render another episode with: node render.mjs ep02
export const RemotionRoot: React.FC = () => (
	<Composition
		id="Episode"
		component={Episode}
		fps={30}
		width={1080}
		height={1920}
		durationInFrames={30 * 38}
		defaultProps={ep01 as EpisodeProps}
		calculateMetadata={({props}) => ({
			fps: props.fps,
			durationInFrames: Math.round(props.end.end * props.fps),
		})}
	/>
);
