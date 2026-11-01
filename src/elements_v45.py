# Éléments v45 (1er nov. 2026) : cartes Matériel de départ en demi-format, sans nom, liste des biens avec icônes ; inspiré des cartes de John Company (bandeau, rangées séparées, coins ornés, pièce en bas).
IMG = 'file:///home/claude/castor-eau-de-vie-tts/src/img/'
MW, MH = 360, 500
SVGI = {'caisse': "<svg width='62' height='62' viewBox='0 0 200 200'><rect x='18' y='26' width='164' height='148' rx='10' fill='#C79A5B' stroke='#5C3A1A' stroke-width='8'/><line x1='18' y1='76' x2='182' y2='76' stroke='#5C3A1A' stroke-width='6'/><line x1='18' y1='126' x2='182' y2='126' stroke='#5C3A1A' stroke-width='6'/><line x1='30' y1='34' x2='170' y2='166' stroke='#5C3A1A' stroke-width='6'/></svg>",
        'edv': "<svg width='62' height='62' viewBox='0 0 200 200'><path d='M84 14 L116 14 L116 56 Q150 74 150 112 L150 176 Q150 188 138 188 L62 188 Q50 188 50 176 L50 112 Q50 74 84 56 Z' fill='#5E8C5A' stroke='#20331E' stroke-width='8'/><rect x='80' y='8' width='40' height='22' rx='4' fill='#8A5A2B' stroke='#20331E' stroke-width='5'/><rect x='62' y='112' width='76' height='46' rx='6' fill='#F2E8C8' stroke='#20331E' stroke-width='4'/></svg>"}
MICON = {'grand': ('canot_grand.png', 118), 'moyen': ('canot_petit.png', 96), 'caisse': ('tok_caisse.png', 62), 'edv': ('tok_bouteille.png', 62),
         'navire': ('navire_gravure.png', 92), 'alambic': ('alambic_gravure.png', 70)}
MAT45 = [[('navire', '1 navire, payé'), ('credit', '1 de crédit'), ('caisse', '1 marchandise'), ('coin', '1')],
         [('moyen', '1 moyen canot'), ('caisse', '2 marchandises'), ('coin', '2')],
         [('moyen', '1 moyen canot'), ('caisse', '1 marchandise'), ('edv', '1 eau-de-vie'), ('coin', '1')],
         [('grand', '1 grand canot'), ('caisse', '2 marchandises'), ('coin', '1')],
         [('grand', '1 grand canot'), ('navire', '1 part de navire'), ('caisse', '1 marchandise'), ('coin', '2')],
         [('navire', '2 parts de navire'), ('caisse', '2 marchandises'), ('coin', '1')],
         [('alambic', '2 parts de distillerie'), ('caisse', '2 marchandises'), ('coin', '2')],
         [('caisse', '3 marchandises'), ('coin', '3')],
         [('edv', '1 eau-de-vie'), ('caisse', '2 marchandises'), ('coin', '2')]]
MCSS = ("*{box-sizing:border-box;margin:0}"
 ".m{width:360px;height:500px;background:#F2EAD3;border-radius:18px;border:3px solid #4E5B3A;display:flex;flex-direction:column;overflow:hidden;position:relative}"
 ".band{background:#4E5B3A;color:#F2EAD3;text-align:center;padding:12px 0 10px;font:italic 30px 'IM Fell English',serif;letter-spacing:.5px}"
 ".band small{display:block;font:400 15px 'IM Fell English SC',serif;letter-spacing:3px;opacity:.85;margin-top:2px}"
 ".rows{flex:1;margin:14px;border:1.5px solid #4E5B3A;border-radius:6px;display:flex;flex-direction:column;position:relative}"
 ".r{flex:1;display:flex;align-items:center;gap:14px;padding:0 16px;border-top:1.5px solid #4E5B3A}.r:first-child{border-top:none}"
 ".ic{flex:none;width:120px;display:flex;justify-content:center;align-items:center}"
 ".tx{font:italic 27px/1.1 'IM Fell English',serif;color:#2A2418}"
 ".r.c{justify-content:center}.tx b{font:700 30px 'Alegreya Sans',sans-serif;font-style:normal;margin-right:2px}"
 ".coin{width:78px;height:78px;border-radius:50%;background:#F7F0DC;border:5px double #2A2418;display:flex;align-items:center;justify-content:center;font:400 40px 'IM Fell English',serif;color:#2A2418}"
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
def mcard(rows): return f"<div class='m'><div class='band'>Matériel<small>de départ</small></div><div class='rows'>{orns()}{''.join(mrow(k, t) for k, t in rows)}</div></div>"
page('deck_mat', 5 * MW, 2 * MH, "<div style='display:grid;grid-template-columns:repeat(5,360px);grid-auto-rows:500px'>" + ''.join(mcard(r) for r in MAT45) + "</div>", MCSS)
page('deck_mat_back', MW, MH, "<div class='m' style='background:#4E5B3A;align-items:center;justify-content:center'><div style='border:2px solid #F2EAD3;border-radius:10px;width:300px;height:440px;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#F2EAD3'><div style=\"font:italic 40px 'IM Fell English',serif\">Matériel</div><div style=\"font:400 18px 'IM Fell English SC',serif;letter-spacing:3px;margin-top:6px\">de départ</div></div></div>", MCSS)
DECKS['mat'] = {'cols': 5, 'rows': 2, 'n': 9, 'names': ['Matériel de départ'] * 9, 'half': True}
# Associés v45 (validés le 1er nov.)
ASSOC45 = [('Pierre Lestage', 'gros équipeur de Montréal', 'Chaque expédition que vous montez reçoit 1 marchandise gratuite.'),
           ('Bouchard, Coton et Bigras', 'société de voyageurs', 'Les voyageurs d’une expédition chaque année ne coûtent rien au départ (l’entretien d’hiver reste dû).'),
           ('Jean-Jérôme Patron', 'bourgeois du congé', 'Vos congés coûtent 1 ₶ de moins à rembourser (minimum 1 ₶).'),
           ('Daniel Greysolon Dulhut', 'commerçant et diplomate', 'Troquer : avant d’échanger, piochez 1 tuile du sac Castor sec et posez-la dans le lac.'),
           ('Simon Réaume', 'voyageur et diplomate', 'Vos coureurs des bois portent 3 charges.'),
           ('Milot', 'marchand de Lachine', 'Le comptoir vous vend les marchandises 1 ₶ moins cher (0,5 ₶ minimum).'),
           ('Jean-Baptiste Migeon', 'bailli et marchand', 'Chaque hiver, transférez un de vos soupçons à un autre joueur.'),
           ('Le cabaretier', 'des Trois-Rivières', 'Le comptoir vous vend l’eau-de-vie 1 ₶ moins cher (1 ₶ minimum).'),
           ('Tonty', 'homme de l’Ouest', 'Vos expéditions peuvent trafiquer dans les Pays fermés. +1 soupçon.'),
           ('Les engagés', 'de la compagnie de la colonie', 'Vos moyens canots portent 4 charges.')]
DECKS['pers'] = sheet('deck_pers', 'Associé', [card_html('Associé', t, fx, q) for t, q, fx in ASSOC45], 'Associés', 'piochez 3 · gardez-en 1'); DECKS['pers']['names'] = [f'{t}, {q}' for t, q, fx in ASSOC45]
# Manigances v45 (validées le 1er nov.) : 10 cartes, 1 exemplaire chacune
KCOL['Manigance'] = '#5A2A4A'
MANIG45 = [('Canotée de trop', 'Pendant votre action « Monter une expédition ».', 'Ajoutez un canot de plus à une expédition.'),
           ('Faussaire', 'Après qu’un joueur a choisi un congé et qu’il en reste encore au moins un autre disponible.', 'Volez le congé. Il reste à sa charge. +1 soupçon.'),
           ('Eau-de-vie coupée', 'Pendant votre action Troquer ou Trafiquer.', 'Vos eaux-de-vie comptent double pour toute l’action.'),
           ('Société secrète', 'Pendant votre action « Vendre des fourrures ».', 'Vendez à Albany sans test de soupçon.'),
           ('Rafler la traite', 'Au moment où un joueur annonce un troc dans votre zone.', 'Troquez à sa place (hors de votre tour).'),
           ('Pillage', 'À tout moment.', 'Une expédition adverse dans votre zone perd 2 charges ; vous en gardez 1. +1 soupçon.'),
           ('Commandant complaisant', 'Quand une expédition arrive dans une zone de troc.', 'Dans un lac avec un fort, réservez 1 peau visible.'),
           ('Fausse dénonciation', 'À tout moment.', 'Un joueur au choix : +2 soupçon.'),
           ('En sous-main', 'Après qu’un joueur a investi dans des parts.', 'Remplacez jusqu’à 2 parts de joueurs adverses par les vôtres sur la ou les cartes financées.'),
           ('Dans le sillage', 'Après qu’un joueur a monté une expédition.', 'Montez une expédition immédiatement.')]
def man_html(t, when, fx):
    k = KCOL['Manigance']
    return (f"<div class='c' style='--k:{k}'><div class='in'><div class='band'><span>Manigance</span><span></span></div><div class='t' style='font-size:58px'>{E(t)}</div><div class='rule'></div>"
            + (f"<div class='fx' style=\"font-family:'IM Fell English',serif;font-style:italic;font-size:50px;line-height:1.12;color:#5A2A4A;padding-bottom:6px\">{E(when)}</div>" if when else '') + f"<div class='fx' style='font-size:52px;line-height:1.22'>{E(fx)}</div></div></div>")
DECKS['man'] = sheet('deck_man', 'Manigance', [man_html(*m) for m in MANIG45], 'Manigances', 'piochées au printemps'); DECKS['man']['names'] = [m[0] for m in MANIG45]
# Sac d'événements du mois (tuiles), 20 tuiles
EVT45 = [('calme', 'Rivière calme', '', '#6F8796', 7), ('raid', 'Raid iroquois', '', '#8E2F25', 2),
         ('hudson', 'Baie d’Hudson', 'Du nord au sud, retirez autant de peaux que de Ravages.', '#1B3A5C', 2),
         ('abondante', 'Saison abondante', 'Regarnissez les lacs.', '#4E7A2C', 1),
         ('mission', 'Mission', 'Ajoutez une mission adjacente à une mission ou à Montréal.', '#1E1A14', 2),
         ('fort', 'Fort', 'Ajoutez un fort adjacent à un fort ou à Montréal.', '#7A5232', 2),
         ('baisse', 'Baisse du prix du castor', 'Prix du castor −1.', '#8A6418', 1), ('hausse', 'Hausse du prix du castor', 'Prix du castor +1.', '#8A6418', 1),
         ('compagnie', 'La Compagnie affrète son navire', '', '#2F5E8E', 1), ('profond', 'Le Profond est réquisitionné par le roi', '', '#2F5E8E', 1)]
ECSS = ("*{box-sizing:border-box;margin:0}.e{width:300px;height:300px;border-radius:22px;background:#F2EAD3;border:4px solid var(--k);display:flex;flex-direction:column;overflow:hidden}"
        ".e .h{background:var(--k);color:#F6EFDC;font:400 20px 'IM Fell English SC',serif;letter-spacing:2px;text-align:center;padding:8px 0 6px}"
        ".e .b{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:6px 10px;gap:8px}"
        ".e .t{font:italic 62px/1.0 'IM Fell English',serif;color:var(--k)}.e .t.s{font-size:44px}.e .x{font:700 32px/1.15 'Alegreya Sans',sans-serif;color:#2A2418}")
for k, t, x, c, n in EVT45:
    page(f'evt_{k}', 300, 300, f"<div class='e' style='--k:{c}'><div class='h'>Événement du mois</div><div class='b'><div class='t{" s" if x or len(t) > 22 else ""}'>{E(t)}</div>" + (f"<div class='x'>{E(x)}</div>" if x else '') + "</div></div>", ECSS)
page('evt_back', 300, 300, "<div class='e' style='--k:#3F6D78;background:#3F6D78;align-items:center;justify-content:center'><div style=\"font:italic 34px/1.1 'IM Fell English',serif;color:#F2EAD3;text-align:center\">Événement<br>du mois</div></div>", ECSS)
json.dump([[k, t, n] for k, t, x, c, n in EVT45], open('evt45.json', 'w'), ensure_ascii=False)
_seen = {}
for _m in MANIFEST: _seen[_m[0]] = _m
MANIFEST[:] = list(_seen.values())
