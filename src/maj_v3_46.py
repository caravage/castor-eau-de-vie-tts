# v3.46 : sac « Raids iroquois » (3 tuiles, tirage au hasard face cachée ; retirées du sac Événements) ; compteur « Force iroquoise » dans la baie d'Hudson ;
# 10 Rivière calme (au lieu de 15) ; Force iroquoise sur 1 ; 2 marqueurs Frasil (Grand Hiver) ; tuile Baie d'Hudson evt8 (symbole de Région du lac Supérieur) ; Prix du castor sur 3 ; pions Ravages, Prix et Année
# sur les points d'accroche ; symboles de raid sur les cartes de la Rivière (deck_riv_v46) ; essai : Grands événements sans SidewaysCard.
import json, sys, random
R = sys.argv[1] if len(sys.argv) > 1 else './'
P = R + 'Castor_et_eau-de-vie.json'; d = json.load(open(P)); O = d['ObjectStates']
GH = 'https://raw.githubusercontent.com/caravage/castor-eau-de-vie-tts/main/img/v18/'
cp = lambda o: json.loads(json.dumps(o)); gid = lambda: ''.join(random.choice('0123456789abcdef') for _ in range(6))
get = lambda nom: [o for o in O if o.get('Nickname') == nom][0]
def place(o, x, z):
    n = json.loads(o['GMNotes']); n.update(x=x, z=z); o['GMNotes'] = json.dumps(n); o['Transform'].update(posX=x, posZ=z)
def walk(os_, f):
    for o in os_: f(o); walk(o.get('ContainedObjects', []), f)
HUD = "Région du lac Supérieur : on retire une peau de chaque zone de traite sans fort. ↻ avec flocon : retour au sac à l'hiver."
def maj(o):
    ci = o.get('CustomImage', {})
    if ci.get('ImageURL', '').endswith('evt7_hudson.png'): ci['ImageURL'] = GH + 'evt8_hudson.png'; o['Description'] = HUD
    cd = o.get('CustomDeck', {})
    for k, v in cd.items():
        if 'deck_riv.png' in v.get('FaceURL', ''): v['FaceURL'] = GH + 'deck_riv_v46.png'
walk(O, maj)
for nom in ('Aide de jeu (recto)', 'Aide de jeu (verso)'):
    ci = get(nom)['CustomImage']
    for k in ('ImageURL', 'ImageSecondaryURL'): ci[k] = ci[k].replace('aide_b_v43.png', 'aide_b_v46.png')
# 1. Raids : les 3 tuiles quittent le sac Événements pour un sac « Raids iroquois » (tirage au hasard, face cachée)
ev = get('Événements du mois')
raids = [c for c in ev['ContainedObjects'] if c.get('Nickname') == 'Raid iroquois']; assert len(raids) == 3
ev['ContainedObjects'] = [c for c in ev['ContainedObjects'] if c.get('Nickname') != 'Raid iroquois']
ev['Description'] = "Piochez une tuile à la fin de chaque mois. Mise en place : ajoutez-y 1 tuile du sac Raids iroquois, sans la regarder."
for c in raids: c['GMNotes'] = json.dumps({'w': 1.05, 'd': 1.05, 'face': 'down'})
sr = get('Sac Ravage'); rb = cp(sr); rb['GUID'] = gid(); rb['Nickname'] = 'Raids iroquois'
rb['Description'] = "3 tuiles Raid iroquois, tirées au hasard et face cachée : 1 entre dans le sac Événements à la mise en place, la 2e quand la Force iroquoise atteint 3, la 3e quand elle atteint 5."
rb['ColorDiffuse'] = {'r': 0.31, 'g': 0.17, 'b': 0.48}; rb['ContainedObjects'] = raids
rb['GMNotes'] = json.dumps({'w': 1.4, 'x': 22.35, 'z': 30.35, 'h': 0.8, 'y3': True, 'rnd': True, 'lock': True, 'drop': True}); rb['Transform'].update(posX=22.35, posZ=30.35)
O.append(rb)
place(get('Réserve Épidémie'), 18.5, 30.35)
# 1b. Occasion plus fréquente (≈ 5 par partie) : 10 Rivière calme au lieu de 15
calmes = [c for c in ev['ContainedObjects'] if c.get('Nickname') == 'Rivière calme']; assert len(calmes) == 15
for c in calmes[10:]: ev['ContainedObjects'].remove(c)
# 2. Frasil : 2 marqueurs (Grand Hiver)
zf = get('Zones fermées')['ContainedObjects'][0]
for k, x in enumerate((19.75, 20.9)):
    t = cp(zf); t['GUID'] = gid(); t['Nickname'] = 'Frasil'; t['Description'] = 'Grand Hiver : posez ce marqueur sur le mois qui devient un mois de frasil.'
    t['CustomImage'].update(ImageURL=GH + 'frasil.png', ImageSecondaryURL=GH + 'frasil.png')
    t['GMNotes'] = json.dumps({'w': 1.0, 'd': 1.0, 'x': x, 'z': 30.35, 'h': 0.5}); t['Transform'].update(posX=x, posY=2.0, posZ=30.35); t['Locked'] = False
    O.append(t)
# 3. compteur Force iroquoise, dans la baie d'Hudson (sous le nom de la baie)
S, F = 8000 / 5600, 2.490857; BX, BZ, BW, BD = -2.96, 6.721, 59.558, 43.961
fx, fz = round(BX + (4390 / 8000 - 0.5) * BW, 3), round(BZ + (0.5 - 1600 / 5904) * BD, 3)
cnt = {'GUID': gid(), 'Name': 'Counter', 'Transform': {'posX': fx, 'posY': 2.0, 'posZ': fz, 'rotX': 0, 'rotY': 180, 'rotZ': 0, 'scaleX': 1.0, 'scaleY': 1.0, 'scaleZ': 1.0},
       'Nickname': 'Force iroquoise', 'Description': 'Force iroquoise (0 à 6, départ 1) : force des raids. Monte avec les peaux parties chez les Anglais (Hudson, Albany).',
       'GMNotes': json.dumps({'w': 1.6, 'x': fx, 'z': fz, 'h': 0.4, 'y3': True, 'lock': True}), 'ColorDiffuse': {'r': 0.31, 'g': 0.17, 'b': 0.48},
       'Locked': True, 'Grid': False, 'Snap': False, 'Tooltip': True, 'Hands': False, 'HideWhenFaceDown': False, 'Counter': {'value': 1}}
O.append(cnt)
# 4. pions sur les points d'accroche ; Prix du castor sur 3
bc = lambda x, y: (round(BX + (x * S / 8000 - 0.5) * BW, 3), round(BZ + (0.5 - y * S / 5904) * BD, 3))
place(get('Ravages'), *bc(1833, 785)); place(get('Prix du castor'), *bc(3694 + 108.6 * 2, 785)); place(get('Année'), *bc(1405, 111.5))
# 5. essai : Grands événements sans le drapeau SidewaysCard (le format couché vient de la planche)
g = get('Grands événements'); g.pop('SidewaysCard', None)
for c in g['ContainedObjects']: c.pop('SidewaysCard', None)
json.dump(d, open(P, 'w'), ensure_ascii=False, indent=2); print('v3.46 appliquée ; Force iroquoise en', fx, fz)
