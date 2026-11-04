import sys, json
from playwright.sync_api import sync_playwright
PX=1860/16.275   # px par unité TTS
CW,CH=round(3.5*PX),round(3.5*88/63.5*PX)   # carte Rivière / Associé
caisse="<svg width='70' height='70' viewBox='0 0 200 200'><rect x='18' y='26' width='164' height='148' rx='10' fill='#C79A5B' stroke='#5C3A1A' stroke-width='8'/><line x1='18' y1='76' x2='182' y2='76' stroke='#5C3A1A' stroke-width='6'/><line x1='18' y1='126' x2='182' y2='126' stroke='#5C3A1A' stroke-width='6'/><line x1='30' y1='34' x2='170' y2='166' stroke='#5C3A1A' stroke-width='6'/></svg>"
edv="<svg width='60' height='70' viewBox='0 0 200 200'><path d='M84 14 L116 14 L116 56 Q150 74 150 112 L150 176 Q150 188 138 188 L62 188 Q50 188 50 176 L50 112 Q50 74 84 56 Z' fill='#5E8C5A' stroke='#20331E' stroke-width='8'/><rect x='80' y='8' width='40' height='22' rx='4' fill='#8A5A2B' stroke='#20331E' stroke-width='5'/><rect x='62' y='112' width='76' height='46' rx='6' fill='#F2E8C8' stroke='#20331E' stroke-width='4'/></svg>"
def canot(n,w): 
    cw=(w-24)/n; cells=''.join(f"<rect x='{12+i*cw+3:.1f}' y='8' width='{cw-6:.1f}' height='18' fill='#fff' stroke='#2A2418' stroke-width='2'/>" for i in range(n))
    return f"<svg width='{w}' height='36' viewBox='0 0 {w} 36'><path d='M2 4 L{w-2} 4 L{w-12} 32 L12 32 Z' fill='#F7F3EA' stroke='#2A2418' stroke-width='3'/>{cells}</svg>"
castor=lambda c:f"<svg width='90' height='56' viewBox='0 0 150 90'><ellipse cx='80' cy='48' rx='48' ry='30' fill='{c}' stroke='#3E2A16' stroke-width='4'/><circle cx='124' cy='40' r='13' fill='{c}' stroke='#3E2A16' stroke-width='4'/><path d='M34 52 L4 72 L18 80 L40 62 Z' fill='#5C3A1A' stroke='#3E2A16' stroke-width='3'/></svg>"
def slotbag(): return "<div class='pmbag' style='width:120px;height:120px'></div>"
def bag(icon,lab,show):
    badge="<div style=\"position:absolute;left:40px;bottom:-52px;width:40px;height:40px;border-radius:50%;background:#2A2418;color:#F4EBD6;font:700 22px 'Alegreya Sans';display:flex;align-items:center;justify-content:center\">0</div>" if show else ''
    return f"<div style='display:flex;flex-direction:column;align-items:center;gap:4px'><div style='position:relative;width:120px;height:120px;border-radius:50%;background:#EFE6CC;box-shadow:inset 0 0 0 2px #8F8572;display:flex;align-items:center;justify-content:center'>{icon}{badge}</div></div>"
def html(name,col,dark,show):
    circ=''.join(f"<div style='display:flex;flex-direction:column;align-items:center;gap:3px'><div style='width:72px;height:72px;border-radius:50%;background:#F2EAD3;box-shadow:inset 0 0 0 2.5px #8F8572'></div><div style=\"font:700 22px 'Alegreya Sans';color:#6B5F45\">{i}</div></div>" for i in range(7))
    slot=f"<div style='width:{CW}px;height:{CH}px;box-sizing:border-box;border:2px dashed #BFAE7F;border-radius:16px;background:rgba(246,239,220,.6)'></div>"
    def box(t,inner,w=None): return f"<div style='width:{(w or CW)-14}px;margin:0 7px;box-sizing:border-box;background:#F6EFDC;border:2px solid #2A2418;box-shadow:0 0 0 5px #F4EBD6,0 0 0 6.5px #2A2418;display:flex;flex-direction:column;align-items:center;padding:8px 6px'><div style=\"font:italic 30px 'IM Fell English';color:#2A2418\">{t}</div><div style='flex:1;width:100%;display:flex;align-items:center;justify-content:space-around;padding-bottom:50px;box-sizing:border-box'>{inner}</div></div>"
    title=lambda t:f"<div style='display:flex;align-items:center;gap:20px;height:34px'><div style='flex:1;height:1.5px;background:#BFAE7F'></div><div style=\"font:400 32px 'IM Fell English';font-variant:small-caps;color:#2A2418\">{t}</div><div style='flex:1;height:1.5px;background:#BFAE7F'></div></div>"
    return f"""<html><head><meta charset='utf-8'><link href='https://fonts.googleapis.com/css2?family=Alegreya+Sans:wght@400;700&family=IM+Fell+English:ital@0;1&display=block' rel='stylesheet'></head>
<body style='margin:0'><div style='width:1860px;height:1200px;box-sizing:border-box;background:#22332F;border-radius:30px;padding:12px'>
<div style='width:100%;height:100%;box-sizing:border-box;background:#E6DAB6;border-radius:20px;padding:16px 40px 22px;display:flex;flex-direction:column;gap:12px'>
 <div style='display:flex;align-items:center;height:100px'>
  <div style='height:86px;padding:0 64px;background:{col};clip-path:polygon(4% 0,96% 0,100% 50%,96% 100%,4% 100%,0 50%);display:flex;align-items:center'><div style="font:400 54px 'IM Fell English';font-variant:small-caps;color:#F4EBD6">{name}</div></div>
  <div style='margin-left:auto;display:flex;align-items:center;gap:18px'><div style="font:italic 34px 'IM Fell English';color:#2A2418">Soupçon</div><div style='display:flex;gap:10px'>{circ}</div></div>
 </div>
 {title('Société de traite')}
 <div style='display:flex;justify-content:space-between'>{slot*4}</div>
 {title('Entrepôt à Québec')}
 <div style='flex:1;display:flex;justify-content:space-between;padding:7px 0'>
  {box('Charges',slotbag()+slotbag())}
  {box('Canots',bag(canot(3,84),'moyen',False)+bag(canot(5,92),'grand',False))}
  {box('Fourrures',slotbag())}
  <div style='width:{CW-14}px;margin:0 7px;box-sizing:border-box;background:#F6EFDC;border:4px solid {col};box-shadow:0 0 0 5px #F4EBD6,0 0 0 7px {col};padding:8px 18px;color:#2A2418;display:flex;flex-direction:column'><div style="font:400 36px 'IM Fell English';font-variant:small-caps;text-align:center;color:{col}">Capital</div><div style="font:italic 25px/1.28 'IM Fell English';display:grid;grid-template-columns:24px 1fr;margin-top:2px"><span></span><span>charges <span style='font-size:20px'>(10 max)</span></span><span>+</span><span>fourrures × prix</span><span>+</span><span>parts</span><span>+</span><span>livres</span></div><div style='display:flex;align-items:center;gap:10px;margin-top:6px;border-top:1.5px solid #BFAE7F;padding-top:8px'><span style="font:400 34px 'IM Fell English'">=</span><div class='ctr' style='width:110px;height:110px'></div></div></div>
 </div>
</div></div></body></html>"""
P=[('Famille Le Moyne','#A8322A','#6E1E18'),('Famille Gamelin','#2F5E8E','#1D3B5A'),('Famille Couagne','#4E7A2C','#2F4A1A')]
geo={}
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1860,'height':1200})
    for i,(n,c,dk) in enumerate(P):
        for show in (False,True):
            pg.set_content(html(n,c,dk,show)); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(2500)
            pg.screenshot(path=f'pmat_v3_{i}{"_demo" if show else ""}.png',omit_background=True)
        if i==0:
            geo=pg.evaluate("""()=>{const r=e=>{const b=e.getBoundingClientRect();return [b.x+b.width/2,b.y+b.height/2,b.width,b.height]};
              return {slots:[...document.querySelectorAll("div[style*='dashed']")].map(r),
                      souf:[...document.querySelectorAll("div[style*='width:72px']")].map(r),
                      bags:[...document.querySelectorAll('.pmbag')].map(r),ctr:[...document.querySelectorAll('.ctr')].map(r)}}""")
    b.close()
json.dump(geo,open('pmat_geo.json','w')); print({k:len(v) for k,v in geo.items()}, geo['slots'][0])
