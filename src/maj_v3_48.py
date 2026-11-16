# v3.48 : plateau table_v3_48_hd (typographie IM Fell : portages en italique, cartouches en petites capitales, Pays et lacs en italique).
# Généré par src/plateau_hd (build_map_html.py, fonction polices) puis compose.py.
import json, sys
R = sys.argv[1] if len(sys.argv) > 1 else './'
P = R + 'Castor_et_eau-de-vie.json'; d = json.load(open(P))
GH = 'https://raw.githubusercontent.com/caravage/castor-eau-de-vie-tts/main/img/v18/'
t = [o for o in d['ObjectStates'] if o.get('Nickname') == 'Table du castor'][0]
assert t['CustomImage']['ImageURL'].endswith('table_v3_40_hd.jpg')
t['CustomImage'].update(ImageURL=GH + 'table_v3_48_hd.jpg', ImageSecondaryURL=GH + 'table_v3_48_hd.jpg')
json.dump(d, open(P, 'w'), ensure_ascii=False, indent=2); print('v3.48 appliquée')
