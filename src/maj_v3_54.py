# v3.54 (17 nov. 2026) : plateau table_v3_54_hd — tireté Domaine du Roi – Québec supprimé (src/plateau_hd/build_map_html.py).
import json, sys
R = sys.argv[1] if len(sys.argv) > 1 else './'
P = R + 'Castor_et_eau-de-vie.json'; s = open(P).read()
assert s.count('table_v3_53_hd.jpg') == 2
d = json.loads(s.replace('table_v3_53_hd.jpg', 'table_v3_54_hd.jpg'))
d['SaveName'] = 'Castor et eau-de-vie v3.54'; d['Date'] = '11/17/2026 1:20:00 AM'
json.dump(d, open(P, 'w'), ensure_ascii=False, indent=2); print('v3.54 appliquée')
