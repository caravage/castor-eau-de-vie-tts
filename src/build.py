# Construit la sauvegarde Tabletop Simulator : Castor et eau-de-vie (3 joueurs, sans automatisation)
import json, random
from PIL import Image
random.seed(1670)
URL = 'https://raw.githubusercontent.com/caravage/castor-eau-de-vie-tts/main/img/'
M = json.load(open('manifest.json')); DK = M['decks']
used = set()
def guid():
    while True:
        g = '%06x' % random.randrange(16 ** 6)
        if g not in used: used.add(g); return g
def size(n): return Image.open(f'img/{n}.png').size
def col(h): h = h.lstrip('#'); return {'r': int(h[0:2], 16) / 255, 'g': int(h[2:4], 16) / 255, 'b': int(h[4:6], 16) / 255}
WHITE = col('#FFFFFF'); GREY = col('#9A948A'); INKC = col('#2A2418')
PLAYERS = [('rouge', 'Red', col('#C0392B')), ('bleu', 'Blue', col('#2F6FB0')), ('vert', 'Green', col('#4E8A2C'))]

def T(x, z, y=1.0, s=1.0, rot=180):
    return {'posX': x, 'posY': y, 'posZ': z, 'rotX': 0, 'rotY': rot, 'rotZ': 0, 'scaleX': s, 'scaleY': 1.0, 'scaleZ': s}
def base(name, nick, x, z, s=1.0, y=1.0, color=WHITE, locked=False, desc=''):
    return {'GUID': guid(), 'Name': name, 'Transform': T(x, z, y, s), 'Nickname': nick, 'Description': desc, 'ColorDiffuse': color,
            'Locked': locked, 'Grid': not locked and False, 'Snap': True, 'Tooltip': True, 'HideWhenFaceDown': False, 'Hands': False}
# Largeur voulue en unités de table -> échelle (une tuile d'échelle 1 fait environ 2 unités de large)
def tile(nick, front, x, z, w, back=None, typ=0, thick=0.1, stack=False, color=WHITE, locked=False, y=1.0, desc=''):
    o = base('Custom_Tile', nick, x, z, w / 2, y, color, locked, desc)
    o['CustomImage'] = {'ImageURL': URL + front + '.png', 'ImageSecondaryURL': URL + (back or front) + '.png', 'ImageScalar': 1.0, 'WidthScale': 0.0,
                        'CustomTile': {'Type': typ, 'Thickness': thick, 'Stackable': stack, 'Stretch': False}}
    return o
def token(nick, img, x, z, w, color=WHITE, y=1.2, desc='', thick=0.2):
    o = base('Custom_Token', nick, x, z, w / 2, y, color, False, desc)
    o['CustomImage'] = {'ImageURL': URL + img + '.png', 'ImageSecondaryURL': '', 'ImageScalar': 1.0, 'WidthScale': 0.0,
                        'CustomToken': {'Thickness': thick, 'MergeDistancePixels': 15.0, 'StandUp': False, 'Stackable': True}}
    return o
def bag(nick, x, z, items, color=col('#8A6A45'), desc=''):
    o = base('Bag', nick, x, z, 1.0, 1.5, color, False, desc); o['MaterialIndex'] = 0
    for it in items: it['Transform'] = T(0, 0, 0)
    random.shuffle(items); o['ContainedObjects'] = items; return o
def infinite(nick, x, z, proto, color=col('#6B5F45')):
    o = base('Infinite_Bag', nick, x, z, 1.0, 1.5, color); proto['Transform'] = T(0, 0, 0); o['ContainedObjects'] = [proto]; return o

DECK_ID = {'pers': 1, 'riv': 2, 'mat': 3, 'ev': 4, 'dem': 5, 'grand': 6}
DECK_NAME = {'pers': 'Associés', 'riv': 'Rivière de recrutement', 'mat': 'Matériel de départ', 'ev': 'Événements de fin de mois', 'dem': 'Demande de Paris', 'grand': 'Grands événements'}
CARD_S = 1.0
def deck(k, x, z, rot=180):
    d = DK[k]; did = DECK_ID[k]
    cd = {str(did): {'FaceURL': URL + f'deck_{k}.png', 'BackURL': URL + f'deck_{k}_back.png', 'NumWidth': d['cols'], 'NumHeight': d['rows'],
                     'BackIsHidden': True, 'UniqueBack': False, 'Type': 0}}
    cards = []
    for i, nm in enumerate(d['names']):
        c = base('Card', nm, 0, 0, CARD_S); c['CardID'] = did * 100 + i; c['CustomDeck'] = cd; c['Transform'] = T(0, 0, 0, CARD_S); cards.append(c)
    random.shuffle(cards)
    o = base('Deck', DECK_NAME[k], x, z, CARD_S, 1.2); o['Transform']['rotZ'] = 180  # face cachée
    o['DeckIDs'] = [c['CardID'] for c in cards]; o['CustomDeck'] = cd; o['ContainedObjects'] = cards; o['Hands'] = False
    return o

OBJ = []
# ---------------- Plateaux (verrouillés)
BOARD_W = 40; BX, BZ = -14, 8
OBJ.append(tile('Plateau', 'plateau', BX, BZ, BOARD_W, locked=True, thick=0.2, y=0.9))
RW = 30.7; RX, RZ = 27, 8; rw, rh = size('reserve'); RK = RW / rw
OBJ.append(tile('Réserve générale', 'reserve', RX, RZ, RW, locked=True, thick=0.2, y=0.9))
def R(px, py): return RX + (px - rw / 2) * RK, RZ - (py - rh / 2) * RK
MW = 18; MZ = -21
for i, (nm, seat, c) in enumerate(PLAYERS):
    OBJ.append(tile(f'Plateau du marchand {nm}', f'mat_{nm}', -33 + i * 19.5, MZ, MW, locked=True, thick=0.2, y=0.9))

# ---------------- Paquets
OBJ.append(deck('riv', *R(215, 420)))
OBJ.append(deck('ev', *R(255, 1745)))
OBJ.append(deck('dem', *R(1155, 1745)))
OBJ.append(deck('grand', *R(1605, 1745)))
OBJ.append(deck('pers', 16, -10))
OBJ.append(deck('mat', 19.5, -10))

# ---------------- Sacs de tuiles
def castor(tag, n, sup):
    lab = ('Supérieur' if sup else 'Grands Lacs')
    return tile(f'Castor ×{n} ({lab})', f'tile_{tag}{n}_sec', 0, 0, 1.0, back=f'tile_{tag}{n}_gras', typ=3, stack=False,
                desc=f'Paquet de {n} castor sec. Retourné côté gras (★) s’il n’est pas troqué à la fin de l’année.')
gl = [castor('G', n, False) for n, k in ((1, 9), (2, 6), (3, 3)) for _ in range(k)]
sp = [castor('S', n, True) for n, k in ((1, 3), (2, 5), (3, 4)) for _ in range(k)]
OBJ.append(bag('Sac des Grands Lacs (tuiles visibles)', 24, -6, gl, col('#8A6A45'), '18 paquets : 9 × 1, 6 × 2, 3 × 3'))
OBJ.append(bag('Sac du lac Supérieur (tuiles visibles)', 27, -6, sp, col('#8A6418'), '12 paquets : 3 × 1, 5 × 2, 4 × 3'))
HN = {'fur1': 'Traite : 1 castor', 'fur2': 'Traite : 2 castors', 'fur3': 'Traite : 3 castors', 'mission': 'Missionnaire', 'present': 'Présent', 'fievre': 'Fièvre', 'gatees': 'Peaux gâtées'}
hid = [tile(HN[k], f'hid_{k}', 0, 0, 1.0, back='hid_back', typ=3) for k, n in (('fur1', 6), ('fur2', 6), ('fur3', 3), ('mission', 2), ('present', 2), ('fievre', 2), ('gatees', 2)) for _ in range(n)]
for h in hid: h['Transform']['rotZ'] = 180
OBJ.append(bag('Jetons cachés (tous les lacs)', 30, -6, hid, col('#3A2618'), '23 jetons, posés face cachée (?)'))
cg = [tile(f'Congé · {n} voyageur' + ('s' if n > 1 else ''), f'conge_{n}', 0, 0, 1.4, back='conge_back', typ=3) for n, k in ((1, 6), (2, 4), (0, 2)) for _ in range(k)]
OBJ.append(bag('Sac des congés', *R(3240, 500), cg, col('#8E2F25'), '12 congés : 6 à 1 place, 4 à 2 places, 2 sans place'))

# ---------------- Réserve commune
for k, (lab, img) in enumerate([('Représentant', 'voy_rep'), ('Guide', 'voy_guide'), ('Milicien', 'voy_mil'), ('Interprète', 'voy_int')]):
    OBJ.append(infinite(f'{lab}s', *R(2165 + k * 380, 1720), token(lab, img, 0, 0, 0.9)))
OBJ.append(infinite('Marchandises du comptoir (gris)', *R(2355, 1010), token('Marchandise (comptoir)', 'tok_caisse_w', 0, 0, 0.7, GREY)))
OBJ.append(infinite('Eau-de-vie du comptoir (gris)', *R(3115, 1010), token('Eau-de-vie (comptoir)', 'tok_bouteille_w', 0, 0, 0.7, GREY)))
OBJ.append(token('Grand canot du comptoir', 'canot_grand', *R(2355, 1270), 2.4, GREY))
OBJ.append(token('Petit canot du comptoir', 'canot_petit', *R(3115, 1270), 1.6, GREY))
OBJ.append(infinite('Peaux à l’unité', 33, -6, tile('Peau', 'tok_peau_sec', 0, 0, 0.7, back='tok_peau_gras', typ=2, stack=True)))
for k in range(6):
    x, z = R(400 + (k % 3) * 600, 1015 + (k // 3) * 250)
    OBJ.append(tile('Carte de navire', 'carte_navire', x, z, 4.6, typ=3, thick=0.08))
OBJ.append(token('Navire du roi', 'navire_roi', BX + 8, BZ + 8, 2.0))
OBJ.append(token('Navire marchand', 'navire_marchand', BX + 11, BZ + 8, 2.0))
for k in range(3): OBJ.append(tile('Prendre le pas · 1er', 'tok_pas', 36 + k * 1.8, -10, 1.3, typ=3))
for j, (lab, c) in enumerate((('Mois', INKC), ('Année', INKC), ('Ravages', col('#8E2F25')), ('Prix de Paris', col('#C9952B')), ('Demande · Grands Lacs', INKC), ('Demande · Supérieur', INKC))):
    OBJ.append(token(lab, 'tok_marker' if lab not in ('Demande · Grands Lacs', 'Demande · Supérieur') else 'tok_disc', BX - 22, BZ + 14 - j * 1.6, 0.7, c))
for k, (lab, c) in enumerate((('Dé', WHITE), ('Dé', WHITE), ('Dé de traversée', col('#8E2F25')))):
    d = base('Die_6', lab, 23 + k * 1.5, -10, 1.0, 1.5, c); d['RotationValues'] = []; OBJ.append(d)

# ---------------- Pièces des joueurs (teintées)
for i, (nm, seat, c) in enumerate(PLAYERS):
    mx = -33 + i * 19.5; z0 = MZ - 9
    OBJ.append(infinite(f'Marchandises {nm}', mx - 7, z0, token(f'Marchandise {nm}', 'tok_caisse_w', 0, 0, 0.7, c), c))
    OBJ.append(infinite(f'Eau-de-vie {nm}', mx - 5, z0, token(f'Eau-de-vie {nm}', 'tok_bouteille_w', 0, 0, 0.7, c), c))
    OBJ.append(infinite(f'Disques de parts {nm}', mx - 3, z0, token(f'Part {nm}', 'tok_disc', 0, 0, 0.6, c), c))
    for k, lab in enumerate(['Livres', 'Livres +20', 'Dette', 'Soupçon']):
        OBJ.append(token(f'{lab} {nm}', 'tok_marker', mx - 1 + k * 0.9, z0, 0.6, c))
    for k, (lab, img, w) in enumerate([('Grand canot', 'canot_grand', 2.4), ('Grand canot', 'canot_grand', 2.4), ('Petit canot', 'canot_petit', 1.6), ('Petit canot', 'canot_petit', 1.6),
                                         ('Canot de coureur des bois', 'canot_coureur', 1.2), ('Canot de coureur des bois', 'canot_coureur', 1.2)]):
        OBJ.append(token(f'{lab} {nm}', img, mx + 3.5 + (k // 2) * 2.6, z0 + 1.2 - (k % 2) * 1.6, w, c))
    for k in range(2): OBJ.append(token(f'Navire {nm}', 'navire', mx - 6 + k * 2.2, z0 - 2.2, 2.0, c))
    for k in range(2): OBJ.append(token(f'Alambic {nm}', 'alambic', mx - 1.5 + k * 1.4, z0 - 2.2, 1.0, c))

# ---------------- Carnet : règles
rules = open('rules.txt').read().strip().split('\n\n')
rules = [r.replace('navire avec 1 livre de dette', 'navire avec 2 livres de dette') for r in rules]
setup = ("Module Tabletop Simulator (3 joueurs, sans automatisation). Argent et dette se suivent sur les pistes de votre plateau de marchand : "
         "Livres 0 à 19 (au-delà, un 2ᵉ marqueur sur la piste vaut 20) et Dette envers La Rochelle 0 à 9. Payez toujours avant d’agir ; s’il manque de l’argent, la dette monte. "
         "Tuiles visibles : paquets de 1 à 3 castors secs, tirés du sac de la zone (Grands Lacs ou Supérieur), retournés côté gras (★) s’ils ne sont pas troqués à la fin de l’année. "
         "Congés : joueurs moins 1 par an, tirés du sac des congés ; chaque place accueille un voyageur au choix (représentant 2 livres ; guide, milicien, interprète 1 livre). Un congé ne donne pas de canot. "
         "Marchandise : une caisse. Eau-de-vie : une bouteille. Les pièces grises appartiennent au comptoir de Québec.")
body = '\n\n'.join([setup] + rules)
SAVE = {'SaveName': 'Castor et eau-de-vie', 'EpochTime': 0, 'Date': '', 'VersionNumber': 'v13.2.2', 'GameMode': 'Castor et eau-de-vie', 'GameType': '', 'GameComplexity': '',
        'Tags': [], 'Gravity': 0.5, 'PlayArea': 0.75, 'Table': 'Table_Glass', 'Sky': 'Sky_Museum', 'Note': '', 'TabStates': {
            '0': {'title': 'Règles', 'body': body, 'color': 'Grey', 'visibleColor': {'r': 0.5, 'g': 0.5, 'b': 0.5}, 'id': 0}},
        'Grid': {'Type': 0, 'Lines': False, 'Color': {'r': 0, 'g': 0, 'b': 0}, 'Opacity': 0.75, 'ThickLines': False, 'Snapping': False, 'Offset': False, 'BothSnapping': False,
                 'xSize': 2.0, 'ySize': 2.0, 'PosOffset': {'x': 0, 'y': 1, 'z': 0}},
        'LuaScript': '', 'LuaScriptState': '', 'XmlUI': '', 'ObjectStates': OBJ}
json.dump(SAVE, open('Castor_et_eau-de-vie.json', 'w'), ensure_ascii=False, indent=1)
print(len(OBJ), 'objets')
