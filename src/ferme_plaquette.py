# Plaquette « Ferme du castor » (une seule face), style plateau du joueur. 1500 x 960 px (150 px / unité : 10 x 6,4).
import json
from playwright.sync_api import sync_playwright
FONT="<link href='https://fonts.googleapis.com/css2?family=Alegreya+Sans:wght@400;700&family=IM+Fell+English:ital@0;1&family=IM+Fell+English+SC&display=block' rel='stylesheet'>"
COL='#5C3A1A'
def cadre(inner):
    return (f"<div style='width:1500px;height:960px;box-sizing:border-box;background:#22332F;border-radius:44px;padding:14px'>"
            f"<div style='position:relative;width:100%;height:100%;box-sizing:border-box;background:#E6DAB6;border-radius:32px;padding:26px 40px;display:flex;flex-direction:column;gap:22px'>{inner}</div></div>")
def banniere(t):
    return (f"<div style='display:flex;align-items:center;gap:26px'><div style='height:92px;padding:0 64px;background:{COL};clip-path:polygon(5% 0,95% 0,100% 50%,95% 100%,5% 100%,0 50%);display:flex;align-items:center'>"
            f"<div style=\"font:400 60px 'IM Fell English';font-variant:small-caps;color:#F4EBD6\">{t}</div></div></div>")
def boite(t,inner,extra=''):
    return (f"<div style='position:relative;background:#F6EFDC;border:2px solid #2A2418;box-shadow:0 0 0 5px #F4EBD6,0 0 0 6.5px #2A2418;margin:7px;padding:34px 22px 18px;{extra}'>"
            f"<div style=\"position:absolute;left:50%;top:-24px;transform:translateX(-50%);background:#E6DAB6;padding:0 18px;font:400 38px 'IM Fell English';font-variant:small-caps;color:#2A2418;white-space:nowrap\">{t}</div>{inner}</div>")
def piste(n,cls,size=88):
    c=''.join(f"<div class='{cls}' style='width:{size}px;height:{size}px;border-radius:50%;background:#EFE6CC;box-shadow:inset 0 0 0 5px #8F8572;display:flex;align-items:center;justify-content:center;font:700 {size*0.45:.0f}px \"Alegreya Sans\";color:#2A2418'>{v}</div>" for v in range(1,n+1))
    return f"<div style='display:flex;justify-content:space-between;gap:18px'>{c}</div>"
def politiques():
    P=[('Prix fixe','toutes les peaux'),('Rationnement quantitatif','jusqu’au remplissage des navires'),('Rationnement qualitatif','castor gras seulement'),('Commerce libre','les marchands expédient ; droit d’entrée par peau')]
    c=''.join(f"<div class='pol' style='flex:1;display:flex;flex-direction:column;align-items:center;gap:8px'><div style='width:96px;height:96px;border-radius:50%;border:3px dashed #8F8572;background:#EFE6CC'></div>"
              f"<div style=\"font:400 32px/1.05 'IM Fell English';font-variant:small-caps;color:#2A2418;text-align:center\">{a}</div><div style=\"font:italic 26px/1.15 'IM Fell English';color:#6B5F45;text-align:center\">{b}</div></div>" for a,b in P)
    return f"<div style='display:flex;gap:14px;align-items:flex-start;padding-top:10px'>{c}</div>"
entrepot=lambda: boite('Entrepôt de Québec',"<div class='ent' style='height:100%;min-height:120px;border:3px dashed #BFAE7F;border-radius:14px'></div>","flex:1;display:flex;flex-direction:column")
recto=cadre(banniere('Ferme du castor')
            +boite('Prix en France',piste(10,'pfr'))
            +"<div style='flex:1;display:flex;gap:26px'>"
            +"<div style='flex:1.6;display:flex;flex-direction:column;gap:30px'>"+boite('Prospérité',piste(4,'pro',80),'padding-left:120px;padding-right:120px')
            +boite('Politique d’achat',politiques(),'flex:1;display:flex;flex-direction:column')+"</div>"
            +entrepot()+"</div>")
geo={}
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1500,'height':960})
    for nom,h in (('ferme_recto',recto),):
        pg.set_content(f"<html><head><meta charset='utf-8'>{FONT}</head><body style='margin:0;background:transparent'>{h}</body></html>")
        pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(2500); pg.screenshot(path=nom+'.png',omit_background=True)
        if nom=='ferme_recto':
            geo=pg.evaluate("""()=>{const r=e=>{const b=e.getBoundingClientRect();return [b.x+b.width/2,b.y+b.height/2]};
              return {pfr:[...document.querySelectorAll('.pfr')].map(r),pol:[...document.querySelectorAll('.pol > div:first-child')].map(r),pro:[...document.querySelectorAll('.pro')].map(r)}}""")
    b.close()
json.dump(geo,open('ferme_geo.json','w')); print({k:len(v) for k,v in geo.items()})
