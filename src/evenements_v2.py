# Tuiles « Événements du mois » v2 (7 nov. 2026) : d'après le tableau de « Cartes et tuiles ».
# Rouge = acte de guerre ou de violence. Flèche en boucle = la tuile retourne au sac (« +1 » : on ajoute une copie).
# v3 : titres seuls (le texte complet est dans la description TTS et l'aide de jeu) ; images evt3_*.
# v4 : icône du dé de région (dé beige, rond tricolore) ; Le Profond : 1er tirage = il part et la tuile revient, 2nd = il est retiré ; images evt4_*. Le Profond et Grand Hiver en noir (tableau du 7 nov.) ; Grand Hiver : cases Oct. et Mai rayées comme les mois de frasil : images evt6_*.
# Usage : python3 evenements_v2.py <racine du dépôt> <dossier node_modules/@fontsource>
import sys, html, math
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright
import os
DE = "<svg width='58' height='58' viewBox='0 0 58 58'><rect x='3' y='3' width='52' height='52' rx='10' fill='#F3EEE2' stroke='#2A2418' stroke-width='3'/><path d='M29 29 L29 13 A16 16 0 0 1 42.86 37 Z' fill='#2F4373'/><path d='M29 29 L42.86 37 A16 16 0 0 1 15.14 37 Z' fill='#6A9A48'/><path d='M29 29 L15.14 37 A16 16 0 0 1 29 13 Z' fill='#963A26'/></svg>"
def frasil(mois, i):
    # case de mois de frasil du calendrier (fond bleu pâle, rayures blanches et gris-bleu), dans le carré du dé de région
    pid = f'fr{i}'
    return (f"<svg width='62' height='62' viewBox='0 0 62 62'><defs><pattern id='{pid}' width='13' height='13' patternUnits='userSpaceOnUse' patternTransform='rotate(45)'>"
            "<rect width='13' height='13' fill='#D3E2EA'/><rect x='0' width='3' height='13' fill='#96A5BC'/><rect x='6.5' width='2.5' height='13' fill='#FFFFFF'/></pattern></defs>"
            f"<rect x='3' y='3' width='56' height='56' rx='10' fill='url(#{pid})' stroke='#2A2418' stroke-width='3'/>"
            "<text x='31' y='37' text-anchor='middle' font-family='IM Fell English SC' font-size='19' fill='#2A2418' stroke='#EEF4F7' stroke-width='4' paint-order='stroke'>"
            f"{mois}</text></svg>")
def profond(K, nav):
    ship = f"<img src='{nav}' style='width:52px'>"
    loop = (f"<svg width='34' height='34' viewBox='0 0 40 40'><path d='M30 9 A14 14 0 1 0 34 22' fill='none' stroke='{K}' stroke-width='4.5' stroke-linecap='round'/>"
            f"<path d='M22 3 L34 7 L29 17 Z' fill='{K}'/></svg>")
    barre = (f"<div style='position:relative;width:52px;height:46px'>{ship}<svg width='52' height='46' style='position:absolute;left:0;top:0' viewBox='0 0 52 46'>"
             "<path d='M8 6 L44 40 M44 6 L8 40' stroke='#8E2F25' stroke-width='4.5' stroke-linecap='round'/></svg></div>")
    n = lambda a, b: f"<span class='n'>{a}<sup>{b}</sup></span>"
    sep = f"<div style='width:2px;height:40px;background:{K};opacity:.4;margin:0 4px'></div>"
    return n('1', 'er') + ship + loop + sep + n('2', 'nd') + barre
R, F = sys.argv[1], sys.argv[2]
E = html.escape
ROUGE, NOIR, VERT = '#8E2F25', '#2A2622', '#4E7A2C'  # couleurs du tableau « Cartes et tuiles »
# clé, titre, texte, couleur, boucle ('' / 'boucle' / 'plus1')
EVT = [('hudson', 'Baie d’Hudson', 'Dé de région : retirez 1 peau de chaque zone de traite sans fort.', ROUGE, ''),
       ('abondante', 'Saison abondante', 'Dé de région : regarnissez chaque zone comme au printemps.', VERT, ''),
       ('profond', 'Le Profond', 'Pas en jeu : il part de La Rochelle au prochain mois sans frasil. En jeu : retirez‑le avec cette tuile.', NOIR, ''),
       ('hiver', 'Grand Hiver', 'Les prochains mois d’octobre et de mai deviennent des mois de frasil.', NOIR, ''),
       ('epidemie', 'Épidémie', 'Retirez 1 peau de chaque zone de traite de la Région qui a le plus de canots.', ROUGE, 'plus1'),
       ('epuise', 'Lac épuisé', 'Dé de région : la zone en Ravage ferme, puis Ravage sur la zone la moins garnie.', ROUGE, 'boucle')]
FONTS = f"""@font-face{{font-family:'IM Fell English SC';src:url(file://{F}/im-fell-english-sc/files/im-fell-english-sc-latin-400-normal.woff2)}}
@font-face{{font-family:'IM Fell English';font-style:italic;src:url(file://{F}/im-fell-english/files/im-fell-english-latin-400-italic.woff2)}}
@font-face{{font-family:'Alegreya Sans';font-weight:700;src:url(file://{F}/alegreya-sans/files/alegreya-sans-latin-700-normal.woff2)}}"""
CSS = (FONTS + "*{box-sizing:border-box;margin:0}body{width:300px;height:300px;overflow:hidden}"
       ".e{width:300px;height:300px;border-radius:22px;background:#F2EAD3;border:4px solid var(--k);display:flex;flex-direction:column;overflow:hidden;position:relative}"
       ".h{background:var(--k);color:#F6EFDC;font:400 20px 'IM Fell English SC',serif;letter-spacing:2px;text-align:center;padding:8px 0 6px}"
       ".b{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:4px 12px 10px;gap:6px}"
       ".t{font:italic 62px/1.0 'IM Fell English',serif;color:var(--k)}.x{font:700 30px/1.12 'Alegreya Sans',sans-serif;color:#2A2418}"
       ".ic{position:absolute;left:50%;bottom:14px;transform:translateX(-50%);display:flex;gap:5px;align-items:center}"
       ".n{font:italic 26px 'IM Fell English',serif;color:var(--k)}.n sup{font-size:15px}"
       ".lp{position:absolute;right:68px;bottom:34px;display:flex;align-items:center;gap:2px;color:var(--k);font:700 26px 'Alegreya Sans',sans-serif}")
def boucle(path, c):
    # même flèche que les tuiles Raid (raid_boucle.py)
    K = tuple(int(c[i:i+2], 16) for i in (1, 3, 5)); t = Image.open(path).convert('RGBA')
    S = 4; big = Image.new('RGBA', (t.width*S, t.height*S), (0, 0, 0, 0)); d = ImageDraw.Draw(big)
    cx, cy, r, w = 252*S, 252*S, 17*S, 4*S
    d.arc((cx-r, cy-r, cx+r, cy+r), start=-60, end=230, fill=K, width=w)
    a = math.radians(-60); ex, ey = cx+r*math.cos(a), cy+r*math.sin(a); tx, ty = -math.sin(a), math.cos(a); h = 9*S
    nx, ny = math.cos(a), math.sin(a)
    d.polygon([(ex-tx*h*0.2+nx*h*0.8, ey-ty*h*0.2+ny*h*0.8), (ex-tx*h*0.2-nx*h*0.8, ey-ty*h*0.2-ny*h*0.8), (ex+tx*h*1.1, ey+ty*h*1.1)], fill=K)
    t.alpha_composite(big.resize(t.size, Image.LANCZOS)); t.convert('RGB').save(path)
FIT = """() => { const b=document.querySelector('.b'), t=document.querySelector('.t'), x=document.querySelector('.x'); let s=30;
  const cs=getComputedStyle(b), room=b.clientHeight-parseFloat(cs.paddingTop)-parseFloat(cs.paddingBottom)-6;
  while (t.offsetHeight + x.offsetHeight > room && s > 18) { s -= 1; x.style.fontSize = s + 'px'; } return s; }"""
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(viewport={'width': 300, 'height': 300})
    for k, t, x, c, lp in EVT:
        extra = "<div class='lp'>+1</div>" if lp == 'plus1' else ''
        nav = 'file://' + os.path.abspath(R + 'src/assets/navire_noir.png')
        ic = DE if x.startswith('Dé de région') else (profond(c, nav) if k == 'profond' else (frasil('Oct.', 1) + frasil('Mai', 2) if k == 'hiver' else ''))
        if ic: extra += f"<div class='ic'>{ic}</div>"
        open('/tmp/evt2.html','w').write(f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body><div class='e' style='--k:{c}'>"
                       f"<div class='h'>Événement du mois</div><div class='b'{" style='padding-bottom:76px'" if (lp or x.startswith('Dé de région') or k in ('profond', 'hiver')) else ''}><div class='t'>{E(t)}</div></div>{extra}</div></body></html>"); pg.goto('file:///tmp/evt2.html')
        pg.evaluate('document.fonts.ready'); s = 62
        pg.screenshot(path=f'{R}img/v18/evt6_{k}.png', omit_background=False)
        if lp: boucle(f'{R}img/v18/evt6_{k}.png', c)
        print(k, s)
    br.close()
