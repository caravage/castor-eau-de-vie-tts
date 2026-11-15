# Symboles de raid sur les cartes de la Rivière (paquet actuel, 15 cartes) : 1/3 Tortue (Lacs d'en haut), 1/3 Oniare (Lacs d'en bas),
# 1/3 portage (3 Saint-Laurent, 2 rivière des Outaouais). Symbole en bas à droite ; en bas à gauche, graphique du prix du castor à Paris
# (montant +1, descendant −1, ou rien : 5 cartes chacun, réparties dans chaque groupe de symbole) → img/v18/deck_riv_v46.png.
import subprocess, os, base64
R = os.path.abspath('.') + '/'
A = R + 'src/assets/'
REP = {200: 'tortue', 203: 'tortue', 206: 'tortue', 209: 'tortue', 212: 'tortue',
       201: 'oniare', 204: 'oniare', 207: 'oniare', 210: 'oniare', 213: 'oniare',
       202: 'Saint-Laurent', 205: 'Outaouais', 208: 'Saint-Laurent', 211: 'Outaouais', 214: 'Saint-Laurent'}
FEN = R + 'src/plateau_hd/node_modules/@fontsource/im-fell-english/files/im-fell-english-latin-400-normal.woff2'
FSC = R + 'src/plateau_hd/node_modules/@fontsource/im-fell-english-sc/files/im-fell-english-sc-latin-400-normal.woff2'
FL = {200: 'h', 203: 'b', 206: '', 209: 'h', 212: 'b', 201: 'b', 204: '', 207: 'h', 210: 'b', 213: '', 202: '', 205: 'h', 208: 'b', 211: '', 214: 'h'}
def fleche(x, y, sens):
    # graphique de prix, noir : axes + courbe montante ou descendante terminée par une pointe
    pts, tip = (("10,50 22,40 32,44 46,24", "M40 20 L54 16 L49 30 Z") if sens == 'h' else ("10,18 22,30 32,26 46,44", "M38 48 L54 54 L48 39 Z"))
    return (f"<svg style='position:absolute;left:{x}px;top:{y}px' width='66' height='66' viewBox='0 0 66 66'>"
            f"<path d='M5 4 V61 H62' fill='none' stroke='#000' stroke-width='3.5' stroke-linecap='square'/>"
            f"<polyline points='{pts}' fill='none' stroke='#000' stroke-width='4.5' stroke-linejoin='round' stroke-linecap='round'/>"
            f"<path d='{tip}' fill='#000'/></svg>")
TOP = 700 - 38 - 66  # même ligne pour tous les pictogrammes
INI = {'Saint-Laurent': 'S-L', 'Outaouais': 'RdO'}
cells = ''
for cid, sens in FL.items():
    if sens:
        i = cid - 200; x, y = (i % 10) * 500, (i // 10) * 700
        cells += fleche(x + 25, y + TOP, sens)
for cid, s in REP.items():
    i = cid - 200; x, y = (i % 10) * 500, (i // 10) * 700
    ix = x + 500 - 30 - 66
    if s in ('tortue', 'oniare'):
        cells += f"<img src='file://{A}region_{s}.png' style='position:absolute;left:{ix}px;top:{y + TOP}px;width:66px;height:66px'>"
    else:
        cells += (f"<img src='file://{A}rapide_portage.png' style='position:absolute;left:{ix}px;top:{y + TOP}px;width:66px;height:66px'>"
                  f"<div style=\"position:absolute;left:{ix - 12 - 150}px;top:{y + TOP}px;width:150px;height:66px;display:flex;align-items:center;justify-content:flex-end;font:400 40px EN;color:#2A2418\">{INI[s]}</div>")
html = (f"<!doctype html><meta charset=utf-8><style>@font-face{{font-family:SC;src:url(file://{FSC})}}@font-face{{font-family:EN;src:url(file://{FEN})}}body{{margin:0;width:5000px;height:1400px;position:relative}}</style>"
        f"<img src='file://{R}img/v18/deck_riv.png' style='position:absolute;left:0;top:0;width:5000px;height:1400px'>{cells}")
open('/tmp/riv46.html', 'w').write(html)
subprocess.run(['google-chrome', '--headless=new', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files', '--window-size=5000,1400',
                '--virtual-time-budget=3000', f'--screenshot={R}img/v18/deck_riv_v46.png', 'file:///tmp/riv46.html'], capture_output=True)
print('ok')
