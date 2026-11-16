# v3.47 : marqueurs Ravagé, Zone fermée, Zone détruite, Raid et Frasil sans contour (images *_v47) ; sac Événements du mois à gauche du calendrier ;
# compteur Force iroquoise = tuile drapeau haudenosaunee avec boutons − / + (0 à 6) dans la baie d'Hudson ; jetons Alliance recto / verso (Tortue, Lynx).
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
BX, BZ, BW, BD = -2.96, 6.721, 59.558, 43.961
pt = lambda x, y: (round(BX + (x / 8000 - 0.5) * BW, 3), round(BZ + (0.5 - y / 5904) * BD, 3))   # pixel du plateau HD -> table
# 1. marqueurs sans contour
REMP = {'ravage.png?v38': 'ravage_v47.png', 'zone_fermee.png?v39': 'zone_fermee_v47.png', 'zone_detruite.png': 'zone_detruite_v47.png',
        'raid.png': 'raid_v47.png', 'frasil.png': 'frasil_v47.png'}
def maj(o):
    for blk, keys in (('CustomImage', ('ImageURL', 'ImageSecondaryURL')), ('CustomMesh', ('DiffuseURL',))):
        b = o.get(blk, {})
        for k in keys:
            for a, n in REMP.items():
                if b.get(k) == GH + a: b[k] = GH + n
walk(O, maj)
# 2. sac Événements du mois : à gauche du calendrier (case Printemps)
place(get('Événements du mois'), *pt(745, 425))
# 3. Force iroquoise : tuile drapeau avec valeur et boutons − / +
old = get('Force iroquoise'); O.remove(old)
fx, fz = old['Transform']['posX'], old['Transform']['posZ']
LUA = '''-- Force iroquoise : 0 à 6, départ 1. Boutons − / +.
local v = 1
local C = {0.96, 0.95, 0.92}
local T = {0, 0, 0, 0}
function onLoad(s)
  if s and s ~= "" then v = tonumber(s) or 1 end
  local function b(f, l, x, fs) self.createButton({click_function = f, function_owner = self, label = l, position = {x, 0.11, 0.62}, width = (f == "rien") and 0 or 380, height = 380, font_size = fs, color = T, font_color = C, hover_color = {1, 1, 1, 0.15}, press_color = {1, 1, 1, 0.3}}) end
  b("moins", "−", -0.62, 420); b("rien", tostring(v), 0, 460); b("plus", "+", 0.62, 420)
end
function onSave() return tostring(v) end
function rien() end
local function maj() self.editButton({index = 1, label = tostring(v)}) self.setName("Force iroquoise : " .. v) end
function moins() if v > 0 then v = v - 1 maj() end end
function plus() if v < 6 then v = v + 1 maj() end end
'''
fr = get('Frasil')
t = cp(fr); t['GUID'] = gid(); t['Nickname'] = 'Force iroquoise : 1'
t['Description'] = "Force iroquoise (0 à 6, départ 1) : force des raids. +1 par 5 tuiles parties chez les Anglais ; −1 par Festin aux Lacs d'en bas. 2e Raid à 3, 3e Raid à 5."
t['CustomImage'].update(ImageURL=GH + 'force_iroquoise_v47.png', ImageSecondaryURL=GH + 'force_iroquoise_v47.png')
t['LuaScript'] = LUA; t['LuaScriptState'] = '1'; t['Locked'] = True
t['GMNotes'] = json.dumps({'w': 1.5, 'd': 1.5, 'x': fx, 'z': fz, 'h': 0.4, 'lock': True}); t['Transform'].update(posX=fx, posY=2.0, posZ=fz)
O.append(t)
# 4. jetons Alliance recto (Alliée) / verso (Neutre) : Tortue alliée, Lynx neutre au départ
ax = pt(745, 0)[0]
for nom, img, z, neutre in (('Alliance Tortue', 'tortue', pt(0, 1000)[1], False), ('Alliance Lynx', 'lynx', pt(0, 1330)[1], True)):
    a = cp(fr); a['GUID'] = gid(); a['Nickname'] = nom
    a['Description'] = 'Recto : alliée. Verso : neutre. Festin : retournez sur Alliée ; Affront : retournez sur Neutre.'
    a['CustomImage'].update(ImageURL=GH + f'alliance_{img}_alliee.png', ImageSecondaryURL=GH + f'alliance_{img}_neutre.png')
    a['CustomImage']['CustomTile'] = {'Type': 2, 'Thickness': 0.1, 'Stackable': False, 'Stretch': False}
    a['GMNotes'] = json.dumps({'w': 1.8, 'd': 1.8, 'x': ax, 'z': z, 'h': 0.5}); a['Transform'].update(posX=ax, posY=2.0, posZ=z, rotZ=180 if neutre else 0)
    a['Locked'] = False
    O.append(a)
json.dump(d, open(P, 'w'), ensure_ascii=False, indent=2); print('v3.47 appliquée')
