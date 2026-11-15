# v3.45 : aperçu couché des Grands événements ; marqueur Raid (sac infini) ; sacs de marqueurs regroupés par forme à droite du plateau ;
# dés des zones et dé sec / gras à la taille d'un dé normal ; points d'accroche recalculés sur le plateau HD ;
# canots gris du comptoir et figurine « Navire du roi » retirés.
import json, sys, random, re
R = sys.argv[1] if len(sys.argv) > 1 else './'
P = R + 'Castor_et_eau-de-vie.json'; d = json.load(open(P)); O = d['ObjectStates']
GH = 'https://raw.githubusercontent.com/caravage/castor-eau-de-vie-tts/main/img/v18/'
cp = lambda o: json.loads(json.dumps(o)); gid = lambda: ''.join(random.choice('0123456789abcdef') for _ in range(6))
get = lambda nom: [o for o in O if o.get('Nickname') == nom][0]
def place(o, x, z):
    n = json.loads(o['GMNotes']); n.update(x=x, z=z); o['GMNotes'] = json.dumps(n); o['Transform'].update(posX=x, posZ=z)
# 1. cartes couchées : aperçu horizontal
get('Grands événements')['SidewaysCard'] = True
# 2. marqueur Raid
zf = get('Zones fermées'); r = cp(zf); r['GUID'] = gid(); r['Nickname'] = 'Raids'
r['Description'] = 'Marqueurs Raid en nombre illimité : posés sur la zone frappée par un raid iroquois.'
r['CustomMesh'].update(MeshURL=GH + 'sac_raid.obj', DiffuseURL=GH + 'raid.png')
t = r['ContainedObjects'][0]; t['GUID'] = gid(); t['Nickname'] = 'Raid'; t['Description'] = 'Raid iroquois.'
for k in ('ImageURL', 'ImageSecondaryURL'):
    if t['CustomImage'].get(k): t['CustomImage'][k] = GH + 'raid.png'
O.append(r)
# 3. sacs de marqueurs regroupés par forme, à droite du plateau (hexagones et ronds en haut, carrés en bas)
for nom, x, z in (('Forts français', 27.7, 21.8), ('Forts anglais', 29.1, 21.8), ('Missions', 30.5, 21.8), ('Jetons Abîmé', 32.3, 21.8), ('Milice', 33.9, 21.8),
                  ('Marqueurs Ravagé', 27.7, 20.36), ('Raids', 29.1, 20.36), ('Zones fermées', 30.5, 20.36), ('Zones détruites', 31.9, 20.36)):
    place(get(nom), x, z)
# 4. dés personnalisés à la taille d'un dé normal (0,84)
for nom in ('Dé des zones', 'Dé sec / gras'):
    o = get(nom); n = json.loads(o['GMNotes']); n['w'] = 0.84; o['GMNotes'] = json.dumps(n)
# 5. points d'accroche recalculés depuis les sources du plateau HD (board.html, over.html) : Ravages, Prix du castor, Tour, rade, La Rochelle, Montréal, partis
S, F = 8000 / 5600, 2.490857; BX, BZ, BW, BD = -2.96, 6.721, 59.558, 43.961
tab = lambda px, py: (round(BX + (px / 8000 - 0.5) * BW, 3), round(BZ + (0.5 - py / 5904) * BD, 3))
bc = lambda x, y: tab(x * S, y * S); mc = lambda X, Y: tab(716 * S + X * F, 944 * S - 8 * F + Y * F)
rc = json.load(open(R + 'src/plateau_hd/rects_snap.json'))
pts = [bc(1833 + 108.7 * i, 785) for i in range(7)] + [bc(3694 + 108.6 * i, 785) for i in range(8)] + [bc(1405 + 123.4 * i, 111.5) for i in range(8)]
pts += [mc(c[0], c[1]) for c in sorted(rc['rade'], key=lambda c: (round(c[1]), c[0]))]
pts += [mc(c[0], c[1]) for c in sorted(rc['lr'], key=lambda c: (round(c[1]), c[0]))]
pts += [mc(c[0], c[1]) for c in sorted(rc['oval'])] + [mc(c[0], c[1]) for c in sorted(rc['ring'])]
L = d['LuaScript']; i = L.index('local SNAP = ') + len('local SNAP = '); j = L.index('}}', i) + 2
d['LuaScript'] = L[:i] + '{' + ','.join('{%s,%s}' % p for p in pts) + '}' + L[j:]
# 6. tuiles de navire v45 : navires des joueurs à 4 états (neutre, rouge, bleu, vert) ; la Compagnie ; Le Profond
NAV = ["L’Aigle d’Or", "Le Courageux", "Le Jardin de Hollande", "Le Saint-Jean-Baptiste", "La Famille", "Le Vieux Siméon"]
ETATS = ('neutre', 'rouge', 'bleu', 'vert')
def img(o, f):
    o['CustomImage'].update(ImageURL=GH + f, ImageSecondaryURL=GH + f)
for k, nom in enumerate(NAV):
    o = get('Navire · ' + nom); img(o, f'navire45_{k+1}_neutre.png'); o.pop('States', None)
    o['Description'] = 'Changer d’état (touches 1 à 4) : neutre, rouge, bleu, vert, selon le premier armateur.'
    st = {}
    for i, e in enumerate(ETATS[1:], start=2):
        c = cp(o); c['GUID'] = gid(); img(c, f'navire45_{k+1}_{e}.png'); st[str(i)] = c
    o['States'] = st
img(get('Navire de la compagnie'), 'navire45_compagnie.png'); img(get('Le Profond (navire du roi)'), 'navire45_profond.png')
# 7. objets retirés
d['ObjectStates'] = [o for o in O if o.get('Nickname') not in ('Grand canot (comptoir)', 'Moyen canot (comptoir)', 'Navire du roi')]
json.dump(d, open(P, 'w'), ensure_ascii=False, indent=2); print('v3.45 :', len(pts), 'points d’accroche')
