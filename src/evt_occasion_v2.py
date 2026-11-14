# Tuile « Occasion » v2 (14 nov. 2026) : icône double flèche + flocon = la défausse est remélangée dans le sac à l'hiver. : refaite exactement dans le gabarit des autres tuiles Événements du mois
# (evenements_v2.py : bandeau et bord pleins, fond crème, titre IM Fell italique, flèche en boucle des Raids), couleur or.
# Usage : python3 evt_occasion_v2.py <racine du dépôt> <dossier node_modules/@fontsource>
import sys, types
R, F = sys.argv[1], sys.argv[2]
src = open(R + 'src/evenements_v2.py').read()
ns = {'__name__': 'occ'}; sys.argv = [sys.argv[0], R, F]
exec(src[:src.index('FIT = ')], ns)          # CSS, polices, boucle()
from playwright.sync_api import sync_playwright
OR = '#A8781C'
html = (f"<!doctype html><html><head><meta charset='utf-8'><style>{ns['CSS']}</style></head><body><div class='e' style='--k:{OR}'>"
        "<div class='h'>Événement du mois</div><div class='b' style='padding-bottom:76px'><div class='t'>Occasion</div></div></div></body></html>")
open('/tmp/occ.html', 'w').write(html)
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(viewport={'width': 300, 'height': 300})
    pg.goto('file:///tmp/occ.html'); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(300)
    out = R + 'img/v18/evt7_occasion.png'; pg.screenshot(path=out); br.close()
# double flèche en cycle (remélange) + flocon (à l'hiver), même trait que la boucle des Raids
from PIL import Image, ImageDraw
import math
K = tuple(int(OR[i:i+2], 16) for i in (1, 3, 5)); t = Image.open(out).convert('RGBA'); S = 4
big = Image.new('RGBA', (t.width*S, t.height*S), (0, 0, 0, 0)); d = ImageDraw.Draw(big)
cx, cy, r, w = 248*S, 250*S, 21*S, 4*S
for st, en in ((200, 330), (20, 150)):
    d.arc((cx-r, cy-r, cx+r, cy+r), start=st, end=en, fill=K, width=w)
    a = math.radians(en); ex, ey = cx+r*math.cos(a), cy+r*math.sin(a); tx, ty = -math.sin(a), math.cos(a); nx, ny = math.cos(a), math.sin(a); h = 8*S
    d.polygon([(ex-tx*h*0.2+nx*h*0.8, ey-ty*h*0.2+ny*h*0.8), (ex-tx*h*0.2-nx*h*0.8, ey-ty*h*0.2-ny*h*0.8), (ex+tx*h*1.1, ey+ty*h*1.1)], fill=K)
fr = 9*S
for k in range(6):
    b = math.radians(90+60*k); fx, fy = cx+fr*math.cos(b), cy+fr*math.sin(b)
    d.line((cx, cy, fx, fy), fill=K, width=int(2.3*S))
    for sg in (-1, 1):
        b2 = b+sg*math.radians(40); mx, my = cx+0.6*fr*math.cos(b), cy+0.6*fr*math.sin(b)
        d.line((mx, my, mx+0.38*fr*math.cos(b2), my+0.38*fr*math.sin(b2)), fill=K, width=int(1.7*S))
t.alpha_composite(big.resize(t.size, Image.LANCZOS)); t.convert('RGB').save(out)
print(out)
