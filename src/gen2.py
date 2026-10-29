# Composants du module TTS, dans le style du plateau (parchemin, encre, couleurs sobres).
import json, os, html, math
D = json.load(open('data.json'))
OUT = 'html'; os.makedirs(OUT, exist_ok=True)
F = os.path.abspath('node_modules/@fontsource')
INK = '#2A2418'; MUTED = '#6B5F45'; EDGE = '#B7A675'; PCARD = '#F2EAD3'; PAPER = '#F6EFDC'; LAND = '#D6C89C'; FRAME = '#22332F'; WATER = '#9DBDC2'
PELT = '#8A5A2B'; PELT_D = '#5C3A1A'; GOLD = '#C9952B'
KCOL = {'Associé': '#8A5A14', 'Recrue': '#6B4A2A', 'Contrat': '#3E5A7A', 'Alliance': '#2F5E4A', 'Charge': '#7A2E3A', 'Matériel de départ': '#4E5B3A',
        'Fin de mois': '#3F6D78', 'Demande de Paris': '#5A4A7A', 'Grand événement': '#8E2F25'}
DISP = "'IM Fell English SC',serif"; SER = "'IM Fell English',serif"; BODY = "'Alegreya Sans',sans-serif"
E = html.escape
MANIFEST = []
FONTS = f"""@font-face{{font-family:'IM Fell English SC';src:url(file://{F}/im-fell-english-sc/files/im-fell-english-sc-latin-400-normal.woff2)}}
@font-face{{font-family:'IM Fell English';src:url(file://{F}/im-fell-english/files/im-fell-english-latin-400-normal.woff2)}}
@font-face{{font-family:'IM Fell English';font-style:italic;src:url(file://{F}/im-fell-english/files/im-fell-english-latin-400-italic.woff2)}}
@font-face{{font-family:'Alegreya Sans';font-weight:400;src:url(file://{F}/alegreya-sans/files/alegreya-sans-latin-400-normal.woff2)}}
@font-face{{font-family:'Alegreya Sans';font-weight:500;src:url(file://{F}/alegreya-sans/files/alegreya-sans-latin-500-normal.woff2)}}
@font-face{{font-family:'Alegreya Sans';font-weight:700;src:url(file://{F}/alegreya-sans/files/alegreya-sans-latin-700-normal.woff2)}}"""
BASE = FONTS + f"*{{box-sizing:border-box;margin:0;padding:0}}html,body{{background:transparent;color:{INK};font-family:{BODY}}}"

def page(name, w, h, body, css='', bg='transparent'):
    open(f'{OUT}/{name}.html', 'w').write(f"<!doctype html><html><head><meta charset='utf-8'><style>{BASE}body{{width:{w}px;height:{h}px;overflow:hidden;background:{bg}}}{css}</style></head><body>{body}</body></html>")
    MANIFEST.append((name, w, h))

def T(x, y, s, size=28, anchor='start', fam=BODY, weight=400, fill=INK, italic=False):
    return f"<text x='{x}' y='{y}' font-family=\"{fam}\" font-size='{size}' font-weight='{weight}' text-anchor='{anchor}' fill='{fill}' {'font-style=\"italic\"' if italic else ''}>{E(s)}</text>"

def svg(name, w, h, inner, bg='transparent'):
    page(name, w, h, f"<svg width='{w}' height='{h}' xmlns='http://www.w3.org/2000/svg'>{inner}</svg>", bg=bg)

HATCH = f"<defs><pattern id='h' width='14' height='14' patternUnits='userSpaceOnUse' patternTransform='rotate(45)'><rect width='14' height='14' fill='#EFE7D2'/><line x1='0' y1='0' x2='0' y2='14' stroke='{INK}' stroke-width='2.4' opacity='.25'/></pattern></defs>"

def zone(x, y, w, h, title, sub='', fill=PCARD, dash=True):
    return (f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='14' fill='{fill}' stroke='{EDGE}' stroke-width='3' {'stroke-dasharray=\"14 9\"' if dash else ''}/>"
            + T(x + 22, y + 46, title, 34, fam=DISP) + (T(x + 22, y + 80, sub, 22, fill=MUTED) if sub else ''))

# ------------------------------------------------------------ Réserve générale (même style que le plateau)
def reserve():
    W, H = 3600, 2000; g = [HATCH]
    g.append(f"<rect x='0' y='0' width='{W}' height='{H}' rx='40' fill='{FRAME}'/><rect x='30' y='30' width='{W-60}' height='{H-60}' rx='26' fill='#E6DAB6'/>")
    g.append(T(80, 110, "Québec · réserve générale", 52, fam=DISP))
    g.append(T(80, 200, "Rivière de recrutement", 38, fam=DISP)); g.append(T(80, 236, "Recruter : payez le prix de la case · fin de mois : la carte de droite part à la défausse, les autres glissent, une nouvelle entre à 3 livres", 22, fill=MUTED))
    labs = [("pioche", None), ("3", 3), ("2", 2), ("1", 1), ("1", 1), ("défausse", None)]
    for k, (lab, p) in enumerate(labs):
        x = 80 + k * 300
        g.append(f"<rect x='{x}' y='260' width='270' height='380' rx='16' fill='{PAPER if p else PCARD}' stroke='{EDGE}' stroke-width='3' {'' if p else 'stroke-dasharray=\"14 9\"'}/>")
        if p: g.append(f"<circle cx='{x+135}' cy='680' r='30' fill='{GOLD}'/>" + T(x + 135, 691, str(p), 32, 'middle', weight=700, fill='#fff') + T(x + 135, 735, 'livre' + ('s' if p > 1 else ''), 22, 'middle', fill=MUTED))
        else: g.append(T(x + 135, 690, lab, 26, 'middle', fill=MUTED))
    g.append(zone(1950, 160, 1570, 600, "Sacs", "piochez sans regarder · remettez les jetons dans leur sac"))
    for k, lab in enumerate(["congés", "Grands Lacs", "lac Supérieur", "jetons cachés", "peaux à l’unité"]):
        x = 1985 + k * 305
        g.append(f"<rect x='{x}' y='290' width='280' height='400' rx='18' fill='{PAPER}' stroke='{EDGE}' stroke-width='3' stroke-dasharray='12 8'/>" + T(x + 140, 730, lab, 24, 'middle', fill=MUTED))
    g.append(zone(80, 800, 1840, 640, "Chantier de La Rochelle", "cartes de navire · 5 parts de 1 livre · un disque de couleur par part · le plus de parts : armateur principal"))
    for k in range(6):
        x = 120 + (k % 3) * 600; y = 920 + (k // 3) * 250
        g.append(f"<rect x='{x}' y='{y}' width='560' height='230' rx='14' fill='{PAPER}' stroke='{EDGE}' stroke-width='2.5' stroke-dasharray='12 8'/>")
    g.append(zone(1950, 800, 1570, 640, "Comptoir de Québec · stock", "gris · mis en vente sur la piste des prix au milieu des prix des joueurs", fill='#E9E4D6'))
    for k, lab in enumerate(["marchandises", "eau-de-vie"]):
        x = 1990 + k * 760
        g.append(f"<rect x='{x}' y='920' width='730' height='480' rx='14' fill='{PAPER}' stroke='{EDGE}' stroke-width='2.5' stroke-dasharray='12 8'/>" + T(x + 20, 960, lab, 26, fill=MUTED))
    g.append(zone(80, 1480, 1840, 460, "Paquets", ""))
    for k, lab in enumerate(["associés", "matériel", "fin de mois", "défausse", "demande de Paris", "grand événement"]):
        x = 110 + k * 300
        g.append(f"<rect x='{x}' y='1560' width='270' height='340' rx='16' fill='{PCARD}' stroke='{EDGE}' stroke-width='3' stroke-dasharray='14 9'/>" + T(x + 135, 1740, lab, 24, 'middle', fill=MUTED))
    g.append(zone(1950, 1480, 1570, 460, "Voyageurs et dés", "représentant 2 livres · guide, milicien, interprète 1 livre"))
    for k, lab in enumerate(["représentant", "guide", "milicien", "interprète", "dés · 1er"]):
        x = 1985 + k * 305
        g.append(f"<rect x='{x}' y='1600' width='280' height='300' rx='16' fill='{PAPER}' stroke='{EDGE}' stroke-width='2.5' stroke-dasharray='12 8'/>" + T(x + 140, 1880, lab, 24, 'middle', fill=MUTED))
    svg('reserve', W, H, ''.join(g))

# ------------------------------------------------------------ Cartes
CW, CH = 500, 700
CARD_CSS = f""".grid{{display:grid;grid-template-columns:repeat(var(--n),{CW}px);grid-auto-rows:{CH}px}}
.c{{width:{CW}px;height:{CH}px;padding:14px}}
.in{{height:100%;border-radius:26px;background:{PAPER};border:3px solid {EDGE};overflow:hidden;display:flex;flex-direction:column;position:relative}}
.band{{background:var(--k);color:#F6EFDC;font-size:22px;letter-spacing:.14em;text-transform:uppercase;font-weight:700;padding:16px 26px 14px;display:flex;justify-content:space-between}}
.t{{font-family:{DISP};font-size:44px;line-height:1.05;padding:24px 26px 6px;color:{INK}}}
.rule{{height:3px;margin:8px 26px 4px;background:linear-gradient(90deg,var(--k),transparent)}}
.fx{{font-size:30px;line-height:1.32;padding:12px 26px;color:{INK}}}
.nt{{margin-top:auto;font-family:{SER};font-style:italic;font-size:24px;line-height:1.3;color:{MUTED};padding:16px 26px 22px;border-top:2px solid #E3D7B5}}
.back .in{{background:var(--k);align-items:center;justify-content:center;text-align:center;color:#F6EFDC;border-color:var(--k)}}
.back .frame{{position:absolute;inset:18px;border:2px solid rgba(246,239,220,.55);border-radius:18px}}
.back .bt{{font-family:{DISP};font-size:56px;line-height:1.05;padding:0 40px}} .back .bs{{font-size:22px;letter-spacing:.14em;text-transform:uppercase;margin-top:18px;opacity:.85}}
.back .game{{position:absolute;bottom:46px;font-family:{SER};font-style:italic;font-size:24px;opacity:.85;width:100%;text-align:center}}"""

def card_html(kind, title, fx, note='', star=0):
    k = KCOL.get(kind, INK)
    return (f"<div class='c' style='--k:{k}'><div class='in'><div class='band'><span>{E(kind)}</span><span>{'★' * star}</span></div>"
            f"<div class='t'>{E(title)}</div><div class='rule'></div><div class='fx'>{E(fx)}</div>{f'<div class=nt>{E(note)}</div>' if note else ''}</div></div>")

def sheet(name, kind, cards, back_title, back_sub, css=None):
    n = len(cards); cols = min(10, n); rows = math.ceil(n / cols)
    page(name, cols * CW, rows * CH, f"<div class='grid' style='--n:{cols}'>{''.join(cards)}</div>", (css or CARD_CSS))
    k = KCOL.get(kind, INK)
    page(name + '_back', CW, CH, f"<div class='c back' style='--k:{k}'><div class='in'><div class='frame'></div><div class='bt'>{E(back_title)}</div><div class='bs'>{E(back_sub)}</div><div class='game'>Castor et eau-de-vie</div></div></div>", CARD_CSS)
    return {'cols': cols, 'rows': rows, 'n': n}

DECKS = {}
def decks():
    pers = [c for c in D['CARDS'] if c['kind'] == 'personnage']
    for c in pers:
        if c['id'] == 'mercier': c['effect'] = "Le comptoir vous vend les marchandises 1 livre moins cher, jamais sous 2 livres."
    DECKS['pers'] = sheet('deck_pers', 'Associé', [card_html('Associé', c['title'], c['effect'], c.get('note', '')) for c in pers], 'Associés', 'piochez 3 · gardez-en 1'); DECKS['pers']['names'] = [c['title'] for c in pers]
    rk = {'recrue': 'Recrue', 'contrat': 'Contrat', 'nation': 'Alliance', 'charge': 'Charge'}
    rc = D['RCARDS']
    for c in rc:
        if c['id'] == 'c_ferme': c['effect'] = "Vendez à Québec jusqu’à 3 de vos peaux au prix de Paris moins 1, sans navire."
    DECKS['riv'] = sheet('deck_riv', 'Recrue', [card_html(rk[c['kind']], c['title'], c['effect'], c.get('note', ''), c.get('star', 0)) for c in rc], 'Rivière', 'recrutement'); DECKS['riv']['names'] = [c['title'] for c in rc]
    for kd, plur in (('recrue', 'Recrues'), ('contrat', 'Contrats'), ('nation', 'Alliances'), ('charge', 'Charges')):
        cs = [c for c in rc if c['kind'] == kd]
        DECKS['riv_' + kd] = sheet('deck_riv_' + kd, rk[kd], [card_html(rk[kd], c['title'], c['effect'], c.get('note', ''), c.get('star', 0)) for c in cs], plur, 'rivière de recrutement'); DECKS['riv_' + kd]['names'] = [c['title'] for c in cs]
    mats = [("Navire", "Une carte de navire du chantier, entièrement payée, et 2 de crédit envers la compagnie."), ("Parts de navire", "2 parts payées sur une carte de navire au chantier, et 3 livres."),
            ("Bourse", "4 livres."), ("Ballots de marchandises", "4 marchandises."), ("Eau-de-vie", "2 bouteilles et 1 livre."), ("Assortiment", "2 marchandises et 1 bouteille."),
            ("Petit canot", "1 petit canot et 2 livres."), ("Grand canot", "1 grand canot et 1 livre."), ("Distillerie", "1 distillerie et 1 livre.")]
    DECKS['mat'] = sheet('deck_mat', 'Matériel de départ', [card_html('Matériel de départ', t, fx) for t, fx in mats], 'Matériel', 'distribué en entier · 3 par marchand', css=CARD_CSS.replace('.t{font-family:', '.t{font-size:60px!important;font-family:').replace('.fx{font-size:30px', '.fx{font-size:44px')); DECKS['mat']['names'] = [t for t, _ in mats]
    ev = [(e['title'], e['text']) for e in D['MONTH_EVENTS'] for _ in range(e['w'])]
    DECKS['ev'] = sheet('deck_ev', 'Fin de mois', [card_html('Fin de mois', t, x) for t, x in ev], 'Fin de mois', 'événement'); DECKS['ev']['names'] = [t for t, _ in ev]
    dm = [(d['title'], f"{d['text']} Prix de Paris {'+' if d['d']>0 else ''}{d['d']}.") for d in D['DEMANDE']]
    DECKS['dem'] = sheet('deck_dem', 'Demande de Paris', [card_html('Demande de Paris', t, x) for t, x in dm], 'Demande de Paris', 'tirée en hiver'); DECKS['dem']['names'] = [t for t, _ in dm]
    gr = [(g['name'], g['text']) for g in D['GRAND']]
    DECKS['grand'] = sheet('deck_grand', 'Grand événement', [card_html('Grand événement', t, x) for t, x in gr], 'Grand événement', 'ravages à 4'); DECKS['grand']['names'] = [t for t, _ in gr]

# ------------------------------------------------------------ Tuiles et jetons
def pelt(cx, cy, s, gras=False):
    # peau tendue sur cerceau : ovale à quatre lobes
    c = PELT_D if gras else PELT; st = '#3A2410'
    return (f"<g transform='translate({cx} {cy}) scale({s})'>"
            f"<ellipse cx='0' cy='0' rx='34' ry='44' fill='{c}' stroke='{st}' stroke-width='4'/>"
            f"<ellipse cx='0' cy='0' rx='22' ry='30' fill='none' stroke='#F2E2C4' stroke-width='2.5' opacity='.55'/>"
            + "".join(f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{st}' stroke-width='3'/>" for x1, y1, x2, y2 in [(0, -44, 0, -54), (0, 44, 0, 54), (-34, 0, -44, 0), (34, 0, 44, 0)])
            + "</g>")

def tile_frame(S, fill, stroke=EDGE):
    return f"<rect x='8' y='8' width='{S-16}' height='{S-16}' rx='46' fill='{fill}' stroke='{stroke}' stroke-width='8'/>"

def pelts_row(n, cy, gras, S=400):
    sc = 1.25 if n == 1 else (1.05 if n == 2 else 0.9); gap = 118 if n == 3 else 140
    x0 = S / 2 - (n - 1) * gap / 2
    return ''.join(pelt(x0 + i * gap, cy, sc, gras) for i in range(n))

def tiles():
    S = 400
    for n in (1, 2, 3):
        for sup in (False, True):
            tag = 'S' if sup else 'G'; corner = T(S - 44, 66, 'Sup.', 28, 'end', weight=700, fill=MUTED) if sup else ''
            svg(f'tile_{tag}{n}_sec', S, S, tile_frame(S, PAPER) + T(S / 2, 92, 'castor sec', 32, 'middle', fam=SER, italic=True, fill=MUTED) + pelts_row(n, 205, False) + T(S / 2, 348, str(n), 62, 'middle', weight=700) + corner)
            svg(f'tile_{tag}{n}_gras', S, S, tile_frame(S, '#E8D5A8', GOLD) + T(S / 2, 92, 'castor gras', 32, 'middle', fam=SER, italic=True, fill=PELT_D) + pelts_row(n, 205, True) + T(S / 2, 350, f"★ {n}", 62, 'middle', weight=700, fill=PELT_D) + corner)
    svg('hid_back', S, S, tile_frame(S, '#C9BB91') + T(S / 2, 250, '?', 190, 'middle', fam=DISP, fill=INK) + T(S / 2, 340, 'village', 30, 'middle', fam=SER, italic=True, fill=INK))
    for n in (1, 2, 3):
        svg(f'hid_fur{n}', S, S, tile_frame(S, PAPER) + T(S / 2, 92, 'traite au village', 30, 'middle', fam=SER, italic=True, fill=MUTED) + pelts_row(n, 205, False) + T(S / 2, 348, str(n), 62, 'middle', weight=700))
    traps = {'mission': ("Missionnaire", "Avec de l’eau-de-vie à bord : +1 soupçon. Charge perdue."),
             'present': ("Présent", "Une peau sèche, et votre charge vous est rendue."),
             'fievre': ("Fièvre", "Un voyageur reste au village ; sans voyageur, une charge est perdue."),
             'gatees': ("Peaux gâtées", "Invendables : la charge est perdue.")}
    for k, (t, txt) in traps.items():
        words = txt.split(' '); lines = []; cur = ''
        for w in words:
            if len(cur) + len(w) > 20: lines.append(cur); cur = w
            else: cur = (cur + ' ' + w).strip()
        lines.append(cur)
        svg(f'hid_{k}', S, S, tile_frame(S, '#EADFC2', '#8E2F25') + T(S / 2, 112, t, 50, 'middle', fam=DISP, fill='#8E2F25') + ''.join(T(S / 2, 190 + i * 42, l, 30, 'middle') for i, l in enumerate(lines)))
    # Congés : marchandises offertes dans le crédit, et coût en crédit
    seal = f"<circle cx='{S/2}' cy='70' r='30' fill='#8E2F25'/><circle cx='{S/2}' cy='70' r='20' fill='none' stroke='#F2D9B0' stroke-width='3'/>"
    for n, c in ((4, 3), (3, 2), (2, 1)):
        svg(f'conge_m{n}', S, S, tile_frame(S, PAPER) + seal + T(S / 2, 150, 'Congé', 50, 'middle', fam=DISP) + T(S / 2, 250, f'{n} marchandises', 40, 'middle', weight=700) + T(S / 2, 330, f'coût : {c} crédit', 32, 'middle', fill='#A3352A', weight=700) + T(S / 2, 378, 'plus pauvre : −1', 24, 'middle', fill=MUTED))
    svg('conge_back', S, S, tile_frame(S, '#8E2F25', '#5E1F18') + T(S / 2, 215, 'Congé', 66, 'middle', fam=DISP, fill='#F6EFDC') + T(S / 2, 268, "de l’intendant", 30, 'middle', fam=SER, italic=True, fill='#F6EFDC'))
    # Voyageurs
    VOY = {'guide': ('Guide', '#2F5E4A'), 'mil': ('Milicien', '#3E5A7A'), 'int': ('Interprète', '#8A5A14')}
    for k, (lab, c) in VOY.items():
        svg(f'voy_{k}', 240, 240, f"<circle cx='120' cy='120' r='112' fill='{c}' stroke='#F6EFDC' stroke-width='8'/><circle cx='120' cy='88' r='30' fill='#F6EFDC'/><path d='M62 176 Q120 112 178 176 Z' fill='#F6EFDC'/>" + T(120, 214, lab, 24 if len(lab) < 10 else 20, 'middle', weight=700, fill='#F6EFDC'))
    # Caisse (marchandise) et bouteille (eau-de-vie)
    svg('tok_caisse', 200, 200, f"<rect x='18' y='26' width='164' height='148' rx='10' fill='#C79A5B' stroke='#5C3A1A' stroke-width='8'/><line x1='18' y1='76' x2='182' y2='76' stroke='#5C3A1A' stroke-width='6'/><line x1='18' y1='126' x2='182' y2='126' stroke='#5C3A1A' stroke-width='6'/><line x1='30' y1='34' x2='170' y2='166' stroke='#5C3A1A' stroke-width='6'/>")
    svg('tok_bouteille', 200, 200, f"<path d='M84 14 L116 14 L116 56 Q150 74 150 112 L150 176 Q150 188 138 188 L62 188 Q50 188 50 176 L50 112 Q50 74 84 56 Z' fill='#5E8C5A' stroke='#20331E' stroke-width='8'/><rect x='80' y='8' width='40' height='22' rx='4' fill='#8A5A2B' stroke='#20331E' stroke-width='5'/><rect x='62' y='112' width='76' height='46' rx='6' fill='#F2E8C8' stroke='#20331E' stroke-width='4'/>")
    svg('tok_caisse_w', 200, 200, "<rect x='18' y='26' width='164' height='148' rx='10' fill='#F4F4F4' stroke='#3A3A3A' stroke-width='8'/><line x1='18' y1='76' x2='182' y2='76' stroke='#3A3A3A' stroke-width='6'/><line x1='18' y1='126' x2='182' y2='126' stroke='#3A3A3A' stroke-width='6'/><line x1='30' y1='34' x2='170' y2='166' stroke='#3A3A3A' stroke-width='6'/>")
    svg('tok_bouteille_w', 200, 200, "<path d='M84 14 L116 14 L116 56 Q150 74 150 112 L150 176 Q150 188 138 188 L62 188 Q50 188 50 176 L50 112 Q50 74 84 56 Z' fill='#F4F4F4' stroke='#3A3A3A' stroke-width='8'/><rect x='80' y='8' width='40' height='22' rx='4' fill='#BBBBBB' stroke='#3A3A3A' stroke-width='5'/><rect x='62' y='112' width='76' height='46' rx='6' fill='#FFFFFF' stroke='#3A3A3A' stroke-width='4'/>")
    # Peau à l'unité, recto sec / verso gras
    svg('tok_peau_sec', 200, 200, f"<circle cx='100' cy='100' r='94' fill='{PAPER}' stroke='{EDGE}' stroke-width='7'/>" + pelt(100, 96, 1.25))
    svg('tok_peau_gras', 200, 200, f"<circle cx='100' cy='100' r='94' fill='#E8D5A8' stroke='{GOLD}' stroke-width='7'/>" + pelt(100, 92, 1.15, True) + T(100, 182, '★', 34, 'middle', fill=PELT_D))
    # Canots (teintés par couleur de joueur dans TTS) : coque claire, cases
    for name, cells in (('grand', 5), ('petit', 3), ('coureur', 2)):
        cw = 120; w = cells * cw + 120; h = 210
        hull = f"<path d='M14 34 L{w-14} 34 L{w-62} {h-14} L62 {h-14} Z' fill='#F4F4F4' stroke='#3A3A3A' stroke-width='8' stroke-linejoin='round'/>"
        cs = ''.join(f"<rect x='{60+i*cw}' y='52' width='{cw-14}' height='{cw-14}' rx='12' fill='#FFFFFF' stroke='#8A8A8A' stroke-width='4'/>" for i in range(cells))
        svg(f'canot_{name}', w, h, hull + cs)
    ship = lambda fill, lab: (f"<path d='M14 130 L286 130 L244 200 L56 200 Z' fill='{fill}' stroke='#3A3A3A' stroke-width='8' stroke-linejoin='round'/><line x1='150' y1='14' x2='150' y2='130' stroke='#3A3A3A' stroke-width='8'/>"
                              f"<path d='M160 22 L254 100 L160 112 Z' fill='#FFFFFF' stroke='#3A3A3A' stroke-width='6'/>" + (T(150, 184, lab, 30, 'middle', weight=700, fill='#fff') if lab else ''))
    svg('navire', 300, 214, ship('#F4F4F4', ''))
    svg('navire_roi', 300, 214, ship('#9A8F78', 'ROI'))
    svg('navire_marchand', 300, 214, ship('#9A8F78', 'MARCHAND'))
    svg('alambic', 220, 240, "<ellipse cx='104' cy='160' rx='82' ry='68' fill='#F4F4F4' stroke='#3A3A3A' stroke-width='8'/><path d='M104 92 L104 36 L190 36 L190 132' fill='none' stroke='#3A3A3A' stroke-width='9' stroke-linecap='round'/><rect x='170' y='130' width='40' height='50' rx='6' fill='#F4F4F4' stroke='#3A3A3A' stroke-width='6'/>")
    svg('tok_disc', 200, 200, "<circle cx='100' cy='100' r='92' fill='#F4F4F4' stroke='#3A3A3A' stroke-width='8'/>")
    svg('tok_marker', 200, 200, "<rect x='10' y='10' width='180' height='180' rx='40' fill='#F4F4F4' stroke='#3A3A3A' stroke-width='8'/>")
    svg('tok_noir', 200, 200, f"<circle cx='100' cy='100' r='92' fill='{INK}' stroke='#000' stroke-width='6'/><circle cx='100' cy='100' r='56' fill='none' stroke='{EDGE}' stroke-width='5'/>")
    svg('tok_pas', 260, 170, f"<rect x='8' y='8' width='244' height='154' rx='36' fill='{PAPER}' stroke='{EDGE}' stroke-width='8'/>" + T(130, 112, '1er', 72, 'middle', weight=700))
    # carte de navire (chantier)
    w, h = 560, 280
    circles = ''.join(f"<circle cx='{72+i*104}' cy='150' r='40' fill='#fff' stroke='{EDGE}' stroke-width='4' stroke-dasharray='10 7'/>" + T(72 + i * 104, 160, '1 l.', 24, 'middle', fill=MUTED) for i in range(5))
    svg('carte_navire', w, h, f"<rect x='8' y='8' width='{w-16}' height='{h-16}' rx='22' fill='{PAPER}' stroke='{EDGE}' stroke-width='6'/><rect x='8' y='8' width='{w-16}' height='62' rx='22' fill='{FRAME}'/><rect x='8' y='48' width='{w-16}' height='22' fill='{FRAME}'/>"
        + T(32, 52, 'Navire · 4 cales · 3 places + 1 réservée', 28, weight=700, fill='#F6EFDC') + circles + T(32, 250, 'le plus de parts : armateur principal', 24, fill=MUTED))


# ------------------------------------------------------------ Plateaux des marchands
PCOL = {'rouge': ('#A8322A', '#6E1F19'), 'bleu': ('#2F5E8E', '#1B3B5C'), 'vert': ('#4E7A2C', '#2F4D19')}
def mats():
    W, H = 1800, 1000
    for name, (c, cd) in PCOL.items():
        g = [f"<rect x='0' y='0' width='{W}' height='{H}' rx='40' fill='{FRAME}'/><rect x='20' y='20' width='{W-40}' height='{H-40}' rx='28' fill='#E6DAB6'/>",
             f"<path d='M20 48 Q20 20 48 20 L{W-48} 20 Q{W-20} 20 {W-20} 48 L{W-20} 150 L20 150 Z' fill='{c}'/>",
             T(60, 108, f"Marchand {name}", 56, fam=DISP, fill='#F6EFDC'), T(1012, 100, "Soupçon", 34, 'end', fam=DISP, fill='#F6EFDC')]
        for k in range(7):
            x = 1040 + k * 104
            g.append(f"<rect x='{x}' y='40' width='92' height='92' rx='12' fill='{PAPER}' stroke='{cd}' stroke-width='4'/>" + T(x + 46, 102, str(k), 42, 'middle', weight=700, fill=(INK if k < 3 else '#8E2F25')))
        g.append(zone(40, 180, 820, 300, "Peaux à Québec", "en attente d’un navire pour Paris"))
        g.append(zone(900, 180, 860, 300, "Disques de parts", "un disque par part prise au chantier"))
        g.append(zone(40, 510, 1720, 450, "Associé, recrues, alliances, charges, congés", "contrats : en main, deux au plus"))
        svg(f'mat_{name}', W, H, ''.join(g))


reserve(); decks(); tiles(); mats()
# ------------------------------------------------------------ Navires nommés (carte au chantier + jeton du même nom)
SHIPS = ["L’Aigle d’Or", "Le Saint-Sébastien", "Le Jardin de Hollande", "Le Saint-Jean-Baptiste", "Le Chat de Hollande", "Le Vieux Siméon"]
def ships():
    for i, nm in enumerate(SHIPS):
        W, H = 600, 320
        circ = ''.join(f"<circle cx='{300+(k%3)*96}' cy='{150+(k//3)*92}' r='38' fill='#fff' stroke='{EDGE}' stroke-width='4' stroke-dasharray='10 7'/>" for k in range(5))
        svg(f'carte_navire_{i+1}', W, H, f"<rect x='6' y='6' width='{W-12}' height='{H-12}' rx='22' fill='{PAPER}' stroke='{EDGE}' stroke-width='6'/>"
            f"<path d='M6 28 Q6 6 28 6 L{W-28} 6 Q{W-6} 6 {W-6} 28 L{W-6} 76 L6 76 Z' fill='{FRAME}'/>" + T(W / 2, 56, nm, 38, 'middle', fam=DISP, fill='#F6EFDC')
            + f"<rect x='26' y='100' width='220' height='170' rx='14' fill='none' stroke='{INK}' stroke-width='3' stroke-dasharray='10 7' opacity='.5'/>" + T(136, 196, 'navire', 26, 'middle', fill=MUTED)
            + circ + T(492, 250, '5 parts', 24, 'middle', fill=MUTED))
        short = nm.split(' ', 1)[1] if nm.startswith(('Le ', 'La ')) else nm.replace('L’', '')
        svg(f'navire_{i+1}', 320, 280, f"<path d='M24 120 L296 120 L254 190 L66 190 Z' fill='#F4F4F4' stroke='#3A3A3A' stroke-width='8' stroke-linejoin='round'/><line x1='160' y1='10' x2='160' y2='120' stroke='#3A3A3A' stroke-width='8'/>"
            f"<path d='M170 18 L264 92 L170 104 Z' fill='#FFFFFF' stroke='#3A3A3A' stroke-width='6'/><rect x='6' y='202' width='308' height='70' rx='16' fill='{FRAME}'/>"
            + T(160, 250, short, 36 if len(short) < 14 else 28, 'middle', weight=700, fill='#F6EFDC'))
ships()
# Petites cartes de matériel : même contenu, texte plus grand
MINI = CARD_CSS.replace(".t{font-family:", ".t{font-size:58px!important;font-family:").replace(".fx{font-size:30px", ".fx{font-size:42px")

json.dump({'manifest': MANIFEST, 'decks': DECKS}, open('manifest.json', 'w'), ensure_ascii=False, indent=1)
print(len(MANIFEST), 'pages')

# ------------------------------------------------------------ Aide de jeu (recto : actions ; verso : déroulement)
AIDE_CSS = f""".s{{width:1600px;height:1150px;padding:20px}}.in{{height:100%;border-radius:30px;background:{PAPER};border:4px solid {EDGE};padding:26px 34px}}
h1{{font-family:{DISP};font-weight:400;font-size:46px;margin-bottom:12px;color:{INK};border-bottom:3px solid {FRAME};padding-bottom:6px}}
.sea{{border-radius:22px;padding:10px 22px 8px;margin-bottom:12px;border:3px solid var(--b);background:var(--c)}}
.sea>h2{{font-family:{DISP};font-weight:400;font-size:38px;margin:0 0 4px;color:var(--t)}}.sea>h2 span{{font-family:{BODY};font-size:22px;color:{MUTED};margin-left:12px}}
.g2{{display:grid;grid-template-columns:1fr 1fr;column-gap:18px}}.cols{{display:grid;grid-template-columns:1fr 1fr;column-gap:34px}}
.sub{{border-radius:16px;padding:8px 16px 4px;background:var(--c);border:2px solid var(--b)}}
h3{{font-family:{DISP};font-weight:400;font-size:31px;margin:2px 0 4px;color:var(--t)}}h4{{font-family:{DISP};font-weight:400;font-size:26px;margin:8px 0 2px;color:{FRAME}}}
.a{{margin-bottom:6px;font-size:22px;line-height:1.22}}.big .a{{font-size:28px;margin-bottom:12px;line-height:1.3}}.big .sea{{padding:16px 26px 12px;margin-bottom:18px}}.a b{{font-weight:700}}"""
def A(t, x): return f"<div class='a'><b>{E(t)}</b> — {E(x)}</div>"
def SEA(title, sub, c, b, t, body): return f"<div class='sea' style='--c:{c};--b:{b};--t:{t}'><h2>{E(title)}<span>{E(sub)}</span></h2>{body}</div>"
def SUB(title, c, b, t, body): return f"<div class='sub' style='--c:{c};--b:{b};--t:{t}'><h3>{E(title)}</h3>{body}</div>"
# Saison du castor (recto) : Québec et Expédition
recto = ("<h1>Aide de jeu · l’année en trois saisons</h1>"
  + SEA("Saison du castor", "d’avril à novembre · une action par mois · au verso : printemps et hiver", "#F9EEDA", "#D9B978", "#7A5232",
    "<div class='cols'><div>"
    + A("Début du mois", 'congés d’avril à juin : délivrés sur 3+ en avril, 2+ en mai, d’office en juin, une fois par an ; tirez autant de congés que de joueurs +1.')
    + "</div><div>"
    + A("Tour", 'une action chacun, dans l’ordre du tour, et une action par expédition en cours.') + A("Fin du mois", 'navires qui partent ; canots en transit avancent d’une case ronde ; en juillet, la rivière glisse ; événement de fin de mois.')
    + "</div></div><div class='g2'>"
    + SUB("À Québec", "#E7F1FB", "#9DB9D6", "#2F4E6E",
        A("Vendre des peaux", 'au bureau de la compagnie, au prix du castor, contre une lettre de change payée en hiver (castor gras ★ : +2 par peau) ; ou à Albany : 2 par peau, payé deux mois plus tard, +2 soupçon.') + A("Investir", 'en livres : parts de navire au chantier (1 livre la part, 5 parts), grand canot 3, petit canot 2, distillerie 4. Les navires s’arment en saison.') + A("Recruter", 'prenez une carte de la rivière au prix de sa case : 3, 2 ou 1 livre ; la rivière glisse.')
        + A("Changer les prix", 'reposez sur la piste tous vos produits, canots et navires.') + A("Prendre le pas", 'vous jouerez en premier le mois prochain.') + A("Attendre", 'laissez passer le mois.')
        + "<h4>Sans action</h4>" + A("Jouer un contrat", 'de votre main (deux au plus), puis jouez votre tour.') + A("Faire partir votre navire", 'avant qu’il soit plein : 1 livre de faux fret par place vide.') + A("Ouvrir votre place réservée", 'au public, sur votre navire en rade.')
        + "<h4>Navires en rade de Québec</h4>" + A("Places", '3 publiques et 1 réservée au propriétaire ; une tuile occupe une place.') + A("Chargement", 'la compagnie charge les peaux achetées au bureau et paie le fret au propriétaire.') + A("Départ", 'plein ; dès fin septembre, au choix du propriétaire. Pas parti fin novembre : il hiverne.'))
    + SUB("En expédition", "#F9ECE7", "#D9A48E", "#8E3F25",
        A("Partir (action)", 'à Montréal, avec un congé : composez le canot et posez-le sur la première case ronde de sa route. Canot (achat ou location) et voyageurs se paient en livres.') + A("Transit", 'sans action : en fin de mois, le canot avance d’une case ronde. Frasil en avril et en novembre : bouger est risqué (dé).') + A("Échanger (action)", 'une action par lac de votre zone, pour tous vos canots : une charge contre une tuile ou un jeton.') + A("Retour (action)", 'une action pour tous vos canots : ils quittent la zone et reprennent le transit.') + A("Arrivée", 'à Montréal, déchargement automatique sur votre plateau.')
        + A("Coureurs des bois", 'sans congé ni voyageur : un jeton Coureur des bois et 2 éléments de votre stock ; +1 soupçon. Au retour, ils gardent la moitié du total des peaux (arrondi à l’inférieur).')
        + "<h4>Voyageurs · payés en livres au départ</h4>" + A("Guide · 1", 'regarde les jetons cachés avant d’échanger.') + A("Interprète · 1", 'le premier baril échangé à chaque lac ne fait pas de ravage.') + A("Milicien · 1", 'sans effet pour l’instant.'))
    + "</div>"))
# Printemps et hiver (verso)
verso = ("<h1>Aide de jeu · printemps et hiver</h1><div class='cols big'><div>"
  + SEA("Printemps", "avant avril", "#E5F4E4", "#9CC39A", "#2F5E2C",
    A("La Rochelle", 'chaque navire qui part lance un dé : 4 ou plus, il arrive en mai, sinon en juin.') + A("Lacs", 'chaque lac ouvert est regarni de ses tuiles visibles et cachées.') + A("Congés", 'pris sans payer (côté « à payer ») : 4, 3 ou 2 marchandises pour un coût de 3, 2 ou 1, payé en livres l’hiver. Le joueur le plus pauvre (plus faible fortune commerciale) paie 1 de moins.'))
  + SEA("Lacs", "toute l’année", "#F6EFDC", "#C9B88E", "#7A5232",
    A("Demande", 'simulée par les tuiles visibles. L’eau-de-vie est toujours acceptée, mais chaque baril fait monter les ravages ; +1 soupçon si un fort ou une mission est dans la zone.') + A("Castor", 'tuiles visibles de 1 à 3 castors secs ; non troquées à la fin de l’année, elles passent côté gras (★).') + A("Ravages", 'à 4 : grand événement à chaque passage ; à 6 : interdiction royale et fin de partie.'))
  + "</div><div>"
  + SEA("Hiver", "après novembre", "#DCE9EC", "#8FB0B7", "#2E5560",
    A("Lettres de change", 'payées en livres.') + A("Crédit", 'payez vos congés en livres (impayé : il s’alourdit). Remboursez le crédit de France au prix d’une case selon votre rang en fortune (à 3 joueurs : 3, 4, 5 ; +1 au plus soupçonné). Cédez une distillerie ou un navire contre 2 cases. Puis la dette glisse : zone rayée 1 case, zone rouge 2 ; en 9-10, faillite.') + A("Prix du castor", 'selon l’offre de l’année, puis tirez la carte Prix du castor.') + A("Ravages", '−1.') + A("Entretien", '3 livres par navire qui hiverne à Québec ; 1 livre par canot hiverné.') + A("Commande", 'à La Rochelle, négociée entre joueurs, toujours à crédit, dans la limite de la place des navires.') + A("Investissement", 'un gratuit, sans action.'))
  + "</div></div>")
for nm, body in (('aide_a', recto), ('aide_b', verso)):
    page(nm, 1600, 1150, f"<div class='s'><div class='in'>{body}</div></div>", AIDE_CSS)

# ------------------------------------------------------------ Jetons fort, mission, abîmé (réserves illimitées)
svg('fort_fr', 220, 220, "<rect x='10' y='10' width='200' height='200' rx='34' fill='#F2EAD3' stroke='#2A2418' stroke-width='8'/>"
    "<polygon points='97.9,64.8 92.6,57.5 110.0,32.0 127.4,57.5 122.1,64.8 153.0,87.3 158.3,80.0 188.0,88.7 169.1,113.1 160.5,110.3 148.7,146.7 157.3,149.4 158.2,180.3 129.1,169.9 129.1,160.9 90.9,160.9 90.9,169.9 61.8,180.3 62.7,149.4 71.3,146.7 59.5,110.3 50.9,113.1 32.0,88.7 61.7,80.0 67.0,87.3' fill='#FFFFFF' stroke='#111' stroke-width='7' stroke-linejoin='round'/>"
    "<polygon points='110.0,65.0 156.6,98.9 138.8,153.6 81.2,153.6 63.4,98.9' fill='#FFFFFF' stroke='#111' stroke-width='5' stroke-linejoin='round'/>"
    "<g transform='translate(110 118) scale(1.12)' fill='#E8A93C'><path d='M0,-27 C9,-17 10,-6 4,7 L-4,7 C-10,-6 -9,-17 0,-27 Z'/><path d='M5,6 C9,-6 20,-12 27,-5 C32,1 28,11 21,10 C25,5 21,0 16,3 C12,6 11,8 9,8 Z'/><path d='M-5,6 C-9,-6 -20,-12 -27,-5 C-32,1 -28,11 -21,10 C-25,5 -21,0 -16,3 C-12,6 -11,8 -9,8 Z'/><rect x='-14' y='8' width='28' height='5' rx='1.5'/><path d='M-3,13 L3,13 L4,21 L0,26 L-4,21 Z'/><path d='M-6,13 C-8,19 -13,22 -17,20 C-13,19 -11,16 -11,13 Z'/><path d='M6,13 C8,19 13,22 17,20 C13,19 11,16 11,13 Z'/></g>")
svg('fort_uk', 220, 220, "<rect x='10' y='10' width='200' height='200' rx='34' fill='#F2EAD3' stroke='#2A2418' stroke-width='8'/>"
    "<polygon points='97.9,64.8 92.6,57.5 110.0,32.0 127.4,57.5 122.1,64.8 153.0,87.3 158.3,80.0 188.0,88.7 169.1,113.1 160.5,110.3 148.7,146.7 157.3,149.4 158.2,180.3 129.1,169.9 129.1,160.9 90.9,160.9 90.9,169.9 61.8,180.3 62.7,149.4 71.3,146.7 59.5,110.3 50.9,113.1 32.0,88.7 61.7,80.0 67.0,87.3' fill='#FFFFFF' stroke='#111' stroke-width='7' stroke-linejoin='round'/>"
    "<polygon points='110.0,65.0 156.6,98.9 138.8,153.6 81.2,153.6 63.4,98.9' fill='#FFFFFF' stroke='#111' stroke-width='5' stroke-linejoin='round'/>"
    "<defs><clipPath id='ukc'><circle cx='0' cy='0' r='36'/></clipPath></defs><g transform='translate(110 114)' clip-path='url(#ukc)'><rect x='-40' y='-40' width='80' height='80' fill='#012169'/><line x1='-40' y1='-40' x2='40' y2='40' stroke='#fff' stroke-width='12'/><line x1='40' y1='-40' x2='-40' y2='40' stroke='#fff' stroke-width='12'/><line x1='1.4' y1='-1.4' x2='-38.6' y2='-41.4' stroke='#C8102E' stroke-width='4'/><line x1='1.4' y1='1.4' x2='41.4' y2='-38.6' stroke='#C8102E' stroke-width='4'/><line x1='-1.4' y1='1.4' x2='38.6' y2='41.4' stroke='#C8102E' stroke-width='4'/><line x1='-1.4' y1='-1.4' x2='-41.4' y2='38.6' stroke='#C8102E' stroke-width='4'/><rect x='-40' y='-10' width='80' height='20' fill='#fff'/><rect x='-10' y='-40' width='20' height='80' fill='#fff'/><rect x='-40' y='-6' width='80' height='12' fill='#C8102E'/><rect x='-6' y='-40' width='12' height='80' fill='#C8102E'/></g>")
svg('mission', 220, 220, "<rect x='10' y='10' width='200' height='200' rx='34' fill='#1E1A14' stroke='#2A2418' stroke-width='8'/>"
    "<rect x='98' y='36' width='24' height='150' fill='#FFFFFF'/><rect x='62' y='70' width='96' height='24' fill='#FFFFFF'/>")
svg('abime', 220, 220, "<circle cx='110' cy='110' r='100' fill='#F2EAD3' stroke='#A3352A' stroke-width='8'/>"
    "<path d='M30 104 L190 104 L162 150 L58 150 Z' fill='#C9A77A' stroke='#2A2418' stroke-width='6' stroke-linejoin='round'/>"
    "<path d='M104 104 L118 122 L102 134 L116 150' fill='none' stroke='#A3352A' stroke-width='8' stroke-linejoin='round'/>" + T(110, 190, 'Abîmé', 30, 'middle', weight=700, fill='#A3352A'))
# ------------------------------------------------------------ Canots numérotés (teintés dans TTS) et cartes Expédition
for name, cells in (('grand', 5), ('petit', 3), ('coureur', 2)):
    cw = 120; w = cells * cw + 120; h = 210
    hull = f"<path d='M14 34 L{w-14} 34 L{w-62} {h-14} L62 {h-14} Z' fill='#F4F4F4' stroke='#3A3A3A' stroke-width='8' stroke-linejoin='round'/>"
    for n in 'ABC':
        svg(f'canot_{name}_{n}', w, h, hull + T(w / 2, 150, n, 120, 'middle', weight=700, fill='#1E1E1E'))
EXP_CSS = (f".g{{display:grid;grid-template-columns:repeat(3,1050px);grid-auto-rows:750px}}"
           f".e{{width:1050px;height:750px;position:relative;background:{PAPER};border:18px solid var(--c);border-radius:44px}}"
           f".e h1{{position:absolute;left:0;right:0;top:0;height:112px;background:var(--c);color:#F6EFDC;font:400 62px {DISP};padding:20px 36px 0}}"
           f".z{{position:absolute;background:#E9E0C6;border:5px dashed {EDGE};display:flex;align-items:center;justify-content:center;font:500 34px {BODY};color:{MUTED}}}"
           f".cg{{left:30px;top:146px;width:300px;height:300px;border-radius:30px}}"
           f".v{{top:176px;width:150px;height:216px;border-radius:50%;border-style:solid;border-color:var(--d);font-size:28px;text-align:center;line-height:1.1}}"
           f".m{{left:30px;right:30px;top:478px;height:226px;border-radius:30px}}"
           f".bk{{width:1050px;height:750px;background:var(--c);border-radius:44px;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#F6EFDC}}"
           f".bk div{{font:400 110px {DISP}}}.bk span{{font:500 40px {BODY};opacity:.8;margin-top:10px}}")
TYPES = (('grand', 'Grand canot', 3), ('petit', 'Petit canot', 3), ('coureur', 'Coureur des bois', 0))
for pn, (c, cd) in PCOL.items():
    cards = []
    for n in 'ABC':
        for key, lab, nv in TYPES:
            cg = 'Coureur<br>des bois' if key == 'coureur' else 'Congé'
            vs = ''.join(f"<div class='z v' style='left:{380 + k * 220}px'>Voyageur<br>{k + 1}</div>" for k in range(nv))
            cards.append(f"<div class='e' style='--c:{c};--d:{cd}'><h1>Expédition <b style=\"font:700 56px {BODY}\">{n}</b> · {lab}</h1><div class='z cg' style='text-align:center'>{cg}</div>{vs}<div class='z m'>Marchandises</div></div>")
    page(f'exp_{pn}', 3150, 2250, f"<div class='g'>{''.join(cards)}</div>", EXP_CSS)
    page(f'exp_{pn}_back', 1050, 750, f"<div class='bk' style='--c:{c}'><div>Expédition</div><span>Castor et eau-de-vie</span></div>", EXP_CSS)
DECKS['exp'] = {'cols': 3, 'rows': 3, 'n': 9, 'names': [f'Expédition {n} · {lab}' for n in 'ABC' for _, lab, _ in TYPES]}
# Jeton Coureur des bois (taille d'un congé), posé sur la carte Expédition des coureurs à la place du congé
import base64, io
from PIL import Image as _I
_im = _I.open('coureur_src.png').convert('RGB'); _im = _im.crop((0, 0, _im.width, _im.width)); _b = io.BytesIO(); _im.save(_b, 'JPEG', quality=90)
_u = 'data:image/jpeg;base64,' + base64.b64encode(_b.getvalue()).decode()
svg('tok_coureur', 400, 400, f"<defs><clipPath id='cp'><rect x='16' y='16' width='368' height='368' rx='40'/></clipPath></defs><rect x='8' y='8' width='384' height='384' rx='46' fill='{PAPER}' stroke='{EDGE}' stroke-width='8'/>"
    f"<image href='{_u}' x='16' y='16' width='368' height='368' clip-path='url(#cp)' preserveAspectRatio='xMidYMid slice'/><rect x='16' y='300' width='368' height='84' fill='{FRAME}' opacity='.85' clip-path='url(#cp)'/>" + T(200, 356, 'Coureur des bois', 44, 'middle', fam=DISP, fill='#F6EFDC'))
# Canots 3D : texture 1024 × 512, pont en haut (cases de place), flanc en bas (lettre), couleur du joueur cuite dans l'image
CN = {'grand': 5, 'petit': 3, 'coureur': 2}
def canot_tex(name, c, cd, cells, letter):
    # Proportions identiques au modèle 3D (meshes.py) : longueur L = 120 × cases + 92, largeur 150, hauteur 100 ; 1,5 px par unité
    S = 1.5; L = cells * 120 + 92; W = round(L * S); DH = round(150 * S); SH = round(100 * S); H = DH + SH + 24
    g = [f"<rect x='0' y='0' width='{W}' height='{H}' fill='{cd}'/><rect x='6' y='6' width='{W-12}' height='{DH}' rx='14' fill='{c}' stroke='{cd}' stroke-width='8'/>"]
    sq = 106 * S
    for k in range(cells):
        x = W / 2 + (k - (cells - 1) / 2) * 120 * S - sq / 2
        g.append(f"<rect x='{x:.1f}' y='{6 + DH/2 - sq/2:.1f}' width='{sq:.1f}' height='{sq:.1f}' rx='14' fill='#FFFFFF' stroke='{cd}' stroke-width='6'/>")
    m = 48 * S; y0 = DH + 18
    g.append(f"<path d='M6 {y0} L{W-6} {y0} L{W-6-m:.1f} {H-6} L{6+m:.1f} {H-6} Z' fill='{c}' stroke='{cd}' stroke-width='8' stroke-linejoin='round'/>")
    if letter: g.append(T(W / 2, H - 30, letter, 130, 'middle', weight=700, fill=PAPER))
    svg(name, W, H, ''.join(g))
for pn, (c, cd) in PCOL.items():
    for key, cells in CN.items():
        for L in ('A', 'B', 'C', ''):
            canot_tex(f'cn_{pn}_{key}' + (f'_{L}' if L else ''), c, cd, cells, L)
    for key, lab in (('grand', 'Grand canot'), ('petit', 'Petit canot'), ('coureur', 'Coureurs des bois')):
        svg(f'sacexp_{pn}_{key}', 560, 400, f"<rect x='0' y='0' width='560' height='400' rx='40' fill='{c}'/><rect x='18' y='18' width='524' height='364' rx='28' fill='none' stroke='#F6EFDC' stroke-width='6'/>"
            + T(280, 170, 'Expéditions', 64, 'middle', fam=DISP, fill='#F6EFDC') + T(280, 260, lab, 50, 'middle', weight=700, fill='#F6EFDC') + T(280, 330, 'A · B · C', 40, 'middle', fill='#F6EFDC'))
json.dump({'manifest': MANIFEST, 'decks': DECKS}, open('manifest.json', 'w'), ensure_ascii=False, indent=1)
