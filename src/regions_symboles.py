# Symboles des Régions (Mishipeshu, Mishi-mikinaak, Oniare) :
# 1. dé des zones : chaque face porte le médaillon de sa Région (gabarit D6 de TTS) ;
# 2. cartouches de la carte : le filigrane du canot est remplacé par le filigrane du symbole de la Région.
import sys
from PIL import Image, ImageDraw
import numpy as np
R = sys.argv[1]; A = R+'src/assets/'
MED = {k: Image.open(A+f'region_{k}.png').convert('RGBA') for k in ('mishipeshu', 'tortue', 'oniare')}
def fond(im):                              # couleur du médaillon (pixels foncés, hors figure)
    a = np.array(im).reshape(-1, 4); a = a[(a[:, 3] > 250) & (a[:, :3].sum(1) < 400)]
    return tuple(int(v) for v in np.median(a[:, :3], 0))
# --- 1. dé des zones
C = 2048//3; POS = {2: (0, 0), 4: (1, 0), 5: (2, 0), 1: (0, 1), 3: (1, 1), 6: (2, 1)}
REG = {1: 'mishipeshu', 6: 'mishipeshu', 2: 'tortue', 5: 'tortue', 3: 'oniare', 4: 'oniare'}
D = Image.new('RGB', (2048, 2048), (60, 60, 60))
for v, k in REG.items():
    f = Image.new('RGBA', (C, C), fond(MED[k]) + (255,)); m = MED[k].resize((C-40, C-40), Image.LANCZOS)
    f.alpha_composite(m, (20, 20)); f = f.convert('RGB')
    c, r = POS[v]; D.paste(f.rotate(180) if v in (1, 6) else f, (c*C, 2048-2*C+r*C))
D.save(R+'img/v18/cdice_zones.png')
# --- 2. cartouches (plateau table_v17r.png, coordonnées en px du plateau)
T = Image.open(R+'img/v18/table_v3_22.png').convert('RGB')
W, H = 547, 461; BAND = 79; BG = np.array((243, 238, 226)); INNER = (201, 192, 174)
CART = [((1660, 1120), '#2F4373', 'mishipeshu'), ((2342, 1312), '#2F4373', 'mishipeshu'), ((779, 1745), '#2F4373', 'mishipeshu'),
        ((1627, 2832), '#6A9A48', 'tortue'), ((1378, 2223), '#6A9A48', 'tortue'), ((2067, 2225), '#6A9A48', 'tortue'),
        ((3928, 2650), '#963A26', 'oniare'), ((3234, 2657), '#963A26', 'oniare')]
def rgb(h): return np.array([int(h[i:i+2], 16) for i in (1, 3, 5)])
def figure(k, h):                          # silhouette crème du médaillon -> masque
    a = np.array(MED[k]).astype(int); m = (a[:, :, 0] > 190) & (a[:, :, 1] > 180) & (a[:, :, 3] > 200)
    ys, xs = np.nonzero(m); m = Image.fromarray((m*255).astype('uint8')).crop((xs.min(), ys.min(), xs.max()+1, ys.max()+1))
    s = h/m.height; return m.resize((round(m.width*s), h), Image.LANCZOS)
for (x, y), col, k in CART:
    card = np.array(T.crop((x, y, x+W, y+H))).astype(float); orig = card.copy()
    band = 0.4*rgb(col)+0.6*BG; lum = card.mean(2)
    # bandeau : on garde le texte (foncé) et le double filet, le reste devient la couleur pleine du bandeau
    keep = lum[:BAND] < band.mean()-45
    card[:BAND][~keep] = band
    # corps : fond uni + filigrane du symbole (sépia, 18 %)
    card[BAND+9:] = BG
    m = np.array(figure(k, 300)).astype(float)/255; mh, mw = m.shape
    ox, oy = (W-mw)//2, BAND+9+(H-BAND-9-mh)//2; ink = np.array((107, 90, 69))
    reg = card[oy:oy+mh, ox:ox+mw]; card[oy:oy+mh, ox:ox+mw] = reg*(1-0.18*m[..., None])+ink*0.18*m[..., None]
    out = Image.fromarray(card.clip(0, 255).astype('uint8')); d = ImageDraw.Draw(out)
    d.rounded_rectangle((13, 13, W-14, H-14), radius=18, outline=INNER, width=2)
    o = np.array(out).astype(float)
    o[:BAND][~keep] = band                                  # filet intérieur sous le bandeau : masqué par sa couleur
    lb = (o[:BAND] == INNER).all(2) if False else None
    o[BAND:BAND+9] = orig[BAND:BAND+9]                      # double filet du bandeau
    o[368-20:434+20, 455-20:521+20] = np.where(((orig[368-20:434+20, 455-20:521+20].mean(2) < 120)[..., None]), orig[368-20:434+20, 455-20:521+20], o[368-20:434+20, 455-20:521+20])
    # coins arrondis : hors de la carte, on remet l'original
    mk = Image.new('L', (W, H), 0); ImageDraw.Draw(mk).rounded_rectangle((2, 2, W-3, H-3), radius=24, fill=255); mk = np.array(mk)[..., None]/255
    o = o*mk+orig*(1-mk)
    T.paste(Image.fromarray(o.clip(0, 255).astype('uint8')), (x, y))
T.save(R+'img/v18/table_v3_22.png')
print('ok')
