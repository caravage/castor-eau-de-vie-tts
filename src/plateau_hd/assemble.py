# Assemble map_hd.png = base_terrain_hd.png + over_hd.png (étape 3 du README, écrite ici pour être rejouable).
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
b = Image.open('base_terrain_hd.png').convert('RGBA'); o = Image.open('over_hd.png').convert('RGBA')
Image.alpha_composite(b, o).convert('RGB').save('map_hd.png')
