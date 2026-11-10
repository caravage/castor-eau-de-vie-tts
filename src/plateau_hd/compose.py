from PIL import Image, ImageDraw
Image.MAX_IMAGE_PIXELS = None
S = 8000 / 5600; F = 2.490857
B = Image.open('board_hd.png').convert('RGB')
M = Image.open('map_hd.png').convert('RGB')
mx, my = 716 * S, 944 * S - 8 * F                      # origine css (0,-8) de la carte
X0, Y0, X1, Y1 = 718 * S, 935 * S, 5600 * S, 3560 * S
cx0, cy0 = round(X0 - mx), round(Y0 - my)
crop = M.crop((cx0, cy0, cx0 + round(X1 - X0), cy0 + round(Y1 - Y0)))
B.paste(crop, (round(X0), round(Y0)))
d = ImageDraw.Draw(B); DARK = (42, 36, 24)
def rect(x0, y0, x1, y1, w):
    d.rectangle((round(x0 * S), round(y0 * S), round(x1 * S), round(y1 * S)), outline=DARK, width=round(w * S))
rect(718 + 6, 935 + 6, 5600 - 7, 3560 - 7, 7)
rect(718 + 20, 935 + 20, 5600 - 21, 3560 - 21, 2)
B.save('table_hd.png', optimize=True)
print(B.size)
