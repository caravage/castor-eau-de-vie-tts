# Capital circulant diminué du soupçon (9 nov. 2026) : −1 par point de soupçon (jeton « Soupçon <couleur> » sur la piste 0-6 du plateau du joueur).
# Piste : case 0 à +0,753 du centre du plateau, pas de 0,910 (image pmat_*, 1860 px pour 16,275 unités). Usage : python3 capital_soupcon.py <racine du dépôt>
import json, sys
P=sys.argv[1]+'Castor_et_eau-de-vie.json'; d=json.load(open(P)); L=d['LuaScript']
rep=[
("-- Capital circulant (livret) : charges (10 au plus) + tuiles de fourrure x prix du castor + parts + valeur « capital » de la piste Livres.",
 "-- Capital circulant (livret) : charges (10 au plus) + tuiles de fourrure x prix du castor + parts + valeur « capital » de la piste Livres − soupçon."),
("local function arrondi(v) return math.floor(v + 0.5) end",
 "local function arrondi(v) return math.floor(v + 0.5) end\nlocal SOUP0, SOUPAS = 0.753, 0.910   -- piste Soupçon du plateau du joueur : case 0, pas"),
("local sacs, cpt, parts, cartes, livres, prix, jch, exps = {}, {}, {}, {}, {}, nil, {}, {}",
 "local sacs, cpt, parts, cartes, livres, prix, jch, exps, plat, soup = {}, {}, {}, {}, {}, nil, {}, {}, {}, {}"),
("    elseif nm == \"Prix du castor\" then prix = o end",
 "    elseif nm:find(\"^Plateau du joueur \") then plat[nm:sub(19)] = o\n    elseif nm:find(\"^Soupçon \") then soup[nm:sub(10)] = o\n    elseif nm == \"Prix du castor\" then prix = o end"),
("    local total = tostring(charges + (q[\"castor\"] or 0) * p + np + palier(nl))",
 "    local ns = 0\n    if soup[c] and plat[c] then\n      ns = math.max(0, math.min(6, arrondi(((soup[c].getPosition().x - plat[c].getPosition().x) / F - SOUP0) / SOUPAS)))\n    end\n    local total = tostring(math.max(0, charges + (q[\"castor\"] or 0) * p + np + palier(nl) - ns))"),
]
for a,b in rep:
    assert L.count(a)==1, a[:60]
    L=L.replace(a,b)
d['LuaScript']=L
for o in d['ObjectStates']:
    if (o.get('Nickname') or '').startswith('Capital circulant '):
        o['Description']=o['Description'].replace('+ valeur « capital » de la piste Livres.','+ valeur « capital » de la piste Livres − soupçon.')
json.dump(d,open(P,'w'),ensure_ascii=False,indent=2); print('ok')
