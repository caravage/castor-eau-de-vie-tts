# Cartes Grands événements, pleine image (700×500). Image bord à bord, texte sur parchemin fondu.
import os, subprocess, html
HERE = os.path.dirname(os.path.abspath(__file__)); FONTS = os.path.join(HERE, '..', 'plateau_hd', 'fonts.css'); E = html.escape
INK, BX, OR, PAP = '#2B1B12', '#7E2A20', '#A8792E', '239,226,195'
CSS = f"""*{{box-sizing:border-box;margin:0;padding:0}}body{{width:700px;height:500px;background:transparent;overflow:hidden}}
.c{{position:absolute;inset:0;border-radius:0;overflow:hidden;background:rgb({PAP})}}
.zone{{position:absolute;overflow:hidden}}
.img{{position:absolute;inset:0;background-repeat:no-repeat;background-size:cover;filter:grayscale(1) sepia(.62) contrast(1.12) brightness(.98)}}
.vign{{position:absolute;inset:0;box-shadow:inset 0 0 60px rgba(50,28,12,.5)}}
.grain{{position:absolute;inset:0;mix-blend-mode:multiply;opacity:.5}}
.t{{position:absolute;text-align:center;font-family:'IM Fell English SC';color:{INK};line-height:1.02}}
.fx{{position:absolute;text-align:center;font-family:'IM Fell English';color:{INK};line-height:1.26}}.ico .fx{{line-height:1.75}}
.fx b{{font-weight:400;font-family:'IM Fell English SC';color:{BX};letter-spacing:1.5px;font-size:.92em}}
.sig{{position:absolute;object-fit:contain;filter:sepia(1) saturate(1.8) hue-rotate(-12deg) brightness(.42) contrast(1.6);mix-blend-mode:multiply}}"""
GRAIN = ("<svg class='grain' width='700' height='500'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3' seed='7'/>"
         "<feColorMatrix values='0 0 0 0 .45  0 0 0 0 .33  0 0 0 0 .18  0 0 0 .55 0'/></filter>"
         "<filter id='t'><feTurbulence type='fractalNoise' baseFrequency='.012' numOctaves='3' seed='3'/><feColorMatrix values='0 0 0 0 .55  0 0 0 0 .40  0 0 0 0 .20  0 0 0 .4 0'/></filter>"
         "<rect width='100%' height='100%' filter='url(#t)' opacity='.5'/><rect width='100%' height='100%' filter='url(#n)' opacity='.35'/></svg>")
def orn(x, y, w):
    return (f"<svg style='position:absolute;left:{x-w}px;top:{y}px' width='{2*w}' height='18'><path d='M0 9 L{w-22} 9 M{w+22} 9 L{2*w} 9' stroke='{OR}' stroke-width='1'/>"
            f"<path d='M{w} 2 L{w+7} 9 L{w} 16 L{w-7} 9 Z' fill='{BX}'/><path d='M{w-12} 9 L{w-17} 5 L{w-22} 9 L{w-17} 13 Z M{w+12} 9 L{w+17} 5 L{w+22} 9 L{w+17} 13 Z' fill='{OR}'/></svg>")
def photo(c):
    if c['img'] == 'paix':
        s = "<div class='img' style='filter:none;background:#EFE3C4'></div>"
        src = f'{HERE}/sources'
        s += f"<img class='sig' src='file://{src}/paix_01.svg' style='left:200px;top:22px;width:300px;height:54px'>"
        for k, n in enumerate(['04', '07', '22', '03', '05', '06']):
            s += f"<img class='sig' src='file://{src}/paix_{n}.svg' style='left:{28 + k*108}px;top:86px;width:104px;height:150px'>"
        return s
    return f"<div class='img' style=\"background-image:url('file://{HERE}/sources/{c['img']}');background-position:{c['pos']};transform:scale({c.get('zoom',1)});transform-origin:{c['pos']}\"></div>"
def haut(c):   # image en haut sur h px, fondu de 70 px dans le parchemin
    h = c.get('h', 300)
    b = (f"<div class='c'><div class='zone' style='left:0;right:0;top:0;height:{h}px'>{photo(c)}<div class='vign'></div></div>"
         f"<div style='position:absolute;left:0;right:0;top:{h-70}px;height:70px;background:linear-gradient(to bottom,rgba({PAP},0),rgb({PAP}))'></div>" + GRAIN)
    y = h + 2
    b += f"<div class='t' style='left:30px;right:30px;top:{y}px;font-size:36px'>{E(c['titre'])}</div>" + orn(350, y + 42, 170)
    b += f"<div class='fx' style='left:58px;right:58px;top:{y+68 + (14 if c.get('fs',21) >= 24 else 0)}px;font-size:{c.get('fs',21)}px'>{c['fx']}</div></div>"
    return b
def gauche(c):  # image à gauche sur w px, fondu de 70 px
    w = c.get('w', 330)
    b = (f"<div class='c'><div class='zone' style='left:0;top:0;bottom:0;width:{w}px'>{photo(c)}<div class='vign'></div></div>"
         f"<div style='position:absolute;top:0;bottom:0;left:{w-70}px;width:70px;background:linear-gradient(to right,rgba({PAP},0),rgb({PAP}))'></div>" + GRAIN)
    cx = (w + 700) / 2
    b += f"<div class='t' style='left:{w+10}px;right:24px;top:{c.get('ty',160)}px;font-size:36px'>{E(c['titre'])}</div>" + orn(cx, c.get('ty',160) + 84, 120)
    b += f"<div class='fx' style='left:{w+18}px;right:34px;top:{c.get('ty',160)+112}px;font-size:{c.get('fs',21)}px'>{c['fx']}</div></div>"
    return b
IMG = os.path.abspath(os.path.join(HERE, '..', '..', 'img', 'v18'))
def ic(n, h=30, extra=''):
    return f"<img src='file://{IMG}/{n}.png' style='height:{h}px;vertical-align:middle;margin:0 2px;{extra}'>"
def de(n, s=26):
    pts = {1: [(2, 2)], 2: [(1, 1), (3, 3)], 3: [(1, 1), (2, 2), (3, 3)], 4: [(1, 1), (3, 1), (1, 3), (3, 3)], 5: [(1, 1), (3, 1), (2, 2), (1, 3), (3, 3)], 6: [(1, 1), (3, 1), (1, 2), (3, 2), (1, 3), (3, 3)]}
    d = ''.join(f"<circle cx='{x*6}' cy='{y*6}' r='1.9' fill='#F6ECD2'/>" for x, y in pts[n]) if n else "<text x='12' y='17' text-anchor='middle' font-size='14' fill='#F6ECD2' font-family='IM Fell English'>?</text>"
    return f"<svg width='{s}' height='{s}' viewBox='0 0 24 24' style='vertical-align:middle;margin:0 1px'><rect x='1' y='1' width='22' height='22' rx='4' fill='{INK}'/>{d}</svg>"
def fi(s=30):   # Force iroquoise : casse-tête blanc sur fond brun-rouge
    return (f"<svg width='{s}' height='{s}' viewBox='0 0 30 30' style='vertical-align:middle;margin:0 2px'><rect x='1' y='1' width='28' height='28' rx='6' fill='#5A2418' stroke='#2B1209' stroke-width='1.5'/>"
            "<path d='M9 24 L19 10' stroke='#F6ECD2' stroke-width='2.6' stroke-linecap='round'/><circle cx='20.5' cy='8.5' r='4.2' fill='#F6ECD2'/>"
            "<path d='M7 13 L13 7' stroke='#C9952B' stroke-width='1.6'/><path d='M7 9 l3 0 M8 7 l0 3' stroke='#C9952B' stroke-width='1.2'/></svg>")
def pv(s=30):
    return (f"<svg width='{s}' height='{s}' viewBox='0 0 30 30' style='vertical-align:middle;margin:0 2px'><circle cx='15' cy='15' r='13.5' fill='#C9952B' stroke='#5C3216' stroke-width='1.5'/>"
            "<text x='15' y='19.5' text-anchor='middle' font-family='IM Fell English SC' font-size='13' fill='#2B1B12'>VP</text></svg>")
FLECHE = "<span style='font-family:serif;color:#7E2A20'>→</span>"
L = lambda t: f"<b>{t}</b>"
ICONES = {
 'incendie': f"Chaque joueur {de(0)} · {de(0)} en plus = 2 {ic('part_lt',26)} · garde le meilleur<br>Le plus bas : − crédit = {de(0)}<br><span style='font-size:.82em'>Égalité : tous perdent</span>",
 'lachine': f"{fi(34)} +3<br>{ic('evt_raid',46)} {FLECHE} rivière des Outaouais",
 'guerre': (f"{L('1re pioche')} &nbsp;{fi()} +2 &nbsp; {ic('ravage')} +1 &nbsp; {ic('fort_uk')} Albany, pris : −2 {pv()}<br>"
            f"{L('Course')} &nbsp;{ic('navire')} {de(1)} coulé, au chantier · {de(2)}{de(3)} rien · {de(4)}{de(5)}{de(6)} +4 {ic('part_lt',26)}<br>"
            f"{L('2e pioche')} &nbsp;{ic('navire')} traverse : {de(1)}{de(2)} coulé, au chantier<br><span style='font-size:.8em;font-style:italic'>Après la 1re pioche, la carte est remélangée dans le paquet.</span>"),
 'ordonnance': f"{ic('conge_back',46)} <span style='font-size:1.6em;color:#7E2A20;vertical-align:middle'>✕</span><br>{ic('fort_fr',34)} 1 par région, les autres fermés",
 'paix': f"{fi(36)} {FLECHE} 0",
 'variole': f"+1 {ic('evt7_epidemie',52)} au sac, définitivement",
}
CARTES = [
 dict(id='incendie', f=haut, img='incendie.jpg', pos='50% 62%', h=300, fs=19.5, titre="Incendie de la basse-ville",
      fx="Chaque joueur lance 1 dé et peut acheter des dés en plus, pour 2 ₶ chacun ; il garde le meilleur. Le joueur au dé le plus bas perd autant de crédit que la valeur de son dé. En cas d'égalité, tous les ex aequo perdent."),
 dict(id='lachine', f=gauche, img='lachine.jpg', pos='50% 26%', zoom=1.3, w=340, fs=23, ty=150, titre="Massacre de Lachine",
      fx="La Force iroquoise augmente de 3. Un raid frappe immédiatement la rivière des Outaouais."),
 dict(id='guerre', f=haut, img='guerre.jpg', pos='42% 28%', zoom=1.1, h=214, fs=16.2, titre="Guerre avec l'Angleterre",
      fx="<b>1re pioche</b> · La Force iroquoise augmente de 2 et le Ravage de 1. Un joueur pris lors d'une vente à Albany perd 2 VP. Au lieu de traverser, un navire peut partir en course : il lance 1 dé ; sur 1, il est coulé et remis au chantier ; sur 2 ou 3, rien ne se passe ; sur 4 à 6, il rapporte 4 ₶. La carte est ensuite remélangée dans le paquet.<br><b>2e pioche</b> · Chaque navire qui traverse lance 1 dé ; sur 1 ou 2, il est coulé et remis au chantier."),
 dict(id='ordonnance', f=gauche, img='ordonnance_lisse.jpg', pos='50% 34%', zoom=1.25, w=320, ty=120, fs=21, titre="Ordonnance royale",
      fx="Cette année, aucun congé n'est émis. Dans chaque région, un seul fort reste ouvert, au choix du joueur le plus haut sur la piste du Gouverneur ; les autres sont fermés."),
 dict(id='paix', f=haut, img='paix', h=270, fs=25, titre="Grande Paix de Montréal", fx="La Force iroquoise retombe à 0."),
 dict(id='amnistie', f=gauche, img='amnistie.jpg', pos='40% 60%', zoom=1.18, w=330, ty=150, fs=23, titre="Amnistie des coureurs des bois", fx="Chaque joueur retire 2 points de soupçon."),
]
import sys
ICO = 'ico' in sys.argv
for c in CARTES:
    import re as _re
    c['fx'] = _re.sub(r" ([;:!?])", "\u00a0\\1", c['fx'])
    c['fx'] = _re.sub(r"(\b(?:de|à|sur|lance|perd|rapporte|\d)) (\d|dé|₶|VP|ou)", "\\1\u00a0\\2", c['fx'])
    if ICO: c['fx'] = ICONES[c['id']]; c['fs'] = {'guerre': 17, 'incendie': 19}.get(c['id'], 23)
    p = f"{HERE}/html/full_{'ico_' if ICO else ''}{c['id']}.html"
    open(p, 'w').write(f"<!doctype html><html><head><meta charset='utf-8'><link rel='stylesheet' href='file://{FONTS}'><style>{CSS}</style></head><body>{c['f'](c)}</body></html>")
    subprocess.run(['google-chrome', '--headless=new', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files', '--force-device-scale-factor=2',
                    '--default-background-color=00000000', '--virtual-time-budget=4000', f"--screenshot={HERE}/png/full_{'ico_' if ICO else ''}{c['id']}.png", '--window-size=700,500', f'file://{p}'],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
print('ok')

# Dos du paquet (même format) et planche TTS 3 × 2 (cellules 1050 × 750)
FIL = os.path.abspath(os.path.join(HERE, '..', 'assets', 'quebec_filigrane.png'))
dos = (f"<div class='c' style='background:#2E1913'><div style='position:absolute;inset:14px;border-radius:13px;overflow:hidden;background:radial-gradient(ellipse at 50% 45%,#F6ECD2,#E6D3A8 70%,#D2BA88)'>"
       f"<img src='file://{FIL}' style='position:absolute;left:50%;top:50%;width:560px;transform:translate(-50%,-50%);opacity:.22;mix-blend-mode:multiply'>{GRAIN}"
       f"<div style='position:absolute;inset:10px;border:1.6px solid {OR};border-radius:7px'></div><div style='position:absolute;inset:15px;border:.7px solid {OR};border-radius:5px'></div></div>"
       f"<div class='t' style='left:0;right:0;top:196px;font-size:50px'>Grand événement</div>" + orn(350, 262, 200)
       + f"<div class='fx' style='left:0;right:0;top:292px;font-size:19px;font-style:italic'>Castor et eau-de-vie</div></div>")
p = f"{HERE}/html/full_dos.html"
open(p, 'w').write(f"<!doctype html><html><head><meta charset='utf-8'><link rel='stylesheet' href='file://{FONTS}'><style>{CSS}</style></head><body>{dos}</body></html>")
subprocess.run(['google-chrome', '--headless=new', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files', '--force-device-scale-factor=2',
                '--default-background-color=00000000', '--virtual-time-budget=4000', f"--screenshot={HERE}/png/full_dos.png", '--window-size=700,500', f'file://{p}'],
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
if not ICO:
    from PIL import Image
    ORDRE = ['incendie', 'lachine', 'guerre', 'ordonnance', 'paix', 'amnistie']
    W, H = 1050, 750
    sheet = Image.new('RGB', (W * 3, H * 2), (46, 25, 19))
    for k, n in enumerate(ORDRE):
        im = Image.open(f'{HERE}/png/full_{n}.png').convert('RGBA').resize((W, H), Image.LANCZOS)
        bg = Image.new('RGBA', (W, H), (46, 25, 19, 255)); bg.alpha_composite(im)
        sheet.paste(bg.convert('RGB'), ((k % 3) * W, (k // 3) * H))
    out = os.path.abspath(os.path.join(HERE, '..', '..', 'img', 'v18'))
    sheet.save(f'{out}/deck_grand_v2.jpg', quality=90)
    d = Image.open(f'{HERE}/png/full_dos.png').convert('RGBA').resize((W, H), Image.LANCZOS)
    bg = Image.new('RGBA', (W, H), (46, 25, 19, 255)); bg.alpha_composite(d); bg.convert('RGB').save(f'{out}/deck_grand_v2_back.jpg', quality=90)
    print('planche', sheet.size)
