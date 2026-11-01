# Éléments v45 (1er nov. 2026) : cartes Matériel de départ en demi-format, sans nom, liste des biens avec icônes ; inspiré des cartes de John Company (bandeau, rangées séparées, coins ornés, pièce en bas).
IMG = 'file:///home/claude/castor-eau-de-vie-tts/src/img/'
MW, MH = 360, 500
SVGI = {'caisse': "<svg width='62' height='62' viewBox='0 0 200 200'><rect x='18' y='26' width='164' height='148' rx='10' fill='#C79A5B' stroke='#5C3A1A' stroke-width='8'/><line x1='18' y1='76' x2='182' y2='76' stroke='#5C3A1A' stroke-width='6'/><line x1='18' y1='126' x2='182' y2='126' stroke='#5C3A1A' stroke-width='6'/><line x1='30' y1='34' x2='170' y2='166' stroke='#5C3A1A' stroke-width='6'/></svg>",
        'edv': "<svg width='62' height='62' viewBox='0 0 200 200'><path d='M84 14 L116 14 L116 56 Q150 74 150 112 L150 176 Q150 188 138 188 L62 188 Q50 188 50 176 L50 112 Q50 74 84 56 Z' fill='#5E8C5A' stroke='#20331E' stroke-width='8'/><rect x='80' y='8' width='40' height='22' rx='4' fill='#8A5A2B' stroke='#20331E' stroke-width='5'/><rect x='62' y='112' width='76' height='46' rx='6' fill='#F2E8C8' stroke='#20331E' stroke-width='4'/></svg>"}
MICON = {'grand': ('canot_grand.png', 118), 'moyen': ('canot_petit.png', 96), 'caisse': ('tok_caisse.png', 62), 'edv': ('tok_bouteille.png', 62),
         'navire': ('navire_gravure.png', 92), 'alambic': ('alambic_gravure.png', 70)}
MAT45 = [[('navire', '1 navire, payé'), ('credit', '1 de crédit')],
         [('moyen', '1 moyen canot'), ('caisse', '2 marchandises')],
         [('moyen', '1 moyen canot'), ('caisse', '1 marchandise'), ('edv', '1 eau-de-vie')],
         [('grand', '1 grand canot'), ('edv', '1 eau-de-vie')],
         [('grand', '1 grand canot'), ('navire', '1 part de navire')],
         [('navire', '2 parts de navire'), ('edv', '1 eau-de-vie')],
         [('alambic', '2 parts de distillerie'), ('edv', '1 eau-de-vie'), ('caisse', '1 marchandise')],
         [('caisse', '3 marchandises'), ('coin', '1')],
         [('edv', '2 eau-de-vie'), ('caisse', '1 marchandise')]]
MCSS = ("*{box-sizing:border-box;margin:0}"
 ".m{width:360px;height:500px;background:#F2EAD3;border-radius:18px;border:3px solid #4E5B3A;display:flex;flex-direction:column;overflow:hidden;position:relative}"
 ".band{background:#4E5B3A;color:#F2EAD3;text-align:center;padding:12px 0 10px;font:italic 30px 'IM Fell English',serif;letter-spacing:.5px}"
 ".band small{display:block;font:400 15px 'IM Fell English SC',serif;letter-spacing:3px;opacity:.85;margin-top:2px}"
 ".rows{flex:1;margin:14px;border:1.5px solid #4E5B3A;border-radius:6px;display:flex;flex-direction:column;position:relative}"
 ".r{flex:1;display:flex;align-items:center;gap:14px;padding:0 16px;border-top:1.5px solid #4E5B3A}.r:first-child{border-top:none}"
 ".ic{flex:none;width:120px;display:flex;justify-content:center;align-items:center}"
 ".tx{font:italic 27px/1.1 'IM Fell English',serif;color:#2A2418}"
 ".r.c{justify-content:center}.tx b{font:700 30px 'Alegreya Sans',sans-serif;font-style:normal;margin-right:2px}"
 ".coin{width:96px;height:96px;border-radius:50%;background:#F7F0DC;border:5px double #2A2418;display:flex;align-items:center;justify-content:center;font:400 40px 'IM Fell English',serif;color:#2A2418}"
 ".orn{position:absolute;width:26px;height:26px}")
ORN = "<svg class='orn' style='{p}' viewBox='0 0 26 26'><path d='M2 2C10 2 14 6 14 13M2 2C2 10 6 14 13 14M8 8C10 10 10 12 8 13' fill='none' stroke='#4E5B3A' stroke-width='1.6' transform='{t}'/></svg>"
def orns():
    return ''.join(ORN.format(p=p, t=t) for p, t in (("left:-1px;top:-1px", ''), ("right:-1px;top:-1px", 'translate(26 0) scale(-1 1)'),
                                                      ("left:-1px;bottom:-1px", 'translate(0 26) scale(1 -1)'), ("right:-1px;bottom:-1px", 'translate(26 26) scale(-1 -1)')))
def mrow(k, t):
    if k == 'coin': return f"<div class='r c'><div class='coin'><b style=\"font:700 38px 'Alegreya Sans',sans-serif\">{t}</b>&nbsp;₶</div></div>"
    if k == 'credit': ic = "<svg width='70' height='54' viewBox='0 0 70 54'><defs><pattern id='hs' width='8' height='8' patternUnits='userSpaceOnUse' patternTransform='rotate(45)'><rect width='4' height='8' fill='#C9B48A'/></pattern></defs><rect x='3' y='3' width='64' height='48' rx='6' fill='url(#hs)' stroke='#7A1F18' stroke-width='4'/></svg>"
    elif k in SVGI: ic = SVGI[k]
    else:
        f, w = MICON[k]; ic = f"<img src='{IMG}{f}' style='width:{w}px'>"
    return f"<div class='r'><div class='ic'>{ic}</div><div class='tx'><b>{t.split(' ',1)[0]}</b> {t.split(' ',1)[1]}</div></div>"
for i, rows in enumerate(MAT45, 1):
    page(f'mat45_{i}', MW, MH, f"<div class='m'><div class='band'>Matériel<small>de départ</small></div><div class='rows'>{orns()}{''.join(mrow(k, t) for k, t in rows)}</div></div>", MCSS)
page('mat45_back', MW, MH, "<div class='m' style='background:#4E5B3A;align-items:center;justify-content:center'><div style='border:2px solid #F2EAD3;border-radius:10px;width:300px;height:440px;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#F2EAD3'>"
     "<div style=\"font:italic 40px 'IM Fell English',serif\">Matériel</div><div style=\"font:400 18px 'IM Fell English SC',serif;letter-spacing:3px;margin-top:6px\">de départ</div>"
     "<div style=\"font:italic 16px 'IM Fell English',serif;margin-top:40px;opacity:.8\">Castor et eau-de-vie</div></div></div>", MCSS)
_seen = {}
for _m in MANIFEST: _seen[_m[0]] = _m
MANIFEST[:] = list(_seen.values())
