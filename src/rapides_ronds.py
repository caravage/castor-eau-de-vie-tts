# Raid : ronds ①②③ sur les trois rapides (① Saint-Laurent, ② Rivière des Outaouais, ③ Sault Sainte-Marie).
import sys, math
from PIL import Image, ImageDraw, ImageFont
R, FONT, IMG = sys.argv[1], sys.argv[2], sys.argv[3]
T = Image.open(R+IMG).convert('RGB'); K = (142, 47, 37); BG = (243, 238, 226)
f = ImageFont.truetype(FONT, 44)
RAP = {1: ((4262, 2490), 135), 2: ((4048, 2217), 135), 3: ((2440, 1930), 228)}   # centre du rapide, angle du rond (degrés, sens écran)
S = 4; big = Image.new('RGBA', (T.width, T.height), (0, 0, 0, 0))
for n, ((cx, cy), ang) in RAP.items():
    a = math.radians(ang); bx, by = cx+math.cos(a)*92, cy-math.sin(a)*92; r = 30
    tile = Image.new('RGBA', (r*2*S+8*S, r*2*S+8*S), (0, 0, 0, 0)); d = ImageDraw.Draw(tile); o = 4*S
    d.ellipse((o, o, o+2*r*S, o+2*r*S), fill=BG+(255,), outline=K, width=5*S)
    tile = tile.resize((tile.width//S, tile.height//S), Image.LANCZOS)
    big.alpha_composite(tile, (int(bx-r-4), int(by-r-4)))
    ImageDraw.Draw(big).text((bx, by+1), str(n), font=f, fill=K, anchor='mm')
T = T.convert('RGBA'); T.alpha_composite(big); T.convert('RGB').save(R+IMG)
print('ok')
