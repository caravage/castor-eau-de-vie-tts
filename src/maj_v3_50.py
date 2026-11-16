# v3.50 (16 nov. 2026) :
# - plateau table_v3_50_hd : légende agrandie, Raccourci « 3 ou plus » puis « 1-2 : reste sur place », ligne Frasil
#   (navire 1 : coulé ; canot 1 : abîmé, déjà abîmé : détruit) — src/plateau_hd/build_map_html.py ;
# - « Sac Ravage » retiré : Épidémie et Lac épuisé posés à côté de la Réserve Épidémie ;
# - nouvelle tuile Événement du mois « Tempête » (evt7_tempete.png, src/evt_tempete.py) dans le sac Événements du mois ;
# - Force iroquoise : chiffre imprimé sur l'image, 7 états (force_iroquoise_v50_N.png, src/force_iroquoise_v50.py).
import json, sys, copy, random
R = sys.argv[1] if len(sys.argv) > 1 else './'
P = R + 'Castor_et_eau-de-vie.json'; d = json.load(open(P))
GH = 'https://raw.githubusercontent.com/caravage/castor-eau-de-vie-tts/main/img/v18/'
OS = d['ObjectStates']
used = set()
def walk(objs):
    for o in objs:
        used.add(o.get('GUID')); walk(o.get('ContainedObjects', []))
        for s in (o.get('States') or {}).values(): used.add(s.get('GUID'))
walk(OS)
def guid():
    while True:
        g = '%06x' % random.randrange(16 ** 6)
        if g not in used: used.add(g); return g
by = lambda n: [o for o in OS if o.get('Nickname') == n][0]

# 1. plateau
t = by('Table du castor')
assert t['CustomImage']['ImageURL'].endswith('table_v3_49_hd.jpg')
t['CustomImage'].update(ImageURL=GH + 'table_v3_50_hd.jpg', ImageSecondaryURL=GH + 'table_v3_50_hd.jpg')

# 2. Sac Ravage retiré, ses tuiles posées face visible à gauche de la Réserve Épidémie
sac = by('Sac Ravage'); OS.remove(sac)
for k, o in enumerate(sac['ContainedObjects']):
    o['Transform'].update(posX=16.0 - 1.25 * k, posY=2.0, posZ=30.35, rotX=0, rotY=180, rotZ=0)
    OS.append(o)

# 3. Tempête dans le sac Événements du mois
ev = by('Événements du mois')
calme = [o for o in ev['ContainedObjects'] if o.get('Nickname') == 'Rivière calme'][0]
tp = copy.deepcopy(calme); tp['GUID'] = guid(); tp['Nickname'] = 'Tempête'
tp['Description'] = ("Chaque navire ou bateau en traversée lance un dé : sur 1 ou 2, il coule. "
                     "Si une Rivière calme sort à la fin du mois suivant, la tempête continue.")
tp['CustomImage']['ImageURL'] = GH + 'evt7_tempete.png'
ev['ContainedObjects'].append(tp)

# 4. Force iroquoise : un état par valeur (0 à 6), chiffre sur l'image
fi = [o for o in OS if o.get('Nickname', '').startswith('Force iroquoise')][0]
LUA = '''-- Force iroquoise : 0 à 6 ; un état par valeur (chiffre imprimé sur l'image). Boutons − / +.
local V = %d
local C = {0.96, 0.95, 0.92}
local T = {0, 0, 0, 0}
function onLoad()
  local function b(f, l, x) self.createButton({click_function = f, function_owner = self, label = l, position = {x, 0.11, 0.62}, width = 380, height = 380, font_size = 420, color = T, font_color = C, hover_color = {1, 1, 1, 0.15}, press_color = {1, 1, 1, 0.3}}) end
  b("moins", "−", -0.62); b("plus", "+", 0.62)
end
function moins() if V > 0 then self.setState(V) end end
function plus() if V < 6 then self.setState(V + 2) end end
'''
base = copy.deepcopy(fi); base.pop('States', None)
def etat(v):
    o = copy.deepcopy(base); o['GUID'] = guid() if v != 1 else fi['GUID']
    o['Nickname'] = f'Force iroquoise : {v}'; o['LuaScript'] = LUA % v; o['LuaScriptState'] = ''
    o['CustomImage']['ImageURL'] = o['CustomImage']['ImageSecondaryURL'] = GH + f'force_iroquoise_v50_{v}.png'
    return o
new = etat(1); new['States'] = {str(v + 1): etat(v) for v in range(7) if v != 1}
OS[OS.index(fi)] = new
json.dump(d, open(P, 'w'), ensure_ascii=False, indent=2); print('v3.50 appliquée')
