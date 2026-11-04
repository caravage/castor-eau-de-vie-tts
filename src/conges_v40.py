# Congés v40 (3 nov. 2026) : style « contrat » (parchemin, « Congé » en tête, prix centré en bas, ruban « 2 ans »,
# fort = hexagone blanc à lys d'or, mission = hexagone noir à croix blanche, officier = ovale blanc à lys d'or).
import json, html, math, sys
E = html.escape
INK='#2A2418'; PAP='#F6EFDC'; ROUGE='#8E2F25'; ROUGE_CR='#A3352A'; PARCH='#EEDFBC'; BORD='#8A6A3A'; OR='#E3B520'; BLANC='#FFFDF6'
SER="'IM Fell English',serif"; BODY="'Alegreya Sans',sans-serif"; DISP="'IM Fell English SC',serif"
def tx(x,y,s,size,fill=INK,anchor='middle',fam=SER,italic=False,weight=400):
    return f"<text x='{x}' y='{y}' font-family=\"{fam}\" font-size='{size}' font-weight='{weight}' text-anchor='{anchor}' fill='{fill}'"+(" font-style='italic'" if italic else '')+f">{E(s)}</text>"
FLEUR=("<path d='M0 -10C3 -6 3 -2 0 2C-3 -2 -3 -6 0 -10Z'/><path d='M-1 2C-6 -4 -11 0 -8 4C-6 2 -4 2 -2 4Z'/>"
       "<path d='M1 2C6 -4 11 0 8 4C6 2 4 2 2 4Z'/><rect x='-5' y='3' width='10' height='2.5'/><path d='M-2 5.5L0 10L2 5.5Z'/>")
def lys(x,y,k,c=OR): return f"<g transform='translate({x} {y}) scale({k})' fill='{c}'>{FLEUR}</g>"
def hexa(cx,cy,r,fill):
    pts=' '.join(f"{cx+r*math.cos(math.radians(90+60*k)):.2f},{cy+r*math.sin(math.radians(90+60*k)):.2f}" for k in range(6))
    return f"<polygon points='{pts}' fill='{fill}' stroke='{INK}' stroke-width='1'/>"
def croix(x,y): return f"<path d='M{x} {y}L{x+6} {y+6}M{x+6} {y}L{x} {y+6}' stroke='{ROUGE_CR}' stroke-width='1.6'/>"
def caisses(n,y):
    x0=55-(n*12+(n-1)*3)/2
    return ''.join(f"<rect x='{x0+i*15:.1f}' y='{y}' width='12' height='12' fill='#C9A869' stroke='#3A2410' stroke-width='1'/>" for i in range(n))
def perso(p,y):
    px=34 if p=='mis' else 38
    if p=='off': o=f"<ellipse cx='{px}' cy='{y}' rx='7.7' ry='9.35' fill='{BLANC}' stroke='{INK}' stroke-width='1'/>"+lys(px,y,.62)
    else: o=(f"<ellipse cx='{px}' cy='{y}' rx='7.7' ry='9.35' fill='#EADFC2' stroke='{INK}' stroke-width='.8'/>"
             f"<path d='M{px} {y-5.5}V{y+5.5}M{px-3.3} {y-2.2}H{px+3.3}' stroke='{INK}' stroke-width='1.4'/>")
    return o+tx(px+12,y-2.5,'avec',10,anchor='start',italic=True)+tx(px+12,y+8,'officier' if p=='off' else 'missionnaire',11,anchor='start',italic=True)
def cadre():
    return (f"<rect x='2' y='2' width='106' height='106' rx='5' fill='{PARCH}' stroke='{BORD}' stroke-width='2'/>"
            f"<rect x='7' y='7' width='96' height='96' rx='2' fill='none' stroke='{BORD}' stroke-width='.6'/>"
            f"<rect x='9' y='9' width='92' height='92' rx='1.5' fill='none' stroke='{BORD}' stroke-width='.3'/>"
            + tx(55,25,'Congé',15,fam=DISP))
def face(prix, items, ans2=False, credit=False):
    g=[cadre()]
    if ans2:
        g.append(f"<defs><clipPath id='ct'><rect x='2' y='2' width='106' height='106' rx='5'/></clipPath></defs><g clip-path='url(#ct)'><g transform='rotate(45 98 12)'>"
                 f"<rect x='78' y='7' width='40' height='10' fill='{ROUGE}'/>"+tx(98,14.6,'2 ans',7.5,PAP,fam=BODY,weight=700)+"</g></g>"
                 f"<rect x='2' y='2' width='106' height='106' rx='5' fill='none' stroke='{BORD}' stroke-width='2'/>")
    y=43 if len(items)>=3 else 47
    for it in items:
        k=it[0]
        if k=='t': g.append(tx(55,y,it[1],11,italic=True)); y+=12
        elif k=='x':
            w=len(it[1])*2.5; g+=[croix(55-w-4,y-6),tx(59,y,it[1],11,italic=True)]; y+=12
        elif k=='p': g.append(perso(it[1],y+6)); y+=23
        elif k=='c': g.append(caisses(it[1],y-4)); y+=16
        elif k=='fort': g.append(hexa(55,y+5,11,BLANC)+lys(55,y+5,.62)); y+=26
        elif k=='mis': g.append(hexa(55,y+5,11,INK)+f"<path d='M55 {y-1.5}V{y+11.5}M50.5 {y+2.5}H59.5' stroke='{BLANC}' stroke-width='2'/>"); y+=26
    g.append(tx(55,97,prix,16,ROUGE_CR if credit else INK,fam=BODY,weight=700))
    return ''.join(g)
def non_paye(p):
    return (cadre()+f"<g transform='rotate(-18 55 58)'><rect x='19' y='47' width='72' height='20' rx='2' fill='none' stroke='{ROUGE_CR}' stroke-width='2'/>"
            + tx(55,62,'NON PAYÉ',13,ROUGE_CR,fam=BODY,weight=700)+"</g>"+tx(55,97,f'{p} ₶',16,fam=BODY,weight=700))
H="Lacs d'en haut"; B="Lacs d'en bas"; S='Lac Supérieur'
# (id, nom TTS, prix, crédit, items, 2 ans, nombre) — d'après « Cartes et tuiles » (3 nov. 2026)
CONGES=[
 ('ord_m','Congé ordinaire',3,False,[('t','moyen canot')],False,1),
 ('ord_m_off','Congé ordinaire',2,False,[('t','moyen canot'),('p','off')],False,1),
 ('ord_g','Congé ordinaire',4,False,[('t','grand canot')],False,1),
 ('ord_g_off','Congé ordinaire',4,False,[('t','grand canot'),('p','off')],False,1),
 ('garn2','Congé de garnison',2,False,[('t','comptoir avec fort'),('fort',)],False,1),
 ('garn3','Congé de garnison',3,False,[('t','comptoir avec fort'),('fort',)],False,1),
 ('mis2','Congé de mission',2,False,[('t','comptoir avec mission'),('mis',)],False,1),
 ('mis3','Congé de mission',3,False,[('t','comptoir avec mission'),('mis',)],False,1),
 ('lib','Congé libre',5,False,[],False,2),
 ('lib_off','Congé libre',5,False,[('p','off')],False,1),
 ('lib_mis','Congé libre',5,False,[('p','mis')],False,1),
 ('lib3','Congé libre',3,False,[],False,1),
 ('veuve',"Veuve d'officier",2,False,[('t','si capital'),('t','le plus bas')],False,1),
 ('gentil','Gentilhomme',1,True,[('c',1)],False,1),
 ('seigneur','Seigneur',7,False,[('c',2)],False,1),
 ('fabrique','Fabrique Notre-Dame',3,False,[('t','soupçon ≤ 1'),('x','eau-de-vie'),('p','mis')],False,2),
 ('faveur',"Faveur de l'intendant",1,True,[('t','soupçon ≤ 2'),('p','off')],False,1),
 ('rochelle','Fournisseur de La Rochelle',2,True,[('t','soupçon ≤ 2'),('c',4)],False,1),
 ('bordeaux','Fournisseur de Bordeaux',2,True,[('c',3)],False,1),
 ('outaouais','Congé des Outaouais',3,False,[('t',H),('t','ou Témiscamingue')],False,1),
 ('sup','Congé du Lac Supérieur',3,False,[('t',S)],True,1),
 ('ouest',"Congé de l'Ouest",4,False,[('x',B),('c',1)],False,1),
 ('pays','Congé de Pays',3,False,[('t','Pays')],True,1),
 ('nord','Congé du Nord',2,False,[('t',S)],True,1),
 ('dulhut','Congé de Dulhut',3,False,[('t',S)],True,1),
 ('michigan','Congé du lac Michigan',2,False,[('t',H)],False,1),
 ('jesuites','Congé des missions jésuites',2,False,[('t',H),('p','mis')],False,1),
 ('ontario','Congé du lac Ontario',3,False,[('t',B)],False,1),
 ('lasalle','Congé de La Salle',3,False,[('t',B),('p','off')],False,1),
 ('mississippi','Congé du Mississippi',3,False,[('t','Pays')],True,1),
 ('prairies','Congé des Prairies',3,False,[('t','Pays')],True,1),
]
if __name__=='__main__':
    out=sys.argv[1]; F=sys.argv[2]
    css=(f"@font-face{{font-family:'IM Fell English';src:url({F}im-fell-english/files/im-fell-english-latin-400-normal.woff2)}}"
         f"@font-face{{font-family:'IM Fell English';font-style:italic;src:url({F}im-fell-english/files/im-fell-english-latin-400-italic.woff2)}}"
         f"@font-face{{font-family:'IM Fell English SC';src:url({F}im-fell-english-sc/files/im-fell-english-sc-latin-400-normal.woff2)}}"
         f"@font-face{{font-family:'Alegreya Sans';font-weight:700;src:url({F}alegreya-sans/files/alegreya-sans-latin-700-normal.woff2)}}")
    tiles=[(f'c40_{c[0]}',face(f"{c[2]} crédit{'s' if c[2]>1 else ''}" if c[3] else f'{c[2]} ₶',c[4],c[5],c[3])) for c in CONGES]
    tiles+=[(f'c40_np{p}',non_paye(p)) for p in sorted({c[2] for c in CONGES if not c[3]})]
    body=''.join(f"<div id='{n}' style='width:400px;height:400px'><svg width='400' height='400' viewBox='0 0 110 110'>{s}</svg></div>" for n,s in tiles)
    open(out,'w').write(f"<!doctype html><meta charset=utf-8><style>{css}body{{margin:0;background:transparent}}</style>{body}")
    json.dump([[c[0],c[1],c[2],c[3],c[5],c[6]] for c in CONGES],open('conges_v40.json','w'),ensure_ascii=False)
    print(len(tiles), sum(c[6] for c in CONGES))
