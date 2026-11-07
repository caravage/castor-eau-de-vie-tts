# v3.29-v3.30 : flèche de remontée dans chaque rapide (le dé ne se lance qu'en remontant, vers l'ouest)
# et légende Rapide / Raccourci en bas de la carte, entre la Belle Rivière et l'encart des Antilles.
# Usage : python3 legende_rapides.py <image source> <image cible> <dossier des polices>
import sys, math
from PIL import Image, ImageDraw, ImageFont
import numpy as np
SRC, DST, FD = sys.argv[1:4]
BLUE, DARK, FILL = (78, 140, 153), (42, 36, 24), (240, 242, 236)
CART, CARTB, TXT = (243, 239, 226), (150, 140, 120), (42, 36, 24)
T = Image.open(SRC).convert('RGB')
f = ImageFont.truetype(FD + '/alegreya500.ttf', 46)
fi = ImageFont.truetype(FD + '/alegreya400i.ttf', 40)

# sens de la remontée (x, y écran), en s'éloignant de Montréal
RAP = {'Saint-Laurent': ((4262, 2490), (-0.87, 0.5)), 'Rivière des Outaouais': ((4048, 2217), (-1, 0)),
       'Sault Sainte-Marie': ((2440, 1930), (-0.8, -0.6)), 'Chutes du Niagara': ((3107, 2875), (-1, 0))}
DEUX_SENS = {'Chutes du Niagara'}

def fleche(d, cx, cy, ux, uy, L, w, head):
    n = math.hypot(ux, uy); ux, uy = ux / n, uy / n; px, py = -uy, ux
    x0, y0 = cx - ux * L / 2, cy - uy * L / 2; x1, y1 = cx + ux * L / 2, cy + uy * L / 2
    bx, by = x1 - ux * head, y1 - uy * head
    d.line([(x0, y0), (bx, by)], fill=BLUE, width=w)
    d.polygon([(x1, y1), (bx + px * head * 0.6, by + py * head * 0.6), (bx - px * head * 0.6, by - py * head * 0.6)], fill=BLUE)

def chev(d, x, y, w, h, wd): d.line([(x, y + h), (x + w / 2, y), (x + w, y + h)], fill=BLUE, width=wd, joint='curve')

d = ImageDraw.Draw(T)
for name, ((ax, ay), (ux, uy)) in RAP.items():
    a = np.array(T.crop((ax - 170, ay - 170, ax + 170, ay + 170))).astype(int); lum = a.mean(2)
    yy, xx = np.mgrid[:340, :340]; rr = np.hypot(xx - 170, yy - 170)
    ys, xs = np.nonzero((lum < 90) & (rr > 94) & (rr < 108))
    cx, cy, _ = np.linalg.lstsq(np.c_[2 * xs, 2 * ys, np.ones(len(xs))], xs ** 2 + ys ** 2, rcond=None)[0]
    cx, cy = ax - 170 + cx, ay - 170 + cy
    if name in DEUX_SENS:   # chute : jet dans les deux sens (v3.30)
        fleche(d, cx - 18, cy - 64, -1, 0, 36, 6, 18); fleche(d, cx + 18, cy - 64, 1, 0, 36, 6, 18)
    else:
        fleche(d, cx, cy - 64, ux, uy, 60, 6, 20)
    print(name, round(cx), round(cy))

# légende
X0, Y0, X1, Y1 = 3990, 3215, 4680, 3495
d.rounded_rectangle((X0, Y0, X1, Y1), radius=18, fill=CART, outline=CARTB, width=3)
# ligne 1 : rapide (petit cercle avec flèche et chevrons)
cx, cy, r = X0 + 95, Y0 + 75, 52
d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=FILL, outline=DARK, width=3)
fleche(d, cx, cy - 18, -1, 0, 44, 5, 15)
for row, n in ((0, 3), (1, 2)):
    y = cy + 8 + row * 12; x0 = cx - (n * 16) / 2 + 2
    for i in range(n): chev(d, x0 + i * 16, y, 12, 6, 3)
tx = X0 + 185
d.text((tx, cy - 26), 'Rapide', font=f, fill=TXT)
w = d.textlength('Raccourci', font=f)
d.text((tx + w + 30, cy - 26), '2+', font=f, fill=TXT)
d.text((tx + w + 30 + d.textlength('2+', font=f) + 30, cy - 20), '1 : abîmé', font=fi, fill=TXT)
# ligne 2 : raccourci (tiret-point avec chevron)
y = Y0 + 205; x = X0 + 30; xe = X0 + 160
while x < xe:
    d.line([(x, y), (min(x + 22, xe), y)], fill=DARK, width=4); x += 32
    if x < xe: d.ellipse((x - 3, y - 3, x + 3, y + 3), fill=DARK); x += 13
d.line([(X0 + 83, y - 11), (X0 + 97, y), (X0 + 83, y + 11)], fill=DARK, width=4)
d.text((tx, y - 26), 'Raccourci', font=f, fill=TXT)
d.text((tx + w + 30, y - 26), '3+', font=f, fill=TXT)
d.text((tx + w + 30 + d.textlength('3+', font=f) + 30, y - 20), '1 : abîmé', font=fi, fill=TXT)
T.save(DST, optimize=True)
print(DST)
