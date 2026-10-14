# Guitar audio → chords & tabs: plan

**Goal (v1):** a phone app that listens to guitar, either a recorded/imported file or live through the mic, and shows the chords and a playable tab. Rhythm, technique, theory, ear training and sheet reading come later and reuse the same analysis pipeline.

## 1. Recommended stack

| Layer | Choice | Why |
|---|---|---|
| App | **React Native (Expo dev build)**, iOS + Android | One codebase, fast UI iteration, easy to add native audio/ML modules. Flutter is an equal alternative; pick whichever David prefers to read. |
| Live audio | `react-native-audio-api` (low-latency mic buffers) | Gives raw PCM frames for streaming analysis. |
| File import / record | `expo-document-picker`, `expo-audio` | Import mp3/m4a/wav, record takes. |
| On-device ML | **ONNX Runtime Mobile** (`onnxruntime-react-native`) | Runs the same exported models on both platforms; Core ML / NNAPI acceleration. |
| Tab rendering | **alphaTab** (MPL-2.0) in a WebView | Renders guitar tab + standard notation, plays back with cursor sync. Also reads/writes Guitar Pro & MusicXML for the later sheet-reading feature. |
| Research pipeline | Python: librosa, basic-pitch, madmom, mir_eval | Validate accuracy before porting anything to the phone. |

## 2. Chord detection

1. Audio → CQT / chroma features (12 pitch classes, ~10 frames/s).
2. Small CNN (or CRNN) predicts chord per frame: start with **major, minor, 7, maj7, m7, sus2/4, power chords, N (no chord)**, 12 roots.
3. HMM / Viterbi smoothing so chords don't flicker; optional key estimate to break ties.
4. Live mode: 1–2 s sliding window, update every ~200 ms; show the "current chord" plus the last few.

Building blocks: classic chroma + template matching works as a day-one baseline; madmom's deep-chroma + CRF is a strong reference (its pretrained models are **non-commercial**, so use for benchmarking only); train our own small model on GuitarSet (CC BY 4.0) + IDMT-SMT-Guitar for something shippable.

## 3. Audio → tab

1. **Note transcription:** Spotify **Basic Pitch** (Apache-2.0, ~17k-param model, polyphonic, already exportable to ONNX/TFLite) → notes with onset, offset, pitch.
2. **Fret assignment:** each pitch has several (string, fret) options. Choose the path with dynamic programming minimizing hand movement and stretch, biased toward open-position shapes and toward the detected chord's common voicing. Standard tuning first; capo/drop-D as settings.
3. **Quantize** onsets to a beat grid (beat tracker: madmom or BeatNet for research; a lightweight onset/tempo estimator on device) → emit alphaTab/Guitar Pro structure.
4. Later upgrade: a direct guitar-tab model (TabCNN / FretNet-style, trained on GuitarSet) that predicts string+fret, which handles ambiguous positions better than rules.

Honest accuracy expectation: chords on clean strumming are reliable (~80%+ frame accuracy); note-level tabs for single-note lines are decent; dense strumming tabs will be approximate, so the UI should show tabs as "suggested" and let users correct them.

## 4. Where analysis runs

- **Recorded files:** on device for short clips; offer optional cloud processing for long songs or a heavier model.
- **Live playing:** on device only (latency). Chords live in v1; live tab is a stretch goal.
- Start by prototyping the pipeline in Python, then export the chosen models to ONNX for the app.

## 5. MVP scope

**In:** record or import a clip (≤ 3 min) → chord timeline + chord diagrams → suggested tab in alphaTab → playback with synced cursor; live "chord tuner" screen showing the current chord; standard tuning, capo setting.

**Out (later phases):** rhythm/strum-pattern feedback, finger-technique detection (bends, slides, hammer-ons), theory overlays (fretboard notes, intervals, scales on top of the detected key), ear-training drills, sheet-music reading, accounts/sync.

## 6. Milestones

1. **Pipeline prototype (Python):** chords + Basic Pitch + fret assignment on GuitarSet and a few of David's own recordings; output Guitar Pro/MusicXML files; measure accuracy with mir_eval.
2. **App shell:** Expo app with record/import, alphaTab viewer showing prototype output.
3. **On-device models:** ONNX export, file analysis on the phone.
4. **Live chord mode.**
5. Polish, edit/correct tabs, then phase-2 features.

## 7. Licensing watch-list

OK for a product: Basic Pitch (Apache-2.0), librosa (ISC), alphaTab (MPL-2.0), ONNX Runtime (MIT), GuitarSet (CC BY 4.0). Research only / avoid in the shipped app: madmom pretrained models (CC BY-NC-SA), Essentia (AGPL), aubio (GPL), Chordino (GPL).
