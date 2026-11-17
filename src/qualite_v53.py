# Passe qualité v3.53 (17 nov. 2026) : corrections visuelles validées après l'analyse du plateau et des images.
#  2 tuiles Événements du mois : coins transparents          7 dos des congés : « Congé » seul
# 11 jeton Coureur des bois en gravure                      13 distillerie : gravure de l'alambic partout
# 14 tuile Scorbut : pagaie barrée (icône des voyageurs)     15 congé Lacs d'en haut : tortue centrée
# 16 cartes Navire et Distillerie : textes agrandis          8 jetons voyageurs : IM Fell + Alegreya Sans
# Usage (depuis src/) : python3 qualite_v53.py <dossier de sortie>
import base64, html, io, os, sys
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright
from polices import CSS as POLCSS, CHROME
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
V = R + 'img/v18/'; A = R + 'src/assets/'
OUT = (sys.argv[1] if len(sys.argv) > 1 else 'out').rstrip('/') + '/'; os.makedirs(OUT, exist_ok=True)
E = html.escape
INK, MUTED, EDGE, PAPER, FRAME = '#2A2418', '#6B5F45', '#B7A675', '#F6EFDC', '#22332F'
DISP, SER, BODY = "'IM Fell English SC',serif", "'IM Fell English',serif", "'Alegreya Sans',sans-serif"
def uri(p, mime='image/png'): return f'data:{mime};base64,' + base64.b64encode(open(p, 'rb').read()).decode()
PAGES = []
def page(nom, w, h, corps, css=''):
    PAGES.append((nom, w, h, f"<!doctype html><meta charset=utf-8><style>{POLCSS}*{{box-sizing:border-box;margin:0;padding:0}}"
                             f"html,body{{background:transparent}}{css}</style><body style='width:{w}px;height:{h}px;overflow:hidden'>{corps}</body>"))
def svg(nom, w, h, k, inner, css=''):
    page(nom, w * k, h * k, f"<svg xmlns='http://www.w3.org/2000/svg' width='{w*k}' height='{h*k}' viewBox='0 0 {w} {h}'>{inner}</svg>", css)

# ---------------------------------------------------------------- 2. Événements du mois : coins transparents
def coins_transparents():
    for n in ('evt_back', 'evt_calme', 'evt6_abondante', 'evt6_hiver', 'evt7_epidemie', 'evt7_epuise', 'evt7_occasion', 'evt7_profond',
              'evt7_tempete', 'evt8_hudson', 'evt_raid1_b', 'evt_raid2_b', 'evt_raid3_b'):
        im = Image.open(V + n + '.png').convert('RGB'); w, h = im.size
        d = next(i for i in range(w // 2) if sum(im.getpixel((i, i))) < 700)        # première diagonale non blanche
        r = round(d / (1 - 2 ** -.5)) + 1; k = 4
        m = Image.new('L', (w * k, h * k), 0); ImageDraw.Draw(m).rounded_rectangle((k, k, w * k - k - 1, h * k - k - 1), r * k, fill=255)
        im.putalpha(m.resize((w, h), Image.LANCZOS)); im.save(OUT + 'evt53_' + n.split('_', 1)[1] + '.png')

# ---------------------------------------------------------------- 7. Dos des congés : « Congé » seul
svg('conge_back_v53', 400, 400, 1, f"<rect x='8' y='8' width='384' height='384' rx='46' fill='#8E2F25' stroke='#5E1F18' stroke-width='8'/>"
    f"<text x='200' y='222' text-anchor='middle' font-family=\"{DISP}\" font-size='72' fill='#F6EFDC'>Congé</text>")

# ---------------------------------------------------------------- 11. Coureur des bois : gravure (source de l'Amnistie)
def _coureur():
    im = Image.open(R + 'src/grands_evenements/sources/amnistie.jpg').convert('L').crop((287, 716, 1719, 2148)).resize((736, 736), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, 'JPEG', quality=88); return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
svg('tok_coureur_v53', 400, 400, 1,
    "<defs><clipPath id='cp'><rect x='16' y='16' width='368' height='368' rx='40'/></clipPath>"
    "<filter id='sep'><feColorMatrix type='matrix' values='.80 0 0 0 .16  .74 0 0 0 .13  .62 0 0 0 .08  0 0 0 1 0'/></filter></defs>"
    f"<rect x='8' y='8' width='384' height='384' rx='46' fill='{PAPER}' stroke='{EDGE}' stroke-width='8'/>"
    f"<image href='{_coureur()}' x='16' y='16' width='368' height='368' clip-path='url(#cp)' filter='url(#sep)'/>"
    f"<rect x='16' y='304' width='368' height='80' fill='{FRAME}' opacity='.9' clip-path='url(#cp)'/>"
    f"<text x='200' y='357' text-anchor='middle' font-family=\"{DISP}\" font-size='42' fill='#F6EFDC'>Coureur des bois</text>")

# ---------------------------------------------------------------- 13 et 16. Cartes Navire / Distillerie, pions Distillerie
BROWN, COPPER = '#4A3324', '#8A4B2A'
SHIPS = ["L’Aigle d’Or", "Le Courageux", "Le Jardin de Hollande", "Le Saint-Jean-Baptiste", "La Famille", "Le Vieux Siméon"]
DISTILLERIES = [('Fonds-Saint-Jacques', 'Fonds-St-Jacques'), ('La Lise', 'La Lise'), ('Petit-Goâve', 'Petit-Goâve'), ('Saint-Louis', 'Saint-Louis')]
NAV, ALB = uri(A + 'navire_gravure.png'), uri(A + 'alambic_gravure.png')
CSS20 = (f".t20{{font-family:{DISP};font-size:32px;fill:#F6EFDC}}.lv{{font-family:{BODY};font-weight:700;font-size:24px;fill:{INK}}}"
         f".fd{{font-family:{SER};font-style:italic;font-size:22px;fill:{MUTED}}}.lb{{font-family:{SER};font-style:italic;font-size:24px;fill:{MUTED}}}"
         f".rl{{font-family:{BODY};font-weight:500;font-size:25px;fill:{INK}}}.nm{{font-family:{DISP};fill:{INK}}}")
def frame20(title, color):
    W, H = 600, 320
    c = lambda x, y, r: f"<g transform='translate({x} {y}) rotate({r})'><path d='M0 0 L22 0 M0 0 L0 22' stroke='{EDGE}' stroke-width='2'/><circle cx='6' cy='6' r='2.5' fill='{EDGE}'/></g>"
    return (f"<rect x='4' y='4' width='{W-8}' height='{H-8}' rx='20' fill='{PAPER}' stroke='{EDGE}' stroke-width='5'/>"
            f"<rect x='13' y='13' width='{W-26}' height='{H-26}' rx='13' fill='none' stroke='{INK}' stroke-width='.8' opacity='.45'/>"
            + c(19, 19, 0) + c(W - 19, 19, 90) + c(W - 19, H - 19, 180) + c(19, H - 19, 270)
            + f"<path d='M44 26 L{W-44} 26 L{W-30} 50 L{W-44} 74 L44 74 L30 50 Z' fill='{color}'/>"
            f"<path d='M46 30 L{W-46} 30 L{W-35} 50 L{W-46} 70 L46 70 L35 50 Z' fill='none' stroke='#E7C27A' stroke-width='.8' opacity='.7'/>"
            f"<text x='{W/2}' y='61' text-anchor='middle' class='t20'>{E(title)}</text>")
def parts(n, x0, step, cy=166):     # mêmes centres qu'avant en x ; ronds remontés de 10 pour loger les textes agrandis
    s = ''
    for k in range(n):
        cx = x0 + k * step
        s += (f"<circle cx='{cx}' cy='{cy+2}' r='27' fill='#000' opacity='.10'/><circle cx='{cx}' cy='{cy}' r='27' fill='#FFFDF6' stroke='{INK}' stroke-width='1.6'/>"
              f"<circle cx='{cx}' cy='{cy}' r='22' fill='none' stroke='{EDGE}' stroke-width='1.2' stroke-dasharray='3 3'/><text x='{cx}' y='{cy+53}' text-anchor='middle' class='lv'>1 ₶</text>")
    return s
BOTTLE = (f"<g transform='translate(540 268) scale(.95)'><path d='M5 0 h8 v7 q7 4 7 12 v20 q0 4 -4 4 h-14 q-4 0 -4 -4 v-20 q0 -8 7 -12 z' fill='{COPPER}' stroke='{INK}' stroke-width='1.3'/>"
          f"<rect x='3' y='18' width='12' height='9' rx='1.5' fill='{PAPER}'/></g>")
for i, nm in enumerate(SHIPS):
    tx, ty, tw, th = 26, 92, 176, 150
    svg(f'carte_navire53_{i+1}', 600, 320, 2, frame20(nm, BROWN)
        + f"<rect x='{tx}' y='{ty}' width='{tw}' height='{th}' rx='12' fill='#EFE6CF' stroke='{EDGE}' stroke-width='2'/>"
        f"<rect x='{tx+6}' y='{ty+6}' width='{tw-12}' height='{th-12}' rx='8' fill='none' stroke='{INK}' stroke-width='1' stroke-dasharray='4 4' opacity='.45'/>"
        f"<image href='{NAV}' x='{tx+20}' y='{ty+10}' width='{tw-40}' height='{th-20}' opacity='.18'/>"
        f"<text x='{tx+tw/2}' y='{ty+th+27}' text-anchor='middle' class='lb'>Navire</text>"
        + parts(5, 262, 67) + "<text x='262' y='126' text-anchor='middle' class='fd'>fondateur</text>"
        + f"<line x1='232' y1='246' x2='566' y2='246' stroke='{EDGE}' stroke-width='1'/>"
        "<text x='399' y='284' text-anchor='middle' class='rl'>Armé à 5 parts.</text>", CSS20)
for i, (nm, sh) in enumerate(DISTILLERIES):
    cx, cy = 114, 166
    svg(f'carte_distillerie53_{i+1}', 600, 320, 2, frame20(nm, COPPER)
        + f"<circle cx='{cx}' cy='{cy}' r='64' fill='#EFE6CF' stroke='{EDGE}' stroke-width='2'/>"
        f"<circle cx='{cx}' cy='{cy}' r='57' fill='none' stroke='{INK}' stroke-width='1' stroke-dasharray='4 4' opacity='.45'/>"
        f"<image href='{ALB}' x='{cx-50}' y='{cy-50}' width='100' height='100' opacity='.9'/>"
        f"<text x='{cx}' y='{cy+95}' text-anchor='middle' class='lb'>Distillerie</text>"
        + parts(4, 280, 80)
        + f"<line x1='232' y1='246' x2='566' y2='246' stroke='{EDGE}' stroke-width='1'/>"
        "<text x='399' y='272' text-anchor='middle' class='rl' style='font-size:22px'>Construite à 4 parts.</text>"
        "<text x='399' y='297' text-anchor='middle' class='rl' style='font-size:22px'>Produit 4 eaux-de-vie.</text>", CSS20)
    fs = 24 if len(sh) > 11 else 28
    svg(f'pion_distillerie53_{i+1}', 220, 300, 2,
        f"<defs><clipPath id='ca'><circle cx='110' cy='122' r='88'/></clipPath></defs><circle cx='110' cy='122' r='104' fill='{PAPER}' stroke='{COPPER}' stroke-width='7'/>"
        f"<image href='{ALB}' x='14' y='26' width='192' height='192' clip-path='url(#ca)'/><circle cx='110' cy='122' r='88' fill='none' stroke='{INK}' stroke-width='1.5'/>"
        f"<rect x='8' y='246' width='204' height='46' rx='10' fill='{PAPER}' stroke='{INK}' stroke-width='2.5'/>"
        f"<text x='110' y='{269+fs*0.33:.0f}' text-anchor='middle' class='nm' style='font-size:{fs}px'>{E(sh)}</text>", CSS20)

# ---------------------------------------------------------------- 14. Tuile Scorbut : pagaie (icône des places de voyageur) barrée
def tx(x, y, s, size, fill=INK, fam=SER): return f"<text x='{x}' y='{y}' font-family=\"{fam}\" font-size='{size}' text-anchor='middle' fill='{fill}'>{E(s)}</text>"
PAG = (f"<g transform='translate(41 44) rotate(-18) scale(.36)' fill='{INK}'><rect x='-2.5' y='-56' width='5' height='74' rx='2'/>"
       "<path d='M0 12 C-14 20 -14 50 0 58 C14 50 14 20 0 12 Z'/><rect x='-8' y='-59' width='16' height='7' rx='3'/></g>")
svg('hid53_scorbut', 96, 96, 400 / 96, "<rect x='1.5' y='1.5' width='93' height='93' rx='14' fill='#F6EFDC' stroke='#3A2618' stroke-width='3'/>"
    + tx(48, 19, 'Scorbut', 13, '#8E2F25', DISP) + PAG + "<path d='M58 33L72 47M72 33L58 47' stroke='#8E2F25' stroke-width='2.4' stroke-linecap='round'/>"
    + tx(48, 76, '−1 voyageur,', 11, INK, BODY) + tx(48, 89, 'sinon −1 stock', 11, INK, BODY))

# ---------------------------------------------------------------- 15. Congé Lacs d'en haut : tortue centrée, « ou Témiscamingue » dessous
def conge_haut():
    src = open(R + 'src/conges_v52.py').read(); ns = {'__name__': 'v53', '__file__': R + 'src/conges_v52.py'}
    exec(src[:src.index("if __name__ == '__main__':")], ns)
    corps = (f"<div style='display:flex;flex-direction:column;align-items:center;gap:0'><img src='file://{ns['IMG']}{ns['REG']['haut'][2]}' style='width:84px;height:84px'>"
             f"<span style='font:italic 31px/1.1 Fell;color:{INK}'>ou Témiscamingue</span></div>")
    t = ns['tuile'](ns['REG']['haut'][1], ns['REG']['haut'][0], corps, [], ns['P'](3))
    PAGES.append(('cg53_haut', 400, 400, ns['html_de'](t)))

# ---------------------------------------------------------------- 8. Jetons voyageurs : IM Fell (titre) + Alegreya Sans (chiffre, effet), prix inclus
def voyageurs():
    src = open(R + 'src/voyageurs_voy2.py').read(); ns = {'__name__': 'v53'}; sys_argv = sys.argv; sys.argv = ['x', '/tmp']
    exec(src[:src.index("if __name__ == '__main__':")], ns); sys.argv = sys_argv
    B = '#4E8C99'
    RAPIDE = ("<svg width='120' height='120' viewBox='0 0 120 120'><circle cx='60' cy='60' r='54' fill='none' stroke='#2A2418' stroke-width='5'/>"
              f"<line x1='86' y1='38' x2='42' y2='38' stroke='{B}' stroke-width='8'/><path d='M46 24 L26 38 L46 52 Z' fill='{B}'/>"
              + ''.join(f"<polyline points='{x},{y+8} {x+7},{y} {x+14},{y+8}' fill='none' stroke='{B}' stroke-width='5' stroke-linejoin='round' stroke-linecap='round'/>"
                        for y, xs in ((66, (29, 46, 63, 80)), (80, (37, 54, 71))) for x in xs) + "</svg>")
    # icône de l'artisan : reprise de l'image v51 (pas de source vectorielle) ; fond ramené au blanc puis fusion « multiply »
    ic = Image.open(V + 'voy2_artisan.png').convert('RGB').crop((40, 112, 256, 262)); fond = ic.getpixel((2, 2))
    ic = Image.merge('RGB', [ch.point(lambda v, f=f: min(255, round(v * 255 / f))) for ch, f in zip(ic.split(), fond)])
    b = io.BytesIO(); ic.save(b, 'PNG')
    ART = f"<img src='data:image/png;base64,{base64.b64encode(b.getvalue()).decode()}' style='width:216px;height:150px;mix-blend-mode:multiply'>"
    css = (".t{position:absolute;left:0;top:0;width:300px;height:432px;border-radius:30px}"
           f".h{{position:absolute;top:16px;width:300px;text-align:center;font:400 44px {DISP};color:#F2EAD3;letter-spacing:.5px}}"
           ".p{position:absolute;left:10px;top:80px;width:276px;height:338px;border-radius:14px;border:2px solid rgba(42,36,24,.4);"
           "background:radial-gradient(ellipse 70% 60% at 45% 30%,#F9F2DF,#F0E5CB)}"
           ".i{position:absolute;left:0;top:30px;width:276px;height:170px;display:flex;align-items:center;justify-content:center}"
           f".n{{position:absolute;top:186px;width:276px;text-align:center;font:700 60px/1.1 {BODY}}}"
           f".e{{position:absolute;top:254px;width:276px;text-align:center;font:700 33px/1.08 {BODY};color:#2A2418}}"
           ".pu{position:absolute;left:10px;top:80px;width:276px;height:338px;border-radius:14px;border:2px solid rgba(242,234,211,.45)}"
           f".u{{position:absolute;top:146px;width:276px;text-align:center;font:400 36px {DISP};letter-spacing:3px;color:#F2EAD3}}"
           ".b{position:absolute;left:14px;top:16px;width:64px;height:64px;border-radius:50%;background:#F2EAD3;border:4px solid #B8923A;"
           "box-shadow:inset 0 0 0 3px #F2EAD3,inset 0 0 0 4.5px #D8CBA6;display:flex;align-items:center;justify-content:center;"
           f"font:700 27px {BODY};color:#2A2418}}")
    J = (('guide', 'Guide', '#2F5E4A', ns['GUIDE_ICON'], '+1', "<span style='font-size:29px'>au raccourci<br>et aux traversées</span>", 1),
         ('milicien', 'Milicien', '#44464C', ns['FUSIL'], '×2', 'au combat', 1),
         ('interprete', 'Interprète', '#8A5A14', ns['WAMPUM'], '+1', 'dé au troc', 2),
         ('pilote', 'Pilote', '#2F5A7A', RAPIDE, "<span style='font-size:46px'>Sans jet</span>", 'aux rapides', 2),
         ('artisan', 'Artisan', '#7A3823', ART, '1', 'réparation', 1))
    for k, titre, c, ic, n, e, prix in J:
        page(f'voy53_{k}', 300, 432, f"<div class=t style='background:{c}'><div class=h>{titre}</div><div class=p><div class=i>{ic}</div>"
             f"<div class=b>{prix}&nbsp;₶</div><div class=n style='color:{c}'>{n}</div><div class=e>{e}</div></div></div>", css)
        page(f'voy53_{k}_used', 300, 432, f"<div class=t style='background:{c}'><div class=h>{titre}</div><div class=pu><div class=u>Utilisé</div></div></div>", css)

if __name__ == '__main__':
    coins_transparents(); conge_haut(); voyageurs()
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME); pg = b.new_page()
        for nom, w, h, doc in PAGES:
            w, h = round(w), round(h); pg.set_viewport_size({'width': w, 'height': h})
            f = f'/tmp/{nom}.html'; open(f, 'w').write(doc); pg.goto('file://' + f); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(150)
            pg.screenshot(path=OUT + nom + '.png', omit_background=True, clip={'x': 0, 'y': 0, 'width': w, 'height': h})
        b.close()
    print(len(PAGES) + 13, 'images dans', OUT)
