# Dé noir à points blancs (marché de Québec) : cube OBJ (largeur 1) + texture 3×2 faces de 200 px.
from PIL import Image, ImageDraw
import os; os.makedirs('img', exist_ok=True)
S = 200; FACES = {1: (0, 0), 2: (1, 0), 3: (2, 0), 4: (0, 1), 5: (1, 1), 6: (2, 1)}   # valeur -> case de l'atlas
PIPS = {1: [(.5, .5)], 2: [(.27, .27), (.73, .73)], 3: [(.27, .27), (.5, .5), (.73, .73)], 4: [(.27, .27), (.73, .27), (.27, .73), (.73, .73)],
        5: [(.27, .27), (.73, .27), (.5, .5), (.27, .73), (.73, .73)], 6: [(.27, .25), (.73, .25), (.27, .5), (.73, .5), (.27, .75), (.73, .75)]}
im = Image.new('RGB', (3 * S, 2 * S), '#161412'); d = ImageDraw.Draw(im)
for v, (cx, cy) in FACES.items():
    x0, y0 = cx * S, cy * S
    d.rectangle([x0, y0, x0 + S - 1, y0 + S - 1], outline='#2C2722', width=6)
    for px, py in PIPS[v]:
        r = 17; X, Y = x0 + px * S, y0 + py * S; d.ellipse([X - r, Y - r, X + r, Y + r], fill='#F6EFDC')
im.save('img/de_noir.png')
# faces du cube : valeur, normale, 4 sommets (dans l'ordre u0v0, u1v0, u1v1, u0v1 de la case)
h = .5
CUBE = [(1, (0, 1, 0), [(-h, 1, -h), (h, 1, -h), (h, 1, h), (-h, 1, h)]), (6, (0, -1, 0), [(-h, 0, h), (h, 0, h), (h, 0, -h), (-h, 0, -h)]),
        (2, (0, 0, 1), [(-h, 1, h), (h, 1, h), (h, 0, h), (-h, 0, h)]), (5, (0, 0, -1), [(h, 1, -h), (-h, 1, -h), (-h, 0, -h), (h, 0, -h)]),
        (3, (1, 0, 0), [(h, 1, h), (h, 1, -h), (h, 0, -h), (h, 0, h)]), (4, (-1, 0, 0), [(-h, 1, -h), (-h, 1, h), (-h, 0, h), (-h, 0, -h)])]
L = []; nv = nt = 0
for k, (val, n, vs) in enumerate(CUBE):
    cx, cy = FACES[val]; u0, u1 = cx / 3 + .004, (cx + 1) / 3 - .004; v1, v0 = 1 - cy / 2 - .004, 1 - (cy + 1) / 2 + .004
    for x, y, z in vs: L.append(f'v {x} {y} {z}')
    for u, v in ((u0, v1), (u1, v1), (u1, v0), (u0, v0)): L.append(f'vt {u:.4f} {v:.4f}')
    L.append(f'vn {n[0]} {n[1]} {n[2]}')
    a, b, c, e = (nv + i for i in (1, 2, 3, 4)); ta, tb, tc, te = (nt + i for i in (1, 2, 3, 4)); nn = k + 1
    for f in ((a, ta), (b, tb), (c, tc)), ((a, ta), (c, tc), (e, te)):
        L.append('f ' + ' '.join(f'{p}/{t}/{nn}' for p, t in f)); L.append('f ' + ' '.join(f'{p}/{t}/{nn}' for p, t in reversed(f)))
    nv += 4; nt += 4
open('img/de_noir.obj', 'w').write('\n'.join(L) + '\n'); print('dé noir')
