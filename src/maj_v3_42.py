# v3.42 : tuiles d'événement evt7 (src/evenements_v3.py, src/evt_occasion_v2.py) : ↻ + flocon = retour au sac à l'hiver (Baie d'Hudson, Lac épuisé, Épidémie, Le Profond) ;
# Occasion dans le gabarit des autres tuiles, double flèche + flocon (remélange de la défausse à l'hiver) ; verso de l'aide « Rivière et événements » (aide_b_v42).
import json, sys
R = sys.argv[1] if len(sys.argv) > 1 else './'
P = R + 'Castor_et_eau-de-vie.json'; d = json.load(open(P))
GH = 'https://raw.githubusercontent.com/caravage/castor-eau-de-vie-tts/main/img/v18/'
n = 0
def walk(os_):
    global n
    for o in os_:
        ci = o.get('CustomImage', {})
        for k in ('ImageURL', 'ImageSecondaryURL'):
            for nom in ('occasion', 'hudson', 'profond', 'epidemie', 'epuise'):
                if f'evt6_{nom}.png' in ci.get(k, ''): ci[k] = GH + f'evt7_{nom}.png'; n += 1
            if 'aide_b_v41.png' in ci.get(k, ''): ci[k] = GH + 'aide_b_v42.png'; n += 1
        walk(o.get('ContainedObjects', []))
walk(d['ObjectStates']); assert n
json.dump(d, open(P, 'w'), ensure_ascii=False, indent=2); print(n, 'image(s) remplacée(s)')
