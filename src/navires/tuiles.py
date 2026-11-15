# Tuiles de navire v45 (640 × 560) : 6 navires des joueurs × 4 états (neutre, rouge, bleu, vert), la Compagnie, Le Profond.
import os, subprocess, sys
sys.argv = [sys.argv[0]]
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'maquette.py')).read().split('pages = [')[0]
exec(src)
OUT = os.path.abspath(f'{HERE}/../../img/v18')
NOMS = ["L’Aigle d’Or", "Le Courageux", "Le Jardin de Hollande", "Le Saint-Jean-Baptiste", "La Famille", "Le Vieux Siméon"]
def rendu(nom, body):
    p = f'{HERE}/{nom}.html'
    open(p, 'w').write(f"<!doctype html><html><head><meta charset='utf-8'><link rel='stylesheet' href='file://{FONTS}'><style>{CSS}</style></head><body>{body}</body></html>")
    subprocess.run(['google-chrome', '--headless=new', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files', '--force-device-scale-factor=2',
                    '--default-background-color=00000000', '--virtual-time-budget=3000', f'--screenshot={OUT}/{nom}.png', '--window-size=320,280', f'file://{p}'], capture_output=True)
for k, n in enumerate(NOMS):
    fs = 27 if len(n) <= 14 else 22 if len(n) <= 19 else 19
    for e in ETATS:
        rendu(f'navire45_{k+1}_{e}', joueur(n, e).replace("<div class='nm' style='", f"<div class='nm' style='font-size:{fs}px;"))
rendu('navire45_compagnie', compagnie()); rendu('navire45_profond', profond())
print('ok')
