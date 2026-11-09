# Tuile « Occasion » (8 nov. 2026) : événement du mois doré ; déclenche la phase de prestige puis remélange du sac. Style des tuiles evt6_*.
import sys
from playwright.sync_api import sync_playwright
R=sys.argv[1]
OR1,OR2,ORF='#C9A23C','#E8CD78','#8A6416'
LOOP=(f"<svg width='64' height='64' viewBox='0 0 64 64'><g fill='none' stroke='{ORF}' stroke-width='4.5' stroke-linecap='round'>"
      "<path d='M50 24 A20 20 0 0 0 14 22'/><path d='M14 40 A20 20 0 0 0 50 42'/></g>"
      f"<path d='M8 14 L16 26 L22 13 Z' fill='{ORF}'/><path d='M56 50 L48 38 L42 51 Z' fill='{ORF}'/>"
      f"<text x='32' y='39' text-anchor='middle' font-family='IM Fell English' font-size='20' fill='{ORF}'>✦</text></svg>")
html=f"""<!doctype html><html><head><meta charset='utf-8'>
<link href='https://fonts.googleapis.com/css2?family=IM+Fell+English:ital@0;1&family=IM+Fell+English+SC&display=block' rel='stylesheet'>
<style>*{{box-sizing:border-box;margin:0}}body{{width:300px;height:300px;overflow:hidden}}
.e{{width:300px;height:300px;border-radius:22px;background:radial-gradient(ellipse at 50% 40%,#FBF3DC,#F2E4B8);border:5px solid {OR1};box-shadow:inset 0 0 0 2px {OR2};display:flex;flex-direction:column;overflow:hidden;position:relative}}
.h{{background:linear-gradient(180deg,{OR2},{OR1} 55%,#A8822A);color:#FFF8E4;font:400 21px 'IM Fell English',serif;font-variant:small-caps;letter-spacing:2px;text-align:center;padding:8px 0 6px;text-shadow:0 1px 1px rgba(90,60,10,.6)}}
.b{{flex:1;display:flex;align-items:center;justify-content:center;padding-bottom:70px}}
.t{{font:italic 66px/1 'IM Fell English',serif;color:{ORF};text-shadow:0 1px 0 #FFF6D8}}
.ic{{position:absolute;left:50%;bottom:12px;transform:translateX(-50%)}}</style></head>
<body><div class='e'><div class='h'>Événement du mois</div><div class='b'><div class='t'>Occasion</div></div><div class='ic'>{LOOP}</div></div></body></html>"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':300,'height':300})
    pg.set_content(html); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(2000)
    pg.screenshot(path=R+'img/v18/evt6_occasion.png'); b.close()
