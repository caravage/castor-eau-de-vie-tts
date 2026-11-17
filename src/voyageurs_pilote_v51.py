# Jeton Pilote v3.51 (16 nov. 2026) : « Sans jet aux rapides » (remplace « +1 au rapide »), gabarit voy2 de voyageurs_voy2.py.
# Usage (depuis src/) : python3 voyageurs_pilote_v51.py <dossier de sortie>
import sys
sys.argv = [sys.argv[0], sys.argv[1] if len(sys.argv) > 1 else 'out']
src = open('voyageurs_voy2.py').read(); ns = {'__name__': 'pilote'}
exec(src[:src.index("if __name__ == '__main__':")], ns)
B = '#4E8C99'
RAPIDE = ("<svg width='120' height='120' viewBox='0 0 120 120'><circle cx='60' cy='60' r='54' fill='none' stroke='#2A2418' stroke-width='5'/>"
          f"<line x1='86' y1='38' x2='42' y2='38' stroke='{B}' stroke-width='8'/><path d='M46 24 L26 38 L46 52 Z' fill='{B}'/>"
          + ''.join(f"<polyline points='{x},{y+8} {x+7},{y} {x+14},{y+8}' fill='none' stroke='{B}' stroke-width='5' stroke-linejoin='round' stroke-linecap='round'/>"
                    for y, xs in ((66, (29, 46, 63, 80)), (80, (37, 54, 71))) for x in xs) + "</svg>")
ns['jeton']('pilote2', 'Pilote', '#2F5A7A', RAPIDE, "<span style='font-size:44px'>Sans jet</span>", 'aux rapides')
