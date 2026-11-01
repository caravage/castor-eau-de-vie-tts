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
 ".page{width:1600px;height:1150px;background:#FFFFFF;border-radius:34px;padding:30px;display:flex;flex-direction:column;gap:24px}"
 ".zone{border-radius:18px;border:3px solid;display:flex;flex-direction:column}"
 ".mtl{background:#F6EFDC;border-color:#B7A675}.exp{background:#E3EBD6;border-color:#8FA67A}.free{background:#FBF7EC;border-color:#CFC4A6;border-style:dashed}"
 ".zh{font:400 42px 'IM Fell English SC',serif;padding:14px 24px 8px;display:flex;justify-content:space-between;align-items:baseline}"
 ".mtl .zh{background:#E6DAB6;color:#5A3B24;border-radius:15px 15px 0 0}.exp .zh{background:#8FA67A;color:#F6EFDC;border-radius:15px 15px 0 0}.free .zh{color:#6B5F45;font-size:30px}"
 ".zh small{font:italic 24px 'IM Fell English',serif}"
 ".acts{display:grid;gap:12px;padding:12px 18px 14px}"
 ".a{background:#FFFDF6;border-radius:12px;padding:12px 16px;border:1.5px solid rgba(0,0,0,.12);display:flex;gap:16px;align-items:flex-start}.a svg{flex:none;margin-top:4px}"
 ".a b{display:block;font:400 36px 'IM Fell English SC',serif;margin-bottom:4px}.a p{font:400 25.5px/1.26 'Alegreya Sans',sans-serif;color:#2A2418}"
 ".mtl .a b{color:#7A4E2A}.exp .a b{color:#2F4D19}.note{margin-top:4px;font-size:22px!important;color:#4A3A2C!important}.note u{text-decoration:none;font-weight:700}"
 ".xnote{font:400 23px/1.2 'Alegreya Sans',sans-serif;color:#2F4D19;padding:10px 22px 0}.xnote b{font-weight:700}.free .acts{grid-template-columns:repeat(3,1fr);padding:4px 20px 16px}.free .a{background:transparent;border:none;padding:0 6px}.free .a b{font-size:28px;color:#6B5F45}.free .a p{font-size:22px}")
AM=[('Monter une expédition','Composez une ou des expéditions (choix du congé et/ou Coureur des bois, canots, charges et voyageurs), payez les dépenses puis posez le ou les canots sur une traversée adjacente à Montréal.',''),
    ('Vendre des fourrures','Vendez des fourrures de votre entrepôt :<br>– à Montréal, au prix du castor<br>– à Albany (soupçon), au prix du castor +1',''),
    ('Investir','Achetez un canot, des marchandises, de l’eau-de-vie au Marché de Québec ou des parts de distillerie ou de navire.',''),
    ('Recruter','Achetez une carte de la rivière.','')]
AX=[('Voyager','Faites avancer une expédition d’une zone de troc vers une zone adjacente.',''),
    ('Troquer','Dans un lac ou Pays, une expédition échange autant de charges voulues contre les tuiles présentes. Pour chaque eau-de-vie troquée, lancez un dé : sur un 1, +1 ravage.','<u>Mission :</u> +1 soupçon par eau-de-vie échangée.<br><u>Coureurs des bois :</u> interdits.'),
    ('Trafiquer','Dans un lac ou Pays, une expédition essaye de trafiquer de la fourrure de castor contre une eau-de-vie. Lancez un dé : sur 2 ou plus, piochez une tuile du sac Castor sec. Vous pouvez répéter cette action en ajoutant un dé à chaque essai ; un seul 1 fait échouer l’essai. Échec : perte de l’eau-de-vie, le lac est ravagé (posez-y un marqueur Ravagé), +1 ravage.','<u>Mission :</u> interdit. <br><u>Coureurs des bois :</u> un échec ne ravage pas le lac.')]
AG=[('Jouer une carte','de votre main en respectant la condition écrite sur la carte.',''),
    ('Faire partir votre navire','avant octobre, en payant 1 ₶ de faux fret par place vide.',''),
    ('Échanger entre joueurs','Acheter, louer ou vendre à un prix négocié entre joueurs 1 canot ou jusqu’à 5 charges ou peaux.','')]
def aacts(L, c, sz=70): return ''.join(f"<div class='a'>{icon(t,c,sz)}<div><b>{t}</b><p>{d}</p>" + (f"<p class='note'>{n}</p>" if n else '') + "</div></div>" for t, d, n in L)
page('aide_a', 1600, 1150, "<div class='page'><div style='display:flex;gap:24px;flex:1'>"
     f"<div class='zone exp' style='flex:1.25'><div class='zh'>En expédition <small>Pays-d’en-Haut</small></div><div class='xnote'>Chaque mois : <b>une action par canot</b> qui n’est pas en transit. Action faite : couchez le canot.</div><div class='acts'>{aacts(AX,'#2F4D19')}</div></div>"
     f"<div class='zone mtl' style='flex:1'><div class='zh'>À Montréal</div><div class='acts'>{aacts(AM,'#7A4E2A')}</div></div></div>"
     f"<div class='zone free'><div class='zh'>Actions gratuites <small>une par tour</small></div><div class='acts'>{aacts(AG,'#6B5F45',46)}</div></div></div>", ACSS)
# Marqueur Ravagé : carré comme la mission, flammes
svg('ravage', 220, 220, "<rect x='10' y='10' width='200' height='200' rx='34' fill='#7A1F18' stroke='#2A2418' stroke-width='8'/>"
    "<path d='M110 30 C122 62 160 78 160 128 C160 162 138 186 110 186 C82 186 60 162 60 128 C60 104 72 90 80 80 C82 98 90 106 98 108 C92 84 98 52 110 30 Z' fill='#E8A93C'/>"
    "<path d='M112 82 C118 104 140 116 140 142 C140 164 126 176 110 176 C94 176 80 164 80 142 C80 128 88 120 92 114 C94 126 100 132 106 132 C102 116 104 98 112 82 Z' fill='#F6D57A'/>"
    "<path d='M110 126 C114 140 126 146 126 160 C126 170 118 176 110 176 C102 176 94 170 94 160 C94 150 102 144 110 126 Z' fill='#FFF4D6'/>")
# Verso v45 : saisons (printemps, hiver), même style que le recto ; étapes numérotées
VCSS = ACSS + (".spr{background:#EEF3E2;border-color:#9DB37E}.spr .zh{background:#9DB37E;color:#FBF7EC;border-radius:15px 15px 0 0}"
 ".hiv{background:#E6ECF2;border-color:#7D93AB}.hiv .zh{background:#4F6A86;color:#F2F5F8;border-radius:15px 15px 0 0}"
 ".s{background:#FFFDF6;border-radius:12px;padding:10px 14px;border:1.5px solid rgba(0,0,0,.12);display:flex;gap:12px;align-items:flex-start}"
 ".s i{flex:none;width:40px;height:40px;border-radius:50%;font:700 24px/40px 'Alegreya Sans',sans-serif;text-align:center;color:#FFFDF6;font-style:normal;margin-top:2px}"
 ".spr .s i{background:#6E8A4C}.hiv .s i{background:#4F6A86}"
 ".s b{display:block;font:400 30px 'IM Fell English SC',serif;margin-bottom:2px}.spr .s b{color:#3F5A22}.hiv .s b{color:#2F4A66}"
 ".s p{font:400 22.5px/1.27 'Alegreya Sans',sans-serif;color:#2A2418}"
 ".steps{display:grid;gap:12px;padding:14px 16px 16px}.hcols{display:flex;gap:12px;padding:14px 16px 16px;align-items:flex-start}.hcols .steps{flex:1;padding:0}")
SP=[('Ordre du tour','Du plus fort capital circulant au plus faible, fixé pour toute l’année ; en cas d’égalité, on garde l’ordre de l’année précédente.'),
    ('Départ de La Rochelle','Chaque navire en rade de La Rochelle peut partir si son propriétaire le souhaite ; les navires non joueurs partent automatiquement. Chaque navire lance un dé : sur 4 ou plus, il est placé sur le cercle 1 mois (arrivée en mai), sinon sur le cercle 2 mois (juin).'),
    ('Lacs','Chaque tuile sèche restée au lac passe côté gras. Puis chaque lac ouvert est regarni de 1 tuile visible et 1 jeton caché (au plus 4 tuiles visibles et 2 jetons cachés par lac). Puis bonus de zone : fort +2 tuiles visibles et +2 cachées, mission +1 visible, du lac le plus haut au plus bas.'),
    ('Hivernant','Un hivernant déposé dans un Pays y récolte une tuile Castor gras.'),
    ('Soupçon','Chaque joueur peut piocher autant de cartes Manigance que de soupçon.')]
HV=[('Castors en France','On compte les castors arrivés en France et on les retire des navires ; la compagnie paie 1 ₶ par case de fret aux propriétaires des navires.'),
    ('Entretien','3 ₶ par navire qui hiverne à Québec ; 1 ₶ par canot qui hiverne en exploration ; 1 ₶ par hivernant en exploration.'),
    ('Crédit','Chacun paie d’abord en ₶ ses congés «&nbsp;à&nbsp;payer&nbsp;». Puis chacun rembourse ce qu’il veut de son crédit, au prix d’une case fixé par son rang en capital circulant (le plus soupçonné paie +1). On peut céder une distillerie ou un navire contre 1 case de crédit. Puis : zone rayée (3 à 5), le marqueur recule d’une case ; zone rouge (6 à 8), de deux.'),
    ('Prix du castor','Il monte ou baisse selon les ventes de l’année.'),
    ('Ravages','−1.'),
    ('Tuiles des lacs','Les tuiles visibles et les jetons cachés retirés de la carte retournent dans leur sac.'),
    ('Lacs ravagés','Pour chaque lac ravagé, lancez un dé ; s’il est supérieur au niveau de la piste Ravages, retirez le marqueur Ravagé.'),
    ('Fin de partie','Si c’est le dernier tour (année VIII), la partie s’arrête.'),
    ('Rivière','Faites avancer la rivière.'),
    ('Commande à La Rochelle','Les distilleries produisent d’abord (1 baril d’eau-de-vie gratuit par part). Chaque joueur débloque des cases de crédit, puis commande avec leur valeur aux prix de La Rochelle : marchandise 1 ₶, baril 2 ₶. Les joueurs s’entendent sur la répartition dans les navires en rade de La Rochelle et le prix du fret par navire.'),
    ('Année et mois','Le marqueur Année avance d’une case ; le marqueur Mois revient sur Printemps.')]
def steps(L, k0=1): return ''.join(f"<div class='s'><i>{k}</i><div><b>{t}</b><p>{d}</p></div></div>" for k, (t, d) in enumerate(L, k0))
page('aide_b', 1600, 1150, "<div class='page' style='flex-direction:row'>"
     f"<div class='zone spr' style='flex:1'><div class='zh'>Printemps</div><div class='steps'>{steps(SP)}</div></div>"
     f"<div class='zone hiv' style='flex:2'><div class='zh'>Hiver</div><div class='hcols'><div class='steps'>{steps(HV[:6])}</div><div class='steps'>{steps(HV[6:], 7)}</div></div></div></div>", VCSS)
_seen = {}
for _m in MANIFEST: _seen[_m[0]] = _m
MANIFEST[:] = list(_seen.values())
