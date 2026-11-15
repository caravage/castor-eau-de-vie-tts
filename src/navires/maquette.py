# Maquettes des tuiles de navire (320 × 280, rendu ×2) : navires des joueurs (4 états : neutre, rouge, bleu, vert),
# navire de la Compagnie (gravure dorée sur bleu nuit), Le Profond (navire du roi : semé de lys, médaillon).
import os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); FONTS = os.path.abspath(f'{HERE}/../plateau_hd/fonts.css')
GRAV = os.path.abspath(f'{HERE}/../assets/navire_gravure.png')
ETATS = {'neutre': ('#4A3324', '#7A5A3E'), 'rouge': ('#A8322A', '#D9665A'), 'bleu': ('#2F5E8E', '#6E9BC8'), 'vert': ('#4E7A2C', '#8DB565')}
CSS = """*{box-sizing:border-box;margin:0;padding:0}body{width:320px;height:280px;background:transparent;overflow:hidden}
.t{position:absolute;inset:0;border-radius:26px;overflow:hidden}
.nm{position:absolute;left:24px;right:24px;bottom:16px;height:44px;border-radius:9px;display:flex;align-items:center;justify-content:center;font-family:'IM Fell English SC';font-size:27px}"""
LYS = ("<path d='M0,-27 C9,-17 10,-6 4,7 L-4,7 C-10,-6 -9,-17 0,-27 Z'/><path d='M5,6 C9,-6 20,-12 27,-5 C32,1 28,11 21,10 C25,5 21,0 16,3 C12,6 11,8 9,8 Z'/>"
       "<path d='M-5,6 C-9,-6 -20,-12 -27,-5 C-32,1 -28,11 -21,10 C-25,5 -21,0 -16,3 C-12,6 -11,8 -9,8 Z'/><rect x='-14' y='8' width='28' height='5' rx='1.5'/>"
       "<path d='M-3,13 L3,13 L4,21 L0,26 L-4,21 Z'/>")
def joueur(nom, etat):
    c, cl = ETATS[etat]
    return (f"<div class='t' style='background:{c}'>"
            f"<div style='position:absolute;inset:9px;border-radius:19px;background:radial-gradient(ellipse at 50% 40%,#FBF4E2,#EADCB8 75%,#D9C493);box-shadow:inset 0 0 0 2px {cl},inset 0 0 18px rgba(80,50,20,.25)'></div>"
            f"<img src='file://{GRAV}' style='position:absolute;left:62px;top:16px;width:196px;filter:sepia(.5) contrast(1.15)'>"
            f"<div class='nm' style='background:#FBF6E8;border:3px solid {c};color:#2A2418'>{nom}</div></div>")
def compagnie():   # sobre : cadre ardoise, parchemin, cachet de cire « C »
    return ("<div class='t' style='background:#45463F'>"
            "<div style='position:absolute;inset:9px;border-radius:19px;background:radial-gradient(ellipse at 50% 40%,#F6EEDB,#E2D3AE 75%,#CDBB8F);box-shadow:inset 0 0 0 2px #8C8A7A,inset 0 0 18px rgba(60,50,30,.3)'></div>"
            f"<img src='file://{GRAV}' style='position:absolute;left:62px;top:16px;width:196px;filter:sepia(.7) contrast(1.1) brightness(.92)'>"
            "<svg style='position:absolute;left:22px;top:20px' width='50' height='50' viewBox='0 0 50 50'>"
            "<path d='M25 3 C33 4 37 2 41 8 C47 12 46 17 47 25 C46 33 48 38 42 42 C38 47 33 46 25 47 C17 46 12 48 8 42 C3 38 4 33 3 25 C4 17 2 12 8 8 C12 2 17 4 25 3 Z' fill='#7B3B2E'/>"
            "<circle cx='25' cy='25' r='15' fill='none' stroke='#5E2A20' stroke-width='1.5'/>"
            "<text x='25' y='33' text-anchor='middle' font-family='IM Fell English' font-style='italic' font-size='24' fill='#E8D2B8'>C</text></svg>"
            "<div class='nm' style='background:#FBF6E8;border:3px solid #45463F;color:#2A2418'>La Compagnie</div></div>")
def profond():   # navire du roi : fond blanc semé de lys d'or, médaillon
    semis = ''.join(f"<g transform='translate({x} {y}) scale(.32)' fill='#C9A04A' opacity='.75'>{LYS}</g>" for y in range(14, 280, 34) for x in range(14 + (17 if (y // 34) % 2 else 0), 320, 34))
    return ("<div class='t' style='background:#FDFBF5;box-shadow:inset 0 0 0 7px #C9A04A'>"
            f"<svg style='position:absolute;inset:0' width='320' height='280'>{semis}</svg>"
            "<div style='position:absolute;inset:7px;border-radius:20px;border:2px solid #C9A04A'></div>"
            "<div style='position:absolute;left:60px;top:22px;width:200px;height:170px;border-radius:50%;background:radial-gradient(ellipse at 50% 40%,#FFFDF7,#F1E7CC);border:4px solid #C9A04A;box-shadow:0 0 0 3px #FDFBF5,0 0 0 5px #C9A04A'></div>"
            f"<img src='file://{GRAV}' style='position:absolute;left:84px;top:34px;width:152px;filter:sepia(.4) contrast(1.2)'>"
            f"<svg style='position:absolute;left:146px;top:2px' width='28' height='30' viewBox='-30 -30 60 60'><g fill='#C9A04A' stroke='#FDFBF5' stroke-width='2'>{LYS}</g></svg>"
            "<div class='nm' style='background:#FDFBF5;border:3px solid #C9A04A;color:#2A2418'>Le Profond</div></div>")
pages = [(f'joueur_{e}', joueur("L’Aigle d’Or", e)) for e in ETATS] + [('compagnie', compagnie()), ('profond', profond())]
os.makedirs(f'{HERE}/png', exist_ok=True)
for nom, body in pages:
    p = f'{HERE}/{nom}.html'
    open(p, 'w').write(f"<!doctype html><html><head><meta charset='utf-8'><link rel='stylesheet' href='file://{FONTS}'><style>{CSS}</style></head><body>{body}</body></html>")
    subprocess.run(['google-chrome', '--headless=new', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files', '--force-device-scale-factor=2',
                    '--default-background-color=00000000', '--virtual-time-budget=3000', f'--screenshot={HERE}/png/{nom}.png', '--window-size=320,280', f'file://{p}'], capture_output=True)
from PIL import Image
ims = [Image.open(f'{HERE}/png/{n}.png') for n, _ in pages]
out = Image.new('RGB', (640 * 3 + 80, 560 * 2 + 60), (52, 42, 34))
for k, i in enumerate(ims): out.paste(i, (20 + (k % 3) * 660, 20 + (k // 3) * 580), i)
out.save('/mnt/user-data/outputs/navires_maquette.jpg', quality=90); print('ok')
