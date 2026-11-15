# Cartes Grands événements : gravures d'époque (domaine public, Wikimedia Commons) passées en sépia.
# Rendu : python3 gen.py  → html/*.html puis png/*.png (Chrome headless, ×2)
import os, subprocess, html
HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, '..', 'plateau_hd', 'fonts.css')
os.makedirs(f'{HERE}/html', exist_ok=True); os.makedirs(f'{HERE}/png', exist_ok=True)
E = html.escape

CARTES = [
    dict(id='incendie', titre="Incendie de la basse-ville", img='incendie.jpg', pos='42% 30%', zoom=1.25,
         effet="Chaque joueur lance un dé ; il peut acheter des dés supplémentaires à 2 ₶ chacun et garde le meilleur. Le joueur au dé le plus bas perd autant de crédit que la valeur de son dé (égalité : tous les ex aequo)."),
    dict(id='lachine', titre="Massacre de Lachine", img='lachine.jpg', pos='52% 22%', zoom=1.22,
         effet="Force iroquoise +2, et un raid immédiat sur un portage près de Montréal."),
    dict(id='guerre', titre="Guerre avec l'Angleterre", img='guerre.jpg', pos='40% 30%', zoom=1.3,
         effet="Risque à la traversée des navires. Chaque joueur peut envoyer ses navires en course.",
         second="La guerre s'intensifie : effets renforcés."),
    dict(id='ordonnance', titre="Ordonnance royale", img='ordonnance_lisse.jpg', pos='50% 36%', zoom=1.12,
         effet="Aucun congé émis. Chaque fort sans milice est fermé."),
    dict(id='paix', titre="Grande Paix de Montréal", img=None,
         effet="La Force iroquoise retombe à 0."),
    dict(id='variole', titre="Variole", img='variole.jpg', pos='30% 30%', zoom=1.0,
         effet="1 tuile Épidémie entre dans le sac."),
]

INK, BORDEAUX, OR, OR_C = '#2B1B12', '#7E2A20', '#A8792E', '#D9B56A'

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{width:500px;height:700px;background:transparent;overflow:hidden}
.carte{position:absolute;inset:0;border-radius:22px;background:#2E1913;overflow:hidden}
.carte:before{content:'';position:absolute;inset:0;border-radius:22px;
  background:repeating-linear-gradient(45deg,rgba(255,255,255,.035) 0 2px,transparent 2px 6px)}
.papier{position:absolute;inset:13px;border-radius:13px;overflow:hidden;
  background:radial-gradient(ellipse at 50% 42%,#F6ECD2 0%,#EEDFBC 58%,#DCC79A 100%)}
.grain{position:absolute;inset:0;mix-blend-mode:multiply;opacity:.55}
.filet{position:absolute;inset:9px;border:1.6px solid @OR;border-radius:7px}
.filet2{position:absolute;inset:13px;border:.7px solid @OR;border-radius:5px;opacity:.8}
.coin{position:absolute;width:34px;height:34px}
.bandeau{position:absolute;left:0;right:0;top:33px;text-align:center;font-family:'IM Fell English SC';
  font-size:15px;letter-spacing:4.5px;color:@BX}
.bandeau span{background:transparent;padding:0 10px}
.planche{position:absolute;overflow:hidden;left:34px;right:34px;top:60px;height:316px;background:#E9DAB6;
  outline:1.4px solid @INK;outline-offset:3px;box-shadow:0 0 0 6px #EDE0BF,0 0 0 7.2px @OR}
.planche .img{position:absolute;inset:0;background-repeat:no-repeat;
  filter:grayscale(1) sepia(.62) contrast(1.12) brightness(.98)}
.planche .vign{position:absolute;inset:0;box-shadow:inset 0 0 38px rgba(60,35,15,.55)}
.titre{position:absolute;left:24px;right:24px;top:398px;text-align:center;font-family:'IM Fell English SC';
  font-size:36px;line-height:1.02;color:@INK}
.orn{position:absolute;left:0;right:0;height:18px}
.effet{position:absolute;left:46px;right:46px;text-align:center;font-family:'IM Fell English';
  color:@INK;line-height:1.28}
.second{position:absolute;left:52px;right:52px;text-align:center;font-family:'IM Fell English';font-style:italic;color:@INK;font-size:18.5px;line-height:1.25}
.second b{display:block;font-style:normal;font-weight:400;font-family:'IM Fell English SC';color:@BX;font-size:16px;letter-spacing:2.5px;margin-bottom:2px}
.sig{position:absolute;filter:sepia(1) saturate(1.8) hue-rotate(-12deg) brightness(.42) contrast(1.6) drop-shadow(0 0 .4px #3a2210);mix-blend-mode:multiply}
""".replace('@OR', OR).replace('@BX', BORDEAUX).replace('@INK', INK)

GRAIN = ("<svg class='grain' width='474' height='674'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3' seed='7'/>"
         "<feColorMatrix values='0 0 0 0 .45  0 0 0 0 .33  0 0 0 0 .18  0 0 0 .55 0'/></filter>"
         "<filter id='t'><feTurbulence type='fractalNoise' baseFrequency='.012' numOctaves='3' seed='3'/>"
         "<feColorMatrix values='0 0 0 0 .55  0 0 0 0 .40  0 0 0 0 .20  0 0 0 .45 0'/></filter>"
         "<rect width='100%' height='100%' filter='url(#t)' opacity='.6'/><rect width='100%' height='100%' filter='url(#n)' opacity='.35'/></svg>")

def coin(x, y, rot):
    return (f"<svg class='coin' style='left:{x}px;top:{y}px;transform:rotate({rot}deg)' viewBox='0 0 34 34'>"
            f"<path d='M3 31 C3 15 15 3 31 3' fill='none' stroke='{OR}' stroke-width='1.3'/>"
            f"<path d='M8 31 C8 19 19 8 31 8' fill='none' stroke='{OR}' stroke-width='.7'/>"
            f"<path d='M3 3 L12 3 M3 3 L3 12' stroke='{OR}' stroke-width='1.6'/><circle cx='3' cy='3' r='2.6' fill='{BORDEAUX}'/>"
            f"<path d='M14 14 l3 -5 l3 5 l-3 5 z' fill='{OR}' transform='rotate(-45 17 14)'/></svg>")

def orn(top, w=170):
    c = 250; a, b = c - w, c + w
    return (f"<svg class='orn' style='top:{top}px' viewBox='0 0 500 18'>"
            f"<path d='M{a} 9 L{c-22} 9' stroke='{OR}' stroke-width='1'/><path d='M{c+22} 9 L{b} 9' stroke='{OR}' stroke-width='1'/>"
            f"<circle cx='{a}' cy='9' r='1.8' fill='{OR}'/><circle cx='{b}' cy='9' r='1.8' fill='{OR}'/>"
            f"<path d='M{c} 2 L{c+7} 9 L{c} 16 L{c-7} 9 Z' fill='{BORDEAUX}'/>"
            f"<path d='M{c-12} 9 L{c-17} 5 L{c-22} 9 L{c-17} 13 Z M{c+12} 9 L{c+17} 5 L{c+22} 9 L{c+17} 13 Z' fill='{OR}'/></svg>")

def bandeau():
    return (f"<div class='bandeau'><svg width='432' height='18' viewBox='0 0 432 18' style='position:absolute;left:34px;top:0'>"
            f"<path d='M0 9 L118 9 M314 9 L432 9' stroke='{OR}' stroke-width='1'/><path d='M118 5 L124 9 L118 13 Z M314 5 L308 9 L314 13 Z' fill='{OR}'/></svg>"
            f"<span>Grand événement</span></div>")

def planche_paix():
    src = f'{HERE}/sources'
    s = f"<div class='planche' style='background:#EFE3C4'><div class='vign' style='box-shadow:inset 0 0 30px rgba(90,60,25,.35)'></div>"
    s += f"<img class='sig' src='file://{src}/paix_01.svg' style='left:96px;top:8px;width:240px;height:46px;object-fit:contain'>"
    grid = ['04', '07', '22', '03', '05', '06']
    for k, n in enumerate(grid):
        x = 10 + (k % 3) * 138; y = 62 + (k // 3) * 126
        s += f"<img class='sig' src='file://{src}/paix_{n}.svg' style='left:{x}px;top:{y}px;width:132px;height:122px;object-fit:contain'>"
    return s + "</div>"

def carte(c):
    body = "<div class='carte'><div class='papier'>" + GRAIN + "<div class='filet'></div><div class='filet2'></div></div>"
    body += coin(17, 17, 0) + coin(449, 17, 90) + coin(449, 649, 180) + coin(17, 649, 270)
    body += bandeau()
    if c['img']:
        body += (f"<div class='planche'><div class='img' style=\"background-image:url('file://{HERE}/sources/{c['img']}');"
                 f"background-size:{c['zoom']*100:.0f}% auto;background-size:cover;background-position:{c['pos']};transform:scale({c['zoom']});transform-origin:{c['pos']}\"></div>"
                 "<div class='vign'></div></div>")
    else:
        body += planche_paix()
    titre = c['titre']; fs = 36 if len(titre) <= 22 else 32
    body += f"<div class='titre' style='font-size:{fs}px'>{E(titre)}</div>"
    body += orn(446)
    long = len(c['effet'])
    fs = 24 if long < 90 else 20.5 if long < 150 else 19
    if c.get('second'):
        body += f"<div class='effet' style='top:480px;font-size:{fs}px'>{E(c['effet'])}</div>"
        body += orn(568, 60)
        body += f"<div class='second' style='top:592px'><b>Seconde pioche</b>{E(c['second'])}</div>"
    else:
        top = 528 - (0 if long < 90 else 36 if long < 150 else 52)
        body += f"<div class='effet' style='top:{top}px;font-size:{fs}px'>{E(c['effet'])}</div>"
    return body + "</div>"

for c in CARTES:
    p = f"{HERE}/html/gev_{c['id']}.html"
    open(p, 'w').write(f"<!doctype html><html><head><meta charset='utf-8'><link rel='stylesheet' href='file://{FONTS}'><style>{CSS}</style></head><body>{carte(c)}</body></html>")
    subprocess.run(['google-chrome', '--headless=new', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files',
                    '--force-device-scale-factor=2', '--default-background-color=00000000', '--virtual-time-budget=4000',
                    f"--screenshot={HERE}/png/gev_{c['id']}.png", '--window-size=500,700', f'file://{p}'],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
print('ok')
