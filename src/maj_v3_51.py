# v3.51 (16 nov. 2026) :
# - plateau table_v3_51_hd : légende resserrée, intitulés en IM Fell English, seuils retirés (faces de dé d'échec seulement),
#   Frasil sur une ligne (navire : 1 coulé ; canot : 1 abîmé) — src/plateau_hd/build_map_html.py ;
# - tuiles Événements du mois (sac, Raids iroquois, Réserve Épidémie, Épidémie et Lac épuisé) à la même taille : GMNotes w = d = 2.0
#   (taille d'une tuile à l'échelle 1, celle d'Épidémie et Lac épuisé posées hors sac) ;
# - points d'accroche des pistes Ravages et Prix du castor recalés sur les cercles du plateau (z −0,034), pions aussi ;
# - jetons voyageurs avec leur prix d'embauche (voy2_*_v51.png, src/voyageurs_prix_v51.py) ; Guide 1 ₶, Pilote 2 ₶ « sans jet aux rapides »
#   (src/voyageurs_pilote_v51.py) ; sacs rangés de gauche à droite du moins cher au plus cher ;
# - cubes et sac Milice à la couleur du Milicien (#44464C).
import json, sys, re
R = sys.argv[1] if len(sys.argv) > 1 else './'
P = R + 'Castor_et_eau-de-vie.json'; d = json.load(open(P))
GH = 'https://raw.githubusercontent.com/caravage/castor-eau-de-vie-tts/main/img/v18/'
OS = d['ObjectStates']
def allobj(objs):
    for o in objs:
        yield o; yield from allobj(o.get('ContainedObjects', []))
by = lambda n: [o for o in OS if o.get('Nickname') == n][0]

# 1. plateau
t = by('Table du castor')
assert t['CustomImage']['ImageURL'].endswith('table_v3_50_hd.jpg')
t['CustomImage'].update(ImageURL=GH + 'table_v3_51_hd.jpg', ImageSecondaryURL=GH + 'table_v3_51_hd.jpg')

# 2. tuiles d'événement : même taille partout
n = 0
for o in allobj(OS):
    u = o.get('CustomImage', {}).get('ImageURL', '')
    if '/evt' in u and o.get('Name') == 'Custom_Tile':
        g = json.loads(o.get('GMNotes') or '{}'); g['w'] = g['d'] = 2.0; o['GMNotes'] = json.dumps(g); n += 1
print('tuiles événement', n)

# 3. points d'accroche Ravages / Prix du castor (z 20.351 -> 20.317) et pions
DZ = -0.034
lua = d['LuaScript']; m = re.search(r'local SNAP = (\{.*?\}\})', lua)
pts = re.findall(r'\{(-?[\d.]+),(-?[\d.]+)\}', m.group(1))
pts = [(x, f'{float(z) + DZ:.3f}' if z == '20.351' else z) for x, z in pts]
lua = lua.replace(m.group(1), '{' + ','.join(f'{{{x},{z}}}' for x, z in pts) + '}', 1); d['LuaScript'] = lua
for nom in ('Ravages', 'Prix du castor'):
    o = by(nom); o['Transform']['posZ'] = round(o['Transform']['posZ'] + DZ, 3)
    g = json.loads(o['GMNotes']); g['z'] = round(g['z'] + DZ, 3); o['GMNotes'] = json.dumps(g)

# 4. voyageurs : prix sur les jetons, descriptions, ordre des sacs (1 ₶ puis 2 ₶)
V = (('Guides', 'guide_v43', 'guide_v43', '+1 au jet de raccourci et aux traversées. 1 ₶.'),
     ('Forgerons', 'artisan', 'artisan', None),
     ('Miliciens', 'milicien', 'milicien', None),
     ('Pilotes', 'pilote', 'pilote2', 'Passe les rapides sans jet. 2 ₶.'),
     ('Interprètes', 'interprete', 'interprete', None))
for i, (sac, ancien, k, desc) in enumerate(V):
    b = by(sac); x = 17.0 + 1.5 * i
    b['Transform']['posX'] = x; g = json.loads(b['GMNotes']); g['x'] = x; b['GMNotes'] = json.dumps(g, ensure_ascii=False)
    for o in b['ContainedObjects']:
        assert o['CustomImage']['ImageURL'].endswith(f'voy2_{ancien}.png')
        o['CustomImage']['ImageURL'] = GH + f'voy2_{k}_v51.png'
        if k == 'pilote2': o['CustomImage']['ImageSecondaryURL'] = GH + 'voy2_pilote2_used.png'
        if desc: o['Description'] = desc

# 5. milice à la couleur du Milicien
GRIS = {'r': round(0x44 / 255, 3), 'g': round(0x46 / 255, 3), 'b': round(0x4C / 255, 3)}
m = by('Milice'); m['ColorDiffuse'] = dict(GRIS)
for o in m['ContainedObjects']: o['ColorDiffuse'] = dict(GRIS)
json.dump(d, open(P, 'w'), ensure_ascii=False, indent=2); print('v3.51 appliquée')
