# Tuiles « Événements du mois » v2 (7 nov. 2026) : d'après le tableau de « Cartes et tuiles ».
# Rouge = acte de guerre ou de violence. Flèche en boucle = la tuile retourne au sac (« +1 » : on ajoute une copie).
# v3 : titres seuls (le texte complet est dans la description TTS et l'aide de jeu) ; images evt3_*.
# Usage : python3 evenements_v2.py <racine du dépôt> <dossier node_modules/@fontsource>
import sys, html, math
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright
R, F = sys.argv[1], sys.argv[2]
E = html.escape
ROUGE, BLEU, FROID, VERT = '#8E2F25', '#2F5E8E', '#4A6A82', '#4E7A2C'
# clé, titre, texte, couleur, boucle ('' / 'boucle' / 'plus1')
EVT = [('hudson', 'Baie d’Hudson', 'Dé de région : retirez 1 peau de chaque zone de traite sans fort.', ROUGE, ''),
       ('abondante', 'Saison abondante', 'Dé de région : regarnissez chaque zone comme au printemps.', VERT, ''),
       ('profond', 'Le Profond', 'Pas en jeu : il part de La Rochelle au prochain mois sans frasil. En jeu : retirez‑le avec cette tuile.', BLEU, ''),
       ('hiver', 'Grand Hiver', 'Les prochains mois d’octobre et de mai deviennent des mois de frasil.', FROID, ''),
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
        open('/tmp/evt2.html','w').write(f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body><div class='e' style='--k:{c}'>"
                       f"<div class='h'>Événement du mois</div><div class='b'{" style='padding-bottom:40px'" if lp else ''}><div class='t'>{E(t)}</div></div>{extra}</div></body></html>"); pg.goto('file:///tmp/evt2.html')
        pg.evaluate('document.fonts.ready'); s = 62
        pg.screenshot(path=f'{R}img/v18/evt3_{k}.png', omit_background=False)
        if lp: boucle(f'{R}img/v18/evt3_{k}.png', c)
        print(k, s)
    br.close()
