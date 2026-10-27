# Sauvegarde TTS fidèle à l'artefact « Table du castor » : même plateau, mêmes zones, mêmes positions de départ (3 joueurs).
import json, random
from PIL import Image
ASP = {}
def aspect(img):
    if img not in ASP: w, h = Image.open(f'img/{img}.png').size; ASP[img] = h / w
    return ASP[img]
random.seed(1670)
URL = 'https://raw.githubusercontent.com/caravage/castor-eau-de-vie-tts/main/img/v15/'
DK = json.load(open('manifest.json'))['decks']
TP = json.load(open('table_pieces.json')); SIZE = TP['SIZE']; TW, TH = TP['TW'], TP['TH']
U = 0.035                                   # 1 pixel de l'artefact = 0,035 unité de plan
X0, X1, Y1 = -150, 1995, 1450                # image exportée : x de -150 à 1995, y de 0 à 1265
def P(cx, cy): return round((cx - (X0 + X1) / 2) * U, 3), round(-(cy - Y1 / 2) * U, 3)
used = set()
def guid():
    while True:
        g = '%06x' % random.randrange(16 ** 6)
        if g not in used: used.add(g); return g
def col(h): h = h.lstrip('#'); return {'r': int(h[0:2], 16) / 255, 'g': int(h[2:4], 16) / 255, 'b': int(h[4:6], 16) / 255}
WHITE = col('#FFFFFF'); GREY = col('#8C877E'); INKC = col('#2A2418')
PC = [col('#C0392B'), col('#2F6FB0'), col('#4E8A2C')]; SEAT = ['Red', 'Blue', 'Green']; PN = ['rouge', 'bleu', 'vert']

def T(x=0, z=0, y=2.0, s=1.0, fz=0):
    return {'posX': x, 'posY': y, 'posZ': z, 'rotX': 0, 'rotY': 180, 'rotZ': fz, 'scaleX': s, 'scaleY': 1.0, 'scaleZ': s}
def base(name, nick, wpx, pos=None, color=WHITE, lock=False, h=0.5, fz=0, y3=False, desc='', s0=None):
    w = round(wpx * U, 4); n = {'w': w}
    if pos: n.update({'x': pos[0], 'z': pos[1], 'h': h})
    if lock: n['lock'] = True
    if fz: n['fz'] = fz
    if y3: n['y3'] = True
    x, z = pos if pos else (0, 0)
    return {'GUID': guid(), 'Name': name, 'Transform': T(x, z, 2.0, s0 if s0 else w / 2, fz), 'Nickname': nick, 'Description': desc, 'GMNotes': json.dumps(n),
            'ColorDiffuse': color, 'Locked': bool(pos), 'Grid': False, 'Snap': False, 'Tooltip': True, 'Hands': False, 'HideWhenFaceDown': False}
def tile(nick, front, wpx, pos=None, back=None, typ=3, thick=0.1, color=WHITE, lock=False, h=0.5, fz=0, desc='', face=None):
    o = base('Custom_Tile', nick, wpx, pos, color, lock, h, fz, desc=desc)
    o['GMNotes'] = json.dumps({**json.loads(o['GMNotes']), 'd': round(wpx * aspect(front) * U, 4)})
    if face: o['GMNotes'] = json.dumps({**json.loads(o['GMNotes']), 'face': face})
    o['CustomImage'] = {'ImageURL': URL + front + '.png', 'ImageSecondaryURL': URL + (back or front) + '.png', 'ImageScalar': 1.0, 'WidthScale': 0.0,
                        'CustomTile': {'Type': typ, 'Thickness': thick, 'Stackable': False, 'Stretch': False}}
    return o
def token(nick, img, wpx, pos=None, color=WHITE, h=0.5, desc=''):
    o = base('Custom_Token', nick, wpx, pos, color, False, h, desc=desc, s0=0.1)
    o['GMNotes'] = json.dumps({**json.loads(o['GMNotes']), 'd': round(wpx * aspect(img) * U, 4)})
    o['CustomImage'] = {'ImageURL': URL + img + '.png', 'ImageSecondaryURL': '', 'ImageScalar': 1.0, 'WidthScale': 0.0,
                        'CustomToken': {'Thickness': 0.2, 'MergeDistancePixels': 15.0, 'StandUp': False, 'Stackable': True}}
    return o
def bag(nick, wpx, pos, items, color, desc=''):
    o = base('Bag', nick, wpx, pos, color, False, 0.8, y3=True, desc=desc); o['MaterialIndex'] = 0; o['Bag'] = {'Order': 2}   # ordre de tirage : 0 LIFO, 1 FIFO, 2 aléatoire
    o['GMNotes'] = json.dumps({**json.loads(o['GMNotes']), 'rnd': True})
    for it in items: it['Transform'] = T(fz=it['Transform']['rotZ']); it['Locked'] = False
    random.shuffle(items); o['ContainedObjects'] = items; return o

MESH = json.load(open('meshes.json'))
def mbag(nick, mesh, tex, wpx, pos, items, color=WHITE, desc='', order=0, inf=False):
    # Sac en forme de pièce (Custom_Model_Bag) : le modèle est la pièce agrandie, l'image du jeton sur le dessus.
    o = base('Custom_Model_Infinite_Bag' if inf else 'Custom_Model_Bag', nick, wpx, pos, color, False, 0.6, y3=True, desc=desc, s0=round(wpx * U, 4))
    o['GMNotes'] = json.dumps({**json.loads(o['GMNotes']), 'd': round(wpx * MESH[mesh] * U, 4)})
    o['CustomMesh'] = {'MeshURL': URL + mesh + '.obj', 'DiffuseURL': URL + tex + '.png', 'NormalURL': '', 'ColliderURL': '', 'Convex': True,
                       'MaterialIndex': 1, 'TypeIndex': 7 if inf else 6, 'CastShadows': True}
    o['Bag'] = {'Order': order}; o['MaterialIndex'] = 1
    for it in items: it['Transform'] = T(fz=it['Transform']['rotZ']); it['Locked'] = False
    o['ContainedObjects'] = items; return o
DECK_ID = {'pers': 1, 'riv': 2, 'mat': 3, 'ev': 4, 'dem': 5, 'grand': 6, 'riv_recrue': 7, 'riv_contrat': 8, 'riv_nation': 9, 'riv_charge': 10}
DECK_NAME = {'pers': 'Associés', 'riv': 'Rivière de recrutement', 'mat': 'Matériel de départ', 'ev': 'Événements de fin de mois', 'dem': 'Demande de Paris', 'grand': 'Grands événements', 'riv_recrue': 'Recrues', 'riv_contrat': 'Contrats', 'riv_nation': 'Alliances', 'riv_charge': 'Charges'}
def cdeck(k):
    d = DK[k]; return {str(DECK_ID[k]): {'FaceURL': URL + f'deck_{k}.png', 'BackURL': URL + f'deck_{k}_back.png', 'NumWidth': d['cols'], 'NumHeight': d['rows'],
                                         'BackIsHidden': True, 'UniqueBack': False, 'Type': 0}}
def card(k, i, pos=None, up=False):
    c = base('Card', DK[k]['names'][i], SIZE['card'][0], pos, fz=0 if up else 180, s0=1.0)
    c['GMNotes'] = json.dumps({**json.loads(c['GMNotes']), 'd': round(SIZE['card'][0] * 1.4 * U, 4)})
    c['CardID'] = DECK_ID[k] * 100 + i; c['CustomDeck'] = cdeck(k)
    if not pos: c['Transform'] = T(s=1.0, fz=180); c['Locked'] = False
    return c
def deck(k, pos, skip=()):
    cards = [card(k, i) for i in range(len(DK[k]['names'])) if i not in skip]; random.shuffle(cards)
    o = base('Deck', DECK_NAME[k], SIZE['card'][0], pos, fz=180, s0=1.0)
    o['GMNotes'] = json.dumps({**json.loads(o['GMNotes']), 'd': round(SIZE['card'][0] * 1.4 * U, 4)})
    o['DeckIDs'] = [c['CardID'] for c in cards]; o['CustomDeck'] = cdeck(k); o['ContainedObjects'] = cards
    return o

OBJ = [tile('Table du castor', 'table_full', X1 - X0, P((X0 + X1) / 2, Y1 / 2), typ=0, thick=0.2, lock=True, h=0.1)]
def C(p, kind):  # centre d'une pièce de l'artefact
    w, h = SIZE[kind]; return P(p['x'] + w / 2, p['y'] + h / 2)

CREW = {'rep': ('Représentant', 'voy_rep'), 'guide': ('Guide', 'voy_guide'), 'mil': ('Milicien', 'voy_mil'), 'int': ('Interprète', 'voy_int')}
SHIPS = ['L’Aigle d’Or', 'Le Saint-Sébastien', 'Le Jardin de Hollande', 'Le Saint-Jean-Baptiste', 'Le Chat de Hollande', 'Le Vieux Siméon']
nship = 0
for p in TP['pieces']:
    if p.get('kind') in ('march', 'baril', 'grand', 'petit', 'alambic', 'pawn') and p.get('c', -1) >= 0: continue   # rangés dans les sacs du plateau du joueur
    if p.get('kind') == 'crew' or (p.get('kind') == 'disc' and p.get('c', -1) >= 0 and not p.get('track')): continue
    if p.get('kind') == 'part': continue                                          # parts : une pile à côté du plateau du joueur
    if p.get('kind') in ('baril', 'march') and p.get('c', -1) >= 0: p = {**p, 'x': p['x'] + 56}   # réserve à droite du libellé
    k = p['k']; kind = p.get('kind'); c = p.get('c', -1); color = GREY if c == -1 else PC[c]; who = '(comptoir)' if c == -1 else PN[c] if c >= 0 else ''
    if k == 'card': continue                                         # pas de mise en place : la rivière reste en paquet
    if p.get('bank'): continue                                       # comptoir : rangé dans son stock, plus bas
    elif k == 'deck':
        if p['deck'] == 'rec':                                    # rivière : un paquet par type de carte
            for kd, x, y in (('riv_recrue', 1765, 1112), ('riv_contrat', 1885, 1112), ('riv_nation', 1765, 1288), ('riv_charge', 1885, 1288)): OBJ.append(deck(kd, P(x + 50, y + 70)))
        elif p['deck'] == 'sit': OBJ.append(deck('pers', C(p, 'deck')))
        else: OBJ.append(deck({'ev': 'ev', 'dem': 'dem', 'grand': 'grand'}[p['deck']], C(p, 'deck')))
    elif k == 'bag':
        pos = C(p, 'bag')
        if p['bag'] == 'classic':
            OBJ.append(bag('Sac des Grands Lacs', 46, pos, [tile(f'Castor ×{n} (Grands Lacs)', f'tile_G{n}_sec', 30, back=f'tile_G{n}_gras', desc='Retourné côté gras (★) s’il n’est pas troqué à la fin de l’année.', face='up')
                                                        for n, m in ((1, 9), (2, 6), (3, 3)) for _ in range(m)], col('#8A6A45'), '18 paquets : 9 × 1, 6 × 2, 3 × 3'))
        elif p['bag'] == 'premium':
            OBJ.append(bag('Sac du lac Supérieur', 46, pos, [tile(f'Castor gras ×{n} (Supérieur)', f'tile_S{n}_gras', 30, back=f'tile_S{n}_gras', desc='Castor gras (★) : toutes les tuiles du lac Supérieur sont grasses.', face='up')
                                                         for n, m in ((1, 3), (2, 5), (3, 4)) for _ in range(m)], col('#8A6418'), '12 paquets : 3 × 1, 5 × 2, 4 × 3'))
        else:
            HN = {'fur1': 'Traite : 1 castor', 'fur2': 'Traite : 2 castors', 'fur3': 'Traite : 3 castors', 'mission': 'Missionnaire', 'present': 'Présent', 'fievre': 'Fièvre', 'gatees': 'Peaux gâtées'}
            OBJ.append(bag('Jetons cachés', 46, pos, [tile('', f'hid_{h}', 30, back='hid_back', fz=180, face='down') for h, m in (('fur1', 6), ('fur2', 6), ('fur3', 3), ('mission', 2), ('present', 2), ('fievre', 2), ('gatees', 2)) for _ in range(m)],
                           col('#3A2618'), '23 jetons, posés face cachée (?) sur les lacs'))
    elif k == 'die':
        d = base('Die_6', 'Dé de traversée' if p.get('cross') else 'Dé', 24, C(p, 'die'), col('#8E2F25') if p.get('cross') else WHITE, h=0.7, y3=True, s0=1.0); OBJ.append(d)
    elif k == 'tok':
        pos = C(p, kind); w = SIZE[kind][0]
        if kind in ('num', 'conge'): continue                       # pas de marqueurs de prix ; les congés viennent du sac
        if kind == 'month': OBJ.append(token('Mois', 'tok_marker', 24, pos, INKC))
        elif kind == 'year': OBJ.append(token('Année', 'tok_marker', 22, pos, INKC))
        elif kind == 'cube': OBJ.append(token('Ravages', 'tok_marker', 20, pos, col('#8E2F25')))
        elif kind == 'paris': OBJ.append(token('Prix de Paris', 'tok_marker', 20, pos, col('#C9952B')))
        elif kind == 'disc':
            if p.get('dem'): OBJ.append(token('Demande · ' + ('Grands Lacs' if p['dem'] == 'gl' else 'Supérieur'), 'tok_disc', 16, pos, INKC))
            else: OBJ.append(token(f"{ {'livres': 'Livres', 'credit': 'Crédit'}.get(p.get('track'), 'Soupçon') } {PN[c]}", 'tok_disc', 11 if p.get('track') else 18, pos, color))
        elif kind == 'march': OBJ.append(token(f'Marchandise {who}', 'tok_caisse_w', w, pos, color))
        elif kind == 'baril': OBJ.append(token(f'Eau-de-vie {who}', 'tok_bouteille_w', w, pos, color))
        elif kind == 'grand': OBJ.append(token(f'Grand canot {who}', 'canot_grand', w, pos, color))
        elif kind == 'petit': OBJ.append(token(f'Petit canot {who}', 'canot_petit', w, pos, color))
        elif kind == 'ship':
            if p.get('roi'): OBJ.append(token('Navire du roi', 'navire_roi', w, pos))
            elif p.get('merch'): OBJ.append(token('Navire marchand', 'navire_marchand', w, pos))
            else: continue                                           # les navires viennent des cartes du chantier
        elif kind == 'alambic': OBJ.append(token(f'Alambic {who}', 'alambic', w, pos, color))
        elif kind == 'part': OBJ.append(token(f'Part {who}', 'tok_disc', w, pos, color))
        elif kind == 'shipcard':
            nm = SHIPS[nship]; nship += 1
            OBJ.append(tile(f'Carte de navire · {nm}', f'carte_navire_{nship}', w, pos, typ=3, thick=0.08, desc='Financez-la au chantier ; le propriétaire la pose devant lui et envoie le navire du même nom sur le plateau.'))
            OBJ.append(token(f'Navire · {nm}', f'navire_{nship}', 40, P(p['x'] + 27, p['y'] + 37), h=0.7))
        elif kind == 'pas': OBJ.append(tile('Prendre le pas · 1er', 'tok_pas', w, pos))
        elif kind == 'crew': lab, img = CREW[p['crew']]; OBJ.append(token(lab, img, 26, pos))
        elif kind == 'pawn':
            o = base('PlayerPawn', f'Pion {who}', 18, pos, color, h=0.6, y3=True, s0=1.0); OBJ.append(o)
        else: raise SystemExit('pièce inconnue : ' + kind)

# Ajouts propres à la version actuelle du jeu, posés dans des places libres de la table
# Plateaux des joueurs : tuiles indépendantes posées sur la table, qu’on peut déplacer (les pièces posées dessus suivent)
for i in range(3): OBJ.insert(1 + i, tile(f'Plateau du joueur {PN[i]}', f'pmat_{i}', 465, P(-148 + i * 485 + 232.5, 1222 + 106), typ=3, thick=0.1, h=0.15, desc='Soupçon et personnages du joueur.'))
OBJ.append(deck('mat', P(1740 + 35, 810 + 49)))
OBJ[-1]['GMNotes'] = json.dumps({**json.loads(OBJ[-1]['GMNotes']), 'w': round(70 * U, 4), 'd': round(98 * U, 4)})
for c in OBJ[-1]['ContainedObjects']: c['GMNotes'] = json.dumps({'w': round(70 * U, 4), 'd': round(98 * U, 4)})
# Comptoir de Québec : tout son stock rangé dans sa zone (rien n'est mis en vente d'avance)
OBJ.append(mbag('Marchandises (comptoir)', 'sac_caisse', 'tok_caisse_w', 44, P(1340, 486 + 50), [token('Marchandise (comptoir)', 'tok_caisse_w', 24, None, GREY)], GREY, 'Marchandises génériques, en nombre illimité', inf=True))
OBJ.append(mbag('Eau-de-vie (comptoir)', 'sac_bouteille', 'tok_bouteille_w', 30, P(1400, 486 + 50), [token('Eau-de-vie (comptoir)', 'tok_bouteille_w', 24, None, GREY)], GREY, 'Eau-de-vie générique, en nombre illimité', inf=True))
for ci, (kc, (lab, img)) in enumerate(CREW.items()): OBJ.append(mbag(f'{lab}s', f'sac_voy_{kc}', img, 40, P(1300 + ci * 170 + 70, 680 + 48), [token(lab, img, 22) for _ in range(4)], desc=f'4 {lab.lower()}s'))
OBJ.append(token('Grand canot (comptoir)', 'canot_grand', 52, P(1326, 486 + 105), GREY)); OBJ.append(token('Petit canot (comptoir)', 'canot_petit', 40, P(1392, 486 + 105), GREY))
OBJ.append(token('Navire du roi', 'navire_roi', 40, P(1450, 486 + 105))); OBJ.append(token('Navire marchand', 'navire_marchand', 40, P(1500, 486 + 105)))
OBJ.append(bag('Sac des congés', 40, P(1760, 486 + 140), [tile(f'Congé · {n} marchandises · {c} crédit', f'conge_m{n}', 40, back='conge_back') for n, c, m in ((4, 3, 3), (3, 2, 4), (2, 1, 3)) for _ in range(m)],
               col('#8E2F25'), '10 congés : 3 à 4 marchandises (3 crédit), 4 à 3 marchandises (2 crédit), 3 à 2 marchandises (1 crédit). 4 tirés par an à 3 joueurs, remélangés chaque année. Joueur le plus pauvre : −1 crédit.'))
# Aide de jeu : une par joueur, empilées sous le matériel de départ
for k in range(3): OBJ.append(tile('Aide de jeu', 'aide_a', 430, P(1515, 1120), back='aide_b', typ=3, thick=0.05, h=0.5 + k * 0.3))
OBJ.append(mbag('Coureurs des bois', 'sac_coureur', 'tok_coureur', 34, P(1840, 626), [tile('Coureur des bois', 'tok_coureur', 40, typ=3, thick=0.1)], desc='Jetons Coureur des bois en nombre illimité : un sur la carte Expédition des coureurs, à la place du congé.', inf=True))
CANOT = {'grand': ('Grand canot', 52, 80), 'petit': ('Petit canot', 40, 62), 'coureur': ('Coureurs des bois', 32, 46)}
EXP_ID = 11
for i in range(3):
    mx = -148 + i * 485; Q = lambda x, y: P(mx + x, y); col_ = PC[i]      # y absolu : sacs à 1045, cartes à 1150, plateau dès 1222
    OBJ.append(mbag(f'Marchandises {PN[i]}', 'sac_caisse', 'tok_caisse_w', 40, Q(22, 1045), [token(f'Marchandise {PN[i]}', 'tok_caisse_w', 24, None, col_) for _ in range(8)], col_, '8 marchandises'))
    OBJ.append(mbag(f'Eau-de-vie {PN[i]}', 'sac_bouteille', 'tok_bouteille_w', 28, Q(62, 1045), [token(f'Eau-de-vie {PN[i]}', 'tok_bouteille_w', 24, None, col_) for _ in range(8)], col_, '8 bouteilles'))
    for k, (key, (lab, wp, wb)) in enumerate(CANOT.items()):
        OBJ.append(mbag(f'{lab} {PN[i]}', f'sac_canot_{key}', f'canot_{key}', wb, Q((120, 205, 270)[k], 1045), [token(f'{lab} {n} {PN[i]}', f'canot_{key}_{n}', wp, None, col_) for n in 'ABC'], col_, f'{lab} A, B et C : chacun suit sa carte Expédition.'))
    for k in range(2): OBJ.append(token(f'Alambic {PN[i]}', 'alambic', 26, Q(355 + k * 28, 1045), col_))
    OBJ.append(base('PlayerPawn', f'Pion {PN[i]}', 18, Q(412, 1045), col_, h=0.6, y3=True, s0=1.0))
    for k in range(10): OBJ.append(token(f'Part {PN[i]}', 'tok_disc', 16, Q(444, 1045), col_, h=0.5 + k * 0.3))
    OBJ.append(token(f'Soupçon {PN[i]}', 'tok_disc', 18, Q(254, 1222 + 19), col_))
    # Cartes Expédition : un tas par type (A sur le dessus), face visible, devant le joueur
    cd = {str(EXP_ID + i): {'FaceURL': URL + f'exp_{PN[i]}.png', 'BackURL': URL + f'exp_{PN[i]}_back.png', 'NumWidth': 3, 'NumHeight': 3, 'BackIsHidden': True, 'UniqueBack': False, 'Type': 0}}
    for t, (tx, tlab) in enumerate(((75, 'Grand canot'), (232.5, 'Petit canot'), (390, 'Coureur des bois'))):
        cards = []
        for j in (t, 3 + t, 6 + t):                       # A sur le dessus (premier objet du paquet), C au fond
            c = base('Card', f"{DK['exp']['names'][j]} ({PN[i]})", 150, None, s0=1.0); c['GMNotes'] = json.dumps({**json.loads(c['GMNotes']), 'd': round(107 * U, 4)})
            c['CardID'] = (EXP_ID + i) * 100 + j; c['CustomDeck'] = cd; c['SidewaysCard'] = True; c['Transform'] = T(s=1.0); c['Locked'] = False; cards.append(c)
        d = base('Deck', f'Expéditions · {tlab} ({PN[i]})', 150, Q(tx, 1150), s0=1.0); d['GMNotes'] = json.dumps({**json.loads(d['GMNotes']), 'd': round(107 * U, 4)})
        d['DeckIDs'] = [c['CardID'] for c in cards]; d['CustomDeck'] = cd; d['ContainedObjects'] = cards; d['SidewaysCard'] = True
        OBJ.append(d)
    # Main du joueur, en face de son plateau
    hp = P(mx + 232.5, 1450 + 70)
    OBJ.append({'GUID': guid(), 'Name': 'HandTrigger', 'Transform': {'posX': hp[0], 'posY': 4.0, 'posZ': hp[1], 'rotX': 0, 'rotY': 0, 'rotZ': 0, 'scaleX': round(465 * U, 3), 'scaleY': 5.0, 'scaleZ': 4.0},
                'Nickname': '', 'Description': '', 'GMNotes': json.dumps({'hand': True, 'x': hp[0], 'z': hp[1], 'hw': round(465 * U, 3)}), 'ColorDiffuse': PC[i], 'FogColor': SEAT[i], 'Locked': True})
LUA = open('setup.lua').read().replace('@W@', str((X1 - X0) * U)).replace('@D@', str(Y1 * U))
rules = open('rules.txt').read().strip().split('\n\n')
rules = [r.replace('navire avec 1 livre de dette', 'navire avec 2 de crédit') for r in rules]
intro = ("Module Tabletop Simulator reproduisant la Table du castor, 3 joueurs, sans automatisation des règles. Au premier chargement, un petit script met chaque pièce à sa taille et à sa place, puis s’arrête ; "
         "ensuite il ne fait que remettre à la bonne taille une pièce qui sort d’un sac ou d’un paquet. Les pièces grises appartiennent au comptoir de Québec. "
         "Tuiles visibles : paquets de 1 à 3 castors secs, retournés côté gras (★) s’ils ne sont pas troqués à la fin de l’année. "
         "Congés : tirés du sac, achetés à crédit, ils offrent des marchandises ; un congé ne donne pas de canot. Crédit : piste de 0 à −10. Marchandise : caisse. Eau-de-vie : bouteille.")
SAVE = {'SaveName': 'Castor et eau-de-vie', 'EpochTime': 0, 'Date': '', 'VersionNumber': 'v13.2.2', 'GameMode': 'Castor et eau-de-vie', 'GameType': '', 'GameComplexity': '', 'Tags': [],
        'Gravity': 0.5, 'PlayArea': 1.0, 'Table': 'Table_Custom', 'TableURL': URL + 'table.png', 'Sky': 'Sky_Museum', 'Note': '',
        'TabStates': {'0': {'title': 'Règles', 'body': '\n\n'.join([intro] + rules), 'color': 'Grey', 'visibleColor': {'r': 0.5, 'g': 0.5, 'b': 0.5}, 'id': 0}},
        'LuaScript': LUA, 'LuaScriptState': '', 'XmlUI': '', 'ObjectStates': OBJ}
json.dump(SAVE, open('Castor_et_eau-de-vie.json', 'w'), ensure_ascii=False, indent=1)
print(len(OBJ), 'objets')
