import json, numpy as np
a = json.load(open('/tmp/claude-0/work/analysis.json'))
beats = np.array(a['beats']); CAPO = 1
names = ['C','C#','D','Eb','E','F','F#','G','Ab','A','Bb','B']
flat = {'C#':'Db','F#':'Gb'}
# melody: drop outliers, keep highest note per 50 ms cluster
notes = [n for n in a['notes'] if n[2] <= 88]
mel = []
for n in notes:
    if mel and n[0] - mel[-1][0] < 0.05:
        if n[2] > mel[-1][2]: mel[-1] = n
    else: mel.append(n)
# bar grid: downbeat = beat nearest first note
b0 = int(np.argmin(abs(beats - mel[0][0])))
spb = float(np.median(np.diff(beats)))
start = beats[b0]
nbars = int(np.ceil((a['duration'] - start) / (4*spb)))
# fret assignment by DP (standard tuning, capo), minimize hand movement
OPEN = [64, 59, 55, 50, 45, 40]  # e B G D A E
def opts(p):
    return [(s, p - CAPO - o) for s, o in enumerate(OPEN) if 0 <= p - CAPO - o <= 20]
mel = [n for n in mel if opts(n[2])]
cands = [opts(n[2]) for n in mel]
cost = [[(f if f > 0 else 0) * 0.05 + (0 if f == 0 else 0) for s, f in c] for c in cands]
back = [[None]*len(c) for c in cands]
for i in range(1, len(mel)):
    for j, (s, f) in enumerate(cands[i]):
        best = None
        for k, (s2, f2) in enumerate(cands[i-1]):
            pos = lambda ff: ff if ff > 0 else None
            jump = abs(f - f2)
            c = cost[i-1][k] + jump + 0.3*abs(s - s2) + 0.2*f
            if best is None or c < best[0]: best = (c, k)
        cost[i][j], back[i][j] = best
j = int(np.argmin(cost[-1])); path = []
for i in range(len(mel)-1, -1, -1):
    path.append(cands[i][j]); j = back[i][j] if i else j
path.reverse()
# chord per bar from melody pitch classes (arpeggio) using triad templates
def chord_of(pcs):
    best = None
    for r in range(12):
        for q, iv in [('', (0,4,7)), ('m', (0,3,7))]:
            tones = {(r+i) % 12 for i in iv}
            sc = sum(w for pc, w in pcs.items() if pc in tones) - 0.5*sum(w for pc, w in pcs.items() if pc not in tones) + (0.3*pcs.get(r,0))
            if best is None or sc > best[0]: best = (sc, flat.get(names[r], names[r]) + q, r, q)
    return best
lines = []; out_bars = []
SL = 16
for b in range(nbars):
    t0 = start + b*4*spb
    grid = [['-']*SL for _ in range(6)]; pcs = {}
    for n, (s, f) in zip(mel, path):
        if t0 - spb/8 <= n[0] < t0 + 4*spb - spb/8:
            slot = min(SL-1, max(0, int(round((n[0]-t0)/(spb/4)))))
            grid[s][slot] = str(f)
            pcs[n[2] % 12] = pcs.get(n[2] % 12, 0) + (n[1]-n[0])
    if not pcs: continue
    sc, real, r, q = chord_of(pcs)
    shape = flat.get(names[(r-CAPO) % 12], names[(r-CAPO) % 12]) + q
    out_bars.append((b+1, round(t0,2), real, shape, grid))
# render 2 bars per row
txt = []
for i in range(0, len(out_bars), 2):
    row = out_bars[i:i+2]
    hdr = '  '.join(f"Bar {n} ({t:.1f}s) {real} [shape {shape}]".ljust(SL*3) for n, t, real, shape, g in row)
    txt.append(hdr)
    for s, nm in enumerate('eBGDAE'):
        txt.append(nm + '|' + '|'.join(''.join(c.ljust(3, '-') if c != '-' else '---' for c in g[s]) for *_, g in row) + '|')
    txt.append('')
open('/tmp/claude-0/work/tab.txt', 'w').write('\n'.join(txt))
print('\n'.join(txt)); print('spb', spb, 'bpm', 60/spb, 'bars', [(n, real) for n, t, real, shape, g in out_bars])
