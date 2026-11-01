# Tuiles v39 (31 oct. 2026) : peaux sèches et grasses, dos gras neutre, tuiles secrètes, congés (design B) et face « non payé ».
# Exécuté à la fin de gen2.py : remplace les anciennes images du même nom. Dessins en coordonnées 96 (tuiles) ou 110 (congés).
S4 = 400
PAP = '#F6EFDC'; OCRE = '#B7A675'; OR = '#C9952B'; FOND_GRAS = '#E8D5A8'; BRUN = '#3A2618'; ROUGE = '#8E2F25'; ROUGE_CR = '#A3352A'
VERT_T = '#3B6D2E'; CREME = '#F2E2C4'

def w96(inner): return f"<g transform='scale({S4/96})'>{inner}</g>"
def w110(inner): return f"<g transform='scale({S4/110})'>{inner}</g>"
def tx(x, y, s, size, fill=INK, anchor='middle', fam=SER, italic=False, weight=400, ls=0):
    return (f"<text x='{x}' y='{y}' font-family=\"{fam}\" font-size='{size}' font-weight='{weight}' text-anchor='{anchor}' fill='{fill}'"
            + (" font-style='italic'" if italic else '') + (f" letter-spacing='{ls}'" if ls else '') + f">{E(s)}</text>")

def peau(cx, cy, s, rot=0, fill=PELT, st='#3A2410', ovale=True, court=False, sw=1.2):
    bas = 15 if court else 17
    return (f"<g transform='translate({cx} {cy}) rotate({rot}) scale({s})'><ellipse rx='10' ry='13' fill='{fill}' stroke='{st}' stroke-width='{sw}'/>"
            + (f"<ellipse rx='6.5' ry='9' fill='none' stroke='{CREME}' stroke-width='.5'/>" if ovale else '')
            + f"<path d='M0 -13V-17M0 13V{bas}M-10 0H-14M10 0H14' stroke='{st}' stroke-width='{sw}' fill='none'/></g>")

def cadre96(fill, stroke, sw=3): return f"<rect x='1.5' y='1.5' width='93' height='93' rx='14' fill='{fill}' stroke='{stroke}' stroke-width='{sw}'/>"

SEC_F = ['#8A5A2B', '#9C6A36', '#7A4E24']; GRAS_F = ['#5E3A1A', '#6E4522', '#4E2E14']
def eventail(n, cols, st, tiles_y=None):
    # positions validées : 1 peau (48,42) ×2 ; 2 peaux ±12° ×1,7 ; 3 peaux ±12° ×1,38, la centrale par-dessus
    if n == 1: return peau(48, 42, 2, 0, cols[0], st, court=True)
    if n == 2: return peau(33, 43, 1.7, -12, cols[0], st) + peau(63, 41, 1.7, 10, cols[1], st)
    return peau(28, 44, 1.38, -12, cols[0], st) + peau(68, 44, 1.38, 12, cols[2], st) + peau(48, 41, 1.38, 0, cols[1], st)

POINTS = {1: ([31], 41), 2: ([26, 35], 45), 3: ([22, 31, 40], 50)}
POINTS_G = {1: ([28], 38), 2: ([23, 32], 42), 3: ([19, 28, 37], 47)}
def ligne_bas(n, mot, pts, y=83):
    xs, xt = pts[n]
    return ''.join(f"<circle cx='{x}' cy='{y}' r='3' fill='{INK}'/>" for x in xs) + tx(xt, y + 5, mot, 15, anchor='start', italic=True)

def tuile_sec(n): return w96(cadre96(PAP, OCRE) + eventail(n, SEC_F, '#3A2410') + ligne_bas(n, 'Sec', POINTS, 82))
def tuile_gras(n): return w96(cadre96(FOND_GRAS, OR) + eventail(n, GRAS_F, '#2A1608') + ligne_bas(n, 'Gras', POINTS_G, 82))
def gras_neutre():
    return w96(cadre96(FOND_GRAS, OR) + peau(48, 42, 2, 0, GRAS_F[0], '#2A1608', court=True)
               + tx(48, 51, '?', 22, CREME, fam=BODY, weight=700) + tx(48, 87, 'Gras', 15, italic=True))

for n in (1, 2, 3):
    for tag in ('G', 'S'):
        svg(f'tile_{tag}{n}_sec', S4, S4, tuile_sec(n)); svg(f'tile_{tag}{n}_gras', S4, S4, tuile_gras(n))
svg('tile_gras_neutre', S4, S4, gras_neutre())

# ------------------------------------------------------------ Tuiles secrètes
def titre(t, fill, size=13, y=19): return tx(48, y, t, size, fill, fam=DISP)
def lignes(ls, y0, dy, size, fill=INK): return ''.join(tx(48, y0 + i * dy, l, size, fill, fam=BODY) for i, l in enumerate(ls))
FACE = cadre96(PAP, BRUN)
SECRETES = {
    'back': w96(cadre96(BRUN, OCRE) + "<path d='M22 66Q48 14 74 66Z' fill='#8A6A45' stroke='#E8D5A8' stroke-width='1.5'/>"
                "<path d='M42 66V54Q48 48 54 54V66' fill='#3A2618'/><path d='M48 30Q44 24 48 19Q52 14 48 9' fill='none' stroke='#E8D5A8' stroke-width='1.2'/>"
                "<path d='M28 44H68M25 54H71' stroke='#E8D5A8' stroke-width='.8' opacity='.6'/><line x1='16' y1='66' x2='80' y2='66' stroke='#E8D5A8' stroke-width='1.5'/>"),
    'present': w96(FACE + titre('Présent', VERT_T) + peau(40, 42, 1, 0, PELT, '#3A2410', ovale=False)
                   + "<path d='M56 36H70V50H56Z' fill='#C9A869' stroke='#3A2410' stroke-width='1.2'/><path d='M56 43H70M63 36V50' stroke='#3A2410' stroke-width='.8'/>"
                   + lignes(['1 peau sèche,', 'charge rendue'], 76, 13, 11)),
    'alliance': w96(FACE + titre('Alliance', VERT_T) + "<circle cx='42' cy='38' r='10' fill='none' stroke='#A87A1E' stroke-width='2.5'/><circle cx='54' cy='38' r='10' fill='none' stroke='#A87A1E' stroke-width='2.5'/>"
                    + lignes(['1 peau grasse', '−1 ravage', '−1 voyageur'], 63, 13, 11)),
    'concurrence': w96(FACE + titre('Concurrence', ROUGE, 11.5) + peau(28, 44, 1, 0, PELT, '#3A2410', ovale=False)
                       + f"<path d='M47 44H57M54.5 42L57 44L54.5 46' fill='none' stroke='{ROUGE}' stroke-width='1.3'/><ellipse cx='74' cy='44' rx='12' ry='9' fill='#9DBDC2' stroke='#3E6670' stroke-width='1.2'/>"
                       + lignes(['1 tuile part', 'au lac voisin'], 77, 12, 10)),
    'gatees': w96(FACE + titre('Peaux gâtées', ROUGE, 11.5)
                  + "<g transform='translate(48 46) scale(1.25)'><ellipse rx='10' ry='13' fill='#9A8A70' stroke='#3A2410' stroke-width='1.2'/><circle cx='-3' cy='-4' r='2' fill='#3A2410'/>"
                    "<circle cx='4' cy='3' r='2.5' fill='#3A2410'/><circle cx='-2' cy='7' r='1.5' fill='#3A2410'/><path d='M0 -13V-17M0 13V15M-10 0H-14M10 0H14' stroke='#3A2410' stroke-width='1.2'/></g>"
                  + tx(48, 87, 'charge perdue', 10)),
    'mission': w96(FACE + titre('Missionnaire', ROUGE, 11.5, 18) + f"<path d='M48 24V38M43 28H53' stroke='{INK}' stroke-width='2'/>"
                   + lignes(['Si eau-de-vie en', 'échange ou dans', 'canot : +1 soupçon.', 'Marchandise', 'rendue sinon.'], 50, 10, 9.5)),
    'scorbut': w96(FACE + titre('Scorbut', ROUGE) + f"<circle cx='48' cy='32' r='6' fill='none' stroke='{INK}' stroke-width='2'/><path d='M48 38V52M40 44H56M48 52L42 60M48 52L54 60' stroke='{INK}' stroke-width='2' fill='none'/>"
                   + f"<path d='M60 30L72 42M72 30L60 42' stroke='{ROUGE}' stroke-width='2'/>" + lignes(['−1 voyageur,', 'sinon −1 stock'], 76, 13, 11)),
    'ruine': w96(cadre96('#2A2418', ROUGE) + titre('Ruine', PAP) + "<path d='M30 46A18 18 0 1 1 62 52' fill='none' stroke='#B7A675' stroke-width='2.5'/>"
                 "<path d='M57 30L50 42L56 46L48 60' fill='none' stroke='#C0574A' stroke-width='2'/>" + lignes(['zone sans tuile :', 'elle se ferme'], 76, 13, 11, PAP)),
}
TRAITE_P = {1: lambda: peau(48, 47, 1.45, 0, SEC_F[0], '#3A2410', court=True),
            2: lambda: peau(36, 48, 1.3, -12, SEC_F[0], '#3A2410') + peau(60, 46, 1.3, 10, SEC_F[1], '#3A2410'),
            3: lambda: peau(28, 49, 1.1, -12, SEC_F[0], '#3A2410') + peau(68, 49, 1.1, 12, SEC_F[2], '#3A2410') + peau(48, 46, 1.1, 0, SEC_F[1], '#3A2410')}
for n in (1, 2, 3): SECRETES[f'fur{n}'] = w96(FACE + titre('Traite', VERT_T) + TRAITE_P[n]() + ligne_bas(n, 'Sec', POINTS, 83))
for k, inner in SECRETES.items(): svg(f'hid_{k}', S4, S4, inner)

# ------------------------------------------------------------ Congés (design B) et face « non payé »
FLEUR = ("<g fill='#1F3A6B'><path d='M0 -10C3 -6 3 -2 0 2C-3 -2 -3 -6 0 -10Z'/><path d='M-1 2C-6 -4 -11 0 -8 4C-6 2 -4 2 -2 4Z'/>"
         "<path d='M1 2C6 -4 11 0 8 4C6 2 4 2 2 4Z'/><rect x='-5' y='3' width='10' height='2.5'/><path d='M-2 5.5L0 10L2 5.5Z'/></g>")
def ovale(perso, x, y, s):
    sym = FLEUR if perso == 'off' else f"<path d='M0 -10V10M-6 -4H6' stroke='{INK}' stroke-width='2.5'/>"
    return f"<g transform='translate({x} {y}) scale({s})'><ellipse rx='14' ry='17' fill='#EADFC2' stroke='{INK}' stroke-width='1.5'/>{sym}</g>"
def caisses(n, y):
    x0 = 55 - (n * 12 + (n - 1) * 3) / 2
    return ''.join(f"<rect x='{x0 + i * 15:.1f}' y='{y}' width='12' height='12' fill='#C9A869' stroke='#3A2410' stroke-width='1'/>" for i in range(n))
def croix(x, y): return f"<path d='M{x} {y}L{x+6} {y+6}M{x+6} {y}L{x} {y+6}' stroke='{ROUGE_CR}' stroke-width='1.6'/>"
CLIP = "<defs><clipPath id='cb'><rect x='0' y='0' width='110' height='110' rx='12'/></clipPath></defs>"
def conge_face(nom, prix, credit=False, canot=None, perso=None, n_caisses=0, extra=None):
    band = (f"<rect width='110' height='28' fill='{ROUGE_CR}' clip-path='url(#cb)'/><path d='M0 9H110M0 18H110' stroke='#F2D9B0' stroke-width='.6' opacity='.5'/>" if credit
            else f"<rect width='110' height='28' fill='{ROUGE}' clip-path='url(#cb)'/>")
    g = [CLIP, f"<rect x='1.5' y='1.5' width='107' height='107' rx='12' fill='{PAP}'/>", band,
         f"<rect x='1.5' y='1.5' width='107' height='107' rx='12' fill='none' stroke='{ROUGE}' stroke-width='3'/>",
         tx(55, 20, prix, 14 if credit else 15, PAP, fam=BODY, weight=700)]
    deux = len(nom) == 2; seul = not (canot or perso or n_caisses or extra)
    if deux: g += [tx(55, 46, nom[0], 12, italic=True), tx(55, 60, nom[1], 12, italic=True)]
    else: g.append(tx(55, 70 if seul else (48 if (canot and perso) else (52 if perso else 56)), nom[0], 13 if len(nom[0]) < 16 else 12, italic=True))
    if canot: g.append(tx(55, 66 if perso else 86, canot, 12))
    if extra == 'fabrique':
        g += [ovale('mis', 26, 86, .75), tx(42, 83, 'soupçon ≤ 1', 9.5, anchor='start', fam=BODY), croix(43, 90), tx(52, 96, 'eau-de-vie', 9.5, anchor='start')]
    elif extra == 'faveur':
        g += [ovale('off', 30, 86, .75), tx(48, 90, 'soupçon ≤ 2', 9.5, anchor='start', fam=BODY)]
    elif perso: g.append(ovale(perso, 55, 88 if canot else 82, .8 if canot else 1))
    if extra == 'veuve': g.append(tx(55, 86, 'dernier choix', 11))
    if extra == 'outaouais': g += [tx(55, 83, "Lacs d'en haut", 10.5), tx(55, 96, 'seulement', 10.5)]
    if extra == 'pays': g.append(tx(55, 86, 'Pays seulement', 11))
    if extra == 'ouest': g += [croix(21, 65), tx(33, 72, "Lacs d'en bas", 10.5, anchor='start'), caisses(1, 82)]
    elif n_caisses: g.append(caisses(n_caisses, 76 if not deux else 78))
    return w110(''.join(g))

CONGES = [  # (id, nom, prix, crédit, canot, personnage, caisses, extra, nombre) — d'après « Cartes et tuiles », 31 oct. 2026
    ('ord_m', ['Congé ordinaire'], 3, False, 'moyen canot', None, 0, None, 3),
    ('ord_m_off', ['Congé ordinaire'], 2, False, 'moyen canot', 'off', 0, None, 2),
    ('ord_g', ['Congé ordinaire'], 4, False, 'grand canot', None, 0, None, 3),
    ('ord_g_off', ['Congé ordinaire'], 4, False, 'grand canot', 'off', 0, None, 1),
    ('ord_g_mis', ['Congé ordinaire'], 4, False, 'grand canot', 'mis', 0, None, 1),
    ('lib', ['Congé libre'], 5, False, None, None, 0, None, 3),
    ('lib_off', ['Congé libre'], 5, False, None, 'off', 0, None, 1),
    ('lib_mis', ['Congé libre'], 5, False, None, 'mis', 0, None, 2),
    ('lib3', ['Congé libre'], 3, False, None, None, 0, None, 1),
    ('veuve', ["Veuve d'officier"], 2, False, None, None, 0, 'veuve', 1),
    ('gentil', ['Gentilhomme'], 5, False, None, None, 1, None, 1),
    ('seigneur', ['Seigneur'], 7, False, None, None, 2, None, 1),
    ('fabrique', ['Fabrique', 'Notre-Dame'], 3, False, None, None, 0, 'fabrique', 2),
    ('faveur', ['Faveur de', "l'intendant"], 1, True, None, None, 0, 'faveur', 2),
    ('rochelle', ['Fournisseur de', 'La Rochelle'], 2, True, None, None, 4, None, 2),
    ('bordeaux', ['Fournisseur de', 'Bordeaux'], 2, True, None, None, 3, None, 2),
    ('outaouais', ['Congé des', 'Outaouais'], 3, False, None, None, 0, 'outaouais', 1),
    ('ouest', ["Congé de l'Ouest"], 4, False, None, None, 0, 'ouest', 1),
    ('pays', ['Congé de Pays'], 4, False, None, None, 0, 'pays', 1),
]
for cid, nom, p, cr, canot, perso, nc, extra, nb in CONGES:
    prix = (f'{p} crédit' + ('s' if p > 1 else '')) if cr else f'{p} ₶'
    svg(f'conge_{cid}', S4, S4, conge_face(nom, prix, cr, canot, perso, nc, extra))
for p in sorted({c[2] for c in CONGES if not c[3]}):
    svg(f'conge_np{p}', S4, S4, w110(f"<rect x='1.5' y='1.5' width='107' height='107' rx='12' fill='#5E1F18' stroke='{ROUGE}' stroke-width='3'/>"
        "<rect x='8' y='8' width='94' height='94' rx='8' fill='none' stroke='#F2D9B0' stroke-width='.8' opacity='.6'/>"
        + tx(55, 28, 'Congé', 13, PAP, italic=True) + tx(55, 43, 'NON PAYÉ', 11, '#F2D9B0', fam=BODY, ls=1.5)
        + f"<circle cx='55' cy='75' r='24' fill='{PAP}'/><circle cx='55' cy='75' r='20' fill='none' stroke='{ROUGE}' stroke-width='1'/>"
        + tx(55, 81, f'{p} ₶', 16, ROUGE, fam=BODY, weight=700)))
json.dump(CONGES, open('conges_v39.json', 'w'), ensure_ascii=False)
# une seule entrée par image dans le manifeste (la dernière l'emporte)
_seen = {}
for _m in MANIFEST: _seen[_m[0]] = _m
MANIFEST[:] = list(_seen.values())
