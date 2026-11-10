# Plateau HD (v3.38)

Plateau 8000 × 5904 px, mêmes positions que table_v3_32 (l'objet TTS garde sa taille).

1. `python3 build_map_html.py` : à partir de `carte_src.html` (carte_etendue_tts.dc.html sans le runtime, images locales dans `img/`), produit `base.html` (fond, collines, étendues, eau), `over.html` (cartouches, liaisons, portages, textes, encarts, rose, légende) et `hills.html`.
2. `node shot2.js <page> 2800 1510 2.490857 <sortie> <transparent>` pour base_hd.png, over_hd.png (1) et hills_hd.png (1).
3. `python3 terrain_hd.py` : lacs, rivières, relief, forêts historiques (sous les éléments de jeu) → base_terrain_hd.png ; puis superposer over_hd.png → map_hd.png.
4. `python3 build_board_html.py` puis `node shot2.js board.html 5600 4133 1.428571 board_hd.png 0` (calendrier, pistes, Rivière, Livres, Crédit).
5. `python3 compose.py` → table_hd.png (archive PNG) ; le module utilise la version JPEG.

Polices : @fontsource (IM Fell English, IM Fell English SC, Alegreya Sans) ; texte de la carte en Liberation Serif.
