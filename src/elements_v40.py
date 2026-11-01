# Éléments v40 (31 oct. 2026) : forts (France : fleur de lys d'or sur blanc ; Grande-Bretagne : Union de 1707) et pions lettrés.
FLEUR_LYS = ("<path d='M0-50C9-38 13-24 11-10C10-2 6 4 0 9C-6 4-10-2-11-10C-13-24-9-38 0-50Z'/>"
             "<path d='M-4 6C-8-6-16-14-27-13C-38-12-44-2-41 8C-38 17-28 20-21 15C-26 12-28 6-25 1C-21-4-13-2-9 5Z'/>"
             "<path d='M4 6C8-6 16-14 27-13C38-12 44-2 41 8C38 17 28 20 21 15C26 12 28 6 25 1C21-4 13-2 9 5Z'/>"
             "<rect x='-17' y='9' width='34' height='7' rx='1.5'/><path d='M-5 16H5L3 32C2 40 0 46 0 50C0 46-2 40-3 32Z'/>"
             "<path d='M-7 16C-12 24-20 28-28 26C-24 33-14 34-8 27Z'/><path d='M7 16C12 24 20 28 28 26C24 33 14 34 8 27Z'/>")
svg('fort_fr', 220, 220, "<rect x='10' y='10' width='200' height='200' rx='34' fill='#FFFFFF' stroke='#2A2418' stroke-width='8'/>"
    f"<g transform='translate(110 110) scale(1.55)' fill='#D4A62A' stroke='#8A6418' stroke-width='1.2'>{FLEUR_LYS}</g>")
svg('fort_uk', 220, 220, "<defs><clipPath id='u'><rect x='10' y='10' width='200' height='200' rx='34'/></clipPath></defs><g clip-path='url(#u)'>"
    "<rect x='10' y='10' width='200' height='200' fill='#012169'/><path d='M10 10L210 210M210 10L10 210' stroke='#FFFFFF' stroke-width='40'/>"
    "<path d='M110 10V210M10 110H210' stroke='#FFFFFF' stroke-width='64'/><path d='M110 10V210M10 110H210' stroke='#C8102E' stroke-width='38'/></g>"
    "<rect x='10' y='10' width='200' height='200' rx='34' fill='none' stroke='#2A2418' stroke-width='8'/>")
# Pions : lettre manuscrite (IM Fell English italique), centrée sur sa boîte et réduite pour ne pas toucher le cercle intérieur
for nm, c, d, ink, L, s, bx, by in (('pion_ravages', '#8E2F25', '#5E1E17', '#F6EFDC', 'R', 0.7538, 155.81, 72.83), ('pion_prix', '#C9952B', '#7A5A14', '#2A2418', 'C', 0.8325, 138.0, 57.25)):
    svg(nm, 200, 200, f"<circle cx='100' cy='100' r='96' fill='{c}' stroke='{d}' stroke-width='6'/><circle cx='100' cy='100' r='74' fill='none' stroke='#F6EFDC' stroke-width='3' opacity='.45'/>"
        f"<text x='100' y='100' transform='translate(100 100) scale({s}) translate({-bx} {-by})' font-family=\"'IM Fell English',serif\" font-style='italic' font-size='120' fill='{ink}'>{L}</text>")
_seen = {}
for _m in MANIFEST: _seen[_m[0]] = _m
MANIFEST[:] = list(_seen.values())
