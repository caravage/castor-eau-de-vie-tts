# Supprime le contour (noir ou blanc) des marqueurs : tout ce qui touche le bord prend la couleur du fond.
import sys
from PIL import Image
from collections import deque
def fond(im):
    w,h=im.size; return im.getpixel((w//2, int(h*0.09)))   # couleur de fond, près du haut, sous le contour
TH=8
def traite(src,dst):
    im=Image.open(src).convert('RGBA'); w,h=im.size; px=im.load()
    f=fond(im); # rejoindre la bande de fond
    near=lambda p: p[3]>200 and sum(abs(p[i]-f[i]) for i in range(3))<TH
    seen=[[False]*h for _ in range(w)]; q=deque()
    for x in range(w):
        for y in (0,h-1): q.append((x,y))
    for y in range(h):
        for x in (0,w-1): q.append((x,y))
    while q:
        x,y=q.popleft()
        if x<0 or y<0 or x>=w or y>=h or seen[x][y]: continue
        seen[x][y]=True
        if near(px[x,y]): continue
        px[x,y]=f
        q.extend(((x+1,y),(x-1,y),(x,y+1),(x,y-1)))
    im.convert('RGB').save(dst); print(dst,f)
for n in sys.argv[2:]: traite(f'{sys.argv[1]}/{n}.png', f'{n}_v47.png')
