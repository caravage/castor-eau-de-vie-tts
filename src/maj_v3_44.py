# v3.44 : réserve Épidémie (sac infini, tuile à la taille du sac Événements) ; sac « Zones détruites » (tête de mort) ;
# réserve de cubes marron « Milice » ; aide de jeu v43 (Affront → Albany ; Entretien des lieux ; Ravages / zone détruite) ;
# jeton Guide « +1 au raccourci et aux traversées » ; infobulles Épidémie et Lac épuisé.
import json, sys, random
R = sys.argv[1] if len(sys.argv) > 1 else './'
P = R + 'Castor_et_eau-de-vie.json'; d = json.load(open(P)); O = d['ObjectStates']
GH = 'https://raw.githubusercontent.com/caravage/castor-eau-de-vie-tts/main/img/v18/'
cp = lambda o: json.loads(json.dumps(o))
gid = lambda: ''.join(random.choice('0123456789abcdef') for _ in range(6))
EPI = ("On retire une peau dans chaque zone de traite de la région qui contient le plus de canots (les portages adjacents à une zone de traite "
       "comptent comme faisant partie de la région). En cas d'égalité, dé de région. +1 : ajoutez tout de suite une copie dans le sac ; "
       "la tuile tirée revient à l'hiver (↻ avec flocon).")
LAC = "Dé de région : Ravage dans la zone de traite avec le moins de peaux de la région. ↻ avec flocon : retour au sac à l'hiver."
def walk(os_, f):
    for o in os_:
        f(o); walk(o.get('ContainedObjects', []), f)
def maj(o):
    if o.get('Nickname') == 'Épidémie' and o.get('Name') == 'Custom_Tile': o['Description'] = EPI
    if o.get('Nickname') == 'Lac épuisé': o['Description'] = LAC
    ci = o.get('CustomImage', {})
    for k in ('ImageURL', 'ImageSecondaryURL'):
        v = ci.get(k, '')
        for a, b in (('aide_a_v40.png', 'aide_a_v43.png'), ('aide_b_v42.png', 'aide_b_v43.png'), ('voy2_guide_used.png', 'voy2_guide_v43_used.png'), ('voy2_guide.png', 'voy2_guide_v43.png')):
            if v.endswith(a) or (a in v and '?' in v): ci[k] = GH + b; break
walk(O, maj)
for o in O:
    cm = o.get('CustomMesh', {})
    if cm.get('DiffuseURL', '').endswith('voy2_guide.png'): cm['DiffuseURL'] = GH + 'voy2_guide_v43.png'
# 1. Réserve Épidémie : les 5 tuiles posées sont remplacées par un sac infini de la même taille que les tuiles
pile = [o for o in O if o.get('Nickname') == 'Épidémie' and o.get('Name') == 'Custom_Tile']
assert pile
tuile = cp(pile[0]); tuile['Transform'].update(posX=0, posY=2, posZ=0); tuile['GMNotes'] = json.dumps({'w': 1.05, 'd': 1.05, 'face': 'up'})
for o in pile: O.remove(o)
rav = [o for o in O if o.get('Nickname') == 'Marqueurs Ravagé'][0]
b = cp(rav); b['GUID'] = gid(); b['Nickname'] = 'Réserve Épidémie'; b['Description'] = "Tuiles Épidémie en nombre illimité : on en ajoute une au sac Ravage à chaque Épidémie tirée."
b['CustomMesh']['DiffuseURL'] = GH + 'evt7_epidemie.png'
b['GMNotes'] = json.dumps({'w': 1.05, 'x': 18.5, 'z': 30.9, 'h': 0.6, 'y3': True, 'd': 1.05, 'lock': True, 'drop': True})
b['Transform'].update(posX=18.5, posZ=30.9); b['ContainedObjects'] = [tuile]; O.append(b)
# 2. Zones détruites : même sac que Zones fermées, tête de mort
zf = [o for o in O if o.get('Nickname') == 'Zones fermées'][0]
z = cp(zf); z['GUID'] = gid(); z['Nickname'] = 'Zones détruites'
z['Description'] = "Marqueurs Zone détruite en nombre illimité : une zone ravagée qui rate son dé d'hiver est détruite et sort du jeu jusqu'à la fin."
z['CustomMesh'].update(MeshURL=GH + 'sac_zone_detruite.obj', DiffuseURL=GH + 'zone_detruite.png')
z['GMNotes'] = json.dumps({'w': 1.2, 'x': 27.5, 'z': 20.36, 'h': 0.6, 'y3': True, 'd': 1.2, 'lock': True, 'drop': True}); z['Transform'].update(posX=27.5, posZ=20.36)
t = z['ContainedObjects'][0]; t['GUID'] = gid(); t['Nickname'] = 'Zone détruite'; t['Description'] = 'Zone détruite : hors du jeu jusqu’à la fin de la partie.'
for k in ('ImageURL', 'ImageSecondaryURL'):
    if t['CustomImage'].get(k): t['CustomImage'][k] = GH + 'zone_detruite.png'
O.append(z)
# 3. Milice : réserve infinie de cubes marron
BRUN = {'r': 0.42, 'g': 0.26, 'b': 0.12}
cube = {'GUID': gid(), 'Name': 'BlockSquare', 'Transform': {'posX': 0, 'posY': 2, 'posZ': 0, 'rotX': 0, 'rotY': 180, 'rotZ': 0, 'scaleX': 0.3, 'scaleY': 0.3, 'scaleZ': 0.3},
        'Nickname': 'Milice', 'Description': 'Milice : +1 en défense d’un fort.', 'GMNotes': json.dumps({'w': 0.42, 'y3': True}), 'ColorDiffuse': BRUN,
        'Locked': False, 'Grid': False, 'Snap': False, 'Tooltip': True, 'Hands': False, 'HideWhenFaceDown': False}
m = {'GUID': gid(), 'Name': 'Infinite_Bag', 'Transform': {'posX': 29.0, 'posY': 2.0, 'posZ': 20.36, 'rotX': 0, 'rotY': 180, 'rotZ': 0, 'scaleX': 0.8, 'scaleY': 0.8, 'scaleZ': 0.8},
     'Nickname': 'Milice', 'Description': 'Cubes de milice en nombre illimité (+1 en défense d’un fort).',
     'GMNotes': json.dumps({'w': 1.2, 'x': 29.0, 'z': 20.36, 'h': 0.6, 'y3': True, 'lock': True, 'drop': True}), 'ColorDiffuse': BRUN,
     'Locked': True, 'Grid': False, 'Snap': False, 'Tooltip': True, 'Hands': False, 'HideWhenFaceDown': False, 'MaterialIndex': -1, 'ContainedObjects': [cube]}
O.append(m)
json.dump(d, open(P, 'w'), ensure_ascii=False, indent=2); print('v3.44 appliquée')
