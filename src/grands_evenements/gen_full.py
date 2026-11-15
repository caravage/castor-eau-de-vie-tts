# Essai « full art » horizontal (700×500) : gravure bord à bord, texte sur un parchemin fondu
import os, subprocess, html
HERE = os.path.dirname(os.path.abspath(__file__)); FONTS = os.path.join(HERE, '..', 'plateau_hd', 'fonts.css'); E = html.escape
INK, BX, OR = '#2B1B12', '#7E2A20', '#A8792E'
CSS = f"""*{{box-sizing:border-box;margin:0;padding:0}}body{{width:700px;height:500px;background:transparent;overflow:hidden}}
.c{{position:absolute;inset:0;border-radius:22px;overflow:hidden;background:#E9DAB6}}
.img{{position:absolute;inset:0;background-repeat:no-repeat;background-size:cover;filter:grayscale(1) sepia(.62) contrast(1.12) brightness(.98)}}
.vign{{position:absolute;inset:0;box-shadow:inset 0 0 70px rgba(50,28,12,.55)}}
.grain{{position:absolute;inset:0;mix-blend-mode:multiply;opacity:.5}}
.lab{{position:absolute;font-family:'IM Fell English SC';font-size:15px;letter-spacing:4.5px;color:{BX}}}
.t{{position:absolute;text-align:center;font-family:'IM Fell English SC';color:{INK};line-height:1.02}}
.fx{{position:absolute;text-align:center;font-family:'IM Fell English';color:{INK};line-height:1.28}}"""
GRAIN = ("<svg class='grain' width='700' height='500'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3' seed='7'/>"
         "<feColorMatrix values='0 0 0 0 .45  0 0 0 0 .33  0 0 0 0 .18  0 0 0 .55 0'/></filter><rect width='100%' height='100%' filter='url(#n)' opacity='.35'/></svg>")
def orn(x, y, w):
    return (f"<svg style='position:absolute;left:{x-w}px;top:{y}px' width='{2*w}' height='18'><path d='M0 9 L{w-22} 9 M{w+22} 9 L{2*w} 9' stroke='{OR}' stroke-width='1'/>"
            f"<path d='M{w} 2 L{w+7} 9 L{w} 16 L{w-7} 9 Z' fill='{BX}'/><path d='M{w-12} 9 L{w-17} 5 L{w-22} 9 L{w-17} 13 Z M{w+12} 9 L{w+17} 5 L{w+22} 9 L{w+17} 13 Z' fill='{OR}'/></svg>")
def bas(img, pos, zoom, titre, fx):   # parchemin en bas, fondu vers le haut
    return (f"<div class='c'><div class='img' style=\"background-image:url('file://{HERE}/sources/{img}');bottom:130px;background-position:{pos};transform:scale({zoom});transform-origin:{pos}\"></div>"
            "<div class='vign'></div>"
            "<div style='position:absolute;left:0;right:0;bottom:0;height:250px;background:linear-gradient(to bottom,rgba(239,226,195,0) 0%,rgba(239,226,195,.95) 30%,#EFE2C3 42%)'></div>"
            + GRAIN + f"<div class='lab' style='left:0;right:0;top:300px;text-align:center'>Grand événement</div>"
            f"<div class='t' style='left:30px;right:30px;top:322px;font-size:36px'>{E(titre)}</div>" + orn(350, 364, 170)
            + f"<div class='fx' style='left:70px;right:70px;top:390px;font-size:21px'>{E(fx)}</div></div>")
def droite(img, pos, zoom, titre, fx):   # parchemin à droite, fondu vers la gauche
    return (f"<div class='c'><div class='img' style=\"background-image:url('file://{HERE}/sources/{img}');right:220px;background-position:{pos};transform:scale({zoom});transform-origin:{pos}\"></div>"
            "<div class='vign'></div>"
            "<div style='position:absolute;top:0;bottom:0;right:0;width:400px;background:linear-gradient(to right,rgba(239,226,195,0) 0%,rgba(239,226,195,.92) 30%,#EFE2C3 48%)'></div>"
            + GRAIN + f"<div class='lab' style='left:400px;right:20px;top:70px;text-align:center'>Grand événement</div>"
            f"<div class='t' style='left:410px;right:26px;top:150px;font-size:36px'>{E(titre)}</div>" + orn(545, 236, 120)
            + f"<div class='fx' style='left:420px;right:36px;top:266px;font-size:21px'>{E(fx)}</div></div>")
essais = [('F_guerre', bas('guerre.jpg', '42% 30%', 1.1, "Guerre avec l'Angleterre", "Risque à la traversée des navires. Chaque joueur peut envoyer ses navires en course.")),
          ('F_incendie', bas('incendie.jpg', '50% 60%', 1.0, "Incendie de la basse-ville", "Chaque joueur lance 1 dé ; il peut acheter des dés en plus (2 ₶ chacun) et garde le meilleur. Le plus bas perd autant de crédit que la valeur de son dé. Égalité : tous perdent.")),
          ('F_lachine', droite('lachine.jpg', '50% 26%', 1.3, "Massacre de Lachine", "Force iroquoise +3. Raid immédiat sur la rivière des Outaouais."))]
for nom, body in essais:
    p = f"{HERE}/html/{nom}.html"
    open(p, 'w').write(f"<!doctype html><html><head><meta charset='utf-8'><link rel='stylesheet' href='file://{FONTS}'><style>{CSS}</style></head><body>{body}</body></html>")
    subprocess.run(['google-chrome', '--headless=new', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files', '--force-device-scale-factor=2',
                    '--default-background-color=00000000', '--virtual-time-budget=4000', f"--screenshot={HERE}/png/{nom}.png", '--window-size=700,500', f'file://{p}'],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
print('ok')
