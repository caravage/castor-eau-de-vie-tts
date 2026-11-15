# v3.43 : paquet Grands événements refait (src/grands_evenements/gen_full2.py) : 6 cartes horizontales pleine image,
# gravures d'époque du domaine public passées en sépia ; planche deck_grand_v2.jpg (3 × 2), dos deck_grand_v2_back.jpg.
import json, sys, random
R = sys.argv[1] if len(sys.argv) > 1 else './'
P = R + 'Castor_et_eau-de-vie.json'; d = json.load(open(P))
GH = 'https://raw.githubusercontent.com/caravage/castor-eau-de-vie-tts/main/img/v18/'
CARTES = [
 ("Incendie de la basse-ville", "Chaque joueur lance 1 dé et peut acheter des dés en plus, pour 2 ₶ chacun ; il garde le meilleur. Le joueur au dé le plus bas perd autant de crédit que la valeur de son dé. En cas d'égalité, tous les ex aequo perdent."),
 ("Massacre de Lachine", "La Force iroquoise augmente de 3. Un raid frappe immédiatement la rivière des Outaouais."),
 ("Guerre avec l'Angleterre", "1re pioche : La Force iroquoise augmente de 2 et le Ravage de 1. Un joueur pris lors d'une vente à Albany perd 2 VP. Au lieu de traverser, un navire peut partir en course : il lance 1 dé ; sur 1, il est coulé et remis au chantier ; sur 2 ou 3, rien ne se passe ; sur 4 à 6, il rapporte 4 ₶. La carte est ensuite remélangée dans le paquet.\n2e pioche : Chaque navire qui traverse lance 1 dé ; sur 1 ou 2, il est coulé et remis au chantier."),
 ("Ordonnance royale", "Cette année, aucun congé n'est émis. Dans chaque région, un seul fort reste ouvert, au choix du joueur le plus haut sur la piste du Gouverneur ; les autres sont fermés."),
 ("Grande Paix de Montréal", "La Force iroquoise retombe à 0."),
 ("Amnistie des coureurs des bois", "Chaque joueur retire 2 points de soupçon."),
]
CD = {"6": {"FaceURL": GH + "deck_grand_v2.jpg", "BackURL": GH + "deck_grand_v2_back.jpg", "NumWidth": 3, "NumHeight": 2, "BackIsHidden": True, "UniqueBack": False, "Type": 0}}
W, D = 4.9, 3.5                                  # cartes couchées : largeur > profondeur
n = 0
for o in d['ObjectStates']:
    if o.get('GUID') == '89aee2':
        proto = o['ContainedObjects'][0]
        cards = []
        for i, (nom, fx) in enumerate(CARTES):
            c = json.loads(json.dumps(proto))
            c['GUID'] = f'ge{i}{random.randint(100, 999)}'; c['Nickname'] = nom; c['Description'] = fx
            c['CardID'] = 600 + i; c['CustomDeck'] = CD; c['SidewaysCard'] = True
            c['GMNotes'] = json.dumps({'w': W, 'fz': 180, 'd': D})
            cards.append(c)
        random.shuffle(cards)
        o['ContainedObjects'] = cards; o['DeckIDs'] = [c['CardID'] for c in cards]; o['CustomDeck'] = CD
        g = json.loads(o['GMNotes']); g.update(w=W, d=D); o['GMNotes'] = json.dumps(g)
        o['Description'] = "Au début de l'année, le chef du Parti du Gouverneur pioche 2 cartes, en applique 1 et défausse l'autre."
        n += 1
assert n == 1
json.dump(d, open(P, 'w'), ensure_ascii=False, indent=2); print('paquet Grands événements remplacé')
