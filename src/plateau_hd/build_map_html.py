# Carte HD : découpe la source vectorielle (carte_src.html) en deux calques
#  - base.html : fond, collines, étendues (teinte pleine), lacs, rivières  -> passe terrain / forêts
#  - over.html : tout le reste (cartouches, liaisons, portages, textes, encarts), fond transparent
# en reprenant les corrections du plateau v3.32 (bandeaux, symboles des Régions, rapides, ancres, rose, légende).
import re, math
import numpy as np
from PIL import Image

SRC = open('carte_src.html').read()
head_end = SRC.index('<div style="position: relative; width: 3215px')
root_open = re.match(r'<div style="position: relative;[^>]*>', SRC[head_end:]).group(0)
body = SRC[head_end + len(root_open):]

# ---- découpe en éléments de premier niveau
VOID = {'img', 'br', 'meta', 'link', 'input'}
items = []; depth = 0; start = None; i = 0
tagre = re.compile(r'<(/?)([a-zA-Z][a-zA-Z0-9-]*)([^>]*?)(/?)>')
for m in tagre.finditer(body):
    close, tag, _, selfc = m.group(1), m.group(2).lower(), m.group(3), m.group(4)
    if depth == 0 and not close:
        if tag in VOID or selfc:
            items.append(body[m.start():m.end()]); continue
        start = m.start(); depth = 1; continue
    if depth > 0:
        if tag in VOID or selfc: continue
        if close: depth -= 1
        else: depth += 1
        if depth == 0:
            items.append(body[start:m.end()])
    if tag == 'div' and close and depth < 0: break
items = [it for it in items if it.strip()]
print('éléments :', len(items))

def has(it, s): return s in it
# indices (voir inventaire) : 0 fond, 1 sapins, 2 collines, 3-5 étendues, eau = fill/stroke #9DBDC2 hors encarts
BASE, OVER = [], []
for k, it in enumerate(items):
    if k == 1: continue                                     # anciens sapins : remplacés par la passe forêts
    if k == 0 or k == 2 or k in (3, 4, 5):
        BASE.append(it); continue
    water = ('fill="#9DBDC2"' in it or 'stroke="#9DBDC2"' in it) and it.startswith('<svg') and 'overflow: hidden' not in it
    if water: BASE.append(it)
    else: OVER.append(it)

# ---- étendues : hachures retirées (teinte pleine, ombre intérieure et contour conservés)
def flat(it):
    return re.sub(r'<path d="M-?[\d.]+ -?[\d.]+ L-?[\d.]+ -?[\d.]+"[^>]*stroke="#8A5A1C"[^>]*stroke-width="1"[^>]*></path>', '', it)
BASE = [flat(it) if 'fill="#C98F3E"' in it else it for it in BASE]
OVER_FLAT = True

OVER = [flat(it) if 'fill="#C98F3E"' in it else it for it in OVER]
# ---- cartouches
REG = {'Nipigon': 'mishipeshu', 'Michipicoten': 'mishipeshu', 'Chagouamigon': 'mishipeshu',
       'Baie des Puants': 'tortue', 'Michilimackinac': 'tortue', 'Saint-Joseph': 'tortue',
       'Niagara': 'oniare', 'Fort Frontenac': 'oniare'}
INK = {'mishipeshu': (0x4A, 0x6C, 0xC0), 'tortue': (0x5E, 0x94, 0x40), 'oniare': (0xB5, 0x45, 0x2C)}
for k in INK:                                               # silhouettes teintées, opacité 0,117 (= rendu du plateau)
    a = np.array(Image.open(f'img/region_{k}.png').convert('RGBA')).astype(int)
    m = (a[:, :, 0] > 190) & (a[:, :, 1] > 180) & (a[:, :, 3] > 200)
    ys, xs = np.nonzero(m); m = m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    mi = Image.fromarray((m * 255).astype('uint8')).resize((m.shape[1] * 2, m.shape[0] * 2), Image.LANCZOS)
    mi = mi.filter(__import__('PIL.ImageFilter', fromlist=['x']).GaussianBlur(1.2))
    al = (np.array(mi).astype(float) / 255 * 0.117 * 255).astype('uint8')
    out = np.zeros(al.shape + (4,), 'uint8'); out[..., :3] = INK[k]; out[..., 3] = al
    Image.fromarray(out).save(f'img/sym_{k}.png')
    print(k, 'silhouette', mi.size)
SYM = {k: Image.open(f'img/sym_{k}.png').size for k in INK}

def cartouche(it):
    m = re.search(r'white-space: nowrap; text-align: center;?">([^<]+)</div>', it)
    if not m: return it
    name = m.group(1)
    if name not in REG: return it                           # Témiscamingue : gravure conservée
    col = re.search(r'border-bottom: 5px double (#[0-9A-Fa-f]{6})', it).group(1)
    it = it.replace(f'color-mix(in srgb, {col} 40%, transparent)', f'color-mix(in srgb, {col} 18%, #F3EEE2)')
    k = REG[name]; w, h = SYM[k]; s = min(132 / h, 172 / w); W_, H_ = w * s, h * s
    x = (313.6 - W_) / 2; y = 50.4 + 4.3 + (264 - 50.4 - 4.3 - H_) / 2
    img = f'<img src="img/sym_{k}.png" alt="" style="position: absolute; left: {x:.1f}px; top: {y:.1f}px; width: {W_:.1f}px; height: {H_:.1f}px">'
    it = re.sub(r'<img src="img/6d65d480a22e58080b17f74a7076215f.png"[^>]*>', img, it, count=1)
    return it
def cartouches(it):
    parts = re.split(r'(?=<div style="position: absolute; left: [-\d.]+px; top: [-\d.]+px; width: 313.6px; height: 264.0px)', it)
    return ''.join(cartouche(p) for p in parts)
OVER = [cartouches(it) for it in OVER]

# ---- portages : fond parchemin uni ; rapides : flèche de remontée + deux rangs de chevrons
RAP = {'Saint-Laurent': (-0.87, 0.5), 'Rivière des Outaouais': (-1, 0), 'Sault Sainte-Marie': (-0.8, -0.6), 'Chutes du Niagara': None}
BLUE = '#4E8C99'
def arrow(cx, cy, ux, uy, L, w, hd):
    n = math.hypot(ux, uy); ux, uy = ux / n, uy / n; px, py = -uy, ux
    x0, y0 = cx - ux * L / 2, cy - uy * L / 2; x1, y1 = cx + ux * L / 2, cy + uy * L / 2
    bx, by = x1 - ux * hd, y1 - uy * hd
    return (f'<line x1="{x0:.2f}" y1="{y0:.2f}" x2="{bx:.2f}" y2="{by:.2f}" stroke="{BLUE}" stroke-width="{w}"/>'
            f'<polygon points="{x1:.2f},{y1:.2f} {bx + px * hd * .6:.2f},{by + py * hd * .6:.2f} {bx - px * hd * .6:.2f},{by - py * hd * .6:.2f}" fill="{BLUE}"/>')
def chevrons(cx, y0, rows=((5, 0), (4, 1)), sp=11.47, w=9.18, h=4.59, sw=1.72, dy=8.6):
    out = ''
    for n, r in rows:
        y = y0 + r * dy; x0 = cx - n * sp / 2 + 1.15
        pts = ' '.join(f'{x0 + i * sp:.2f},{y + h:.2f} {x0 + i * sp + w / 2:.2f},{y:.2f} {x0 + i * sp + w:.2f},{y + h:.2f}' for i in range(n))
        for i in range(n):
            xa = x0 + i * sp
            out += f'<polyline points="{xa:.2f},{y + h:.2f} {xa + w / 2:.2f},{y:.2f} {xa + w:.2f},{y + h:.2f}" fill="none" stroke="{BLUE}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"/>'
    return out
def portage(it):
    m = re.match(r'<div style="(position: absolute; left: [-\d.]+px; top: [-\d.]+px; width: 118.0px; height: 118.0px;[^"]*)"', it)
    if not m: return it
    st = m.group(1)
    st2 = re.sub(r'background(-image)?:[^;]*;?', '', st)
    st2 += '; background: #F4F0E4'
    it = it.replace(st, st2, 1)
    it = re.sub(r'<svg[^>]*>.*?</svg>', '', it, flags=re.S) if 'pattern' in it or 'repeating-linear' in it else it
    name = re.sub(r'<[^>]+>', ' ', it); name = ' '.join(name.split())
    key = next((k for k in RAP if k.replace('-', '').replace(' ', '') in name.replace('-', '').replace(' ', '')), None)
    if key:
        c = 59.0
        g = arrow(c - 10.3, c - 36.7, -1, 0, 20.6, 3.44, 10.3) + arrow(c + 10.3, c - 36.7, 1, 0, 20.6, 3.44, 10.3) if RAP[key] is None \
            else arrow(c, c - 36.7, *RAP[key], 34.4, 3.44, 11.5)
        g += chevrons(c, c + 26.4)
        svg = f'<svg viewBox="0 0 118 118" style="position: absolute; left: 0; top: 0; width: 118px; height: 118px; overflow: visible; pointer-events: none">{g}</svg>'
        it = it[:it.rindex('</div>')] + svg + '</div>'
    return it
OVER = [portage(it) for it in OVER]

# ---- ancres des étendues : brun, plus petites
OVER = [re.sub(r'width: 22.7px; height: 22.7px; border-radius: 50%; background: #C98F3E; border: 3.1px solid #2A2418',
               'width: 17.2px; height: 17.2px; margin: 2.75px 0 0 2.75px; border-radius: 50%; background: #785A32; border: 1.72px solid #2A2418', it) for it in OVER]

# ---- encarts reconstruits (Congés, rade de Québec, La Rochelle, Antilles) — vectoriels
def card_frame(x, y, w, h, s, radius=10, inner=7.5):
    return (f'<div style="position: absolute; left: {x}px; top: {y}px; width: {w}px; height: {h}px; box-sizing: border-box; '
            f'background: #F2EAD3; border: {2 * s:.2f}px solid #B7A675; border-radius: {radius * s:.2f}px">'
            f'<div style="position: absolute; left: {inner * s - 2 * s:.2f}px; top: {inner * s - 2 * s:.2f}px; right: {inner * s - 2 * s:.2f}px; bottom: {inner * s - 2 * s:.2f}px; '
            f'border: {1.2 * s:.2f}px solid #CDC3A8; border-radius: {(radius - 4) * s:.2f}px"></div>')
def grid(x, y, s, cols, rows, title, tsize, ty):
    # cols / rows : bornes en px de l'image d'origine ; s = px css par px image
    h = ''
    for r0, r1 in rows:
        cy = (r0 + r1) / 2
        h += f'<div style="position: absolute; left: {cols[0][1] * s:.2f}px; top: {cy * s - 1.2 * s:.2f}px; width: {(cols[-1][0] - cols[0][1]) * s:.2f}px; height: {2.4 * s:.2f}px; background: #C5B78C"></div>'
        for j, (c0, c1) in enumerate(cols):
            bg = '#EBE1CA' if j == 0 else '#F8F2E2'
            ship = (f'<img src="img/navire_gravure.png" alt="" style="position: absolute; left: 12%; top: 12%; width: 76%; height: 76%; object-fit: contain; opacity: 0.32">' if j == 0 else '')
            h += (f'<div style="position: absolute; left: {c0 * s:.2f}px; top: {r0 * s:.2f}px; width: {(c1 - c0) * s:.2f}px; height: {(r1 - r0) * s:.2f}px; box-sizing: border-box; '
                  f'background: {bg}; border: {3 * s:.2f}px solid #C2B07C; border-radius: {11 * s:.2f}px; overflow: hidden">{ship}</div>')
    h += (f'<div style="position: absolute; left: 0; top: {ty * s:.2f}px; width: 100%; text-align: center; font-family: \'IM Fell English SC\', serif; '
          f'font-size: {tsize * s:.2f}px; line-height: 1; color: #2A2418">{title}</div>')
    return h
REPL = {}
s = 452.6 / 720   # Québec
qc = [(26, 136), (151, 247), (262, 358), (373, 469), (484, 580), (595, 690)]
rows = [(101, 200), (221, 320), (341, 440), (461, 560)]
REPL['Rade de Québec'] = card_frame(2325, 396, 452.6, 582 * s, s) + grid(2325, 396, s, qc, rows, 'Québec', 40, 34) + '</div>'
s = 242.7 / 386   # La Rochelle
lr = [(29, 139), (154, 250), (265, 361)]
REPL['Rade de La Rochelle'] = card_frame(2534.9, 817, 242.7, 582 * s, s) + grid(2534.9, 817, s, lr, rows, 'La Rochelle', 50, 36) + '</div>'
s = 238.9 / 380   # Congés
REPL['Congés'] = (card_frame(2016, 396, 238.9, 320 * s, s) +
    f'<img src="img/embleme_conges.png" alt="" style="position: absolute; left: 50%; top: {28 * s:.1f}px; height: {282 * s:.1f}px; transform: translateX(-50%); opacity: 0.30; filter: grayscale(1) sepia(0.25)">'
    f'<div style="position: absolute; left: {20 * s:.1f}px; top: {14 * s:.1f}px; font-family: \'IM Fell English\', serif; font-style: italic; font-size: {38 * s:.1f}px; line-height: 1.1; color: #2A2418">Congés</div></div>')
s = 242.7 / 386   # Antilles
REPL['Antilles'] = (card_frame(2534.9, 1280, 242.7, 130, s) +
    f'<img src="img/antilles_filigrane.png" alt="" style="position: absolute; left: {6 * s:.1f}px; top: {6 * s:.1f}px; width: calc(100% - {12 * s:.1f}px); height: calc(100% - {12 * s:.1f}px); object-fit: cover; opacity: 0.2; filter: grayscale(1) sepia(0.3); border-radius: {6 * s:.1f}px">'
    f'<div style="position: absolute; left: 0; top: 0; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; font-family: \'IM Fell English SC\', serif; font-size: {44 * s:.1f}px; color: #2A2418">Antilles</div></div>')
def repl(it):
    m = re.match(r'<img src="img/[0-9a-f]{32}\.png" alt="([^"]+)"', it)
    return REPL[m.group(1)] if m and m.group(1) in REPL else it
OVER = [repl(it) for it in OVER]

# ---- rose des vents et légende (positions du plateau v3.32, en px css de la carte)
K = 1.7436; OX, OY = 716, 944
def css(x, y): return ((x - OX) / K, (y - OY) / K)
cx, cy = css(1480, 1140); R = 85 / K; g = ''
for i in range(16):
    ang = i * math.pi / 8; L = R if i % 4 == 0 else (R * 0.62 if i % 2 == 0 else R * 0.38); w = (12 if i % 4 == 0 else 8) / K
    p = (cx + L * math.sin(ang), cy - L * math.cos(ang))
    l = (cx + w * math.sin(ang - math.pi / 2), cy - w * math.cos(ang - math.pi / 2))
    r = (cx + w * math.sin(ang + math.pi / 2), cy - w * math.cos(ang + math.pi / 2))
    g += f'<polygon points="{p[0]:.2f},{p[1]:.2f} {l[0]:.2f},{l[1]:.2f} {cx:.2f},{cy:.2f}" fill="#2A2418"/>'
    g += f'<polygon points="{p[0]:.2f},{p[1]:.2f} {r[0]:.2f},{r[1]:.2f} {cx:.2f},{cy:.2f}" fill="#F4F0E4" stroke="#2A2418" stroke-width="0.6" stroke-linejoin="round"/>'
g += f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{R + 10 / K:.2f}" fill="none" stroke="#2A2418" stroke-width="{2 / K:.2f}"/>'
g += f'<text x="{cx:.2f}" y="{cy - R - 16 / K:.2f}" text-anchor="middle" font-family="Alegreya Sans" font-weight="500" font-size="{30 / K:.2f}" fill="#2A2418">N</text>'
ROSE = f'<svg viewBox="0 0 2800 1500" style="position: absolute; left: 0; top: 0; width: 2800px; height: 1500px; overflow: visible; pointer-events: none">{g}</svg>'
X0, Y0 = css(3990, 3215); X1, Y1 = css(4680, 3495)
lc, ly = 95 / K, 75 / K
leg = (f'<div style="position: absolute; left: {X0:.1f}px; top: {Y0:.1f}px; width: {X1 - X0:.1f}px; height: {Y1 - Y0:.1f}px; box-sizing: border-box; background: #F3EFE2; '
       f'border: {3 / K:.2f}px solid #968C78; border-radius: {18 / K:.1f}px; font-family: \'Alegreya Sans\', sans-serif; color: #2A2418">')
gl = f'<circle cx="{lc:.2f}" cy="{ly:.2f}" r="{52 / K:.2f}" fill="#F4F0E4" stroke="#2A2418" stroke-width="{3 / K:.2f}"/>'
gl += arrow(lc, ly - 18 / K, -1, 0, 44 / K, 5 / K, 15 / K)
gl += chevrons(lc, ly + 8 / K, rows=((3, 0), (2, 1)), sp=16 / K, w=12 / K, h=6 / K, sw=3 / K, dy=12 / K)
y2 = 205 / K; dash = ''
x = 30 / K; xe = 160 / K
while x < xe:
    dash += f'<line x1="{x:.2f}" y1="{y2:.2f}" x2="{min(x + 22 / K, xe):.2f}" y2="{y2:.2f}" stroke="#2A2418" stroke-width="{4 / K:.2f}"/>'; x += 32 / K
    if x < xe: dash += f'<circle cx="{x:.2f}" cy="{y2:.2f}" r="{3 / K:.2f}" fill="#2A2418"/>'; x += 13 / K
dash += f'<polyline points="{83 / K:.2f},{y2 - 11 / K:.2f} {97 / K:.2f},{y2:.2f} {83 / K:.2f},{y2 + 11 / K:.2f}" fill="none" stroke="#2A2418" stroke-width="{4 / K:.2f}" stroke-linejoin="round"/>'
leg += f'<svg style="position: absolute; left: 0; top: 0; width: 100%; height: 100%; overflow: visible">{gl}{dash}</svg>'
fs, fi = 46 / K, 40 / K
for yy, word, dd in ((ly, 'Rapide', '2+'), (y2, 'Raccourci', '3+')):
    leg += (f'<div style="position: absolute; left: {185 / K:.1f}px; top: {yy - fs * 0.62:.1f}px; font-size: {fs:.2f}px; font-weight: 500; line-height: 1.2; white-space: nowrap">{word}</div>'
            f'<div style="position: absolute; left: {375 / K:.1f}px; top: {yy - fs * 0.62:.1f}px; font-size: {fs:.2f}px; font-weight: 500; line-height: 1.2">{dd}</div>'
            f'<div style="position: absolute; left: {450 / K:.1f}px; top: {yy - fi * 0.60:.1f}px; font-size: {fi:.2f}px; font-style: italic; line-height: 1.2; white-space: nowrap">1 : abîmé</div>')
leg += '</div>'
OVER += [ROSE, leg]

exec(open('bloc_v3.py').read())
OVER=[it for it in OVER if not (it.startswith('<div') and ('>Congés</div>' in it or '>Québec</div>' in it) and 'card' not in it and 'Montréal' not in it)]
OVER=[it for it in OVER if 'M2135 311 L2135 636' not in it]                 # ancien pointillé Domaine–Montréal
mi=next(i for i,it in enumerate(OVER) if '>Montréal</div>' in it)
OVER[mi]=BLOC                                                              # remplace l'ancienne capsule Montréal
mv=lambda it,dx,dy:f'<div style="position:absolute;left:0;top:0;transform:translate({dx}px,{dy}px)">{it}</div>'
for i,it in enumerate(OVER):
    if 'viewBox="1773 40 367 304"' in it or ('left: 1937px; top: 19px' in it and 'Domaine du Roi' in it): OVER[i]=mv(it,-352,-8)
    elif 'left: 2447.6px; top: 780px' in it or 'left: 2447.6px; top: 1250px' in it or 'left: 2534.9px; top: 817' in it or 'left: 2534.9px; top: 1280' in it: OVER[i]=mv(it,0,30)
OVER.append('<svg viewBox="0 0 3215 1500" style="position:absolute;left:0;top:0;width:3215px;height:1500px;overflow:visible"><path d="M1982 150 L2003 150" stroke="#4A4640" stroke-width="3.02" stroke-dasharray="9 7"/></svg>')
# ---- pages
HEAD = ('<!doctype html><html lang="fr"><head><meta charset="utf-8"><link rel="stylesheet" href="fonts.css"><style>'
        'html,body{margin:0;background:transparent} .root{position:relative;width:2800px;height:1510px;overflow:hidden;font-family:"Liberation Serif",serif}'
        '.in{position:absolute;left:0;top:8px;width:3215px;height:1500px}</style></head><body>')
def page(parts, bg):
    return HEAD + f'<div class="root" style="background:{bg}"><div class="in">' + '\n'.join(parts) + '</div></div></body></html>'
open('base.html', 'w').write(page(BASE, '#D8C99C'))
open('hills.html', 'w').write(page([items[2]], 'transparent'))
open('over.html', 'w').write(page(OVER, 'transparent'))
print('base', len(BASE), 'over', len(OVER))
