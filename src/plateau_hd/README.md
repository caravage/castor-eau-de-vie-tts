# Plateau HD (v3.39)

**Source de vérité pour les modifications : les fichiers HTML vectoriels de ce dossier** (jamais le PNG/JPEG final).
- `carte_src.html` : carte complète (préparée par `prep_carte.py` depuis `../carte_etendue_tts.dc.html`) ; les corrections du plateau (bandeaux, symboles, rapides, encarts, rose, légende) sont appliquées par `build_map_html.py`.
- `base.html` / `over.html` / `hills.html` : calques générés de la carte ; `board.html` : calendrier, pistes, Rivière, Livres, Crédit (généré par `build_board_html.py`).
- `bloc_v3.py` : cartouche unique Montréal – Québec – partis (v3.39), inséré par `build_map_html.py` à la place de la capsule Montréal, des encarts Congés et rade de Québec ; Domaine du Roi décalé à gauche, La Rochelle et Antilles descendus de 30 px. Gravure : `img/gravure_montreal.png`.
- Pour modifier : changer la source ou le générateur, puis relancer la chaîne ci-dessous. `npm install` installe les polices (package.json).

Plateau 8000 × 5904 px, mêmes positions que table_v3_32 (l'objet TTS garde sa taille).

0. `python3 prep_carte.py` (si la carte source a changé)
1. `python3 build_map_html.py` : à partir de `carte_src.html` (carte_etendue_tts.dc.html sans le runtime, images locales dans `img/`), produit `base.html` (fond, collines, étendues, eau), `over.html` (cartouches, liaisons, portages, textes, encarts, rose, légende) et `hills.html`.
2. `node shot2.js <page> 2800 1510 2.490857 <sortie> <transparent>` pour base_hd.png, over_hd.png (1) et hills_hd.png (1).
3. `python3 terrain_hd.py` : lacs, rivières, relief, forêts historiques (sous les éléments de jeu) → base_terrain_hd.png ; puis superposer over_hd.png → map_hd.png.
4. `python3 build_board_html.py` puis `node shot2.js board.html 5600 4133 1.428571 board_hd.png 0` (calendrier, pistes, Rivière, Livres, Crédit).
5. `python3 compose.py` → table_hd.png (archive PNG) ; le module utilise la version JPEG.
6. Module TTS : `python3 ../plateau_v3_39.py ../../` (image, points d'accroche, objets déplacés).

Polices : @fontsource (IM Fell English, IM Fell English SC, Alegreya Sans) ; texte de la carte en Liberation Serif.
