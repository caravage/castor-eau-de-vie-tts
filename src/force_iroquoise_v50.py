# Force iroquoise v3.50 (16 nov. 2026) : le chiffre est imprimé sur l'image (7 états 0 à 6) au lieu d'un bouton Lua invisible ;
# les boutons − / + changent d'état. Usage : python3 force_iroquoise_v50.py <racine du dépôt> <dossier node_modules/@fontsource>
import sys
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont
R, F = sys.argv[1], sys.argv[2]
w2 = F + '/alegreya-sans/files/alegreya-sans-latin-700-normal.woff2'
t = TTFont(w2); t.flavor = None; t.save('/tmp/alegreya700.ttf')
font = ImageFont.truetype('/tmp/alegreya700.ttf', 104)
base = Image.open(R + 'img/v18/force_iroquoise_v47.png').convert('RGB')
for v in range(7):
    im = base.copy(); d = ImageDraw.Draw(im)
    d.text((200, 318), str(v), font=font, fill=(244, 238, 226), anchor='mm')
    im.save(R + f'img/v18/force_iroquoise_v50_{v}.png')
print('ok')
