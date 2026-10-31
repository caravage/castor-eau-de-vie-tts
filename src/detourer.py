# Après render.js : pièces détourées (fond transparent). Les pixels transparents prennent la couleur du bord,
# pour qu'aucun liseré blanc n'apparaisse si TTS ignore la transparence.
import re, os, numpy as np
from PIL import Image
PAT = re.compile(r'^(tile_|hid_|fort_|mission|navire_|pion_)')
for f in sorted(os.listdir('img')):
    if not (f.endswith('.png') and PAT.match(f)): continue
    a = np.array(Image.open('img/' + f).convert('RGBA'))
    h, w = a.shape[:2]; k = min(h, w) // 2
    col = a[:, w // 2]; op = [i for i in range(h) if col[i, 3] > 250]
    if not op: continue
    edge = col[op[0], :3]                                                   # premier pixel opaque en haut, au milieu = couleur du bord
    m = a[:, :, 3] < 255
    a[m, :3] = edge
    Image.fromarray(a).save('img/' + f)
print('détourées')
