# Passe terrain / lacs / rivières / forêts historiques, en HD, sur le calque de base (sans aucun élément de jeu).
# Les arbres évitent tout ce que le calque du dessus (over_hd.png) recouvre.
import numpy as np, cv2
from PIL import Image, ImageDraw
Image.MAX_IMAGE_PIXELS = None
S = 1.428571                      # px HD par px du plateau 5600
F = 2.490857                      # px HD par px css de la carte
a = np.array(Image.open('base_hd.png').convert('RGB')).astype(np.float32)
ov = np.array(Image.open('over_hd.png'))[..., 3]
H, W = a.shape[:2]
rng = np.random.default_rng(7)
def sc(v): return max(1, int(round(v * S)))
def ell(k): k = int(k) | 1; return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k))
def noise(scale, seed):
    r = np.random.default_rng(seed); g = r.random((int(H / scale) + 3, int(W / scale) + 3)).astype(np.float32)
    return cv2.resize(g, (W, H), interpolation=cv2.INTER_CUBIC)
def fractal(scales, seed):
    out = np.zeros((H, W), np.float32); tot = 0
    for i, s in enumerate(scales): w = 0.5 ** i; out += w * noise(s * S, seed + i); tot += w
    return out / tot
r, g, b = a[..., 0], a[..., 1], a[..., 2]
W0 = np.array([157, 189, 194], np.float32)
water = (np.abs(a - W0).sum(2) < 40)
water = cv2.morphologyEx(water.astype(np.uint8), cv2.MORPH_OPEN, ell(3)).astype(bool)
land = ~water
etendue = cv2.GaussianBlur((r - b) / np.maximum(r, 1), (0, 0), 3) > 0.33
hill = np.array(Image.open('hills_hd.png'))[..., 3] > 20
print('eau', round(float(water.mean()), 3), 'étendues', round(float(etendue.mean()), 3), 'collines', round(float(hill.mean()), 4))

# ---------- lacs et rivières
d = cv2.distanceTransform(land.astype(np.uint8) * 0 + (~land).astype(np.uint8), cv2.DIST_L2, 5)   # distance à la rive, dans l'eau
d = cv2.GaussianBlur(d, (0, 0), 2.5 * S) + (fractal([90, 40], 11) - 0.5) * 3.0 * S
wloc = cv2.dilate(d, ell(sc(121)))
lake = np.clip((wloc - 16 * S) / (26 * S), 0, 1)
SHORE = np.array([181, 209, 204], np.float32); DEEP = np.array([117, 160, 176], np.float32)
RIVER = np.array([104, 152, 172], np.float32); LINE = np.array([66, 112, 130], np.float32)
t = (1 - np.exp(-np.maximum(d, 0) / (150 * S)))[..., None]
neww = SHORE * (1 - t) + DEEP * t
del t
neww = neww * lake[..., None] + RIVER * (1 - lake[..., None])
neww *= (1 + (fractal([400, 160], 21) - 0.5) * 0.03)[..., None]
for d0, wd, al in [(10, 2.4, 0.55), (24, 2.2, 0.38), (42, 2.0, 0.24), (64, 1.8, 0.13)]:
    k = (np.clip(wd * S / 2 + 0.7 - np.abs(d - d0 * S), 0, 1) * al * lake)[..., None]
    neww = neww * (1 - k) + LINE * k
# rive : léger trait sombre côté eau
edge = water & (d < 1.6 * S)
neww[edge] = neww[edge] * 0.6 + LINE * 0.4
out = a.copy()
out[water] = neww[water]
del neww

# ---------- terrain
dc = cv2.distanceTransform(land.astype(np.uint8), cv2.DIST_L2, 5)       # distance à l'eau, sur terre
relief = cv2.GaussianBlur(fractal([700, 300], 31) - 0.5, (0, 0), 40 * S)
fac = 1 + relief * 0.07 - 0.13 * np.exp(-dc / (24 * S))
del relief

# couvert historique par région (repère : vue d'ensemble 1960 × 1054 de la carte du plateau 5600)
def ov2hd(ox, oy):
    bx = 718 + ox * 4882 / 1960; by = 935 + oy * 2625 / 1054
    return ((bx - 716) / 1.7436 * F, ((by - 944) / 1.7436 + 8) * F)
q = 10
Dz = np.full((H // q + 1, W // q + 1), 0.92, np.float32); Pz = np.full_like(Dz, 0.05); Rz = np.zeros_like(Dz)
def zone(x0, y0, x1, y1, D=None, P=None, R=None):
    (X0, Y0), (X1, Y1) = ov2hd(x0, y0), ov2hd(x1, y1)
    s_ = slice(max(int(Y0 / q), 0), int(Y1 / q)), slice(max(int(X0 / q), 0), int(X1 / q))
    if D is not None: Dz[s_] = D
    if P is not None: Pz[s_] = P
    if R is not None: Rz[s_] = R
zone(-20, 430, 1100, 760, D=0.72, P=0.30)            # Lacs d'en haut : forêt mixte
zone(560, 560, 1720, 1080, D=0.62, P=0.65)           # Lacs d'en bas : feuillus
zone(780, 830, 1350, 1080, D=0.80, P=0.90)           # vers la Belle Rivière : grande forêt de feuillus
zone(240, 560, 640, 1080, D=0.16, P=0.95)            # Saint-Joseph / Baie des Puants : savane à chênes
zone(-20, 540, 330, 1080, D=0.0, P=0.95, R=1)        # Pays des Illinois : prairie
zone(-20, 480, 240, 560, D=0.25, P=0.8)
sig = 7 * S
Dz = cv2.resize(cv2.GaussianBlur(Dz, (0, 0), sig), (W, H), interpolation=cv2.INTER_LINEAR)
Pz = cv2.resize(cv2.GaussianBlur(Pz, (0, 0), sig), (W, H), interpolation=cv2.INTER_LINEAR)
Rz = cv2.resize(cv2.GaussianBlur(Rz, (0, 0), 6 * S), (W, H), interpolation=cv2.INTER_LINEAR)
riv = (water & (lake < 0.5)).astype(np.uint8)
drv = cv2.distanceTransform(1 - riv, cv2.DIST_L2, 5); del riv
gal = np.clip(1 - (drv - 30 * S) / (70 * S), 0, 1) * 0.85; del drv
D = np.maximum(Dz, gal * np.clip(Rz + (Dz < 0.3), 0, 1))
fo = fractal([330, 140], 41); fo = (fo - fo.min()) / (fo.max() - fo.min())
forest = np.clip(D * (0.35 + 1.3 * fo), 0, 1); del fo, D
forest[etendue] = 0
wash = cv2.GaussianBlur(forest, (0, 0), 45 * S)[..., None] * 0.26
GREEN = np.array([146, 156, 100], np.float32); PRAIRIE = np.array([214, 196, 128], np.float32)
pw = (np.clip(1 - Dz / 0.35, 0, 1) * 0.16 * (1 - gal))[..., None]; del gal
lp = land & ~etendue & ~hill
terr = out * fac[..., None]
terr = terr * (1 - pw) + PRAIRIE * fac[..., None] * pw
terr = terr * (1 - wash) + GREEN * fac[..., None] * wash
out[lp] = terr[lp]
del terr, pw, wash
# étendues : même relief doux
te = out * fac[..., None]; out[etendue & land] = te[etendue & land]; del te, fac

# ---------- forêts : sprites
covered = cv2.dilate((ov > 8).astype(np.uint8), ell(sc(14))).astype(bool)
block = cv2.dilate((water | etendue).astype(np.uint8), ell(sc(41))).astype(bool) | cv2.dilate(hill.astype(np.uint8), ell(sc(27))).astype(bool)
free = ~block & ~covered
yy0, xx0 = int((112.4 + 8) * F), int(438.2 * F); rr = int(60 * F)
free[max(yy0 - rr - 80, 0):yy0 + rr + 10, max(xx0 - rr - 20, 0):xx0 + rr + 20] &= ~(np.hypot(*np.mgrid[max(yy0 - rr - 80, 0):yy0 + rr + 10, max(xx0 - rr - 20, 0):xx0 + rr + 20] - np.array([yy0, xx0])[:, None, None]) < rr + 40)
free[:sc(12)] = False; free[-sc(8):] = False; free[:, :sc(10)] = False; free[:, -sc(6):] = False
print('terre libre', round(float(free.mean()), 3))

def sprite(kind, h):
    SS = 4; w = int(h * (0.62 if kind == 'c' else 0.86)); cw, ch = (w + 8) * SS, (h + 8) * SS
    im = Image.new('RGBA', (cw, ch), (0, 0, 0, 0)); dr = ImageDraw.Draw(im)
    cx = cw // 2; base = ch - 4 * SS; top = 4 * SS; lw = max(1, int(0.9 * SS * S))
    dr.ellipse([cx - w * SS * 0.42, base - 2.2 * SS * S, cx + w * SS * 0.55, base + 2.2 * SS * S], fill=(70, 62, 40, 60))
    dr.line([cx, base, cx, base - h * SS * 0.25], fill=(84, 66, 42, 255), width=int(1.6 * SS * S))
    if kind == 'c':
        Fc, Sd, O = (122, 134, 90, 240), (94, 108, 72, 240), (74, 76, 48, 255)
        hh = base - h * SS * 0.16 - top
        for (y0, y1, hw) in [(0.42, 1.0, 0.50), (0.2, 0.72, 0.40), (0.0, 0.44, 0.29)]:
            ya, yb, x = top + hh * y0, top + hh * y1, w * SS * hw
            dr.polygon([(cx, ya), (cx - x, yb), (cx + x, yb)], fill=Fc)
            dr.polygon([(cx, ya), (cx + x * 0.12, yb), (cx + x, yb)], fill=Sd)
            dr.line([(cx, ya), (cx - x, yb), (cx + x, yb), (cx, ya)], fill=O, width=lw)
    else:
        Fc, Sd, O = (146, 154, 100, 240), (116, 126, 80, 240), (78, 78, 50, 255)
        rr = w * SS * 0.46; cy = top + rr
        dr.ellipse([cx - rr, cy - rr, cx + rr, cy + rr * 0.92], fill=Sd)
        dr.ellipse([cx - rr * 0.92, cy - rr * 0.93, cx + rr * 0.48, cy + rr * 0.5], fill=Fc)
        dr.ellipse([cx - rr, cy - rr, cx + rr, cy + rr * 0.92], outline=O, width=lw)
    im = im.resize((cw // SS, ch // SS), Image.LANCZOS)
    return np.array(im).astype(np.float32)
SPR = {('c', h): sprite('c', sc(h)) for h in (30, 36, 42, 50)}
SPR.update({('d', h): sprite('d', sc(h)) for h in (26, 31, 36)})
pts = []; step = 24 * S; jit = int(9 * S)
for gy in np.arange(60 * S, H - 40 * S, step):
    for gx in np.arange(40 * S, W - 40 * S, step):
        x = int(gx) + int(rng.integers(-jit, jit + 1)); y = int(gy) + int(rng.integers(-jit, jit + 1))
        if not (0 <= x < W and 0 <= y < H) or not free[y, x] or forest[y, x] < rng.random() * 0.9 + 0.08: continue
        kind = 'd' if rng.random() < Pz[y, x] else 'c'
        h = int(rng.choice([30, 36, 36, 42, 42, 50])) if kind == 'c' else int(rng.choice([26, 31, 31, 36]))
        top = y - int(h * S) - 6
        if top < 0 or not free[(y + top) // 2, x] or not free[top, x]: continue
        pts.append((y, x, kind, h))
pts.sort()
for y, x, kind, h in pts:
    sp = SPR[(kind, h)]; sh, sw = sp.shape[:2]
    y0 = y + int(4 * S) - sh; x0 = x - sw // 2
    if y0 < 0 or x0 < 0 or x0 + sw > W or y0 + sh > H: continue
    al = sp[..., 3:4] / 255.0 * 0.92
    out[y0:y0 + sh, x0:x0 + sw] = out[y0:y0 + sh, x0:x0 + sw] * (1 - al) + sp[..., :3] * al
print('arbres', len(pts))
out += rng.normal(0, 2.4, (H, W, 1)).astype(np.float32)     # grain léger
Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save('base_terrain_hd.png')
