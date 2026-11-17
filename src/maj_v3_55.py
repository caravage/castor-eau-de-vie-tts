# v3.55 (17 nov. 2026) : points d'accroche des pistes Ravages (7) et Prix du castor (8) supprimés puis refaits
# d'après le centre réel des cases sur table_v3_54_hd. Cause de l'écart : les cases sont posées dans un cadre à bordure
# de 3 px (build_board_html.py, track()), donc leur centre est à (cx + 3, 788) px plateau et non (cx, 785) ;
# la v3.51 avait corrigé z mais pas x (écart de 0,03 unité vers la gauche). Les deux pions suivent.
import json, re, sys
R = sys.argv[1] if len(sys.argv) > 1 else './'
P = R + 'Castor_et_eau-de-vie.json'; d = json.load(open(P))
S = 8000 / 5600; BX, BZ, BW, BD = -2.96, 6.721, 59.558, 43.961
tab = lambda bx, by: (round(BX + (bx * S / 8000 - 0.5) * BW, 3), round(BZ + (0.5 - by * S / 5904) * BD, 3))
RAV = [tab(1833 + 3 + 108.7 * i, 788) for i in range(7)]; PRIX = [tab(3694 + 3 + 108.6 * i, 788) for i in range(8)]
L = d['LuaScript']; i = L.index('local SNAP = ') + len('local SNAP = '); j = L.index('}}', i) + 2
old = re.findall(r'\{(-?[\d.]+),(-?[\d.]+)\}', L[i:j]); assert len(old) == 68 and all(z == '20.317' for _, z in old[:15])
f = lambda v: ('%.3f' % v).rstrip('0').rstrip('.')
new = ['{%s,%s}' % (f(x), f(z)) for x, z in RAV + PRIX] + ['{%s,%s}' % p for p in old[15:]]
d['LuaScript'] = L[:i] + '{' + ','.join(new) + '}' + L[j:]
for nom, (x, z) in (('Ravages', RAV[0]), ('Prix du castor', PRIX[2])):
    o = [q for q in d['ObjectStates'] if q.get('Nickname') == nom]; assert len(o) == 1; o = o[0]
    n = json.loads(o['GMNotes']); n.update(x=x, z=z); o['GMNotes'] = json.dumps(n, ensure_ascii=False, separators=(', ', ': '))
    o['Transform'].update(posX=x, posZ=z)
d['SaveName'] = 'Castor et eau-de-vie v3.55'; d['Date'] = '11/17/2026 3:40:00 PM'
json.dump(d, open(P, 'w'), ensure_ascii=False, indent=2); print('v3.55 :', RAV, PRIX)
