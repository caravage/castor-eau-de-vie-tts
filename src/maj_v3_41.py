# v3.41 : verso de l'aide de jeu (Printemps / Hiver) refait d'après le livret, même style et format que le recto (src/aide_actions/aide_verso.html, rendu ×2).
import json, sys
R = sys.argv[1] if len(sys.argv) > 1 else './'
P = R + 'Castor_et_eau-de-vie.json'; d = json.load(open(P)); O = d['ObjectStates']
GH = 'https://raw.githubusercontent.com/caravage/castor-eau-de-vie-tts/main/img/v18/'
A, B = GH + 'aide_a_v40.png', GH + 'aide_b_v41.png'
for nom, im1, im2 in (('Aide de jeu (recto)', A, B), ('Aide de jeu (verso)', B, A)):
    o = [q for q in O if q.get('Nickname') == nom][0]
    o['CustomImage'].update(ImageURL=im1, ImageSecondaryURL=im2)
json.dump(d, open(P, 'w'), ensure_ascii=False, indent=2)
