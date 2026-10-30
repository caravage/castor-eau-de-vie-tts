# Sauvegarde TTS fidèle à l'artefact « Table du castor » : même plateau, mêmes zones, mêmes positions de départ (3 joueurs).
import json, random
from PIL import Image
ASP = {}
def aspect(img):
    if img not in ASP: w, h = Image.open(f'img/{img}.png').size; ASP[img] = h / w
    return ASP[img]
random.seed(1670)
URL = 'https://raw.githubusercontent.com/caravage/castor-eau-de-vie-tts/main/img/v18/'
DK = json.load(open('manifest.json'))['decks']
TP = json.load(open('table_pieces.json')); SIZE = TP['SIZE']; TW, TH = TP['TW'], TP['TH']
U = 0.035                                   # 1 pixel de l'artefact = 0,035 unité de plan
X0, X1, Y0, Y1 = -178, 1253, 28, 1007                   # image exportée : plateau + rivière seulement
CX, CY = 640, 567                                       # origine du monde inchangée (pièces aux mêmes places)
def P(cx, cy): return round((cx - CX) * U, 3), round(-(cy - CY) * U, 3)
used = set()
def guid():
    while True:
        g = '%06x' % random.randrange(16 ** 6)
        if g not in used: used.add(g); return g
def col(h): h = h.lstrip('#'); return {'r': int(h[0:2], 16) / 255, 'g': int(h[2:4], 16) / 255, 'b': int(h[4:6], 16) / 255}
WHITE = col('#FFFFFF'); GREY = col('#8C877E'); INKC = col('#2A2418')
PC = [col('#A8322A'), col('#2F5E8E'), col('#4E7A2C')]; SEAT = ['Red', 'Blue', 'Green']; PN = ['rouge', 'bleu', 'vert']   # mêmes couleurs que les plateaux des joueurs

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
def token(nick, img, wpx, pos=None, color=WHITE, h=0.5, desc='', thick=0.2):
    o = base('Custom_Token', nick, wpx, pos, color, False, h, desc=desc, s0=0.1)
    o['GMNotes'] = json.dumps({**json.loads(o['GMNotes']), 'd': round(wpx * aspect(img) * U, 4)})
    o['CustomImage'] = {'ImageURL': URL + img + '.png', 'ImageSecondaryURL': '', 'ImageScalar': 1.0, 'WidthScale': 0.0,
                        'CustomToken': {'Thickness': thick, 'MergeDistancePixels': 15.0, 'StandUp': False, 'Stackable': True}}
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
                       'MaterialIndex': 3, 'TypeIndex': 7 if inf else 6, 'CastShadows': True}
    o['Bag'] = {'Order': order}; o['MaterialIndex'] = 3
    for it in items: it['Transform'] = T(fz=it['Transform']['rotZ']); it['Locked'] = False
    o['ContainedObjects'] = items; return o
def model(nick, mesh, tex, wpx, pos=None, desc=''):
    # Pièce 3D (Custom_Model), couleur cuite dans la texture
    o = base('Custom_Model', nick, wpx, pos, WHITE, False, 0.6, y3=True, desc=desc, s0=round(wpx * U, 4))
    o['GMNotes'] = json.dumps({**json.loads(o['GMNotes']), 'd': round(wpx * MESH[mesh] * U, 4)})
    o['CustomMesh'] = {'MeshURL': URL + mesh + '.obj', 'DiffuseURL': URL + tex + '.png', 'NormalURL': '', 'ColliderURL': '', 'Convex': True, 'MaterialIndex': 3, 'TypeIndex': 0, 'CastShadows': True}
    o['MaterialIndex'] = 3; return o
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

MAT_X0, MAT_X1, MAT_Y0, MAT_Y1 = -324, 1604, -331, 1458   # tapis de jeu (remplace la table TTS), au plus près des pièces
MAT_W = MAT_X1 - MAT_X0
OBJ = [tile('Tapis de jeu', 'tapis', MAT_W, P((MAT_X0 + MAT_X1) / 2, (MAT_Y0 + MAT_Y1) / 2), typ=0, thick=0.2, lock=True, h=-0.2), tile('Table du castor', 'table_full', X1 - X0, P((X0 + X1) / 2, (Y0 + Y1) / 2), typ=0, thick=0.2, lock=True, h=0.1)]
def C(p, kind):  # centre d'une pièce de l'artefact
    w, h = SIZE[kind]; return P(p['x'] + w / 2, p['y'] + h / 2)

CREW = {'guide': ('Guide', 'voy_guide'), 'mil': ('Milicien', 'voy_mil'), 'int': ('Interprète', 'voy_int')}
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
            for kd, x, y in (('riv_recrue', -270, 40), ('riv_contrat', -270, 214), ('riv_nation', -270, 388), ('riv_charge', -270, 562)): OBJ.append(deck(kd, P(x + 50, y + 70)))
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
        elif kind == 'alambic': OBJ.append(token(f'Distillerie {who}', 'alambic', w, pos, color))
        elif kind == 'part': OBJ.append(token(f'Part {who}', 'tok_disc', w, pos, color))
        elif kind == 'shipcard':
            nm = SHIPS[nship]; nship += 1
            OBJ.append(tile(f'Carte de navire · {nm}', f'carte_navire_{nship}', w, pos, typ=3, thick=0.08, desc='Financez-la au chantier ; le propriétaire la pose devant lui et envoie le navire du même nom sur le plateau.'))
            OBJ.append(token(f'Navire · {nm}', f'navire_{nship}', 34, P(p['x'] + 27, p['y'] + 37), h=0.7))
        elif kind == 'pas': OBJ.append(tile('Prendre le pas · 1er', 'tok_pas', w, pos))
        elif kind == 'crew': lab, img = CREW[p['crew']]; OBJ.append(token(lab, img, 26, pos))
        elif kind == 'pawn':
            o = base('PlayerPawn', f'Pion {who}', 18, pos, color, h=0.6, y3=True, s0=1.0); OBJ.append(o)
        else: raise SystemExit('pièce inconnue : ' + kind)

# Ajouts propres à la version actuelle du jeu, posés dans des places libres de la table
# Plateaux des joueurs : tuiles indépendantes posées sur la table, qu’on peut déplacer (les pièces posées dessus suivent)
for i in range(3): OBJ.insert(1 + i, tile(f'Plateau du joueur {PN[i]}', f'pmat_{i}', 465, P(-257 + i * 614 + 232.5, 1216 + 106), typ=3, thick=0.1, h=0.15, desc='Soupçon et personnages du joueur.'))
OBJ.append(deck('mat', P(1290 + 35, 976 + 49)))
OBJ[-1]['GMNotes'] = json.dumps({**json.loads(OBJ[-1]['GMNotes']), 'w': round(70 * U, 4), 'd': round(98 * U, 4)})
for c in OBJ[-1]['ContainedObjects']: c['GMNotes'] = json.dumps({'w': round(70 * U, 4), 'd': round(98 * U, 4)})
# Comptoir de Québec : tout son stock rangé dans sa zone (rien n'est mis en vente d'avance)
OBJ.append(mbag('Marchandises (comptoir)', 'sac_caisse', 'tok_caisse_w', 44, P(1320, 486 + 50), [token('Marchandise (comptoir)', 'tok_caisse_w', 24, None, GREY)], GREY, 'Marchandises génériques, en nombre illimité', inf=True))
OBJ.append(mbag('Eau-de-vie (comptoir)', 'sac_bouteille', 'tok_bouteille_w', 30, P(1380, 486 + 50), [token('Eau-de-vie (comptoir)', 'tok_bouteille_w', 24, None, GREY)], GREY, 'Eau-de-vie générique, en nombre illimité', inf=True))
for ci, (kc, (lab, img)) in enumerate(CREW.items()): OBJ.append(mbag(f'{lab}s', f'sac_voy_{kc}', img, 40, P(1320 + ci * 120, 680 + 48), [token(lab, img, 22) for _ in range(4)], desc=f'4 {lab.lower()}s'))
OBJ.append(token('Grand canot (comptoir)', 'canot_grand', 52, P(1316, 486 + 105), GREY)); OBJ.append(token('Petit canot (comptoir)', 'canot_petit', 40, P(1382, 486 + 105), GREY))
ROI = base('Custom_Model', 'Navire du roi', 40, P(1440, 486 + 105), WHITE, False, 0.8, y3=True, s0=1.0, desc='En rade dès avril les années I et II, 4 places publiques.')   # figurine fournie, en blanc
ROI['CustomMesh'] = {'MeshURL': 'https://steamusercontent-a.akamaihd.net/ugc/952982844368369073/FB63C915DB2529E0210C26EEDFD717929BB7E7A6/', 'DiffuseURL': '', 'NormalURL': '', 'ColliderURL': '', 'Convex': True, 'MaterialIndex': 0, 'TypeIndex': 1, 'CastShadows': True}
ROI['MaterialIndex'] = 0; OBJ.append(ROI); OBJ.append(token('Navire marchand', 'navire_marchand', 40, P(1490, 486 + 105)))
OBJ.append(bag('Sac des congés', 40, P(1610, 486 + 170), [tile(f'Congé · {n} marchandises · {c} crédit', f'conge_m{n}', 40, back='conge_back') for n, c, m in ((4, 3, 3), (3, 2, 4), (2, 1, 3)) for _ in range(m)],
               col('#8E2F25'), '10 congés : 3 à 4 marchandises (3 crédit), 4 à 3 marchandises (2 crédit), 3 à 2 marchandises (1 crédit). 4 tirés par an à 3 joueurs, remélangés chaque année. Joueur le plus pauvre : −1 crédit.'))
# Forts, missions et jetons Abîmé : réserves illimitées ; un fort aux Lacs d'en bas et une mission aux Lacs d'en haut à la mise en place
def ibag(nick, pos, item, color, desc):
    o = base('Infinite_Bag', nick, 44, pos, color, False, 0.8, y3=True, desc=desc); o['MaterialIndex'] = 0
    o['GMNotes'] = json.dumps({**json.loads(o['GMNotes']), 'ry': 0}); o['Transform']['rotY'] = 0   # contenu lisible à l'endroit
    item['Transform'] = T(); item['Locked'] = False; o['ContainedObjects'] = [item]; return o
OBJ.append(ibag('Forts français', P(1765, 560), token('Fort français', 'fort_fr', 26, thick=0.06), col('#7A5232'), 'Forts français en nombre illimité'))
OBJ.append(ibag('Forts anglais', P(1825, 560), token('Fort anglais', 'fort_uk', 26, thick=0.06), col('#012169'), 'Forts anglais en nombre illimité'))
OBJ.append(ibag('Missions', P(1765, 620), token('Mission', 'mission', 26, thick=0.06), col('#1E1A14'), 'Missions en nombre illimité'))
OBJ.append(ibag('Jetons Abîmé', P(1765, 680), token('Abîmé', 'abime', 26, thick=0.06), col('#A3352A'), 'Jetons Abîmé en nombre illimité : sur la carte Expédition du canot abîmé'))
OBJ.append(token('Fort français', 'fort_fr', 22, P(40 + 384, 178 + 380), thick=0.06))      # Lacs d'en bas (fort Frontenac, 1673)
OBJ.append(token('Mission', 'mission', 22, P(40 + 258, 178 + 300), thick=0.06))            # Lacs d'en haut (Saint-Ignace, 1671)
# Aide de jeu : une par joueur, empilées sous le matériel de départ
OBJ.append(tile('Aide de jeu (recto)', 'aide_a', 430, P(640 - 225, -146), back='aide_b', typ=3, thick=0.05)); OBJ.append(tile('Aide de jeu (verso)', 'aide_b', 430, P(640 + 225, -146), back='aide_a', typ=3, thick=0.05))   # au-dessus du plateau, côte à côte
OBJ.append(mbag('Coureurs des bois', 'sac_coureur', 'tok_coureur', 34, P(1690, 656), [tile('Coureur des bois', 'tok_coureur', 40, typ=3, thick=0.1)], desc='Jetons Coureur des bois en nombre illimité : un sur la carte Expédition des coureurs, à la place du congé.', inf=True))
CANOT = {'grand': ('Grand canot', 52, 80), 'petit': ('Petit canot', 40, round(80 * 452 / 692, 1)), 'coureur': ('Coureurs des bois', 32, round(80 * 332 / 692, 1))}   # même largeur, longueur selon les cases
EXP_ID = 11
for i in range(3):
    x0 = -269 + i * 614; mx = x0 + 12; Q = lambda x, y: P(mx + x, y); col_ = PC[i]      # zone du joueur : sacs à 1505, cartes jouées dessous, plateau dès 1662, sacs Expédition à droite
    OBJ.append(mbag(f'Marchandises {PN[i]}', 'sac_caisse', 'tok_caisse_w', 40, Q(22, 1186), [token(f'Marchandise {PN[i]}', 'tok_caisse_w', 24, None, col_) for _ in range(8)], col_, '8 marchandises'))
    OBJ.append(mbag(f'Eau-de-vie {PN[i]}', 'sac_bouteille', 'tok_bouteille_w', 28, Q(62, 1186), [token(f'Eau-de-vie {PN[i]}', 'tok_bouteille_w', 24, None, col_) for _ in range(8)], col_, '8 bouteilles'))
    for k, (key, (lab, wp, wb)) in enumerate(CANOT.items()):
        OBJ.append(mbag(f'{lab} {PN[i]}', f'canot3d_{key}', f'cn_{PN[i]}_{key}', wb, Q((120, 205, 270)[k], 1186), [model(f'{lab} {n} {PN[i]}', f'canot3d_{key}', f'cn_{PN[i]}_{key}_{n}', wb) for n in 'CBA'], WHITE, f'{lab} A, B et C : chacun suit sa carte Expédition. Sortent dans l’ordre A, B, C.'))
    OBJ.append(base('PlayerPawn', f'Pion {PN[i]}', 18, Q(372, 1186), col_, h=0.6, y3=True, s0=1.0))
    for k in range(10): OBJ.append(token(f'Part {PN[i]}', 'tok_disc', 16, Q(404, 1186), col_, h=0.5 + k * 0.3))
    OBJ.append(token(f'Soupçon {PN[i]}', 'tok_disc', 18, Q(254, 1216 + 19), col_))
    # Cartes Expédition : un tas par type (A sur le dessus), face visible, devant le joueur
    cd = {str(EXP_ID + i): {'FaceURL': URL + f'exp_{PN[i]}.png', 'BackURL': URL + f'exp_{PN[i]}_back.png', 'NumWidth': 3, 'NumHeight': 3, 'BackIsHidden': True, 'UniqueBack': False, 'Type': 0}}
    for t, (tx, key, tlab) in enumerate(((1254, 'grand', 'Grand canot'), (1322, 'petit', 'Petit canot'), (1390, 'coureur', 'Coureurs des bois'))):
        cards = []
        for j in (6 + t, 3 + t, t):                       # sortent dans l'ordre A, B, C (le dernier objet du sac sort en premier)
            c = base('Card', f"{DK['exp']['names'][j]} ({PN[i]})", 150, None, s0=1.0); c['GMNotes'] = json.dumps({**json.loads(c['GMNotes']), 'd': round(107 * U, 4), 'face': 'up'})
            c['CardID'] = (EXP_ID + i) * 100 + j; c['CustomDeck'] = cd; c['SidewaysCard'] = True; c['Transform'] = T(s=1.0); c['Locked'] = False; cards.append(c)
        OBJ.append(mbag(f'Expéditions · {tlab} ({PN[i]})', 'sac_exp', f'sacexp_{PN[i]}_{key}', 62, P(x0 + 533, tx), cards, WHITE, 'Cartes Expédition A, B, C, dans cet ordre.'))
    # Main du joueur, en face de son plateau
    hp = P(x0 + 295, 1464 + 60)
    OBJ.append({'GUID': guid(), 'Name': 'HandTrigger', 'Transform': {'posX': hp[0], 'posY': 4.0, 'posZ': hp[1], 'rotX': 0, 'rotY': 0, 'rotZ': 0, 'scaleX': round(590 * U, 3), 'scaleY': 5.0, 'scaleZ': 4.0},
                'Nickname': '', 'Description': '', 'GMNotes': json.dumps({'hand': True, 'x': hp[0], 'z': hp[1], 'hw': round(590 * U, 3)}), 'ColorDiffuse': PC[i], 'FogColor': SEAT[i], 'Locked': True})
# Disposition v20 : plateau centré sur le tapis, joueur bleu au milieu, réserve tassée autour du plateau
def place(o, cx, cy):
    n = json.loads(o['GMNotes']); n['x'] = round((cx - CX) * U, 3); n['z'] = round(-(cy - CY) * U, 3)
    o['GMNotes'] = json.dumps(n); o['Transform']['posX'] = n['x']; o['Transform']['posZ'] = n['z']
def at(o):
    n = json.loads(o['GMNotes']); return n['x'] / U + CX, -n['z'] / U + CY
SPOT = {'Recrues': (30, -226), 'Contrats': (140, -226), 'Alliances': (30, -76), 'Charges': (140, -76),
        'Associés': (1140, -226), 'Événements de fin de mois': (1250, -226), 'Demande de Paris': (1140, -76), 'Grands événements': (1250, -76),
        'Sac des Grands Lacs': (-16, 130), 'Sac du lac Supérieur': (-16, 200), 'Jetons cachés': (-16, 270), 'Sac des congés': (-16, 340),
        'Marchandises (comptoir)': (1285, 715), 'Eau-de-vie (comptoir)': (1330, 715), 'Grand canot (comptoir)': (1385, 715), 'Petit canot (comptoir)': (1445, 715),
        'Navire du roi': (1495, 715), 'Navire marchand': (1545, 715), 'Dé de traversée': (1370, 50),
        'Guides': (1290, 120), 'Miliciens': (1345, 120), 'Interprètes': (1400, 120), 'Coureurs des bois': (1460, 120),
        'Forts français': (1290, 190), 'Forts anglais': (1345, 190), 'Missions': (1400, 190), 'Jetons Abîmé': (1455, 190),
        'Matériel de départ': (1310, 628)}
MULTI = {'Dé': [(1290, 50), (1330, 50)], 'Prendre le pas · 1er': [(1440, 50), (1485, 50), (1530, 50)]}
SHIPS = [(1335, 262), (1475, 262), (1335, 332), (1475, 332), (1335, 402), (1475, 402)]
DX_JOUEURS = 640 - (-257 + 614 + 232.5)               # plateau du joueur bleu centré sous le plateau
cnt = {}; ships = []
for o in OBJ:
    if not o.get('GMNotes', '').startswith('{') or 'x' not in json.loads(o['GMNotes']): continue
    nk = o.get('Nickname', ''); x, y = at(o)
    if y > 1100 and nk != 'Tapis de jeu': place(o, x + DX_JOUEURS, y)
    elif nk in SPOT and (x > 1260 or x < -100): place(o, *SPOT[nk])
    elif nk in MULTI and x > 1260: k = cnt.get(nk, 0); cnt[nk] = k + 1; place(o, *MULTI[nk][k])
    elif nk.startswith('Carte de navire'): ships.append(o)
for k, o in enumerate(ships):
    nm = o['Nickname'].split(' · ', 1)[1]; place(o, *SHIPS[k])
    for t in OBJ:
        if t.get('Nickname') == f'Navire · {nm}': place(t, SHIPS[k][0] - 37, SHIPS[k][1] + 3)
# Distilleries : 4 cartes (4 parts chacune) et leur pion alambic cuivre, posé sur la case de la carte
DIST = [('Fonds-Saint-Jacques', 'Martinique'), ('La Lise', 'Guadeloupe'), ('Petit-Goâve', 'Saint-Domingue'), ('Saint-Louis', 'Saint-Domingue')]
for k, (nm, ile) in enumerate(DIST):
    x, y = (1335, 1475)[k % 2], 472 + (k // 2) * 70
    OBJ.append(tile(f'Carte de distillerie · {nm}', f'carte_distillerie_{k+1}', 120, P(x, y), typ=3, thick=0.08, desc=f'{ile}. Construite à 4 parts ; chaque part produit 1 eau-de-vie.'))
    OBJ.append(token(f'Distillerie · {nm}', f'pion_distillerie_{k+1}', 22, P(x - 37, y + 3), h=0.7, desc=f'Distillerie de {nm} ({ile})'))
LUA = open('setup.lua').read().replace('@W@', str(round(2 * max(CX - MAT_X0, MAT_X1 - CX) * U, 3))).replace('@D@', str(round(2 * max(CY - MAT_Y0, MAT_Y1 - CY) * U, 3)))
rules = open('rules.txt').read().strip().split('\n\n')
rules = [r.replace('navire avec 1 livre de dette', 'navire avec 2 de crédit') for r in rules]
intro = ("Module Tabletop Simulator reproduisant la Table du castor, 3 joueurs, sans automatisation des règles. Au premier chargement, un petit script met chaque pièce à sa taille et à sa place, puis s’arrête ; "
         "ensuite il ne fait que remettre à la bonne taille une pièce qui sort d’un sac ou d’un paquet. Les pièces grises appartiennent au comptoir de Québec. "
         "Tuiles visibles : paquets de 1 à 3 castors secs, retournés côté gras (★) s’ils ne sont pas troqués à la fin de l’année. "
         "Congés : tirés du sac, achetés à crédit, ils offrent des marchandises ; un congé ne donne pas de canot. Crédit : piste de 0 à −10. Marchandise : caisse. Eau-de-vie : bouteille.")
SAVE = {'SaveName': 'Castor et eau-de-vie', 'EpochTime': 0, 'Date': '', 'VersionNumber': 'v13.2.2', 'GameMode': 'Castor et eau-de-vie', 'GameType': '', 'GameComplexity': '', 'Tags': [],
        'Gravity': 0.5, 'PlayArea': 1.0, 'Table': 'Table_None', 'TableURL': '', 'Sky': 'Sky_Museum', 'Note': '',
        'TabStates': {'0': {'title': 'Règles', 'body': '\n\n'.join([intro] + rules), 'color': 'Grey', 'visibleColor': {'r': 0.5, 'g': 0.5, 'b': 0.5}, 'id': 0}},
        'LuaScript': LUA, 'LuaScriptState': '', 'XmlUI': '', 'ObjectStates': OBJ}
open('Castor_et_eau-de-vie.json', 'w').write(json.dumps(SAVE, ensure_ascii=False, indent=1).replace('.png"', '.png?v21"'))   # ?v21 : force TTS à recharger les images
print(len(OBJ), 'objets')
