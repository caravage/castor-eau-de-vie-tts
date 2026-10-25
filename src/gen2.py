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
    # Rivière
    g.append(T(80, 200, "Rivière de recrutement", 38, fam=DISP)); g.append(T(560, 200, "Recruter : payez le prix de la case · en fin de mois, la carte de droite part à la défausse, les autres glissent, une nouvelle entre à 3 livres", 24, fill=MUTED))
    labs = [("pioche", None), ("3 livres", 3), ("2 livres", 2), ("1 livre", 1), ("1 livre", 1), ("défausse", None)]
    for k, (lab, p) in enumerate(labs):
        x = 80 + k * 300
        g.append(f"<rect x='{x}' y='230' width='270' height='380' rx='16' fill='{PAPER if p else PCARD}' stroke='{EDGE}' stroke-width='3' {'' if p else 'stroke-dasharray=\"14 9\"'}/>")
        if p: g.append(f"<circle cx='{x+135}' cy='660' r='34' fill='{GOLD}'/>" + T(x + 135, 672, str(p), 34, 'middle', weight=700, fill='#fff') + T(x + 135, 720, 'livre' + ('s' if p > 1 else ''), 22, 'middle', fill=MUTED))
        else: g.append(T(x + 135, 670, lab, 26, 'middle', fill=MUTED))
    # Congés
    g.append(zone(1950, 160, 1570, 560, "Congés de l’année", "joueurs − 1 · tirés du sac au début d’avril · révélés avant l’enchère secrète"))
    for k in range(3): g.append(f"<rect x='{2000+k*330}' y='300' width='290' height='290' rx='18' fill='{PAPER}' stroke='{EDGE}' stroke-width='3' stroke-dasharray='12 8'/>")
    g.append(T(3040, 340, "sac des congés", 26, fill=MUTED)); g.append(f"<rect x='3020' y='360' width='440' height='280' rx='18' fill='none' stroke='{EDGE}' stroke-width='3' stroke-dasharray='12 8'/>")
    # Chantier
    g.append(zone(80, 780, 1840, 640, "Chantier de La Rochelle", "cartes de navire · 5 parts de 1 livre · un disque de couleur par part · le plus de parts : armateur principal"))
    for k in range(6):
        x = 120 + (k % 3) * 600; y = 900 + (k // 3) * 250
        g.append(f"<rect x='{x}' y='{y}' width='560' height='230' rx='14' fill='{PAPER}' stroke='{EDGE}' stroke-width='2.5' stroke-dasharray='12 8'/>")
    # Comptoir
    g.append(zone(1950, 780, 1570, 640, "Comptoir de Québec", "ne vend que son stock · prix fixé à l’arrivée : milieu des prix des joueurs", fill='#E9E4D6'))
    for k, lab in enumerate(["marchandises", "eau-de-vie", "grand canot à louer", "petit canot à louer"]):
        x = 1990 + (k % 2) * 760; y = 900 + (k // 2) * 250
        g.append(f"<rect x='{x}' y='{y}' width='730' height='230' rx='14' fill='{PAPER}' stroke='{EDGE}' stroke-width='2.5' stroke-dasharray='12 8'/>" + T(x + 20, y + 40, lab, 26, fill=MUTED))
    # Événements et voyageurs
    g.append(zone(80, 1480, 1840, 460, "Événements", "fin de mois · demande de Paris (en hiver) · grand événement (ravages 4)"))
    for k, lab in enumerate(["fin de mois", "défausse", "demande de Paris", "grand événement"]):
        x = 120 + k * 450
        g.append(f"<rect x='{x}' y='1590' width='270' height='310' rx='16' fill='{PCARD}' stroke='{EDGE}' stroke-width='3' stroke-dasharray='14 9'/>" + T(x + 135, 1760, lab, 24, 'middle', fill=MUTED))
    g.append(zone(1950, 1480, 1570, 460, "Voyageurs", "représentant 2 livres · guide, milicien, interprète 1 livre · un par place de congé"))
    for k, lab in enumerate(["représentant", "guide", "milicien", "interprète"]):
        x = 1990 + k * 380
        g.append(f"<rect x='{x}' y='1600' width='350' height='300' rx='16' fill='{PAPER}' stroke='{EDGE}' stroke-width='2.5' stroke-dasharray='12 8'/>" + T(x + 175, 1870, lab, 24, 'middle', fill=MUTED))
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

def sheet(name, kind, cards, back_title, back_sub):
    n = len(cards); cols = min(10, n); rows = math.ceil(n / cols)
    page(name, cols * CW, rows * CH, f"<div class='grid' style='--n:{cols}'>{''.join(cards)}</div>", CARD_CSS)
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
    mats = [("Navire", "1 navire armé, et 2 livres de dette envers La Rochelle."), ("Parts de navire", "2 parts payées sur une carte de navire au chantier, et 3 livres."),
            ("Bourse", "4 livres."), ("Ballots de marchandises", "4 marchandises."), ("Eau-de-vie", "2 bouteilles et 1 livre."), ("Assortiment", "2 marchandises et 1 bouteille."),
            ("Petit canot", "1 petit canot et 2 livres."), ("Grand canot", "1 grand canot et 1 livre."), ("Alambic", "1 alambic et 1 livre.")]
    DECKS['mat'] = sheet('deck_mat', 'Matériel de départ', [card_html('Matériel de départ', t, fx) for t, fx in mats], 'Matériel', 'distribué en entier · 3 par marchand'); DECKS['mat']['names'] = [t for t, _ in mats]
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
    # Congés : 0, 1 ou 2 places de voyageur, au choix du joueur
    seal = f"<circle cx='{S/2}' cy='70' r='30' fill='#8E2F25'/><circle cx='{S/2}' cy='70' r='20' fill='none' stroke='#F2D9B0' stroke-width='3'/>"
    for n in (0, 1, 2):
        slots = ''.join(f"<circle cx='{S/2 + (i - (n - 1) / 2) * 140}' cy='250' r='58' fill='#fff' stroke='{INK}' stroke-width='4' stroke-dasharray='12 8'/>" for i in range(n))
        sub = {0: 'sans voyageur', 1: '1 voyageur', 2: '2 voyageurs'}[n]
        svg(f'conge_{n}', S, S, tile_frame(S, PAPER) + seal + T(S / 2, 150, 'Congé', 50, 'middle', fam=DISP) + slots + T(S / 2, 360, sub + (' au choix' if n else ''), 28, 'middle', fill=MUTED))
    svg('conge_back', S, S, tile_frame(S, '#8E2F25', '#5E1F18') + T(S / 2, 215, 'Congé', 66, 'middle', fam=DISP, fill='#F6EFDC') + T(S / 2, 268, "de l’intendant", 30, 'middle', fam=SER, italic=True, fill='#F6EFDC'))
    # Voyageurs
    VOY = {'rep': ('Représentant', '#7A2E3A'), 'guide': ('Guide', '#2F5E4A'), 'mil': ('Milicien', '#3E5A7A'), 'int': ('Interprète', '#8A5A14')}
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
    W, H = 1800, 1320
    for name, (c, cd) in PCOL.items():
        g = [f"<rect x='0' y='0' width='{W}' height='{H}' rx='40' fill='{FRAME}'/><rect x='20' y='20' width='{W-40}' height='{H-40}' rx='28' fill='#E6DAB6'/>",
             f"<path d='M20 48 Q20 20 48 20 L{W-48} 20 Q{W-20} 20 {W-20} 48 L{W-20} 150 L20 150 Z' fill='{c}'/>",
             T(60, 108, f"Marchand {name}", 56, fam=DISP, fill='#F6EFDC'), T(1012, 100, "Soupçon", 34, 'end', fam=DISP, fill='#F6EFDC')]
        for k in range(7):
            x = 1040 + k * 104
            g.append(f"<rect x='{x}' y='40' width='92' height='92' rx='12' fill='{PAPER}' stroke='{cd}' stroke-width='4'/>" + T(x + 46, 102, str(k), 42, 'middle', weight=700, fill=(INK if k < 3 else '#8E2F25')))
        def track(y, lab, sub, vals, fill):
            out = [T(60, y + 52, lab, 40, fam=DISP), T(60, y + 86, sub, 22, fill=MUTED)]
            for i, v in enumerate(vals):
                x = 340 + i * 142
                out.append(f"<rect x='{x}' y='{y}' width='130' height='110' rx='14' fill='{fill}' stroke='{EDGE}' stroke-width='4'/>" + T(x + 65, y + 72, v, 46, 'middle', weight=700))
            return ''.join(out)
        g.append(track(190, "Livres", "argent", [str(i) for i in range(10)], PAPER))
        g.append(track(316, "", "", [str(i) for i in range(10, 20)], PAPER))
        g.append(T(60, 386, "au-delà de 19 :", 22, fill=MUTED) + T(60, 414, "un 2ᵉ marqueur vaut 20", 22, fill=MUTED))
        g.append(track(470, "Dette", "envers La Rochelle", [str(i) for i in range(10)], '#EADFC2'))
        g.append(T(340, 618, "La Rochelle avance jusqu’à 6 livres (9 avec le Négociant huguenot) · payer d’abord, s’endetter si besoin", 24, fill=MUTED))
        g.append(zone(40, 660, 820, 280, "Peaux à Québec", "en attente d’un navire pour Paris"))
        g.append(zone(900, 660, 860, 280, "Disques de parts", "un disque par part prise au chantier"))
        g.append(zone(40, 980, 1720, 300, "Associé, recrues, alliances, charges, congés", "contrats : en main, deux au plus"))
        svg(f'mat_{name}', W, H, ''.join(g))

reserve(); decks(); tiles(); mats()
json.dump({'manifest': MANIFEST, 'decks': DECKS}, open('manifest.json', 'w'), ensure_ascii=False, indent=1)
print(len(MANIFEST), 'pages')
