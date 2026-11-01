# Éléments v42 (31 oct. 2026) : voyageurs ovales (recto effet, verso « Utilisé »), pion Livres réversible « 30+ ».
VOY42 = [('guide', 'Guide', '#2F5E4A', 46, ['+1 au dé', 'raccourci.', 'Mouv.', 'gratuit.']),
         ('int', 'Interprète', '#8A5A14', 42, ['Annule', '1 tuile', 'secrète.']),
         ('hiv', 'Hivernant', '#3E5A7A', 42, ['Répare', '1 canot.', 'Peut', 'hiverner.'])]   # v45 : textes courts, police agrandie
for k, n, c, fs, lines in VOY42:
    LH = 48; tot = 46 + 22 + len(lines) * LH; y0 = 216 - tot / 2
    svg(f'voy_{k}', 300, 432, f"<ellipse cx='150' cy='216' rx='142' ry='208' fill='{c}' stroke='#2A2418' stroke-width='6'/><ellipse cx='150' cy='216' rx='122' ry='186' fill='#F2EAD3' stroke='#2A2418' stroke-width='2'/>"
        + T(150, y0 + 40, n, fs, 'middle', fam=DISP, fill=c) + ''.join(T(150, y0 + 66 + 38 + i * LH, l, 42, 'middle', weight=600) for i, l in enumerate(lines)))
    svg(f'voy_{k}_used', 300, 432, f"<ellipse cx='150' cy='216' rx='142' ry='208' fill='{c}' stroke='#2A2418' stroke-width='6'/><ellipse cx='150' cy='216' rx='122' ry='186' fill='none' stroke='#F2EAD3' stroke-width='2' opacity='.6'/>"
        + T(150, 206, n, fs, 'middle', fam=DISP, fill='#F2EAD3') + f"<text x='150' y='246' text-anchor='middle' font-family=\"{BODY}\" font-weight='700' font-size='24' letter-spacing='2' fill='#F2EAD3'>UTILISÉ</text>")
PCOL42 = {'rouge': ('#A8322A', '#5E1E17'), 'bleu': ('#2F5E8E', '#1B3A5C'), 'vert': ('#4E7A2C', '#2E4A18')}   # couleurs des joueurs (build3 : PC)
for pn, (c, d) in PCOL42.items():
    ring = f"<circle cx='80' cy='80' r='74' fill='{c}' stroke='{d}' stroke-width='6'/><circle cx='80' cy='80' r='56' fill='none' stroke='#F6EFDC' stroke-width='3' opacity='.4'/>"
    svg(f'disc_livres_{pn}', 160, 160, ring)
    svg(f'disc_livres_{pn}_30', 160, 160, ring + f"<text x='80' y='96' text-anchor='middle' font-family=\"{BODY}\" font-weight='700' font-size='46' fill='#FFFFFF'>+30</text>")
_seen = {}
for _m in MANIFEST: _seen[_m[0]] = _m
MANIFEST[:] = list(_seen.values())
