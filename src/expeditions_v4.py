# Cartes Expédition v4 : planche 3 x 3 par famille, 1050 x 750 px par carte (200 px / unité TTS).
# Bandeau à la couleur de la famille, case Congé / Coureur au format du jeton (1,4), médaillons Voyageur, cale Marchandises.
import json, base64, sys
from playwright.sync_api import sync_playwright
A='/tmp/claude-0/-home-claude/3c5a2878-065c-5165-9c41-6d23b49bdcf8/scratchpad/vision/assets/'
G='data:image/png;base64,'+base64.b64encode(open(A+'gravure.png','rb').read()).decode()
U=200; SL=round(1.4*U)+26            # case congé / coureur : jeton 1,4 + marge
VW,VH=round(0.7*U)+34,round(1.008*U)+34
FONT="<link href='https://fonts.googleapis.com/css2?family=Alegreya+Sans:wght@400;700&family=IM+Fell+English:ital@0;1&family=IM+Fell+English+SC&display=block' rel='stylesheet'>"
BORD='#8A6A3A'; PARCH='#EEDFBC'
CAISSE="<svg width='64' height='64' viewBox='0 0 200 200'><rect x='18' y='26' width='164' height='148' rx='10' fill='none' stroke='#5C3A1A' stroke-width='10'/><line x1='18' y1='76' x2='182' y2='76' stroke='#5C3A1A' stroke-width='8'/><line x1='18' y1='126' x2='182' y2='126' stroke='#5C3A1A' stroke-width='8'/><line x1='30' y1='34' x2='170' y2='166' stroke='#5C3A1A' stroke-width='8'/></svg>"
BOUT="<svg width='54' height='64' viewBox='0 0 200 200'><path d='M84 14 L116 14 L116 56 Q150 74 150 112 L150 176 Q150 188 138 188 L62 188 Q50 188 50 176 L50 112 Q50 74 84 56 Z' fill='none' stroke='#20331E' stroke-width='10'/></svg>"
PAGAIE=lambda c:f"<svg width='34' height='120' viewBox='0 0 34 120'><rect x='15' y='4' width='4' height='70' rx='2' fill='{c}'/><path d='M17 70 C4 78 4 108 17 116 C30 108 30 78 17 70 Z' fill='{c}'/><rect x='10' y='2' width='14' height='6' rx='3' fill='{c}'/></svg>"
def cadre(w,h,label):
    return (f"<div class='cg' style='width:{w}px;height:{h}px;box-sizing:border-box;flex:none;background:{PARCH};border:4px solid {BORD};border-radius:14px;"
            f"box-shadow:inset 0 0 0 9px {PARCH},inset 0 0 0 10.5px {BORD},0 3px 6px rgba(0,0,0,.18);display:flex;align-items:center;justify-content:center;text-align:center;"
            f"font:400 38px/1.05 \"IM Fell English SC\";color:rgba(138,106,58,.75)'>{label}</div>")
def voy(i,col):
    return (f"<div class='voy' style='width:{VW}px;height:{VH}px;flex:none;box-sizing:border-box;border-radius:50%;background:#F3EAD2;"
            f"box-shadow:inset 0 0 0 4px {col},inset 0 0 0 9px #F3EAD2,inset 0 0 0 10.5px {col},0 3px 6px rgba(0,0,0,.18);"
            f"display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px'>"
            f"<div style=\"font:400 34px 'IM Fell English SC';color:{col}\">{['I','II','III'][i]}</div><div style='opacity:.28'>{PAGAIE(col)}</div>"
            "</div>")
def cale(extra=''):
    wm=CAISSE+BOUT
    return (f"<div class='mch' style='flex:1;position:relative;background:#F6EFDC;border:2px solid #2A2418;box-shadow:0 0 0 5px #F4EBD6,0 0 0 6.5px #2A2418;margin:7px;{extra}'>"
            f"<div style='position:absolute;inset:0;display:flex;align-items:center;justify-content:center;gap:40px;opacity:.16'>{wm}</div>"
            f"<div style=\"position:absolute;left:50%;top:-22px;transform:translateX(-50%);background:#E6DAB6;padding:0 18px;font:400 34px 'IM Fell English SC';color:#2A2418\">Marchandises</div></div>")
def card(lettre,kind,col):
    sous={'g':'Grand canot','m':'Moyen canot','c':'Coureurs des bois'}[kind]
    tete=(
          f"<div style='position:relative;display:flex;align-items:center;gap:20px;height:96px'>"
          f"<div style='height:78px;padding:0 50px;background:{col};clip-path:polygon(5% 0,95% 0,100% 50%,95% 100%,5% 100%,0 50%);display:flex;align-items:center;box-shadow:0 2px 0 rgba(0,0,0,.2)'>"
          f"<div style=\"font:400 50px 'IM Fell English';font-variant:small-caps;color:#F4EBD6\">Expédition {lettre}</div></div>"
          f"<div style=\"font:italic 44px 'IM Fell English';color:#1E1A12;text-shadow:0 0 8px #F4EBD6,0 0 14px #F4EBD6\">{sous}</div></div>")
    if kind=='c':
        corps=f"<div style='position:relative;flex:1;display:flex;gap:30px;align-items:stretch;padding-top:10px'><div style='display:flex;align-items:center'>{cadre(SL,SL,'Coureur<br>des bois')}</div>{cale('margin-top:30px')}</div>"
    else:
        n=3 if kind=='g' else 2
        corps=(f"<div style='position:relative;display:flex;align-items:center;gap:30px;padding:8px 0 0 4px'>{cadre(SL,SL,'Congé')}"
               f"<div style='flex:1;display:flex;justify-content:space-evenly'>{''.join(voy(i,col) for i in range(n))}</div></div>{cale('margin-top:26px')}")
    return (f"<div style='width:1050px;height:750px;box-sizing:border-box;background:#22332F;border-radius:36px;padding:12px'>"
            f"<div style='position:relative;width:100%;height:100%;box-sizing:border-box;background:#E6DAB6;border-radius:26px;overflow:hidden;padding:14px 26px 22px;display:flex;flex-direction:column'>"
            f"{tete}{corps}</div></div>")
P=[('rouge','#A8322A'),('bleu','#2F5E8E'),('vert','#4E7A2C')]
only=sys.argv[1:] or [c for c,_ in P]
geo={}
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':3150,'height':2250})
    for c,col in P:
        if c not in only: continue
        cells=''.join(card(l,k,col) for l in 'ABC' for k in 'gmc')
        pg.set_content(f"<html><head><meta charset='utf-8'>{FONT}</head><body style='margin:0;background:transparent'><div style='display:grid;grid-template-columns:repeat(3,1050px)'>{cells}</div></body></html>")
        pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(3000)
        pg.screenshot(path=f'exp4_{c}.png',omit_background=True)
        if c=='rouge':
            geo=pg.evaluate("""()=>{const r=e=>{const b=e.getBoundingClientRect();return [b.x+b.width/2,b.y+b.height/2,b.width,b.height]};
              return {cg:[...document.querySelectorAll('.cg')].map(r),voy:[...document.querySelectorAll('.voy')].map(r),mch:[...document.querySelectorAll('.mch')].map(r)}}""")
    b.close()
if geo: json.dump(geo,open('exp4_geo.json','w')); print({k:len(v) for k,v in geo.items()})
