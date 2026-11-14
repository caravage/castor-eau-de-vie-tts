# v3.40 : sacs « Interprètes » (+1 dé au troc, 2 ₶) et « Miliciens » (6 jetons voy2_milicien, recto ×2 au combat, verso Utilisé), même gabarit que Guides / Pilotes / Forgerons.
# Sacs de pions du haut à droite resserrés (pas 1,6) pour laisser place aux Miliciens après les Forgerons.
import json, copy, random, sys
R = sys.argv[1] if len(sys.argv) > 1 else './'
P = R + 'Castor_et_eau-de-vie.json'; d = json.load(open(P)); O = d['ObjectStates']
GH = 'https://raw.githubusercontent.com/caravage/castor-eau-de-vie-tts/main/img/v18/'
EFF = 'Compte pour 2 voyageurs dans les jets de combat (défense du canot, trafic). 1 ₶.'
used = set()
def walk(os_):
    for o in os_:
        used.add(o.get('GUID')); walk(o.get('ContainedObjects', []))
walk(O)
def guid():
    while True:
        g = '%06x' % random.randrange(16 ** 6)
        if g not in used: used.add(g); return g
src = [o for o in O if o.get('Nickname') == 'Forgerons'][0]
def sac(nom, un, cle, eff):
    assert not any(o.get('Nickname') == nom for o in O)
    bag = copy.deepcopy(src); bag['GUID'] = guid(); bag['Nickname'] = nom; bag['Description'] = f'6 {nom.lower()}. ' + eff
    bag['CustomMesh'].update(MeshURL=GH + f'sac_voy2_{cle}.obj', DiffuseURL=GH + f'voy2_{cle}.png')
    for t in bag['ContainedObjects']:
        t['GUID'] = guid(); t['Nickname'] = un; t['Description'] = eff
        t['CustomImage'].update(ImageURL=GH + f'voy2_{cle}.png', ImageSecondaryURL=GH + f'voy2_{cle}_used.png')
    O.insert(O.index(src) + 1, bag); print(nom, bag['GUID'])
sac('Miliciens', 'Milicien', 'milicien', EFF)
sac('Interprètes', 'Interprète', 'interprete', '+1 dé au troc. 2 ₶.')
note = lambda n: json.dumps(n, ensure_ascii=False, separators=(', ', ': '))
for k, nom in enumerate(('Guides', 'Pilotes', 'Forgerons', 'Interprètes', 'Miliciens', 'Coureurs des bois', 'Zones fermées')):
    o = [q for q in O if q.get('Nickname') == nom][0]; x = round(17.0 + 1.5 * k, 3)
    n = json.loads(o['GMNotes']); n.update(x=x); o['GMNotes'] = note(n); o['Transform']['posX'] = x
json.dump(d, open(P, 'w'), ensure_ascii=False, indent=2)
print('objets', len(O))
# Guide : +1 au raccourci et aux traversées, 2 ₶ (décision du 14 nov.)
d = json.load(open(P)); O = d['ObjectStates']
g = [o for o in O if o.get('Nickname') == 'Guides'][0]
EG = '+1 au jet de raccourci et aux traversées. 2 ₶.'
g['Description'] = '6 guides. ' + EG
for t in g['ContainedObjects']: t['Description'] = EG
json.dump(d, open(P, 'w'), ensure_ascii=False, indent=2)
# Plateau v3.40 : légende des rapides élargie, « Raccourci 3+ — 1 : abîmé et reste sur place » (src/plateau_hd/build_map_html.py).
# Image obtenue en posant la nouvelle légende (rendue depuis over.html) sur table_v3_39_hd.png, seul élément changé.
d = json.load(open(P)); O = d['ObjectStates']
t = [o for o in O if o.get('Nickname') == 'Table du castor'][0]
t['CustomImage'].update(ImageURL=GH + 'table_v3_40_hd.jpg', ImageSecondaryURL=GH + 'table_v3_40_hd.jpg')
json.dump(d, open(P, 'w'), ensure_ascii=False, indent=2)
# Aide de jeu v3.40 : recto = canevas « Plaquette des actions » (src/aide_actions/plaquette_actions.html, rendu ×2, 3200 × 2494),
# verso Printemps / Hiver inchangé, recadré au même format (bandes blanches) pour que les deux faces aient la même proportion.
d = json.load(open(P)); O = d['ObjectStates']
A, B = GH + 'aide_a_v40.png', GH + 'aide_b_v40.png'
for nom, im1, im2 in (('Aide de jeu (recto)', A, B), ('Aide de jeu (verso)', B, A)):
    o = [q for q in O if q.get('Nickname') == nom][0]
    o['CustomImage'].update(ImageURL=im1, ImageSecondaryURL=im2)
    n = json.loads(o['GMNotes']); n['d'] = round(15.05 * 1247 / 1600, 4); o['GMNotes'] = note(n)
json.dump(d, open(P, 'w'), ensure_ascii=False, indent=2)
