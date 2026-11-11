# Cartouche unique « Montréal – Québec – partis » : un cadre, une grille, un seul style de panneau.
# Grille : Québec (pleine largeur) / Château | Palais / Montréal | Congés. Montréal reste en bas à gauche (liaisons).
DARK = '#2A2418'; CH_C = '#6B4423'; PA_C = '#2B3F5E'; GOLD = '#B7A675'; FIL = '#CFC3A4'; PAN = '#F6F0E1'
FS = 11.2
def ab(x, y, w, h, st='', inner=''):
    return f'<div style="position:absolute;left:{x:.1f}px;top:{y:.1f}px;width:{w:.1f}px;height:{h:.1f}px;{st}">{inner}</div>'
def txt(x, y, w, h, t, st=''):
    return ab(x, y, w, h, f"display:flex;align-items:center;font-family:'Liberation Serif',serif;font-size:{FS}px;line-height:1.25;color:{DARK};{st}", f'<div>{t}</div>')
def ico_conge(h=12):
    return (f'<svg viewBox="0 0 19 25" style="width:{h*.76:.1f}px;height:{h}px;vertical-align:-0.2em;margin:0 0.12em">'
            '<path d="M1 1 H13 L18 6 V24 H1 Z" fill="#FBF6EA" stroke="#5A5040" stroke-width="1.3" stroke-linejoin="round"/>'
            '<path d="M13 1 V6 H18" fill="none" stroke="#5A5040" stroke-width="1.3"/><path d="M4.5 11 H14.5 M4.5 15 H14.5 M4.5 19 H14.5" stroke="#5A5040" stroke-width="1.3"/></svg>')
def hexa(bg, sym, h=13):
    return (f'<svg viewBox="0 0 25 27" style="width:{h*25/27:.1f}px;height:{h}px;vertical-align:-0.2em;margin:0 0.12em">'
            f'<polygon points="12.5,1 23.5,7.25 23.5,19.75 12.5,26 1.5,19.75 1.5,7.25" fill="{bg}" stroke="{"#5A5040" if bg!="#1E1A16" else bg}" stroke-width="1.3"/>{sym}</svg>')
OFF = hexa('#FBF6EA', '<text x="12.5" y="18.8" text-anchor="middle" font-family="DejaVu Sans" font-size="14" fill="#B08A2E">⚜</text>')
MIS = hexa('#1E1A16', '<path d="M12.5 6.5 V21 M7.5 11.5 H17.5" stroke="#FBF6EA" stroke-width="3.4"/>')
def ring(cx, cy, r=12.8):
    return ab(cx - r, cy - r, 2 * r, 2 * r, f'box-sizing:border-box;border-radius:50%;border:1.4px solid {GOLD};background:#FBF7EC',
              f'<div style="position:absolute;inset:1.7px;border-radius:50%;border:0.7px solid {GOLD}"></div>')
def hline(x, y, w, c=FIL, t=0.9): return ab(x, y, w, t, f'background:{c}')
def panel(x, y, w, h, title, col=DARK, sub='', bg=''):
    # même panneau partout : fond clair, filet doré, titre en petites capitales entre deux filets
    tw = len(title) * 11.5 + 24
    o = ab(x, y, w, h, f'box-sizing:border-box;background:{PAN};border:1.5px solid {GOLD};border-radius:9px;overflow:hidden', bg)
    o += hline(x + 14, y + 20, (w - tw) / 2 - 14, GOLD, 1) + hline(x + (w + tw) / 2, y + 20, (w - tw) / 2 - 14, GOLD, 1)
    o += ab(x, y + 7, w, 26, f"text-align:center;font-family:'IM Fell English SC',serif;font-size:23px;line-height:1.1;color:{col}", title)
    if sub: o += ab(x, y + 32, w, 13, f"text-align:center;font-family:'IM Fell English',serif;font-style:italic;font-size:10.5px;line-height:1.2;color:{col}", sub)
    return o
X0, X1, Y0, Y1 = 2003, 2786, 11, 801
H = []
H.append('<svg viewBox="0 0 3215 1500" style="position:absolute;left:0;top:0;width:3215px;height:1500px;overflow:visible;pointer-events:none">'
         f'<rect x="{X0}" y="{Y0}" width="{X1-X0}" height="{Y1-Y0}" rx="14" fill="#E8DCBD" stroke="{DARK}" stroke-width="3.6"/>'
         f'<rect x="{X0+6}" y="{Y0+6}" width="{X1-X0-12}" height="{Y1-Y0-12}" rx="10" fill="none" stroke="#9C8C68" stroke-width="1.1"/></svg>')
P = 13; G = 11
cL0, cL1 = X0 + P, (X0 + X1) / 2 - G / 2
cR0, cR1 = (X0 + X1) / 2 + G / 2, X1 - P
# ---- rangée 1 : Québec (rade : 4 navires × 5 cases, en 2 couloirs de 2)
ph = 412; qh = 176; py = Y0 + P; qy = py + ph + G
H.append(panel(cL0, qy, cR1 - cL0, qh, 'Québec'))
lane_w = (cR1 - cL0 - 2 * 14 - 26) / 2; cg = 6; cw = (lane_w - 5 * cg) / 6; ch = 54
for r in range(2):
    for ln in range(2):
        lx = cL0 + 14 + ln * (lane_w + 26); y = qy + 44 + r * (ch + 12)
        H.append(hline(lx + cw, y + ch / 2 - 0.8, lane_w - cw, '#C5B78C', 1.6))
        for j in range(6):
            ship = '<img src="img/navire_gravure.png" alt="" style="position:absolute;left:10%;top:10%;width:80%;height:80%;object-fit:contain;opacity:0.32">' if j == 0 else ''
            H.append(ab(lx + j * (cw + cg), y, cw, ch, f'box-sizing:border-box;background:{"#EDE3CC" if j == 0 else "#FBF7EC"};border:1.5px solid #C2B07C;border-radius:6px;overflow:hidden', ship))
# ---- rangée 2 : Château | Palais (même gabarit)

def parti(x0, x1, nom, col, sub, l1, l2, membre, zt, zin, znote):
    o = panel(x0, py, x1 - x0, ph, nom, col, sub)
    y = py + 52; rh = 56
    for i, t in enumerate((l1, l2, '')):
        yy = y + i * rh
        o += hline(x0 + 12, yy, x1 - x0 - 24)
        o += ab(x0 + 12, yy, 18, rh, f"display:flex;align-items:center;font-family:'Liberation Serif',serif;font-weight:bold;font-size:15px;color:{col}", str(i + 1))
        o += ring(x0 + 50, yy + rh / 2)
        o += txt(x0 + 74, yy, x1 - x0 - 86, rh, t)
    yy = y + 3 * rh; o += hline(x0 + 12, yy, x1 - x0 - 24)
    o += txt(x0 + 12, yy, 70, 46, 'Par membre', f"font-family:'IM Fell English',serif;font-style:italic;font-size:12.5px;line-height:1.05;color:{col}")
    o += txt(x0 + 74, yy, x1 - x0 - 86, 46, membre)
    yy += 46; o += hline(x0 + 12, yy, x1 - x0 - 24)
    o += ab(x0, yy + 5, x1 - x0, 15, f"text-align:center;font-family:'IM Fell English',serif;font-style:italic;font-size:13px;color:{col}", zt)
    bh = py + ph - 12 - (yy + 22)
    o += ab(x0 + 14, yy + 22, x1 - x0 - 28, bh, f'box-sizing:border-box;border:1.3px dashed {GOLD};border-radius:6px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px', zin + (f"<div style=\"font-family:'Liberation Serif',serif;font-size:{FS}px;color:{DARK}\">{znote}</div>" if znote else ''))
    return o
CUBE = ('<svg viewBox="0 0 100 110" style="width:30px;height:33px"><path d="M50 4 L94 28 L50 52 L6 28 Z" fill="#F7F1E2" stroke="#D6CBAE" stroke-width="3"/>'
        '<path d="M6 28 L50 52 L50 104 L6 80 Z" fill="#EFE7D3" stroke="#D6CBAE" stroke-width="3"/><path d="M94 28 L50 52 L50 104 L94 80 Z" fill="#E9E0C9" stroke="#D6CBAE" stroke-width="3"/></svg>')
LIV = '<div style="font-size:40px;line-height:1;color:#E0D3B2;font-family:\'Liberation Serif\',serif">₶</div>'
H.append(parti(cL0, cL1, 'Parti du Gouverneur', CH_C, 'l’Épée · le gouverneur', f'Attribue le premier congé{ico_conge()}de chaque joueur.',
               f'Pour 1 ₶, ajoute un officier{OFF}à son expédition.', f'1 congé{ico_conge()}de plus est émis.', 'Milices', CUBE, '2 ₶ : ajoute une milice dans un fort.'))
H.append(parti(cR0, cR1, 'Parti de l’Intendant', PA_C, 'la Robe · l’intendant', 'Attribue le budget de la colonie.',
               f'Pour 1 ₶, ajoute un missionnaire{MIS}à son expédition.', '+1 dé de vérification de la contrebande à Albany.', 'Caisse de la colonie', LIV, ''))
# ---- rangée 3 : Montréal | Congés
my = qy + qh + G; mh = Y1 - P - my
GRAV = '<img src="img/gravure_montreal.png" alt="" style="position:absolute;left:0;top:0;width:100%;height:100%;object-fit:cover;object-position:50% 60%;opacity:0.2;filter:grayscale(1) sepia(0.35)">'
H.append(panel(cL0, my, cL1 - cL0, mh, 'Montréal', DARK, '', GRAV))
ow, oh = 43, 54
for k in range(3):
    H.append(ab((cL0 + cL1) / 2 - (3 * ow + 2 * 16) / 2 + k * (ow + 16), my + 44 + (mh - 44 - oh) / 2 - 4, ow, oh,
                'box-sizing:border-box;border-radius:50%;border:2.3px dashed #8F8572;background:rgba(251,247,236,0.85)'))
EMB = '<img src="img/embleme_conges.png" alt="" style="position:absolute;left:50%;top:34px;height:calc(100% - 40px);transform:translateX(-50%);opacity:0.22;filter:grayscale(1) sepia(0.25)">'
H.append(panel(cR0, my, cR1 - cR0, mh, 'Congés', DARK, '', EMB))
BLOC = ''.join(H)
