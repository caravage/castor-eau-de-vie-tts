# Plaquette « Ferme du castor » v3.53 : source vectorielle refaite à l'identique de ferme_recto_v8 (dont le générateur n'était pas au dépôt),
# polices IM Fell + Alegreya Sans (au lieu de la police de repli), politiques d'achat sur deux lignes. 1500 × 1200 px.
# Mêmes positions des cases que la v8 (aucun point d'accroche sur cette plaquette). Usage (depuis src/) : python3 ferme_v53.py <sortie.png>
import sys
from playwright.sync_api import sync_playwright
from polices import CSS, CHROME
INK, BORD, RING, FILL, BOX = '#2A2418', '#4A3B28', '#B8A672', '#EFE6CC', '#F2E9D2'
def boite(x, y, w, h, titre, inner):
    return (f"<div style='position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{BOX};border:2px solid {BORD};border-radius:16px'>"
            f"<div style='position:absolute;left:0;right:0;top:12px;display:flex;align-items:center;justify-content:center;gap:22px'>"
            f"<div style='width:104px;height:2px;background:{INK}'></div><div style=\"font:italic 40px/1.1 'IM Fell English';color:{INK}\">{titre}</div>"
            f"<div style='width:104px;height:2px;background:{INK}'></div></div>{inner}</div>")
def rond(cx, cy, r=50): return (f"<div style='position:absolute;left:{cx-r}px;top:{cy-r}px;width:{2*r}px;height:{2*r}px;border-radius:50%;background:{FILL};"
                                f"border:3px solid {RING};box-shadow:inset 0 0 0 4px {BOX},inset 0 0 0 6px {RING}'></div>")
def carre(cx, cy, s=90): return (f"<div style='position:absolute;left:{cx-s/2}px;top:{cy-s/2}px;width:{s}px;height:{s}px;border-radius:10px;background:{FILL};"
                                 f"border:3px solid {RING};box-shadow:inset 0 0 0 4px {BOX},inset 0 0 0 6px {RING}'></div>")
def num(cx, y, t, c=BORD): return f"<div style=\"position:absolute;left:{cx-60}px;top:{y}px;width:120px;text-align:center;font:700 40px/1 'Alegreya Sans';color:{c}\">{t}</div>"
def pointille(x, y, w, h): return f"<div style='position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border:3px dashed {RING};border-radius:14px'></div>"
# coordonnées internes à chaque boîte (origine : coin de la boîte, bordure comprise)
prix = ''.join(rond(111 + 146 * k, 121) + num(111 + 146 * k, 182, k + 2) for k in range(9))
POL = (('Prix fixe', ''), ('Rationnement', 'quantitatif'), ('Rationnement', 'qualitatif'), ('Commerce', 'libre'))
pol = ''.join(f"<div style='position:absolute;left:{190 + 337 * k - 44}px;top:62px;width:88px;height:88px;border-radius:50%;border:3px dashed {RING};background:{FILL}'></div>"
              f"<div style=\"position:absolute;left:{190 + 337 * k - 160}px;top:{156 if b else 170}px;width:320px;text-align:center;font:400 29px/1.0 'IM Fell English SC';color:{INK}\">{a}{'<br>' + b if b else ''}</div>"
              for k, (a, b) in enumerate(POL))
dette = ''.join(carre(135.5 + 134 * k, 114.5) + num(135.5 + 134 * k, 166, 2 - k) for k in range(3))
pros = ''.join(rond(146.5 + 134 * k, 114.5, 45) + num(146.5 + 134 * k, 166, k, '#A3352A' if k == 0 else BORD) for k in range(5))
html = (f"<!doctype html><meta charset=utf-8><style>{CSS}*{{box-sizing:border-box;margin:0}}body{{background:transparent}}</style>"
        "<div style='position:relative;width:1500px;height:1200px;background:#22332F;border-radius:44px'>"
        "<div style='position:absolute;left:14px;top:14px;right:14px;bottom:14px;background:#E6DAB6;border-radius:32px'></div>"
        "<div style='position:absolute;left:54px;top:36px;width:506px;height:84px;background:#5C3A1A;clip-path:polygon(5% 0,95% 0,100% 50%,95% 100%,5% 100%,0 50%);"
        "display:flex;align-items:center;justify-content:center;font:400 58px \"IM Fell English SC\";color:#F4EBD6'>Ferme du castor</div>"
        + boite(54, 136, 1392, 242, 'Prix en France', prix) + boite(54, 394, 1392, 220, 'Politique d’achat', pol)
        + boite(54, 630, 539, 224, 'Dette', dette) + boite(616, 630, 830, 224, 'Prospérité', pros)
        + boite(54, 870, 539, 288, 'Caisse', pointille(22, 68, 491, 200)) + boite(616, 870, 830, 288, 'Entrepôt de Québec', pointille(22, 68, 782, 200)) + "</div>")
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME); pg = b.new_page(viewport={'width': 1500, 'height': 1200})
    pg.set_content(html); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(300)
    pg.screenshot(path=sys.argv[1], omit_background=True); b.close()
