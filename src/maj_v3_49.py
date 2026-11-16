# v3.49 : plateau table_v3_49_hd (légende : Raccourci « 3 ou plus », puis « 1 : abîmé et reste sur place » et « 2 : reste sur place »).
# Généré par src/plateau_hd (build_map_html.py, bloc légende) puis compose.py.
import json, sys
R = sys.argv[1] if len(sys.argv) > 1 else './'
P = R + 'Castor_et_eau-de-vie.json'; d = json.load(open(P))
GH = 'https://raw.githubusercontent.com/caravage/castor-eau-de-vie-tts/main/img/v18/'
t = [o for o in d['ObjectStates'] if o.get('Nickname') == 'Table du castor'][0]
assert t['CustomImage']['ImageURL'].endswith('table_v3_48_hd.jpg')
t['CustomImage'].update(ImageURL=GH + 'table_v3_49_hd.jpg', ImageSecondaryURL=GH + 'table_v3_49_hd.jpg')
json.dump(d, open(P, 'w'), ensure_ascii=False, indent=2); print('v3.49 appliquée')
