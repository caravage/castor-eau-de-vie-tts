# Tuiles Raid : petite flèche en boucle (la tuile retourne dans le sac à la fin du mois).
import sys, math
from PIL import Image, ImageDraw
R = sys.argv[1]; K = (142, 47, 37)
for n in (1, 2, 3):
    t = Image.open(R+f'img/v18/evt_raid{n}.png').convert('RGB')
    S = 4; big = Image.new('RGBA', (t.width*S, t.height*S), (0, 0, 0, 0)); d = ImageDraw.Draw(big)
    cx, cy, r, w = 252*S, 252*S, 17*S, 4*S
    d.arc((cx-r, cy-r, cx+r, cy+r), start=-60, end=230, fill=K, width=w)
    a = math.radians(-60); ex, ey = cx+r*math.cos(a), cy+r*math.sin(a)
    tx, ty = -math.sin(a), math.cos(a)          # tangente (sens horaire)
    h = 9*S
    p1 = (ex+tx*h*1.1, ey+ty*h*1.1); nx, ny = math.cos(a), math.sin(a)
    d.polygon([(ex-tx*h*0.2+nx*h*0.8, ey-ty*h*0.2+ny*h*0.8), (ex-tx*h*0.2-nx*h*0.8, ey-ty*h*0.2-ny*h*0.8), p1], fill=K)
    big = big.resize(t.size, Image.LANCZOS); t = t.convert('RGBA'); t.alpha_composite(big)
    t.convert('RGB').save(R+f'img/v18/evt_raid{n}_b.png')
print('ok')
