// Exercise the Slides player's actual seek function without an LMS or media playback.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const template = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../templates/learner_features.js');
const source = fs.readFileSync(template, 'utf8');
const functionSource = source.match(/function alignVideo\(seek\) \{[\s\S]*?\n\}/)?.[0];
assert.ok(functionSource, 'Slides player must define alignVideo');

const video = {duration: 8, loop: true, currentTime: 0, playbackRate: 1};
const audioPlayer = {currentTime: 22.5, playbackRate: 1.25};
const document = {querySelector: () => video};
const alignVideo = new Function('document', 'audioPlayer', `${functionSource}\nreturn alignVideo;`)(document, audioPlayer);

alignVideo(true);
assert.equal(video.currentTime, 6.5, 'A seek into narration maps into the matching loop cycle');
assert.equal(video.playbackRate, 1.25, 'The visual follows narration playback speed');

audioPlayer.currentTime = 5;
alignVideo(true);
assert.equal(video.currentTime, 5, 'A seek within the first loop keeps its position');

video.loop = false;
audioPlayer.currentTime = 22.5;
alignVideo(true);
assert.ok(Math.abs(video.currentTime - (8 - 1 / 60)) < 0.001,
  'A non-looping video stays on its final frame');

console.log('PASS: looping and finite video seek behavior');
