# Dés de couleur et de peau en Custom Dice TTS (gabarit D6 : 2048², 3 colonnes x 2 rangées dans le bas,
# rangée 1 = faces 2, 4, 5 ; rangée 2 = faces 1, 3, 6, les faces 1 et 6 tournées de 180°).
# Faces opposées : 1-6, 2-5, 3-4. Sec / Gras en IM Fell English italique (non gras), comme sur les tuiles.
import sys
from PIL import Image, ImageDraw, ImageFont
R, FONT = sys.argv[1], sys.argv[2]
C = 2048//3; F = ImageFont.truetype(FONT, 130)
ZC = {'bleu': (47, 67, 115), 'vert': (88, 128, 60), 'rouge': (150, 58, 38)}; PARCH = (234, 218, 182); FOND_GRAS = (232, 213, 168); OR = (201, 149, 43); INK = (42, 24, 10)
def face(col, gras=None, bord=None):
    t = Image.new('RGB', (C, C), col); d = ImageDraw.Draw(t)
    d.rounded_rectangle((26, 26, C-27, C-27), radius=40, outline=bord or tuple(int(v*.55) for v in col), width=16)
    if gras is None: return t
    cx, cy = C/2, C/2-70; rx, ry = 120, 160
    d.line((cx, cy-ry-45, cx, cy+ry+45), fill=INK, width=18); d.line((cx-rx-50, cy, cx+rx+50, cy), fill=INK, width=18)
    d.ellipse((cx-rx, cy-ry, cx+rx, cy+ry), fill=(92, 58, 26) if gras else (139, 90, 43), outline=INK, width=16)
    d.ellipse((cx-rx+35, cy-ry+40, cx+rx-35, cy+ry-40), outline=(240, 224, 190), width=7)
    d.text((cx, C-110), 'Gras' if gras else 'Sec', font=F, fill=INK, anchor='mm')
    return t
POS = {2: (0, 0), 4: (1, 0), 5: (2, 0), 1: (0, 1), 3: (1, 1), 6: (2, 1)}
def atlas(faces, nom):          # faces : dict valeur -> image
    A = Image.new('RGB', (2048, 2048), (60, 60, 60))
    for v, im in faces.items():
        c, r = POS[v]; A.paste(im.rotate(180) if v in (1, 6) else im, (c*C, 2048-2*C+r*C))
    A.save(R+f'img/v18/{nom}.png')
atlas({1: face(ZC['bleu']), 6: face(ZC['bleu']), 2: face(ZC['vert']), 5: face(ZC['vert']), 3: face(ZC['rouge']), 4: face(ZC['rouge'])}, 'cdice_zones')
G = face(FOND_GRAS, 1, OR)   # fond des tuiles de gras (tuiles_v39 : FOND_GRAS, cadre OR)
atlas({1: G, 6: G, 2: face(PARCH, 0), 5: face(PARCH, 0), 3: face(PARCH, 0), 4: face(PARCH, 0)}, 'cdice_castor')
print('ok')
