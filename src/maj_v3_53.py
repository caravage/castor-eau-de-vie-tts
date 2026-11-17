# v3.53 (17 nov. 2026) : passe qualité visuelle (src/qualite_v53.py, src/ferme_v53.py, src/polices.py, src/plateau_hd/).
# - plateau table_v3_53_hd : La Rochelle et Antilles 22 px css à gauche (hors du filet du cadre), « Bas du fleuve », « Albany » et
#   « Baie d'Hudson » en IM Fell, texte des partis agrandi et sans icônes, cases Tour foncées, Ravages sans cases cerclées,
#   colonne Rivière au vert de la case Hiver ; les 12 points d'accroche de La Rochelle suivent (x − 0,408) ;
# - polices IM Fell + Alegreya Sans (locales) : plateaux de joueur, cartes Expédition, Ferme du castor (politiques sur deux lignes),
#   jetons voyageurs, cartes Matériel ;
# - tuiles Événements du mois à coins transparents ; dos des congés « Congé » ; Coureur des bois en gravure ; Scorbut (pagaie barrée) ;
#   congé Lacs d'en haut (tortue centrée) ; cartes Navire et Distillerie (textes agrandis, « Produit 4 eaux-de-vie. », ronds remontés :
#   points d'accroche des cartes ajustés) ; pions Distillerie en gravure ; aide de jeu verso (aide_b_v53).
import json, re, sys
R = sys.argv[1] if len(sys.argv) > 1 else './'
P = R + 'Castor_et_eau-de-vie.json'; d = json.load(open(P))
M = {'table_v3_51_hd.jpg': 'table_v3_53_hd.jpg', 'conge_back.png': 'conge_back_v53.png', 'tok_coureur.png': 'tok_coureur_v53.png',
     'hid_scorbut.png': 'hid53_scorbut.png', 'cg52_haut.png': 'cg53_haut.png', 'ferme_recto_v8.png': 'ferme_recto_v53.png',
     'deck_mat.png': 'deck_mat_v53.png', 'aide_b_v46.png': 'aide_b_v53.png',
     'evt_back.png': 'evt53_back.png', 'evt_calme.png': 'evt53_calme.png', 'evt6_abondante.png': 'evt53_abondante.png', 'evt6_hiver.png': 'evt53_hiver.png',
     'evt7_epidemie.png': 'evt53_epidemie.png', 'evt7_epuise.png': 'evt53_epuise.png', 'evt7_occasion.png': 'evt53_occasion.png',
     'evt7_profond.png': 'evt53_profond.png', 'evt7_tempete.png': 'evt53_tempete.png', 'evt8_hudson.png': 'evt53_hudson.png'}
for i in (1, 2, 3): M[f'evt_raid{i}_b.png'] = f'evt53_raid{i}_b.png'
for i in range(1, 7): M[f'carte_navire_{i}.png'] = f'carte_navire53_{i}.png'
for i in range(1, 5): M[f'carte_distillerie_{i}.png'] = f'carte_distillerie53_{i}.png'; M[f'pion_distillerie_{i}.png'] = f'pion_distillerie53_{i}.png'
for i in range(3): M[f'pmat_v3_{i}.png'] = f'pmat_v53_{i}.png'
for c in ('bleu', 'rouge', 'vert'): M[f'exp5_{c}.png'] = f'exp53_{c}.png'
for a, b in (('guide_v43', 'guide'), ('milicien', 'milicien'), ('interprete', 'interprete'), ('artisan', 'artisan')):
    M[f'voy2_{a}.png'] = M[f'voy2_{a}_v51.png'] = f'voy53_{b}.png'; M[f'voy2_{a}_used.png'] = f'voy53_{b}_used.png'
M['voy2_pilote.png'] = M['voy2_pilote2_v51.png'] = 'voy53_pilote.png'; M['voy2_pilote2_used.png'] = 'voy53_pilote_used.png'
n = {}
def url(u):
    m = re.match(r'(.*/img/v18/)([^/?]+)(\?.*)?$', u)
    if m and m.group(2) in M: n[m.group(2)] = n.get(m.group(2), 0) + 1; return m.group(1) + M[m.group(2)]
    return u
def walk(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if isinstance(v, str) and v.startswith('http'): o[k] = url(v)
            else: walk(v)
    elif isinstance(o, list):
        for v in o: walk(v)
walk(d['ObjectStates'])
assert set(n) == set(M), set(M) - set(n)
# points d'accroche de La Rochelle (12) : 22 px css à gauche = 0,408 unité
lua = d['LuaScript']; k = 0
for x in ('22.88', '24.256', '25.55'):
    for z in ('1.177', '-0.222', '-1.621', '-3.021'):
        a = '{' + x + ',' + z + '}'; assert lua.count(a) == 1, a
        lua = lua.replace(a, '{' + f'{float(x) - 0.408:.3f}'.rstrip('0') + ',' + z + '}'); k += 1
d['LuaScript'] = lua
# cartes Navire / Distillerie : ronds des parts et case du jeton remontés de 10 px (sur 320) = 0,07 unité
c = 0
for o in d['ObjectStates']:
    nm = o.get('Nickname', '')
    if nm.startswith(('Carte de navire', 'Carte de distillerie')):
        g = json.loads(o['GMNotes']); sw = g['snapw']
        sw[0][1] = -0.049 if nm.startswith('Carte de navire') else -0.042
        for p in sw[1:]: p[1] = -0.042
        o['GMNotes'] = json.dumps(g, ensure_ascii=False); c += 1
assert c == 10, c
d['SaveName'] = 'Castor et eau-de-vie v3.53'; d['Date'] = '11/17/2026 1:00:00 AM'
json.dump(d, open(P, 'w'), ensure_ascii=False, indent=2); print('v3.53 appliquée :', sum(n.values()), 'liens,', k, 'points La Rochelle,', c, 'cartes')
