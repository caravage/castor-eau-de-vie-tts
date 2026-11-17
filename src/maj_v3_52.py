# v3.52 (17 nov. 2026) :
# - sac des congés refait : 29 tuiles au nouveau design (src/conges_v52.py, images cg52_*.png) ;
#   retirés : Gentilhomme, Seigneur, Fournisseur de Bordeaux, Congé des Prairies, Congé de l'Ouest ;
#   Fabrique Notre-Dame (×2) sans eau-de-vie ; Faveur et Fournisseur de La Rochelle à 1 crédit ;
#   un congé neutre, un avec officier et un avec missionnaire par Région ;
# - tuiles sans nom ni infobulle ; verso NON PAYÉ au prix (cg52_np*.png), verso = recto pour les congés à crédit.
import json, sys, random, importlib.util
R = sys.argv[1] if len(sys.argv) > 1 else './'
P = R + 'Castor_et_eau-de-vie.json'; d = json.load(open(P))
GH = 'https://raw.githubusercontent.com/caravage/castor-eau-de-vie-tts/main/img/v18/'
OS = d['ObjectStates']
spec = importlib.util.spec_from_file_location('cg', R + 'src/conges_v52.py'); cg = importlib.util.module_from_spec(spec); spec.loader.exec_module(cg)

def guids(objs):
    for o in objs:
        yield o.get('GUID'); yield from guids(o.get('ContainedObjects', []))
pris = set(guids(OS)); rnd = random.Random(352)
def guid():
    while True:
        g = '%06x' % rnd.randrange(16 ** 6)
        if g not in pris: pris.add(g); return g

sac = [o for o in OS if o.get('Nickname') == 'Sac des congés'][0]
modele = sac['ContainedObjects'][0]
tuiles = []
for c in cg.CONGES:
    cid, nb, p, cr = c[0], c[1], c[6], c[7]
    for _ in range(nb):
        t = json.loads(json.dumps(modele))
        t.update(GUID=guid(), Nickname='', Description='', Tooltip=False, GMNotes=json.dumps({'w': 1.4, 'd': 1.4}))
        t['CustomImage']['ImageURL'] = GH + f'cg52_{cid}.png'
        t['CustomImage']['ImageSecondaryURL'] = GH + (f'cg52_{cid}.png' if cr else f'cg52_np{p}.png')
        tuiles.append(t)
assert len(tuiles) == 29, len(tuiles)
sac['ContainedObjects'] = tuiles

d['SaveName'] = 'Castor et eau-de-vie v3.52'; d['Date'] = '11/17/2026 9:00:00 AM'
json.dump(d, open(P, 'w'), ensure_ascii=False, indent=2); print('v3.52 appliquée :', len(tuiles), 'congés')
