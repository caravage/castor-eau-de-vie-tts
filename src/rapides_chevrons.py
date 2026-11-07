# Rapides : hachures retirées, deux rangs de chevrons bleus sous le nom (tout reste dans le cercle).
import sys
from PIL import Image, ImageDraw
import numpy as np
R, IMG = sys.argv[1], sys.argv[2]
T = Image.open(R+IMG).convert('RGB'); FILL = (240, 242, 236); BLUE = (78, 140, 153); DARK = (42, 36, 24)
RAP = {'Saint-Laurent': (4262, 2490), 'Rivière des Outaouais': (4048, 2217), 'Sault Sainte-Marie': (2440, 1930), 'Chutes du Niagara': (3107, 2875)}
def chev(dr, x, y, w, h, col, wd): dr.line([(x, y+h), (x+w/2, y), (x+w, y+h)], fill=col, width=wd, joint='curve')
for name, (ax, ay) in RAP.items():
    c = T.crop((ax-170, ay-170, ax+170, ay+170)); a = np.array(c).astype(int)
    lum = a.mean(2); hat = (a[:, :, 2]-a[:, :, 0] > 6) & (lum > 120)
    yy, xx = np.mgrid[:340, :340]; near = np.hypot(xx-170, yy-170) < 108
    # centre : ajustement du cercle noir existant (pixels sombres dans l'anneau 94-108)
    ring = (lum < 90) & (np.hypot(xx-170, yy-170) > 94) & (np.hypot(xx-170, yy-170) < 108)
    ys, xs = np.nonzero(ring); A = np.c_[2*xs, 2*ys, np.ones(len(xs))]; b = xs**2+ys**2
    cx, cy, c0 = np.linalg.lstsq(A, b, rcond=None)[0]; r = 101
    d = np.hypot(xx-cx, yy-cy)
    a[(d < r-2) & hat] = FILL
    im = Image.fromarray(a.astype('uint8')); dr = ImageDraw.Draw(im)
    for row, n in ((0, 5), (1, 4)):
        y = cy+46+row*15; x0 = cx-(n*20)/2+2
        for i in range(n): chev(dr, x0+i*20, y, 16, 8, BLUE, 3)
    dr.ellipse((cx-r, cy-r, cx+r, cy+r), outline=DARK, width=3)
    T.paste(im, (ax-170, ay-170)); print(name, round(ax-170+cx), round(ay-170+cy), round(r))
T.save(R+IMG)
