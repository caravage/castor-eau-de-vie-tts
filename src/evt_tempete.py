# Tuile « Tempête » (16 nov. 2026) : Événement du mois noir, gabarit de evenements_v2.py (comme Grand Hiver),
# icône nuage d'orage avec éclair, navire, puis faces de dé 1 et 2 (navires en traversée coulés sur 1 ou 2) ;
# 2e ligne : mini tuile Rivière calme → nuage = si Rivière calme sort à la fin du mois suivant, la tempête continue.
# Usage : python3 evt_tempete.py <racine du dépôt> <dossier node_modules/@fontsource>
import sys, os
R, F = sys.argv[1], sys.argv[2]
src = open(R + 'src/evenements_v2.py').read()
ns = {'__name__': 'tempete'}; sys.argv = [sys.argv[0], R, F]
exec(src[:src.index('FIT = ')], ns)          # CSS, polices
from playwright.sync_api import sync_playwright
K = '#2A2418'
NUAGE = (f"<svg width='104' height='84' viewBox='0 0 74 60'>"
         f"<path d='M18 40 C6 40 4 26 15 23 C15 11 31 7 37 16 C42 6 60 8 59 22 C70 23 70 40 58 40 Z' fill='{K}'/>"
         f"<path d='M38 36 L29 50 L36 50 L31 60 L45 45 L38 45 L43 36 Z' fill='#C99A2E'/></svg>")
def de(n):
    pips = {1: [(16, 16)], 2: [(9, 9), (23, 23)]}[n]
    p = ''.join(f"<circle cx='{x}' cy='{y}' r='3.6' fill='#F2EAD3'/>" for x, y in pips)
    return f"<svg width='46' height='46' viewBox='0 0 32 32'><rect x='1' y='1' width='30' height='30' rx='6' fill='{K}'/>{p}</svg>"
CALME = '#6F8C99'
MINI = (f"<svg width='50' height='50' viewBox='0 0 50 50'><rect x='2' y='2' width='46' height='46' rx='7' fill='#F2EAD3' stroke='{CALME}' stroke-width='3'/>"
        f"<path d='M2 9 Q2 2 9 2 L41 2 Q48 2 48 9 L48 13 L2 13 Z' fill='{CALME}'/>"
        f"<path d='M10 27 q4 -5 8 0 t8 0 t8 0 t8 0 M10 36 q4 -5 8 0 t8 0 t8 0 t8 0' fill='none' stroke='{CALME}' stroke-width='2.6' stroke-linecap='round'/></svg>")
FLECHE = f"<svg width='30' height='20' viewBox='0 0 30 20'><path d='M2 10 H22' stroke='{K}' stroke-width='3'/><path d='M20 3 L29 10 L20 17 Z' fill='{K}'/></svg>"
PETIT = NUAGE.replace("width='104' height='84'", "width='62' height='50'")
NUAGE = NUAGE.replace("width='104' height='84'", "width='80' height='65'")
NAV = f"<img src='file://{os.path.abspath(R + 'src/assets/navire_noir.png')}' style='width:56px'>"
html = (f"<!doctype html><html><head><meta charset='utf-8'><style>{ns['CSS']}</style></head><body><div class='e' style='--k:{K}'>"
        "<div class='h'>Événement du mois</div><div class='b'><div class='t' style='font-size:54px'>Tempête</div>"
        f"<div style='display:flex;align-items:center;gap:9px'>{NUAGE}{NAV}{de(1)}{de(2)}</div>"
        f"<div style='display:flex;align-items:center;gap:8px;margin-top:-2px'>{MINI}{FLECHE}{PETIT}</div></div></div></body></html>")
open('/tmp/tempete.html', 'w').write(html)
with sync_playwright() as p:
    br = p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg = br.new_page(viewport={'width': 300, 'height': 300})
    pg.goto('file:///tmp/tempete.html'); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(300)
    out = R + 'img/v18/evt7_tempete.png'; pg.screenshot(path=out); br.close()
print(out)
