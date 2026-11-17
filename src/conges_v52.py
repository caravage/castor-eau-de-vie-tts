# Congés v3.52 : 29 tuiles au nouveau design (cartouche « où » en haut, « qui et combien » en bas).
# Rendu vectoriel HTML -> PNG 400×400 (img/v18/cg52_*.png) + versos NON PAYÉ (cg52_np*.png).
# Usage : python3 src/conges_v52.py   (Playwright + Google Chrome)
import math, os
from playwright.sync_api import sync_playwright

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
F = R + 'src/plateau_hd/node_modules/@fontsource/'
IMG = R + 'src/plateau_hd/img/'
V = R + 'img/v18/'
OUT = V
INK, PAR, EDGE, MUT, OR, ROUGE = '#2A2418', '#F2EAD3', '#B7A675', '#6B5F45', '#D9A520', '#A3352A'
PAYS = '#C9A66B'
REG = {'bas': ('#993321', 'Lacs d’en bas', 'region_oniare.png'), 'sup': ('#2A406E', 'Lac Supérieur', 'region_mishipeshu.png'),
       'haut': ('#5A7832', 'Lacs d’en haut', 'region_tortue.png')}
FONTS = (f"@font-face{{font-family:SC;src:url(file://{F}im-fell-english-sc/files/im-fell-english-sc-latin-400-normal.woff2)}}"
         f"@font-face{{font-family:Fell;font-style:italic;src:url(file://{F}im-fell-english/files/im-fell-english-latin-400-italic.woff2)}}"
         f"@font-face{{font-family:Fell;font-style:normal;src:url(file://{F}im-fell-english/files/im-fell-english-latin-400-normal.woff2)}}"
         f"@font-face{{font-family:A;font-weight:700;src:url(file://{F}alegreya-sans/files/alegreya-sans-latin-700-normal.woff2)}}")
CSS = FONTS + f"*{{box-sizing:border-box;margin:0}}body{{background:transparent}}.t{{width:400px;height:400px;border-radius:26px;position:relative;overflow:hidden;background:{PAR}}}"
FLEUR = ("<path d='M0 -10C3 -6 3 -2 0 2C-3 -2 -3 -6 0 -10Z'/><path d='M-1 2C-6 -4 -11 0 -8 4C-6 2 -4 2 -2 4Z'/>"
         "<path d='M1 2C6 -4 11 0 8 4C6 2 4 2 2 4Z'/><rect x='-5' y='3' width='10' height='2.5'/><path d='M-2 5.5L0 10L2 5.5Z'/>")

def officier(s):
    return (f"<svg width='{s*.82:.0f}' height='{s}' viewBox='-12 -15 24 30'><ellipse rx='11' ry='14' fill='#FFFDF6' stroke='{INK}' stroke-width='1.3'/>"
            f"<g fill='{OR}' transform='scale(.95)'>{FLEUR}</g></svg>")
def missionnaire(s):
    return (f"<svg width='{s*.82:.0f}' height='{s}' viewBox='-12 -15 24 30'><ellipse rx='11' ry='14' fill='#2A2418' stroke='{INK}' stroke-width='1.3'/>"
            f"<path d='M0 -8V8M-5 -3H5' stroke='#FFFDF6' stroke-width='2.6'/></svg>")
def oeil(s): return f"<img src='file://{V}tok_oeil.png' style='width:{s}px;height:{s}px'>"
def jeton(nom, s): return f"<img src='file://{V}{nom}' style='width:{s}px;height:{s}px'>"
def med(k): return f"<img src='file://{IMG}{REG[k][2]}' style='width:92px;height:92px'>"
def flocon(s, c=INK):
    g = ''
    for k in range(6):
        a = math.radians(90 + 60 * k); x, y = 10 * math.cos(a), 10 * math.sin(a)
        g += f"<line x1='0' y1='0' x2='{x:.2f}' y2='{y:.2f}'/>"
        for sg in (-1, 1):
            b = a + sg * math.radians(40); mx, my = 6 * math.cos(a), 6 * math.sin(a)
            g += f"<line x1='{mx:.2f}' y1='{my:.2f}' x2='{mx + 3.6*math.cos(b):.2f}' y2='{my + 3.6*math.sin(b):.2f}'/>"
    return f"<svg width='{s}' height='{s}' viewBox='-12 -12 24 24'><g stroke='{c}' stroke-width='2' stroke-linecap='round'>{g}</g></svg>"
def prix_rond(txt, s=122, credit=False):
    c = ROUGE if credit else INK
    return (f"<div style='width:{s}px;height:{s}px;border-radius:50%;background:{PAR};border:6px solid #B8923A;"
            f"box-shadow:inset 0 0 0 5px {PAR},inset 0 0 0 7px #D8CBA6;display:flex;flex-direction:column;align-items:center;justify-content:center;"
            f"font:700 44px/0.9 A;color:{c};text-align:center'>{txt}</div>")
# Haut : mini-cartouche de zone de traite = OÙ va le canot
def cartouche(entete, couleur, corps, clair=True):
    return (f"<div style='position:absolute;left:22px;right:22px;top:20px;height:196px;border-radius:14px;background:#FBF7EC;border:3px solid {couleur};overflow:hidden'>"
            f"<div style='height:52px;background:{couleur};color:{'#F6EFDC' if clair else INK};font:30px SC,serif;display:flex;align-items:center;justify-content:center;letter-spacing:.5px'>{entete}</div>"
            f"<div style='height:138px;display:flex;align-items:center;justify-content:center;gap:12px;font:italic 30px Fell;color:{INK}'>{corps}</div></div>")
# Bas : QUI part (case « à bord »), case d'hiver, prix
def abord(p, label=True):
    icone = officier(66) if p == 'off' else missionnaire(66)
    return (f"<div style='display:flex;align-items:center;gap:6px'><div style='width:82px;height:96px;border-radius:50%;border:3px dashed {MUT};display:flex;align-items:center;justify-content:center'>{icone}</div>"
            + (f"<div style='font:italic 28px/1.0 Fell;color:{INK}'>avec<br>{'officier' if p == 'off' else 'missionnaire'}</div>" if label else '') + "</div>")
def hiver():   # emplacement d'un pion de joueur : un hiver passé
    return (f"<div style='width:104px;height:104px;border-radius:50%;border:4px dashed {MUT};display:flex;align-items:center;justify-content:center'>"
            f"<div style='opacity:.35'>{flocon(68)}</div></div>")
def caisses(n):
    return "<div style='display:flex;gap:4px'>" + ''.join(f"<img src='file://{V}tok_caisse.png' style='width:38px;height:38px'>" for _ in range(n)) + "</div>"
def si(t): return f"<span style='font:italic 38px/1.05 Fell;color:{INK};text-align:center'>{t}</span>"
def soup(n): return f"<span style='display:flex;align-items:center;gap:2px;font:700 34px A;color:{INK}'>si&nbsp;{oeil(50)}≤{n}</span>"
BELLIN = f"<div style='position:absolute;inset:0;background:url(file://{R}src/assets/carte_bellin.png) center/cover;opacity:.32;mix-blend-mode:multiply'></div>"
def tuile(entete, couleur, corps, gauche, prix, credit=False, clair=True):
    return (f"<div class=t style='border:3px solid {INK}'>{cartouche(entete, couleur, corps, clair)}"
            f"<div style='position:absolute;left:26px;right:22px;bottom:22px;height:126px;display:flex;align-items:center;justify-content:space-between'>"
            f"<div style='display:flex;align-items:center;gap:10px'>{''.join(gauche)}</div>{prix_rond(prix, 122, credit)}</div></div>")
def non_paye(p):   # verso : congé acheté à crédit, pas encore payé
    tampon = (f"<div style='position:absolute;left:50%;top:118px;transform:translateX(-50%) rotate(-12deg);border:7px solid {ROUGE};border-radius:12px;"
              f"padding:6px 18px;font:700 54px A;color:{ROUGE};letter-spacing:1px;white-space:nowrap'>NON PAYÉ</div>")
    return (f"<div class=t style='border:3px solid {INK}'><div style='position:absolute;left:0;right:0;top:40px;text-align:center;font:44px SC,serif;color:{INK}'>Congé</div>"
            f"{tampon}<div style='position:absolute;left:50%;bottom:30px;transform:translateX(-50%)'>{prix_rond(f'{p}&nbsp;₶', 130)}</div></div>")

P = lambda n: f'{n}&nbsp;₶'
CR = lambda n: f'<span>{n}</span><span style="font-size:22px;margin-top:2px">crédit{"s" if n > 1 else ""}</span>'
TOUTE = ('Toute Région', MUT)
PAYS_TXT = si('Mer de l’Ouest,<br>Illinois, Belle Rivière')
# (id, nombre, entête, couleur, corps, bas gauche, prix en ₶ ou None, crédits ou None, entête claire)
CONGES = [
 ('ord_m', 1, *TOUTE, si('<span style="font-size:44px">Moyen canot</span>'), [], 3, None),
 ('ord_m_off', 1, *TOUTE, si('<span style="font-size:44px">Moyen canot</span>'), [abord('off')], 2, None),
 ('ord_g', 2, *TOUTE, si('<span style="font-size:44px">Grand canot</span>'), [], 4, None),
 ('garn2', 1, *TOUTE, jeton('fort_fr.png', 78) + si('dans un fort'), [], 2, None),
 ('garn3', 1, *TOUTE, jeton('fort_fr.png', 78) + si('dans un fort'), [], 3, None),
 ('mis2', 1, *TOUTE, jeton('mission_hex.png', 78) + si('dans une<br>mission'), [], 2, None),
 ('mis3', 1, *TOUTE, jeton('mission_hex.png', 78) + si('dans une<br>mission'), [], 3, None),
 ('lib', 3, *TOUTE, BELLIN, [], 5, None),
 ('lib_off', 1, *TOUTE, BELLIN, [abord('off')], 5, None),
 ('lib3', 1, *TOUTE, BELLIN, [], 3, None),
 ('veuve', 1, *TOUTE, si('si capital<br>le plus bas'), [], 2, None),
 ('fabrique', 2, *TOUTE, soup(2), [abord('mis')], 3, None),
 ('faveur', 1, *TOUTE, soup(3), [abord('off')], None, 1),
 ('rochelle', 1, *TOUTE, soup(3), [caisses(4)], None, 1),
 ('haut', 1, REG['haut'][1], REG['haut'][0], med('haut') + si('ou Témiscamingue'), [], 3, None),
 ('haut_off', 1, REG['haut'][1], REG['haut'][0], med('haut'), [abord('off')], 2, None),
 ('haut_mis', 1, REG['haut'][1], REG['haut'][0], med('haut'), [abord('mis')], 2, None),
 ('sup', 1, REG['sup'][1], REG['sup'][0], med('sup'), [hiver()], 3, None),
 ('sup_off', 1, REG['sup'][1], REG['sup'][0], med('sup'), [hiver(), abord('off', False)], 2, None),
 ('sup_mis', 1, REG['sup'][1], REG['sup'][0], med('sup'), [hiver(), abord('mis', False)], 3, None),
 ('bas', 1, REG['bas'][1], REG['bas'][0], med('bas'), [], 3, None),
 ('bas_off', 1, REG['bas'][1], REG['bas'][0], med('bas'), [abord('off')], 3, None),
 ('bas_mis', 1, REG['bas'][1], REG['bas'][0], med('bas'), [abord('mis')], 2, None),
 ('pays', 2, 'Pays', PAYS, PAYS_TXT, [hiver()], 3, None, False),
]

def html_de(t): return f"<!doctype html><meta charset=utf-8><style>{CSS}</style><body>{t}</body>"

if __name__ == '__main__':
    pages = []
    for c in CONGES:
        cid, nb, ent, col, corps, gauche, p, cr = c[:8]
        clair = c[8] if len(c) > 8 else True
        pages.append((f'cg52_{cid}', tuile(ent, col, corps, gauche, P(p) if p else CR(cr), bool(cr), clair)))
    for p in sorted({c[6] for c in CONGES if c[6]}):
        pages.append((f'cg52_np{p}', non_paye(p)))
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg = b.new_page(viewport={'width': 400, 'height': 400})
        for nom, t in pages:
            f = f'/tmp/{nom}.html'; open(f, 'w').write(html_de(t))
            pg.goto('file://' + f); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(250)
            pg.locator('.t').screenshot(path=OUT + nom + '.png', omit_background=True)
        b.close()
    print(len(pages), 'images ;', sum(c[1] for c in CONGES), 'tuiles')
