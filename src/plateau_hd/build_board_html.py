# Plateau HD (hors carte) : mêmes positions que table_v3_32 (repère 5600 × 4133), rendu à 8000 px.
INK = '#2A2418'; PAR = '#F2EAD3'; EDGE = '#B7A675'; BG = '#E6DAB6'; BROWN = '#8B5A14'; MUT = '#6B5F45'
SC = "font-family: 'IM Fell English SC', serif"; SANS = "font-family: 'Alegreya Sans', sans-serif"; IT = "font-family: 'IM Fell English', serif; font-style: italic"
H = []
def box(x, y, w, h, st='', inner=''):
    H.append(f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;box-sizing:border-box;{st}">{inner}</div>')
def text(x, y, s, st, anchor='left', w=None):
    if anchor == 'center':
        H.append(f'<div style="position:absolute;left:{x - 400}px;top:{y}px;width:800px;text-align:center;transform:translateY(-50%);white-space:nowrap;{st}">{s}</div>')
    else:
        H.append(f'<div style="position:absolute;left:{x}px;top:{y}px;transform:translateY(-50%);white-space:nowrap;{st}">{s}</div>')
# fond
box(0, 0, 5600, 4133, 'background:#22332F')
box(0, 0, 657, 4133, 'background:#231B15')
box(678, 20, 5100, 4094, f'background:{BG};border-radius:50px')
# ---------- Rivière
text(36, 527, 'Rivière', f'{SC};font-size:62px;color:#EFE6D0')
DASH = ""
H.append('<svg style="position:absolute;left:46px;top:625px;width:329px;height:456px;overflow:visible"><rect x="1.3" y="1.3" width="326.4" height="453.4" rx="22" fill="none" stroke="#8C7D5F" stroke-width="2.6" stroke-dasharray="22 12"/></svg>')
for k, (y0, n) in enumerate(((1208, 3), (1780, 2), (2353, 1))):
    box(46, y0, 329, 456, f'background:{PAR};border:2.6px solid #B7A675;border-radius:20px')
    yl = y0 + 456 + 61
    H.append(f'<div style="position:absolute;left:{195 - 20}px;top:{yl - 20}px;width:40px;height:40px;box-sizing:border-box;border:2.2px solid #EFE6D0;border-radius:50%;'
             f'display:flex;align-items:center;justify-content:center;font-family:\'IM Fell English\',serif;font-size:38px;line-height:1;color:#EFE6D0;padding-bottom:4px">{n}</div>')
    text(226, yl - 8, '₶', f"font-family:'IM Fell English',serif;font-size:46px;color:#EFE6D0")
H.append('<svg style="position:absolute;left:46px;top:2925px;width:329px;height:456px;overflow:visible"><rect x="1.3" y="1.3" width="326.4" height="453.4" rx="22" fill="none" stroke="#8C7D5F" stroke-width="2.6" stroke-dasharray="22 12"/></svg>'); box(46, 2925, 329, 456, '', f'<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;{SANS};font-size:34px;color:#B5A684">Défausse</div>')
# ---------- calendrier
text(753, 118, 'Calendrier', f'{SC};font-size:66px;color:{INK}')
text(1196, 116, 'Tour', f'{SANS};font-size:41px;color:{MUT}')
for i, r in enumerate(['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII']):
    box(1352 + i * 123.4, 60, 106, 103, f'background:{PAR};border:3px solid #C0B081;border-radius:14px',
        f'<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;{SANS};font-weight:700;font-size:42px;color:#A99C7C">{r}</div>')
HATCH = 'background:repeating-linear-gradient(45deg,#D2DFE9 0 16px,#A8BCD2 16px 19px,#D2DFE9 19px 29px,#F5F8FA 29px 32px)'
MONTHS = [('Printemps', ['Départ de', 'La Rochelle'], None, 'background:#E3EBD6;border:4px solid #88A275'),
          ('Avril', ['Congés sur 3+'], None, HATCH + ';border:5px solid #5D8E98'),
          ('Mai', ['Congés sur 2+'], None, ''), ('Juin', ['Congés'], None, ''), ('Juillet', [], ['Rivière'], ''),
          ('Août', [], None, ''), ('Septembre', [], None, ''), ('Octobre', [], ['Départ des', 'vaisseaux'], ''),
          ('Novembre', [], None, HATCH + ';border:5px solid #5D8E98'), ('Hiver', [], None, 'background:#22332F;border:none')]
for i, (nm, sub, low, st) in enumerate(MONTHS):
    x = 731 + 482.6 * i; w = 464
    base = f'background:{PAR};border:4px solid {EDGE};border-radius:22px;' + st
    inner = ''
    col = '#EFE6D0' if nm == 'Hiver' else INK
    halo = 'text-shadow:0 0 6px #D2DFE9,0 0 3px #D2DFE9;' if 'repeating' in st else ''
    inner += f'<div style="position:absolute;left:34px;top:44px;{SC};font-size:66px;line-height:1;color:{col};{halo}">{nm}</div>'
    for j, s in enumerate(sub):
        inner += f'<div style="position:absolute;left:34px;top:{133 + j * 58}px;{SANS};font-weight:700;font-size:43px;line-height:1.1;color:{BROWN};{halo}">{s}</div>'
    if nm not in ('Printemps', 'Hiver'):
        inner += f'<div style="position:absolute;left:16px;right:16px;top:203px;height:3px;background:repeating-linear-gradient(90deg,#A99668 0 11px,transparent 11px 20px)"></div>'
    for j, s in enumerate(low or []):
        y0 = 280 if len(low) == 1 else 250
        inner += f'<div style="position:absolute;left:34px;top:{y0 + j * 57}px;{SANS};font-weight:700;font-size:43px;line-height:1.1;color:{BROWN}">{s}</div>'
    box(x, 195, w, 418, base, inner)
# ---------- pistes Ravages / Prix du castor
def track(x0, x1, title, cxs, labels, special):
    w = x1 - x0; inner = ''
    inner += (f'<div style="position:absolute;left:0;right:0;top:30px;display:flex;align-items:center;justify-content:center;gap:34px">'
              f'<div style="width:{(w - 420) / 2 - 40}px;border-top:2px solid {EDGE}"></div>'
              f'<div style="{IT};font-size:60px;line-height:1;color:{INK}">{title}</div>'
              f'<div style="width:{(w - 420) / 2 - 40}px;border-top:2px solid {EDGE}"></div></div>')
    for cx, lab in zip(cxs, labels):
        ring, wd, tc = special.get(lab, ('#C8B98F', 4, MUT))
        inner += (f'<div style="position:absolute;left:{cx - x0 - 50.5}px;top:{785 - 622 - 50.5}px;width:101px;height:101px;box-sizing:border-box;border-radius:50%;'
                  f'background:{PAR};border:{wd}px solid {ring};box-shadow:inset 0 0 0 5px {PAR},inset 0 0 0 6.5px #D8CBA6"></div>'
                  f'<div style="position:absolute;left:{cx - x0 - 40}px;top:{867 - 622 - 20}px;width:80px;text-align:center;{SANS};font-weight:700;font-size:30px;line-height:40px;color:{tc}">{lab}</div>')
    box(x0, 622, w, 276, 'background:#F3EFE2;border:3px solid #968C78;border-radius:18px', inner)
track(1700, 2638, 'Ravages', [1833 + 108.7 * i for i in range(7)], [str(i) for i in range(7)],
      {'4': ('#B86F14', 5, '#B86F14'), '6': ('#A84C3C', 5, '#A84C3C')})
track(3560, 4578, 'Prix du castor', [3694 + 108.6 * i for i in range(8)], [str(i) for i in range(1, 9)], {})
# ---------- Livres / Crédit
text(753, 3726, 'Livres (₶)', f'{SC};font-size:58px;color:{INK}')
text(752, 3805, 'capital', f'{SANS};font-style:italic;font-size:34px;color:#8B704A')
V = [0, 1, 2, 3, 4, 5, 6, 7, 7, 8, 9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 14, 14, 15, 15, 15, 15, 15, 15, 15, 15]
pas = (4399 - 1046) / 31
for i in range(31):
    x = 1046 + pas * i + 3.6; w = pas - 7.2
    big = i % 5 == 0
    lab = '30+' if i == 30 else str(i)
    st = f'background:{PAR};border:{5 if big else 3}px solid {"#7A5434" if big else "#C0B081"};border-radius:12px'
    fs = 34 if i == 30 else 40
    box(x, 3676, w, 100, st, f'<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;{SANS};font-weight:{700 if big else 400};font-size:{fs}px;color:{MUT}">{lab}</div>')
    cx = 1046 + pas * (i + 0.5)
    if i == 0 or V[i] != V[i - 1]:
        H.append(f'<div style="position:absolute;left:{cx - 40}px;top:3786px;width:80px;text-align:center;{SANS};font-weight:500;font-size:34px;line-height:40px;color:#8B704A">{V[i]}</div>')
    else:
        H.append(f'<div style="position:absolute;left:{cx - 2.5}px;top:3800px;width:5px;height:4px;background:#BEAC86"></div>')
text(753, 3910, 'Crédit', f'{SC};font-size:58px;color:{INK}')
CR = {10: ('#7A1F18', '#7A1F18', '#FFFFFF'), 9: ('#7A1F18', '#7A1F18', '#FFFFFF'),
      8: ('#E3AFA5', '#A3352A', '#7A1F18'), 7: ('#E3AFA5', '#A3352A', '#7A1F18'), 6: ('#E3AFA5', '#A3352A', '#7A1F18'),
      5: ('H', '#A3352A', '#7A1F18'), 4: ('H', '#A3352A', '#7A1F18'), 3: ('H', '#A3352A', '#7A1F18'),
      2: (PAR, '#C0B081', INK), 1: (PAR, '#C0B081', INK), 0: (PAR, '#C0B081', INK)}
for i, v in enumerate(range(10, -1, -1)):
    x = 1046 + pas * i + 3.6; w = pas - 7.2
    bgc, bd, tc = CR[v]
    bgs = 'background:repeating-linear-gradient(-45deg,#F2E3D6 0 11px,#D88F80 11px 13.5px)' if bgc == 'H' else f'background:{bgc}'
    box(x, 3860, w, 100, f'{bgs};border:3px solid {bd};border-radius:12px',
        f'<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;{SANS};font-weight:700;font-size:38px;color:{tc}">{v}</div>')
def brace(i0, i1, lab, col, tc):
    xa = 1046 + pas * i0 + 12; xb = 1046 + pas * (i1 + 1) - 12; xm = (xa + xb) / 2
    H.append(f'<svg style="position:absolute;left:0;top:0;width:5600px;height:4133px;overflow:visible" viewBox="0 0 5600 4133">'
             f'<path d="M{xa} 3966 Q{xa} 3986 {xa + 18} 3986 L{xm - 18} 3986 Q{xm} 3986 {xm} 4003 Q{xm} 3986 {xm + 18} 3986 L{xb - 18} 3986 Q{xb} 3986 {xb} 3966" '
             f'fill="none" stroke="{INK}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"/></svg>')
    H.append(f'<div style="position:absolute;left:{xm - 52}px;top:4003px;width:104px;height:54px;box-sizing:border-box;border:3px solid {col};border-radius:12px;background:#EDE2C6;'
             f'display:flex;align-items:center;justify-content:center;{SANS};font-weight:700;font-size:34px;color:{tc}">{lab}</div>')
brace(0, 1, '—', '#A3352A', '#A3352A'); brace(2, 4, '2 ₶', '#A3352A', '#A3352A'); brace(5, 7, '4 ₶', '#A3352A', '#A3352A'); brace(8, 9, '6 ₶', INK, INK)
open('board.html', 'w').write('<!doctype html><html lang="fr"><head><meta charset="utf-8"><link rel="stylesheet" href="fonts.css"><style>html,body{margin:0}'
                              '.r{position:relative;width:5600px;height:4133px;overflow:hidden}</style></head><body><div class="r">' + '\n'.join(H) + '</div></body></html>')
print('ok', len(H))
