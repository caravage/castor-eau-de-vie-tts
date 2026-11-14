# Jetons voyageurs « voy2 » (300 × 432) : bandeau de couleur, titre en petites capitales, panneau crème,
# icône, chiffre de couleur, effet. Verso « Utilisé ». Rendu Chrome headless, police Tinos (= Liberation Serif).
import os, subprocess, sys
F = os.path.abspath('node_modules/@fontsource/tinos/files')
OUT = sys.argv[1] if len(sys.argv) > 1 else 'out'
os.makedirs(OUT, exist_ok=True)
CSS = f"""@font-face{{font-family:T;font-weight:400;src:url(file://{F}/tinos-latin-400-normal.woff2)}}
@font-face{{font-family:T;font-weight:700;src:url(file://{F}/tinos-latin-700-normal.woff2)}}
html,body{{margin:0;background:transparent}}
.t{{position:absolute;left:0;top:0;width:300px;height:432px;border-radius:30px;font-family:T}}
.h{{position:absolute;top:21px;width:300px;text-align:center;font-size:42px;font-variant:small-caps;color:#F2EAD3;letter-spacing:.5px}}
.p{{position:absolute;left:10px;top:80px;width:276px;height:338px;border-radius:14px;border:2px solid rgba(42,36,24,.4);
   background:radial-gradient(ellipse 70% 60% at 45% 30%,#F9F2DF,#F0E5CB)}}
.i{{position:absolute;left:0;top:30px;width:276px;height:170px;display:flex;align-items:center;justify-content:center}}
.n{{position:absolute;top:192px;width:276px;text-align:center;font-weight:700;font-size:57px}}
.e{{position:absolute;top:252px;width:276px;text-align:center;font-weight:700;font-size:34px;color:#2A2418}}
.pu{{position:absolute;left:10px;top:80px;width:276px;height:338px;border-radius:14px;border:2px solid rgba(242,234,211,.45)}}
.u{{position:absolute;top:150px;width:276px;text-align:center;font-weight:700;font-size:31px;letter-spacing:3px;color:#F2EAD3}}"""

def render(name, inner):
    html = f"<!doctype html><meta charset=utf-8><style>{CSS}</style>{inner}"
    p = os.path.abspath(f'{OUT}/{name}.html'); open(p, 'w').write(html)
    subprocess.run(['google-chrome', '--headless=new', '--no-sandbox', '--disable-gpu', '--hide-scrollbars',
                    '--default-background-color=00000000', '--force-device-scale-factor=1', '--window-size=300,432',
                    f'--screenshot={os.path.abspath(OUT)}/{name}.png', 'file://' + p], capture_output=True)

def jeton(key, titre, coul, icone, nombre, effet):
    render(f'voy2_{key}', f"<div class=t style='background:{coul}'><div class=h>{titre}</div><div class=p>"
           f"<div class=i>{icone}</div><div class=n style='color:{coul}'>{nombre}</div><div class=e>{effet}</div></div></div>")
    render(f'voy2_{key}_used', f"<div class=t style='background:{coul}'><div class=h>{titre}</div><div class=pu>"
           f"<div class=u>UTILISÉ</div></div></div>")

GUIDE_ICON = ("<svg width='170' height='40' viewBox='0 0 170 40'><g stroke='#2A2418' stroke-width='4' fill='#2A2418'>"
              "<line x1='5' y1='20' x2='30' y2='20'/><circle cx='42' cy='20' r='3.5' stroke='none'/><line x1='54' y1='20' x2='82' y2='20'/>"
              "<path d='M92 4 L120 20 L92 36 Z' stroke='none'/><line x1='126' y1='20' x2='146' y2='20'/><circle cx='162' cy='20' r='3.5' stroke='none'/></g></svg>")

# Milicien : fusil (silhouette gravée, encre du jeu)
FUSIL = ("<svg width='230' height='150' viewBox='0 0 230 150'><g transform='rotate(-22 115 75)' stroke='#2A2418' stroke-width='3' stroke-linejoin='round'>"
         "<path d='M8 70 L60 62 L70 70 L68 80 L18 92 Q6 94 6 84 Z' fill='#8B5A2B'/>"          # crosse
         "<path d='M66 64 L178 61 L178 69 L70 76 Z' fill='#8B5A2B'/>"                         # fût
         "<rect x='68' y='57' width='154' height='6' rx='2' fill='#6E6E70'/>"                  # canon
         "<path d='M70 66 L88 65 L88 72 L70 73 Z' fill='#6E6E70'/>"                            # platine
         "<path d='M74 65 Q75 54 84 55' fill='none' stroke-width='3.5'/>"                     # chien
         "<path d='M76 76 Q84 88 94 75' fill='none' stroke-width='3'/>"                        # pontet
         "</g></svg>")

# Interprète : collier de wampum (diplomatie)
def _wampum():
    perles = ''.join(f"<rect x='{14+i*13}' y='{20+r*13}' width='11' height='11' rx='2' fill='{('#4B2E5C' if (r in (1,2) and i%6 in (2,3)) or r in (0,3) and i%6 in (0,5) else '#F6F0E2')}' stroke='#2A2418' stroke-width='1.2'/>"
                     for i in range(14) for r in range(4))
    franges = ''.join(f"<line x1='{x}' y1='{y0}' x2='{x+dx}' y2='{y0+16}' stroke='#2A2418' stroke-width='2'/>" for x in (8, 10) for y0, dx in ((28, -6), (50, -6)))
    franges += ''.join(f"<line x1='{x}' y1='{y0}' x2='{x+6}' y2='{y0+16}' stroke='#2A2418' stroke-width='2'/>" for x in (200, 202) for y0 in (28, 50))
    return f"<svg width='214' height='90' viewBox='0 0 214 90'>{franges}<rect x='10' y='16' width='192' height='60' rx='3' fill='#E8DDC4' stroke='#2A2418' stroke-width='3'/>{perles}</svg>"
WAMPUM = _wampum()

if __name__ == '__main__':
    jeton('guide_test', 'Guide', '#2F5E4A', GUIDE_ICON, '+1', 'au raccourci')
    jeton('milicien', 'Milicien', '#44464C', FUSIL, '×2', 'au combat')
    jeton('interprete', 'Interprète', '#8A5A14', WAMPUM, '+1', 'dé au troc')
