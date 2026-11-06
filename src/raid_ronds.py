# Rivière : prix entouré d'un rond (sans le ₶) ; tuiles Raid ①②③ avec le même rond.
import sys
from PIL import Image, ImageDraw, ImageFont
R, FONT = sys.argv[1], sys.argv[2]
# 1. plateau
tb = Image.open(R+'img/v18/table_v17r.png').convert('RGB'); BG = (35, 27, 21); CREAM = (240, 228, 200)
d = ImageDraw.Draw(tb)
for cy, (dx0, dx1) in ((1725, (186, 202)), (2292, (186, 202)), (2864, (186, 202))):
    lt = tb.crop((212, cy-40, 240, cy+30)); d.rectangle((212, cy-40, 240, cy+30), fill=BG)
    tb.paste(lt, (226, cy-40))                       # ₶ décalé à droite
    cx = (dx0+dx1)//2; r = 20
    d.ellipse((cx-r, cy-r, cx+r, cy+r), outline=CREAM, width=3)
tb.save(R+'img/v18/table_v17r.png')
# 2. tuiles Raid
base = Image.open(R+'img/v18/evt_raid.png').convert('RGB'); K = (142, 47, 37); P = base.getpixel((150, 240))
f = ImageFont.truetype(FONT, 46)
for n in (1, 2, 3):
    t = base.copy(); ti = t.crop((20, 95, 280, 236)); dd = ImageDraw.Draw(t)
    dd.rectangle((20, 82, 280, 290), fill=P); t.paste(ti, (20, 75))
    cx, cy, r = 150, 248, 28
    dd.ellipse((cx-r, cy-r, cx+r, cy+r), outline=K, width=4)
    dd.text((cx, cy), str(n), font=f, fill=K, anchor='mm')
    t.save(R+f'img/v18/evt_raid{n}.png')
print('ok')
