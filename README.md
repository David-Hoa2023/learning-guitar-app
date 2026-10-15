# Learning Guitar App

A phone app idea that listens to music and turns it into lessons: chords and tabs first, then rhythm, technique, theory, ear training, and a learn-to-dance module.

## Try the dance trainer
`index.html` is the Bachata Basic Trainer. Open the GitHub Pages link for this repo on your phone. It plays an 8-count with fixed left and right feet, leader and follower views, counts 1 to 4 and 5 to 8 practice, uploaded audio files, and YouTube videos with tempo from your microphone or by tapping.

- YouTube plays through the official embedded player. The page never reads the video's audio.
- Tempo detection and file analysis run in your browser. Nothing is uploaded.
- Spotify links cannot play inside the page and use tap-along mode.
- Counting starts only after you mark the song's count 1 (or tap the beat). Mark count 1 again a few bars later and the tempo is refined from the time between your two marks.

## Contents
- `index.html`: the dance trainer (one file, no build step)
- `plans/`: the guitar app plan and the dance module mapping
- `tools/`: early Python scripts for chords, notes and tab from audio (needs librosa and basic-pitch)

## Run locally
`python3 -m http.server 8000`, then open http://localhost:8000. Opening the file directly will not work because YouTube and the microphone need a web address.
