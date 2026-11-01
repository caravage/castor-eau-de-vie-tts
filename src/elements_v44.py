# Aide de jeu v44 (31 oct. 2026) : recto = actions seulement, texte exact du livret ; expédition (vert sauge) à gauche, Montréal (beige) à droite, icônes.
K="fill='none' stroke='{c}' stroke-width='2.8' stroke-linecap='round' stroke-linejoin='round'"
IC={
'Monter une expédition':"<path d='M4 36Q30 48 56 36Q30 41 4 36Z' {k}/><rect x='14' y='22' width='12' height='11' {k}/><rect x='30' y='22' width='12' height='11' {k}/><path d='M20 22V33M36 22V33' {k}/><path d='M46 6L38 32' {k}/>",
'Vendre des fourrures':"<ellipse cx='17' cy='28' rx='9' ry='12' {k}/><path d='M17 16V11M17 40V45M8 28H4M26 28H30' {k}/><path d='M33 28H41M37 24L41 28L37 32' {k}/><rect x='44' y='18' width='14' height='20' rx='2' {k}/><path d='M47 24H55M47 30H55' {k}/>",
'Investir':"<ellipse cx='30' cy='40' rx='14' ry='5' {k}/><path d='M16 40V32M44 40V32' {k}/><ellipse cx='30' cy='32' rx='14' ry='5' {k}/><path d='M16 32V24M44 32V24' {k}/><ellipse cx='30' cy='24' rx='14' ry='5' {k}/>",
'Recruter':"<circle cx='24' cy='20' r='7' {k}/><path d='M10 44C10 32 38 32 38 44' {k}/><path d='M46 18V30M40 24H52' {k}/>",
'Passer':"<path d='M18 10H42M18 46H42M20 10C20 22 40 22 40 28C40 34 20 34 20 46M40 10C40 22 20 22 20 28' {k}/>",
'Voyager':"<path d='M4 32Q24 42 44 32Q24 36 4 32Z' {k}/><path d='M32 6L22 34' {k}/><path d='M8 46H54M48 40L54 46L48 52' {k}/>",
'Troquer':"<path d='M10 22H46M40 15L47 22L40 29' {k}/><path d='M50 36H14M20 29L13 36L20 43' {k}/>",
'Trafiquer':"<path d='M24 8H36V18Q44 22 44 30V46Q44 50 40 50H20Q16 50 16 46V30Q16 22 24 18Z' {k}/><path d='M16 34H44' {k}/>",
'Jouer une carte':"<rect x='16' y='8' width='26' height='38' rx='4' {k}/><path d='M22 18H36M22 26H36M22 34H30' {k}/>",
'Faire partir votre navire':"<path d='M8 38H52L46 48H14Z' {k}/><path d='M30 38V8' {k}/><path d='M30 10L44 34H30M30 14L18 34H30' {k}/>",
'Échanger entre joueurs':"<circle cx='18' cy='16' r='6' {k}/><path d='M8 36C8 26 28 26 28 36' {k}/><circle cx='42' cy='16' r='6' {k}/><path d='M32 36C32 26 52 26 52 36' {k}/><path d='M20 46H40M35 41L40 46L35 51' {k}/>"}
def icon(t,c,sz=56): return f"<svg width='{sz}' height='{sz}' viewBox='0 0 60 56'>"+IC[t].replace('{k}',K.format(c=c))+"</svg>"

ACSS = ("*{box-sizing:border-box;margin:0}"
 ".page{width:1600px;height:1150px;background:#F2EAD3;border-radius:34px;padding:34px;display:flex;flex-direction:column;gap:24px}"
 ".zone{border-radius:18px;border:3px solid;display:flex;flex-direction:column}"
 ".mtl{background:#F6EFDC;border-color:#B7A675}.exp{background:#E3EBD6;border-color:#8FA67A}.free{background:#FBF7EC;border-color:#CFC4A6;border-style:dashed}"
 ".zh{font:400 40px 'IM Fell English SC',serif;padding:14px 24px 8px;display:flex;justify-content:space-between;align-items:baseline}"
 ".mtl .zh{background:#E6DAB6;color:#5A3B24;border-radius:15px 15px 0 0}.exp .zh{background:#8FA67A;color:#F6EFDC;border-radius:15px 15px 0 0}.free .zh{color:#6B5F45;font-size:30px}"
 ".zh small{font:italic 24px 'IM Fell English',serif}"
 ".acts{display:grid;gap:14px;padding:16px 20px 18px}"
 ".a{background:#FFFDF6;border-radius:12px;padding:12px 16px;border:1.5px solid rgba(0,0,0,.12);display:flex;gap:16px;align-items:flex-start}.a svg{flex:none;margin-top:4px}"
 ".a b{display:block;font:400 31px 'IM Fell English SC',serif;margin-bottom:4px}.a p{font:400 22px/1.3 'Alegreya Sans',sans-serif;color:#2A2418}"
 ".mtl .a b{color:#7A4E2A}.exp .a b{color:#2F4D19}.note{margin-top:6px;font-size:20px!important;color:#4A3A2C!important}.note u{text-decoration:none;font-weight:700}"
 ".free .acts{grid-template-columns:repeat(3,1fr);padding:4px 20px 16px}.free .a{background:transparent;border:none;padding:0 6px}.free .a b{font-size:25px;color:#6B5F45}.free .a p{font-size:20px}")
AM=[('Monter une expédition','Composez une ou des expéditions (choix du congé et/ou Coureur des bois, canots, charges et voyageurs), payez les dépenses puis posez le ou les canots sur une traversée adjacente à Montréal.',''),
    ('Vendre des fourrures','Vendez des fourrures de votre entrepôt : à Montréal, contre des lettres de change ; à Albany au prix du castor +1.',''),
    ('Investir','Achetez un canot (grand 3 ₶ - moyen 2 ₶), des parts de distillerie ou des parts de navire.',''),
    ('Recruter','Prenez une carte de la rivière au prix de sa case. Les cartes restantes glissent et une nouvelle carte est ajoutée.',''),
    ('Passer','Laissez passer le mois.','')]
AX=[('Voyager','Faites avancer vos canots de leur zone de troc vers une traversée adjacente.',''),
    ('Troquer','Vos expéditions échangent dans un lac sélectionné toutes les charges voulues contre les tuiles présentes. Pour chaque eau-de-vie troquée, lancez un dé : sur un 1, +1 ravage.','<u>Mission :</u> +1 soupçon par eau-de-vie échangée. CdB interdits.'),
    ('Trafiquer','Vos expéditions essayent de trafiquer de la fourrure de castor contre une eau-de-vie. Lancez un dé : sur 2 ou plus, piochez une tuile du sac Castor sec. Vous pouvez répéter cette action en ajoutant un dé à chaque essai ; un seul 1 fait échouer l’essai. Échec : perte de l’eau-de-vie, le lac est ravagé (posez-y un marqueur Ravagé), +1 ravage.','<u>Mission :</u> interdit. <u>CdB :</u> un échec ne ravage pas le lac.')]
AG=[('Jouer une carte','de votre main en respectant la condition écrite sur la carte.',''),
    ('Faire partir votre navire','avant octobre, en payant 1 ₶ de faux fret par place vide.',''),
    ('Échanger entre joueurs','Acheter, louer ou vendre à un prix négocié entre joueurs 1 canot ou jusqu’à 5 charges ou peaux.','')]
def aacts(L, c, sz=66): return ''.join(f"<div class='a'>{icon(t,c,sz)}<div><b>{t}</b><p>{d}</p>" + (f"<p class='note'>{n}</p>" if n else '') + "</div></div>" for t, d, n in L)
page('aide_a', 1600, 1150, "<div class='page'><div style='display:flex;gap:24px;flex:1'>"
     f"<div class='zone exp' style='flex:1'><div class='zh'>En expédition <small>Pays-d’en-Haut</small></div><div class='acts'>{aacts(AX,'#2F4D19')}</div></div>"
     f"<div class='zone mtl' style='flex:1.1'><div class='zh'>À Montréal</div><div class='acts'>{aacts(AM,'#7A4E2A')}</div></div></div>"
     f"<div class='zone free'><div class='zh'>Actions gratuites <small>une par tour</small></div><div class='acts'>{aacts(AG,'#6B5F45',46)}</div></div></div>", ACSS)
_seen = {}
for _m in MANIFEST: _seen[_m[0]] = _m
MANIFEST[:] = list(_seen.values())
