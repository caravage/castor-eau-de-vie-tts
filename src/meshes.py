# Modèles 3D des sacs : chaque sac a la forme de la pièce qu'il contient (silhouette extrudée, image du jeton sur le dessus).
# Coordonnées OBJ : x à droite de l'image, z vers le bas de l'image, y vers le haut ; largeur totale = 1.
import math, json, os
import numpy as np, mapbox_earcut as earcut
from PIL import Image
os.makedirs('img', exist_ok=True)

def quad(p0, c, p1, n=8):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * c[0] + t * t * p1[0], (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * c[1] + t * t * p1[1]) for t in [k / n for k in range(1, n + 1)]]

def mesh(name, img, poly, thick, edge_px):
    W, H = Image.open(f'img/{img}.png').size
    xs = [p[0] for p in poly]; ys = [p[1] for p in poly]
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2; k = 1 / (max(xs) - min(xs)); t = thick * k
    tri = earcut.triangulate_float32(np.array(poly, dtype=np.float32).reshape(-1, 2), np.array([len(poly)], dtype=np.uint32)).tolist()
    V, VT, VN, F = [], [], [], []
    def v(x, y, z): V.append((x, y, z)); return len(V)
    def vt(u, w): VT.append((u, w)); return len(VT)
    def vn(x, y, z): VN.append((x, y, z)); return len(VN)
    def face(a, b, c, n):   # deux faces opposées : visible quel que soit le sens retenu à l'import
        F.append((a, b, c, n[0])); F.append((c, b, a, n[1]))
    up, dn = vn(0, 1, 0), vn(0, -1, 0)
    top = [(v((px - cx) * k, t, (py - cy) * k), vt(px / W, 1 - py / H)) for px, py in poly]
    bot = [(v((px - cx) * k, 0, (py - cy) * k), vt(px / W, 1 - py / H)) for px, py in poly]
    for i in range(0, len(tri), 3):
        a, b, c = tri[i:i + 3]
        face(top[a], top[c], top[b], (up, dn)); face(bot[a], bot[b], bot[c], (dn, up))
    e = vt(edge_px[0] / W, 1 - edge_px[1] / H)
    n = len(poly)
    for i in range(n):
        j = (i + 1) % n; (x0, y0), (x1, y1) = poly[i], poly[j]; L = math.hypot(x1 - x0, y1 - y0) or 1
        o, ib = vn((y1 - y0) / L, 0, -(x1 - x0) / L), vn(-(y1 - y0) / L, 0, (x1 - x0) / L)
        A, B, C, D = (top[i][0], e), (top[j][0], e), (bot[j][0], e), (bot[i][0], e)
        face(A, B, C, (o, ib)); face(A, C, D, (o, ib))
    with open(f'img/{name}.obj', 'w') as f:
        f.write(''.join(f'v {x:.5f} {y:.5f} {z:.5f}\n' for x, y, z in V) + ''.join(f'vt {u:.5f} {w:.5f}\n' for u, w in VT) + ''.join(f'vn {x:.4f} {y:.4f} {z:.4f}\n' for x, y, z in VN))
        f.write(''.join(f'f {a[0]}/{a[1]}/{nn} {b[0]}/{b[1]}/{nn} {c[0]}/{c[1]}/{nn}\n' for a, b, c, nn in F))
    return round((max(ys) - min(ys)) / (max(xs) - min(xs)), 4)

ASPECT = {}
ASPECT['sac_caisse'] = mesh('sac_caisse', 'tok_caisse_w', [(14, 22), (186, 22), (186, 178), (14, 178)], 110, (16, 100))
bottle = [(80, 6), (120, 6), (120, 32), (118, 32), (118, 55)] + quad((118, 55), (154, 72), (154, 112)) + [(154, 176)] + quad((154, 176), (154, 192), (138, 192)) + [(62, 192)] + quad((62, 192), (46, 192), (46, 176)) + [(46, 112)] + quad((46, 112), (46, 72), (82, 55)) + [(82, 32), (80, 32)]
ASPECT['sac_bouteille'] = mesh('sac_bouteille', 'tok_bouteille_w', bottle, 40, (48, 140))
for nm, cells in (('grand', 5), ('petit', 3), ('coureur', 2)):
    w = cells * 120 + 120; h = 210
    ASPECT[f'sac_canot_{nm}'] = mesh(f'sac_canot_{nm}', f'canot_{nm}', [(10, 30), (w - 10, 30), (w - 60, h - 10), (60, h - 10)], 70, (w / 2, 31))
circ = [(120 + 116 * math.cos(2 * math.pi * i / 48), 120 + 116 * math.sin(2 * math.pi * i / 48)) for i in range(48)]
for kv in ('rep', 'guide', 'mil', 'int'):
    ASPECT[f'sac_voy_{kv}'] = mesh(f'sac_voy_{kv}', f'voy_{kv}', circ, 50, (120, 30))
json.dump(ASPECT, open('meshes.json', 'w'), indent=1)
print(ASPECT)
# Jeton Coureur des bois : carré arrondi
def rrect(x0, y0, x1, y1, r, n=6):
    pts = []
    for cx, cy, a0 in ((x1 - r, y0 + r, -90), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180)):
        pts += [(cx + r * math.cos(math.radians(a0 + 90 * k / n)), cy + r * math.sin(math.radians(a0 + 90 * k / n))) for k in range(n + 1)]
    return pts
ASPECT['sac_coureur'] = mesh('sac_coureur', 'tok_coureur', rrect(8, 8, 392, 392, 46), 60, (200, 10))
json.dump(ASPECT, open('meshes.json', 'w'), indent=1)
