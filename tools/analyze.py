import sys, json, numpy as np, librosa
from basic_pitch.inference import predict
from basic_pitch import build_icassp_2022_model_path, FilenameSuffix
path = sys.argv[1]
y, sr = librosa.load(path, sr=22050, mono=True)
dur = len(y)/sr
# tempo/beats
tempo, beats = librosa.beat.beat_track(y=y, sr=sr, units='time')
# key (Krumhansl)
chroma = librosa.feature.chroma_cqt(y=librosa.effects.harmonic(y), sr=sr, hop_length=512)
prof_maj = np.array([6.35,2.23,3.48,2.33,4.38,4.09,2.52,5.19,2.39,3.66,2.29,2.88])
prof_min = np.array([6.33,2.68,3.52,5.38,2.60,3.53,2.54,4.75,3.98,2.69,3.34,3.17])
names = ['C','C#','D','Eb','E','F','F#','G','Ab','A','Bb','B']
m = chroma.mean(1)
scores = [(np.corrcoef(np.roll(prof_maj,k),m)[0,1], names[k]+' major') for k in range(12)] + \
         [(np.corrcoef(np.roll(prof_min,k),m)[0,1], names[k]+' minor') for k in range(12)]
scores.sort(reverse=True)
# chords: templates maj/min/7, per beat-pair segments, Viterbi-ish smoothing by simple median
templ, labels = [], []
for r in range(12):
    for q, iv in [('', [0,4,7]), ('m', [0,3,7]), ('7', [0,4,7,10])]:
        t = np.zeros(12); t[[(r+i)%12 for i in iv]] = 1; templ.append(t/np.linalg.norm(t)); labels.append(names[r]+q)
templ = np.array(templ)
times = librosa.frames_to_time(np.arange(chroma.shape[1]), sr=sr, hop_length=512)
bounds = list(beats[::2]) if len(beats) > 4 else list(np.arange(0, dur, 1.0))
bounds = [0.0] + [b for b in bounds if b > 0.1] + [dur]
segs = []
for a, b in zip(bounds[:-1], bounds[1:]):
    idx = (times >= a) & (times < b)
    if not idx.any(): continue
    v = chroma[:, idx].mean(1); v = v/ (np.linalg.norm(v)+1e-9)
    s = templ @ v; s[[i for i,l in enumerate(labels) if l.endswith('7')]] -= 0.04
    lab = labels[int(s.argmax())]
    if segs and segs[-1][2] == lab: segs[-1][1] = b
    else: segs.append([a, b, lab])
# notes
_, midi, notes = predict(path, build_icassp_2022_model_path(FilenameSuffix.onnx),
                         onset_threshold=0.5, frame_threshold=0.3, minimum_note_length=80)
notes = sorted([(float(s), float(e), int(p), float(a)) for s, e, p, a, *_ in notes])
midi.write('/tmp/claude-0/work/clip_notes.mid')
json.dump(dict(duration=dur, tempo=float(np.atleast_1d(tempo)[0]), beats=[float(b) for b in beats],
               key=scores[:3], chords=segs, notes=notes), open('/tmp/claude-0/work/analysis.json','w'))
print('dur', round(dur,1), 'tempo', np.atleast_1d(tempo)[0], 'key', scores[:3])
print('chords:', [(round(a,1), l) for a,b,l in segs])
print('notes', len(notes), 'pitch range', min(n[2] for n in notes), max(n[2] for n in notes))
