# Éléments v42 (31 oct. 2026) : voyageurs ovales (recto effet, verso « Utilisé »), pion Livres réversible « 30+ ».
VOY42 = [('guide', 'Guide', '#2F5E4A', 30, ['+1 au dé', 'du frasil et', 'des raccourcis']),
         ('int', 'Interprète', '#8A5A14', 29, ['Annule une fois', 'une tuile secrète', 'négative', '(sauf Ruine)']),
         ('hiv', 'Hivernant', '#3E5A7A', 29, ['Répare le canot', 'une fois. Hiverne', 'dans un Pays :', '1 tuile grasse'])]
for k, n, c, fs, lines in VOY42:
    tot = 34 + 14 + len(lines) * 27; y0 = 216 - tot / 2 + 8
    svg(f'voy_{k}', 300, 432, f"<ellipse cx='150' cy='216' rx='142' ry='208' fill='{c}' stroke='#2A2418' stroke-width='6'/><ellipse cx='150' cy='216' rx='122' ry='186' fill='#F2EAD3' stroke='#2A2418' stroke-width='2'/>"
        + T(150, y0 + 28, n, fs, 'middle', fam=DISP, fill=c) + ''.join(T(150, y0 + 68 + i * 27, l, 21, 'middle') for i, l in enumerate(lines)))
    svg(f'voy_{k}_used', 300, 432, f"<ellipse cx='150' cy='216' rx='142' ry='208' fill='{c}' stroke='#2A2418' stroke-width='6'/><ellipse cx='150' cy='216' rx='122' ry='186' fill='none' stroke='#F2EAD3' stroke-width='2' opacity='.6'/>"
        + T(150, 206, n, fs, 'middle', fam=DISP, fill='#F2EAD3') + f"<text x='150' y='246' text-anchor='middle' font-family=\"{BODY}\" font-weight='700' font-size='24' letter-spacing='2' fill='#F2EAD3'>UTILISÉ</text>")
svg('disc_livres', 160, 160, "<circle cx='80' cy='80' r='74' fill='#FFFFFF' stroke='#3A3A3A' stroke-width='6'/><circle cx='80' cy='80' r='56' fill='none' stroke='#3A3A3A' stroke-width='3' opacity='.35'/>")
svg('disc_livres_30', 160, 160, "<circle cx='80' cy='80' r='74' fill='#FFFFFF' stroke='#3A3A3A' stroke-width='6'/><circle cx='80' cy='80' r='56' fill='none' stroke='#3A3A3A' stroke-width='3' opacity='.35'/>"
    f"<text x='80' y='96' text-anchor='middle' font-family=\"{BODY}\" font-weight='700' font-size='46' fill='#1E1E1E'>30+</text>")
_seen = {}
for _m in MANIFEST: _seen[_m[0]] = _m
MANIFEST[:] = list(_seen.values())
