# Matériel de départ v49 (3 nov. 2026) : 9 cartes en capital seul (canots, navire, parts, ₶) + 1 Manigance (+1 soupçon) ; charges et crédit via l achat express. Usage : python3 materiel_v49.py <sortie_sans_extension>
import base64, sys
from playwright.sync_api import sync_playwright
R='../'
def b64(p): return 'data:image/png;base64,'+base64.b64encode(open(R+p,'rb').read()).decode()
NAV=b64('src/assets/navire_gravure.png'); ALB=b64('src/assets/alambic_gravure.png')
def canot(n,w):
    cw=(w-24)/n; cells=''.join(f"<rect x='{12+i*cw+3:.1f}' y='8' width='{cw-6:.1f}' height='22' fill='#fff' stroke='#2A2418' stroke-width='2'/>" for i in range(n))
    return f"<svg width='{w}' height='40' viewBox='0 0 {w} 40'><path d='M2 4 L{w-2} 4 L{w-12} 36 L12 36 Z' fill='#F7F3EA' stroke='#2A2418' stroke-width='3'/>{cells}</svg>"
IC={'petit':canot(2,70),'moyen':canot(3,96),'grand':canot(5,118),'navire':f"<img src='{NAV}' style='width:92px'>",'alambic':f"<img src='{ALB}' style='width:70px'>"}
IC['manig']="<svg width='60' height='80' viewBox='0 0 60 80'><rect x='14' y='4' width='40' height='60' rx='5' fill='#E8DCC0' stroke='#2A2418' stroke-width='3'/><rect x='4' y='14' width='40' height='60' rx='5' fill='#7A1F18' stroke='#2A2418' stroke-width='3'/><path d='M14 32 L34 32 M14 42 L34 42 M14 52 L28 52' stroke='#F2EAD3' stroke-width='3'/></svg>"
IC['soup']="<svg width='70' height='44' viewBox='0 0 70 44'><path d='M4 22 Q35 -6 66 22 Q35 50 4 22 Z' fill='#F7F0DC' stroke='#7A1F18' stroke-width='4'/><circle cx='35' cy='22' r='10' fill='#7A1F18'/></svg>"
IC['edv']="<svg width='62' height='62' viewBox='0 0 200 200'><path d='M84 14 L116 14 L116 56 Q150 74 150 112 L150 176 Q150 188 138 188 L62 188 Q50 188 50 176 L50 112 Q50 74 84 56 Z' fill='#5E8C5A' stroke='#20331E' stroke-width='8'/><rect x='80' y='8' width='40' height='22' rx='4' fill='#8A5A2B' stroke='#20331E' stroke-width='5'/><rect x='62' y='112' width='76' height='46' rx='6' fill='#F2E8C8' stroke='#20331E' stroke-width='4'/></svg>"
C=[[('grand','1 grand canot'),('coin','1')],
[('moyen','1 moyen canot'),('edv','1 eau-de-vie'),('coin','1')],
[('moyen','1 moyen canot'),('coin','3')],
[('moyen','1 moyen canot'),('coin','4')],
[('navire','1 navire, payé')],
[('navire','2 parts de navire'),('coin','3')],
[('alambic','2 parts de distillerie'),('coin','2')],
[('coin','5')],
[('manig','1 carte Manigance'),('soup','+1 soupçon')]]
CSS=("*{box-sizing:border-box;margin:0}body{background:#F2EAD3;padding:0}.g{display:grid;grid-template-columns:repeat(5,360px);grid-auto-rows:500px;gap:0}"
".m{width:360px;height:500px;background:#F2EAD3;border-radius:18px;border:3px solid #4E5B3A;display:flex;flex-direction:column;overflow:hidden;position:relative}"
".band{background:#4E5B3A;color:#F2EAD3;text-align:center;padding:12px 0 10px;font:italic 30px 'IM Fell English',serif}"
".band small{display:block;font:400 15px 'IM Fell English SC',serif;letter-spacing:3px;opacity:.85;margin-top:2px}"
".rows{flex:1;margin:14px;border:1.5px solid #4E5B3A;border-radius:6px;display:flex;flex-direction:column;position:relative}"
".r{flex:1;display:flex;align-items:center;gap:14px;padding:0 16px;border-top:1.5px solid #4E5B3A}.r:first-child{border-top:none}"
".ic{flex:none;width:120px;display:flex;justify-content:center;align-items:center}.tx{font:italic 27px/1.1 'IM Fell English',serif;color:#2A2418}"
".r.c{justify-content:center}.tx b{font:700 30px 'Alegreya Sans',sans-serif;font-style:normal;margin-right:2px}"
".coin{width:78px;height:78px;border-radius:50%;background:#F7F0DC;border:5px double #2A2418;display:flex;align-items:center;justify-content:center;font:400 40px 'IM Fell English',serif;color:#2A2418}"
".orn{position:absolute;width:26px;height:26px}")
ORN="<svg class='orn' style='{p}' viewBox='0 0 26 26'><path d='M2 2C10 2 14 6 14 13M2 2C2 10 6 14 13 14M8 8C10 10 10 12 8 13' fill='none' stroke='#4E5B3A' stroke-width='1.6' transform='{t}'/></svg>"
orns=''.join(ORN.format(p=p,t=t) for p,t in (("left:-1px;top:-1px",''),("right:-1px;top:-1px",'translate(26 0) scale(-1 1)'),("left:-1px;bottom:-1px",'translate(0 26) scale(1 -1)'),("right:-1px;bottom:-1px",'translate(26 26) scale(-1 -1)')))
def row(k,t):
    if k=='coin': return f"<div class='r c'><div class='coin'><b style=\"font:700 38px 'Alegreya Sans',sans-serif\">{t}</b>&nbsp;₶</div></div>"
    a,b=t.split(' ',1); return f"<div class='r'><div class='ic'>{IC[k]}</div><div class='tx'><b>{a}</b> {b}</div></div>"
cards=''.join(f"<div class='m'><div class='band'>Matériel<small>de départ</small></div><div class='rows'>{orns}{''.join(row(k,t) for k,t in c)}</div></div>" for c in C)
html=f"<html><head><meta charset='utf-8'><link href='https://fonts.googleapis.com/css2?family=IM+Fell+English:ital@0;1&family=IM+Fell+English+SC&family=Alegreya+Sans:wght@700&display=block' rel='stylesheet'><style>{CSS}</style></head><body><div class='g'>{cards}</div></body></html>"
open(sys.argv[1]+'.html','w').write(html)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1800,'height':1000},device_scale_factor=1)
    pg.set_content(html); pg.wait_for_timeout(2500); pg.screenshot(path=sys.argv[1]+'.png',full_page=False); b.close()
