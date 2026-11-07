# v3.31 : passe graphique sur le plateau (post-traitement de table_v3_30).
#  1. cadre double autour de la carte, grain et vignette
#  2. rives : trait foncé côté terre, halo clair côté eau
#  3. filigranes des cartouches allégés (gravures Témiscamingue / Congés / Québec / Antilles préservées)
#  4. portages : fond parchemin au lieu du blanc froid
#  5. pistes Ravages et Prix du castor dans un cartouche ; rouge vif → rouge brique
#  6. étendues : hachures remplacées par une teinte pleine, ancres en brun
#  7. rose des vents
#  8. encarts Domaine du Roi / La Rochelle / Antilles : même cadre double que la carte
# Usage : python3 plateau_v3_31.py <image source> <image cible> <police Alegreya Sans 500 .ttf>
import sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
SRC, DST, F500 = sys.argv[1:4]
DARK = (42, 36, 24); CART = (243, 239, 226); CARTB = (150, 140, 120)
im = Image.open(SRC).convert('RGB'); a = np.array(im).astype(np.float32); H, W = a.shape[:2]
X0, Y0, X1, Y1 = 718, 935, 5600, 3560                      # carte
r, g, b = a[..., 0], a[..., 1], a[..., 2]
def box(m, x0, y0, x1, y1, v=True): m[y0:y1, x0:x1] = v
def dil(mask, k):
    m = Image.fromarray((mask * 255).astype('uint8')).resize((W // 4, H // 4)).filter(ImageFilter.MaxFilter(k)).resize((W, H))
    return np.array(m) > 127

# ---- 6. étendues : hachures → teinte pleine
hatch = (r - b > 55) & (r > 170) & (g > 140) & (b < 150)
zone = np.zeros((H, W), bool)
for bx in [(X0, Y0, 1600, 1750), (X0, 3050, 1700, Y1), (3200, 3250, 3850, Y1), (4085, 970, 4800, 1480)]: box(zone, *bx)
hatch &= zone
a[hatch] = (207, 184, 134)
dark_h = (r - b > 50) & (r > 150) & (r < 200) & (g < 175) & zone    # rayures foncées
a[dark_h] = (207, 184, 134)

# ---- 2. rives
water = (b - r > 25) & (g > 120) & (b > 140) & (r < 200)
water[:Y0] = False; water[Y1:] = False; water[:, :X0] = False
wm = Image.fromarray((water * 255).astype('uint8'))
edge = np.array(wm.filter(ImageFilter.MaxFilter(5))).astype(bool) & ~water
inner = water & ~np.array(wm.filter(ImageFilter.MinFilter(9))).astype(bool)
a[edge] = a[edge] * 0.55 + np.array([70, 80, 80]) * 0.45
a[inner] = a[inner] * 0.7 + np.array([205, 222, 224]) * 0.3

# ---- 3. filigranes allégés
r, g, b = a[..., 0], a[..., 1], a[..., 2]
cream = np.array(CART, np.float32)
pastel = ((np.abs(r - g) < 40) & (np.abs(g - b) < 40) & (r > 150) & (r < 225) & (b > 150)) | ((g - r > 5) & (g > 170) & (r > 150) & (b < 200) & (r < 210)) | ((r - b > 20) & (r > 200) & (g > 150) & (g < 215))
pastel &= ~water & (np.abs(a - cream).sum(2) > 30)
land = (r - b > 35) & (g - b > 18) & (r >= g); pastel &= ~land
pastel &= dil(np.abs(a - cream).sum(2) < 18, 37)
keep = np.zeros((H, W), bool)
for bx in [(3330, 1470, 3890, 1940), (4230, 1630, 4650, 2000), (4760, 1610, 5600, 2290), (4975, 3110, 5600, 3490), (4975, 2290, 5600, 3090)]: box(keep, *bx)
pastel &= ~keep
a[pastel] = a[pastel] * 0.45 + cream * 0.55

# ---- 4. portages : blanc froid → parchemin
cold = (np.abs(a - np.array([238, 242, 239])).sum(2) < 14); cold[:Y0] = False; cold[Y1:] = False
a[cold] = (244, 240, 228)

# ---- 1. grain + vignette
rng = np.random.default_rng(1)
yy, xx = np.mgrid[Y0:Y1, X0:X1]
vx = ((xx - (X0 + X1) / 2) / ((X1 - X0) / 2)) ** 2 + ((yy - (Y0 + Y1) / 2) / ((Y1 - Y0) / 2)) ** 2
vig = 1 - 0.09 * np.clip(vx - 0.45, 0, 1)[..., None]
a[Y0:Y1, X0:X1] = (a[Y0:Y1, X0:X1] + rng.normal(0, 6, (Y1 - Y0, X1 - X0, 1))) * vig

# ---- 5. rouge vif → brique (piste Ravages)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
red = (r > 150) & (g < 90) & (b < 90); red[Y0:] = False
a[red] = (168, 76, 60)

out = Image.fromarray(np.clip(a, 0, 255).astype('uint8')); d = ImageDraw.Draw(out)

# ---- 5. cartouches des pistes (le fond beige est repeint, les ronds et chiffres sont conservés)
BG = np.array([230, 218, 182])
for (x0, y0, x1, y1) in [(1700, 620, 2640, 900), (3560, 620, 4580, 900)]:
    reg = np.array(out.crop((x0, y0, x1, y1))).astype(int)
    fg = np.abs(reg - BG).sum(2) > 24
    card = Image.new('RGB', (x1 - x0, y1 - y0), (230, 218, 182)); cd = ImageDraw.Draw(card)
    cd.rounded_rectangle((0, 0, x1 - x0 - 1, y1 - y0 - 1), radius=18, fill=CART, outline=CARTB, width=3)
    ca = np.array(card); ca[fg] = reg[fg]
    out.paste(Image.fromarray(ca.astype('uint8')), (x0, y0))

# ---- 1. cadre double
def cadre(x0, y0, x1, y1):
    d.rectangle((x0, y0, x1, y1), outline=DARK, width=7)
    d.rectangle((x0 + 14, y0 + 14, x1 - 14, y1 - 14), outline=DARK, width=2)
cadre(X0 + 6, Y0 + 6, X1 - 7, Y1 - 7)
# ---- 8. encarts, même cadre (dessinés par-dessus le cadre de la carte)
for (x0, y0, x1, y1) in [(4085, 970, 4800, 1480), (4975, 2290, 5593, 3090), (4975, 3115, 5593, 3480)]:
    cadre(x0, y0, x1, y1)

# ---- 6. ancres des étendues (rond orange → brun)
for (ax, ay) in [(856, 1387), (949, 3266), (3163, 3370), (4460, 1136)]:
    d.ellipse((ax - 15, ay - 15, ax + 15, ay + 15), fill=(120, 90, 50), outline=DARK, width=3)
# ---- 7. rose des vents
cx, cy, R = 1480, 1140, 85
f = ImageFont.truetype(F500, 30)
for i in range(16):
    ang = i * math.pi / 8; L = R if i % 4 == 0 else (R * 0.62 if i % 2 == 0 else R * 0.38)
    w = 12 if i % 4 == 0 else 8
    p = (cx + L * math.sin(ang), cy - L * math.cos(ang))
    l = (cx + w * math.sin(ang - math.pi / 2), cy - w * math.cos(ang - math.pi / 2))
    rr = (cx + w * math.sin(ang + math.pi / 2), cy - w * math.cos(ang + math.pi / 2))
    d.polygon([p, l, (cx, cy)], fill=DARK); d.polygon([p, rr, (cx, cy)], fill=(244, 240, 228), outline=DARK)
d.ellipse((cx - R - 10, cy - R - 10, cx + R + 10, cy + R + 10), outline=DARK, width=2)
d.text((cx - 9, cy - R - 46), 'N', font=f, fill=DARK)
out.save(DST, optimize=True); print(DST)
