# Piste Livres v3.28 : retire les étiquettes « +X capital » et imprime, sous la piste, la valeur « capital »
# de chaque case (variante C : chiffre seulement là où la valeur change, point discret sinon).
# Même barème que le Lua (CAPL dans plateau_joueur_v3.py).
# Usage : python3 livres_capital.py <image source> <image cible> <police Alegreya Sans 500 .ttf> <police Alegreya Sans 400 italique .ttf>
import sys
from PIL import Image, ImageDraw, ImageFont
SRC, DST, F500, F400I = sys.argv[1:5]
V = [0, 1, 2, 3, 4, 5, 6, 7, 7, 8, 9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 14, 14, 15, 15, 15, 15, 15, 15, 15, 15]
BG, COUL, POINT = (230, 218, 182), (139, 112, 74), (190, 172, 134)
OX, OY = 700, 3580                       # coin du repère de la piste dans le plateau 5600 px
X0, X1, N = 346, 3699, 31                # bord gauche de la case 0 et bord droit de la case 30+
im = Image.open(SRC).convert('RGB'); d = ImageDraw.Draw(im)
d.rectangle([OX + 330, OY, OX + 3720, OY + 90], fill=BG)          # étiquettes « +X capital »
f, fl = ImageFont.truetype(F500, 34), ImageFont.truetype(F400I, 34)
pas = (X1 - X0) / N
for i, v in enumerate(V):
    cx = OX + X0 + pas * (i + 0.5)
    if i == 0 or v != V[i - 1]:
        t = str(v); w = d.textlength(t, font=f); d.text((cx - w / 2, OY + 206), t, font=f, fill=COUL)
    else:
        d.line([cx - 2, OY + 222, cx + 2, OY + 222], fill=POINT, width=4)
d.text((OX + 52, OY + 206), 'capital', font=fl, fill=COUL)
im.save(DST, optimize=True)
print(DST)
