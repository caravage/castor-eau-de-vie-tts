# v3.39 : cartouche unique Montréal – Québec – partis sur le plateau (plaquettes Château / Palais retirées du module).
# Points d'accroche : rade de Québec (24, nouvelle grille), La Rochelle (12, décalés de 30 px css vers le bas),
# ovales de Montréal (3, nouvelles positions), cases des partis (6, nouvelles) ; pistes et Tour inchangées.
# Objets : Sac des congés (gauche du panneau Congés), Navire de la compagnie (1re case navire de Québec),
# 10 sacs de pions déplacés en haut du plateau (entre Ravages et Prix du castor, et à droite de Prix du castor).
import json, re, sys
R = sys.argv[1] if len(sys.argv) > 1 else './'
P = R + 'Castor_et_eau-de-vie.json'; d = json.load(open(P)); O = d['ObjectStates']
GH = 'https://raw.githubusercontent.com/caravage/castor-eau-de-vie-tts/main/img/v18/'
note = lambda n: json.dumps(n, ensure_ascii=False, separators=(', ', ': '))
# 1. image du plateau
t = [o for o in O if o.get('Nickname') == 'Table du castor'][0]
t['CustomImage'].update(ImageURL=GH + 'table_v3_39_hd.jpg', ImageSecondaryURL=GH + 'table_v3_39_hd.jpg')
# 2. plaquettes des partis retirées
d['ObjectStates'] = O = [o for o in O if o.get('Nickname') not in ('Château', 'Palais')]
# 3. points d'accroche
L = d['LuaScript']; i = L.index('local SNAP = ') + len('local SNAP = '); j = L.index('}}', i) + 2
old = [(float(a), float(b)) for a, b in re.findall(r'\{(-?[\d.]+),(-?[\d.]+)\}', L[i:j])]
keep = old[:23]                                                      # Ravages (7), Prix du castor (8), Tour (8)
LR = [(x, round(z - 0.5563, 3)) for x, z in old[47:59]]              # La Rochelle : +30 px css
QC = [(x, z) for z in (9.053, 7.829) for x in (13.017, 14.122, 15.226, 16.331, 17.436, 18.541, 20.017, 21.122, 22.227, 23.332, 24.437, 25.541)]
MO = [(14.625, 5.139), (15.719, 5.139), (16.813, 5.139)]
PA = [(13.187, 16.731), (13.187, 15.693), (13.187, 14.654), (20.308, 16.731), (20.308, 15.693), (20.308, 14.654)]
new = keep + QC + LR + MO + PA
L = L[:i] + '{' + ','.join('{%s,%s}' % p for p in new) + '}' + L[j:]
L = L.replace("emplacements Mission/Fort", "rade de Québec, La Rochelle, ovales de Montréal, cases des partis")
d['LuaScript'] = L
# 4. objets déplacés
def place(nom, x, z):
    o = [q for q in O if q.get('Nickname') == nom][0]
    n = json.loads(o['GMNotes']); n.update(x=x, z=z); o['GMNotes'] = note(n)
    o['Transform'].update(posX=x, posZ=z)
place('Sac des congés', 20.25, 5.47)
place('Navire de la compagnie', 13.017, 9.053)
for k, nom in enumerate(('Forts français', 'Forts anglais', 'Missions', 'Marqueurs Ravagé', 'Jetons Abîmé')):
    place(nom, round(-3.52 + 1.86 * k, 3), 20.36)
for k, nom in enumerate(('Guides', 'Pilotes', 'Forgerons', 'Coureurs des bois', 'Zones fermées')):
    place(nom, round(17.2 + 1.95 * k, 3), 20.36)
json.dump(d, open(P, 'w'), ensure_ascii=False, indent=2)
print('snaps', len(old), '->', len(new), '; objets', len(O))
