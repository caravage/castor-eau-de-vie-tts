# Cartes de navire et de distillerie (v20), jetons navire et pions distillerie avec leur nom.
# Exécuté à la fin de gen2.py (mêmes fonctions page/MANIFEST, mêmes polices). Images sources dans assets/.
import shutil
for a in ('navire_gravure', 'alambic_gravure'): shutil.copy(f'assets/{a}.png', f'img/{a}.png')

BROWN, COPPER, COPPER_L, COPPER_D = '#4A3324', '#8A4B2A', '#B87333', '#5C3216'
CSS20 = (f".t20{{font-family:{DISP};font-size:32px;fill:#F6EFDC}}.lv{{font-family:{BODY};font-weight:700;font-size:15px;fill:{MUTED}}}"
         f".fd{{font-family:{SER};font-style:italic;font-size:13px;fill:{MUTED}}}.lb{{font-family:{SER};font-style:italic;font-size:17px;fill:{MUTED}}}"
         f".rl{{font-family:{BODY};font-size:13.5px;fill:{INK}}}.rl2{{font-family:{BODY};font-size:12px;fill:{MUTED}}}.nm{{font-family:{DISP};fill:{INK}}}")
ALAMBIC = (f"<ellipse cx='104' cy='160' rx='82' ry='68' fill='{COPPER_L}' stroke='{COPPER_D}' stroke-width='8'/>"
           f"<path d='M104 92 L104 36 L190 36 L190 132' fill='none' stroke='{COPPER_D}' stroke-width='9' stroke-linecap='round'/>"
           f"<rect x='170' y='130' width='40' height='50' rx='6' fill='{COPPER_L}' stroke='{COPPER_D}' stroke-width='6'/>")

def svg2(name, w, h, k, inner):   # dessin en unités w×h, rendu k fois plus grand
    page(name, w * k, h * k, f"<svg xmlns='http://www.w3.org/2000/svg' width='{w*k}' height='{h*k}' viewBox='0 0 {w} {h}'>{inner}</svg>", CSS20)

def frame20(title, color):
    W, H = 600, 320
    c = lambda x, y, r: f"<g transform='translate({x} {y}) rotate({r})'><path d='M0 0 L22 0 M0 0 L0 22' stroke='{EDGE}' stroke-width='2'/><circle cx='6' cy='6' r='2.5' fill='{EDGE}'/></g>"
    return (f"<rect x='4' y='4' width='{W-8}' height='{H-8}' rx='20' fill='{PAPER}' stroke='{EDGE}' stroke-width='5'/>"
            f"<rect x='13' y='13' width='{W-26}' height='{H-26}' rx='13' fill='none' stroke='{INK}' stroke-width='.8' opacity='.45'/>"
            + c(19, 19, 0) + c(W - 19, 19, 90) + c(W - 19, H - 19, 180) + c(19, H - 19, 270)
            + f"<path d='M44 26 L{W-44} 26 L{W-30} 50 L{W-44} 74 L44 74 L30 50 Z' fill='{color}'/>"
            f"<path d='M46 30 L{W-46} 30 L{W-35} 50 L{W-46} 70 L46 70 L35 50 Z' fill='none' stroke='#E7C27A' stroke-width='.8' opacity='.7'/>"
            f"<text x='{W/2}' y='61' text-anchor='middle' class='t20'>{E(title)}</text>")

def coins(n, x0, step, cy=176):
    s = ''
    for k in range(n):
        cx = x0 + k * step
        s += (f"<circle cx='{cx}' cy='{cy+2}' r='27' fill='#000' opacity='.10'/><circle cx='{cx}' cy='{cy}' r='27' fill='#FFFDF6' stroke='{INK}' stroke-width='1.6'/>"
              f"<circle cx='{cx}' cy='{cy}' r='22' fill='none' stroke='{EDGE}' stroke-width='1.2' stroke-dasharray='3 3'/><text x='{cx}' y='{cy+48}' text-anchor='middle' class='lv'>{k+1} ₶</text>")
    return s

def short(nm): return nm.split(' ', 1)[1] if nm.startswith(('Le ', 'La ')) else nm.replace('L’', '')

# Navires : carte (case du jeton, 5 parts, fondateur) et jeton gravé avec étiquette du nom
for i, nm in enumerate(SHIPS):
    tx, ty, tw, th = 26, 96, 176, 154
    body = (frame20(nm, BROWN)
            + f"<rect x='{tx}' y='{ty}' width='{tw}' height='{th}' rx='12' fill='#EFE6CF' stroke='{EDGE}' stroke-width='2'/>"
            f"<rect x='{tx+6}' y='{ty+6}' width='{tw-12}' height='{th-12}' rx='8' fill='none' stroke='{INK}' stroke-width='1' stroke-dasharray='4 4' opacity='.45'/>"
            f"<image href='../img/navire_gravure.png' x='{tx+20}' y='{ty+12}' width='{tw-40}' height='{th-24}' opacity='.18'/>"
            f"<text x='{tx+tw/2}' y='{ty+th+20}' text-anchor='middle' class='lb'>Navire</text>"
            + coins(5, 262, 67) + "<text x='262' y='138' text-anchor='middle' class='fd'>fondateur</text>"
            + f"<line x1='232' y1='262' x2='566' y2='262' stroke='{EDGE}' stroke-width='1'/>"
            "<text x='399' y='286' text-anchor='middle' class='rl'>Armé à 5 parts : la carte va au premier armateur</text>"
            "<text x='399' y='302' text-anchor='middle' class='rl2'>(le plus de parts ; le fondateur en cas d’égalité)</text>")
    svg2(f'carte_navire_{i+1}', 600, 320, 2, body)
    fs = 30 if len(short(nm)) <= 14 else 24
    svg2(f'navire_{i+1}', 320, 280, 2,
         f"<rect x='4' y='4' width='312' height='272' rx='26' fill='{PAPER}' stroke='{BROWN}' stroke-width='8'/>"
         f"<image href='../img/navire_gravure.png' x='52' y='14' width='216' height='192'/>"
         f"<rect x='22' y='212' width='276' height='48' rx='10' fill='{PAPER}' stroke='{INK}' stroke-width='2.5'/>"
         f"<text x='160' y='{236+fs*0.33:.0f}' text-anchor='middle' class='nm' style='font-size:{fs}px'>{E(short(nm))}</text>")

# Distilleries : 4 parts, chaque carte a son pion alambic cuivre portant le nom du lieu
DISTILLERIES = [('Fonds-Saint-Jacques', 'Fonds-St-Jacques'), ('La Lise', 'La Lise'), ('Petit-Goâve', 'Petit-Goâve'), ('Saint-Louis', 'Saint-Louis')]
BOTTLE = (f"<g transform='translate(487 275) scale(.72)'><path d='M5 0 h8 v7 q7 4 7 12 v20 q0 4 -4 4 h-14 q-4 0 -4 -4 v-20 q0 -8 7 -12 z' fill='{COPPER}' stroke='{INK}' stroke-width='1.3'/>"
          f"<rect x='3' y='18' width='12' height='9' rx='1.5' fill='{PAPER}'/></g>")
for i, (nm, sh) in enumerate(DISTILLERIES):
    cx, cy = 114, 173
    body = (frame20(nm, COPPER)
            + f"<circle cx='{cx}' cy='{cy}' r='64' fill='#EFE6CF' stroke='{EDGE}' stroke-width='2'/>"
            f"<image href='../img/alambic_gravure.png' x='{cx-56}' y='{cy-56}' width='112' height='112' opacity='.22'/>"
            f"<circle cx='{cx}' cy='{cy}' r='56' fill='none' stroke='{COPPER_L}' stroke-width='1.5' stroke-dasharray='4 4'/>"
            f"<g transform='translate({cx-36} {cy-40}) scale(.33)' opacity='.9'>{ALAMBIC}</g>"
            f"<text x='{cx}' y='{cy+90}' text-anchor='middle' class='lb'>Distillerie</text>"
            + coins(4, 280, 80)
            + f"<line x1='232' y1='262' x2='566' y2='262' stroke='{EDGE}' stroke-width='1'/>"
            "<text x='482' y='292' text-anchor='end' class='rl'>Construite à 4 parts. Produit 4</text>" + BOTTLE)
    svg2(f'carte_distillerie_{i+1}', 600, 320, 2, body)
    fs = 24 if len(sh) > 11 else 28
    svg2(f'pion_distillerie_{i+1}', 220, 300, 2,
         ALAMBIC + f"<rect x='8' y='246' width='204' height='46' rx='10' fill='{PAPER}' stroke='{INK}' stroke-width='2.5'/>"
         f"<text x='110' y='{269+fs*0.33:.0f}' text-anchor='middle' class='nm' style='font-size:{fs}px'>{E(sh)}</text>")

# Une seule entrée par image (les versions v20 remplacent les anciennes)
_seen = {}
for e in MANIFEST: _seen[e[0]] = e
MANIFEST[:] = list(_seen.values())
