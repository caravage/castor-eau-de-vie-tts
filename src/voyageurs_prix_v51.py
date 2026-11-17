# Voyageurs v3.51 (16 nov. 2026) : prix d'embauche (₶) ajouté sur chaque jeton, pastille ronde en haut à gauche du panneau.
# Part des images voy2 existantes ; sorties voy2_<nom>_v51.png. Usage : python3 voyageurs_prix_v51.py <racine du dépôt> <node_modules/@fontsource>
import sys
from playwright.sync_api import sync_playwright
R, F = sys.argv[1], sys.argv[2]
PRIX = {'guide_v43': 1, 'pilote2': 2, 'artisan': 1, 'interprete': 2, 'milicien': 1}   # Guide 1 ₶, Pilote 2 ₶ (16 nov.)
FONT = f"@font-face{{font-family:A;font-weight:700;src:url(file://{F}/alegreya-sans/files/alegreya-sans-latin-700-normal.woff2)}}"
with sync_playwright() as p:
    br = p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg = br.new_page(viewport={'width': 300, 'height': 432})
    for k, v in PRIX.items():
        src = f'file://{R}img/v18/voy2_{k}.png'
        html = (f"<!doctype html><meta charset=utf-8><style>{FONT}html,body{{margin:0;background:transparent}}"
                ".b{position:absolute;left:24px;top:96px;width:64px;height:64px;box-sizing:border-box;border-radius:50%;"
                "background:#F2EAD3;border:4px solid #B8923A;box-shadow:inset 0 0 0 3px #F2EAD3,inset 0 0 0 4.5px #D8CBA6;"
                "display:flex;align-items:center;justify-content:center;font:700 27px A,sans-serif;color:#2A2418}</style>"
                f"<img src='{src}' style='position:absolute;left:0;top:0;width:300px;height:432px'><div class=b>{v}&nbsp;₶</div>")
        open('/tmp/voy.html', 'w').write(html)
        pg.goto('file:///tmp/voy.html'); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(200)
        pg.screenshot(path=f'{R}img/v18/voy2_{k}_v51.png', omit_background=True)
    br.close()
print('ok')
