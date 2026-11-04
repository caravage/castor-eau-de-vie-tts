# geo (pmat_geo.json) : [centre x, centre y, largeur, hauteur] en pixels de l'image du plateau.
# Plateau du joueur v3 : images, points d'aimantation, mini-sacs de l'entrepôt, calcul du capital (Lua), cartes 63,5 x 88.
# À lancer après build_v17.py, sur Castor_et_eau-de-vie.json.
import json, copy, hashlib, shutil, math, os
D='/tmp/claude-0/-home-claude/3c5a2878-065c-5165-9c41-6d23b49bdcf8/scratchpad/'
R=D+'repo/'; P=R+'Castor_et_eau-de-vie.json'; V=D+'vision/'
GH='https://raw.githubusercontent.com/caravage/castor-eau-de-vie-tts/main/img/v18/'
d=json.load(open(P)); objs=d['ObjectStates']
geo=json.load(open(V+'pmat_geo.json'))
IW,IH=1860,1200; MW=16.275; PX=IW/MW
COLS=['rouge','bleu','vert']
KINDS=['marchandises','eau-de-vie','castor']
LABEL={'marchandises':'Marchandises','eau-de-vie':'Eau-de-vie','moyen canot':'Moyens canots','grand canot':'Grands canots','castor':'Fourrures'}

# 1. images du plateau
for i,c in enumerate(COLS): shutil.copy(V+f'pmat_v3_{i}.png', R+f'img/v18/pmat_v3_{i}.png')
# 2. textures + maillages des mini-sacs (même visuel pour les trois familles)
from PIL import Image
src=open(R+'src/meshes.py').read()
def block(name):
    i=src.index(f'def {name}('); lines=src[i:].split('\n'); out=[lines[0]]
    for l in lines[1:]:
        if l and not l[0].isspace(): break
        out.append(l)
    return '\n'.join(out)
ns={}; exec('import math, json, os\nimport numpy as np, mapbox_earcut as earcut\nfrom PIL import Image\n'+block('mesh'),ns)
im=Image.open(V+'pmat_v3_0.png').convert('RGB')
S=240; circ=[(S/2+(S/2-2)*math.cos(2*math.pi*i/64),S/2+(S/2-2)*math.sin(2*math.pi*i/64)) for i in range(64)]
cwd=os.getcwd(); os.chdir(R)
SLUG={'marchandises':'marchandises','eau-de-vie':'eaudevie','moyen canot':'moyen','grand canot':'grand','castor':'castor'}
for k,(x,y,w,h) in zip(KINDS,geo['bags']):
    ns['mesh'](f'v18/sac_pm_{SLUG[k]}',f'v18/pm_{SLUG[k]}',circ,20,(S//2,3))
os.chdir(cwd)

def guid(seed):
    used={q.get('GUID') for q in objs}; g=hashlib.md5(seed.encode()).hexdigest()[:6]
    while g in used: g=hashlib.md5((g+'x').encode()).hexdigest()[:6]
    return g
def local(px,py):   # pixel du plateau -> coordonnées locales de la tuile (rotY 180)
    return round(-((px/IW)*2-1),4), round(((py/IH)*2-1)*(IH/IW),4)
def world(cx,cz,px,py):
    return round(cx+(px-IW/2)/PX,3), round(cz-(py-IH/2)/PX,3)

tpl=[q for q in objs if q.get('Nickname')=='Moyen canot rouge'][0]
mats={c:[q for q in objs if q.get('Nickname')=='Plateau du joueur '+c][0] for c in COLS}
for i,c in enumerate(COLS):
    m=mats[c]
    for kk in ('ImageURL','ImageSecondaryURL'): m['CustomImage'][kk]=GH+f'pmat_v3_{i}.png?v43'
    n=json.loads(m['GMNotes']); n['cap']=c; m['GMNotes']=json.dumps(n,ensure_ascii=False,separators=(', ',': '))
    # 3. points d'aimantation : 4 cartes (avec rotation) + 7 cases de soupçon
    sp=[]
    for (x,y,w,h) in geo['slots'][:4]:
        lx,lz=local(x,y); sp.append({'Position':{'x':lx,'y':0.05,'z':lz},'Rotation':{'x':0,'y':0,'z':0}})
    for (x,y,w,h) in geo['souf']:
        lx,lz=local(x,y); sp.append({'Position':{'x':lx,'y':0.05,'z':lz}})
    m.pop('AttachedSnapPoints',None)
    sw=[[round((x-IW/2)/PX,3),round(-(y-IH/2)/PX,3),1] for (x,y,w,h) in geo['slots'][:4]]+[[round((x-IW/2)/PX,3),round(-(y-IH/2)/PX,3),0] for (x,y,w,h) in geo['souf']]
    n=json.loads(m['GMNotes']); n['snapw']=sw; m['GMNotes']=json.dumps(n,ensure_ascii=False,separators=(', ',': '))
    # 4. mini-sacs de l'entrepôt (vides au départ)
    cx,cz=m['Transform']['posX'],m['Transform']['posZ']
    for k,(x,y,w,h) in zip(KINDS,geo['bags']):
        b=copy.deepcopy(tpl); b['ContainedObjects']=[]; b['GUID']=guid(f'pm{c}{k}')
        X,Z=world(cx,cz,x,y); dia=round(w/PX,3)
        b['Nickname']=f'Entrepôt · {LABEL[k]} ({c})'
        b['Description']='Propriétés du joueur à Québec. Le nombre affiché se met à jour seul.'
        b['GMNotes']=json.dumps({'w':dia,'x':X,'z':Z,'h':0.3,'y3':True,'lock':True,'pm':c,'k':k},ensure_ascii=False,separators=(', ',': '))
        b['CustomMesh']=dict(tpl['CustomMesh'],MeshURL=GH+f'sac_pm_{SLUG[k]}.obj',DiffuseURL=GH+f'pm_{SLUG[k]}.png?v42',TypeIndex=6)
        b['Transform'].update(posX=X,posZ=Z,posY=2.0,scaleX=dia,scaleY=dia,scaleZ=dia)
        b['Locked']=True; objs.append(b)
# 5. capital : pastille à la couleur du joueur dans la case « = » (remplace les compteurs TTS)
COUL={}
for c in COLS:
    COUL[c]=[q for q in objs if q.get('Nickname')=='Part '+c][0]['ColorDiffuse']
objs[:]=[q for q in objs if not (q.get('Name')=='Counter' and (q.get('Nickname') or '').startswith('Capital circulant'))]
# 5b. parts : 20 par joueur dans un sac verrouillé (la pile tombait au chargement)
os.chdir(R); circP=[(100+98*math.cos(2*math.pi*i/48),100+98*math.sin(2*math.pi*i/48)) for i in range(48)]
ns['mesh']('v18/sac_part','v18/tok_disc',circP,16,(100,3)); os.chdir(cwd)
for c in COLS:
    parts=[q for q in objs if q.get('Nickname')=='Part '+c]
    objs[:]=[q for q in objs if q.get('Nickname')!='Part '+c]
    X,Z=parts[0]['Transform']['posX'],parts[0]['Transform']['posZ']
    b=copy.deepcopy(tpl); b['GUID']=guid('parts'+c); b['Nickname']='Parts '+c; b['Description']='20 parts de navire ou de distillerie.'
    for q in parts: q['Transform'].update(posX=0,posY=0,posZ=0); q['Locked']=False
    b['ContainedObjects']=parts; b['ColorDiffuse']=parts[0]['ColorDiffuse']
    b['CustomMesh']=dict(tpl['CustomMesh'],MeshURL=GH+'sac_part.obj',DiffuseURL=GH+'tok_disc.png?v38',TypeIndex=6)
    b['GMNotes']=json.dumps({'w':0.7,'x':X,'z':Z,'h':0.6,'y3':True,'lock':True},ensure_ascii=False,separators=(', ',': '))
    b['Transform'].update(posX=X,posZ=Z,scaleX=0.7,scaleY=0.7,scaleZ=0.7); b['Locked']=True; objs.append(b)
# 5c. jetons marchandises / eau-de-vie : sortent des sacs à l'endroit
def face(os_):
    for q in os_:
        if (q.get('Nickname') or '').startswith(('Eau-de-vie','Marchandises')) or q.get('Name')=='Custom_Token' and 'tok_bouteille' in str(q.get('CustomImage')):
            try: n=json.loads(q.get('GMNotes') or '')
            except Exception: n=None
            if isinstance(n,dict) and 'w' in n and 'x' not in n: n['face']='up'; q['GMNotes']=json.dumps(n,ensure_ascii=False,separators=(', ',': '))
        face(q.get('ContainedObjects',[]))
face(objs)
# 5d. pastilles du capital (hôte du nombre affiché)
for c in COLS:
    m=mats[c]; cx,cz=m['Transform']['posX'],m['Transform']['posZ']
    X,Z=world(cx,cz,geo['slots'][3][0],geo['ctr'][0][1])
    h=copy.deepcopy(tpl); h.pop('ContainedObjects',None); h.pop('Bag',None); h['Name']='Custom_Model'; h['GUID']=guid('capd'+c)
    h['Nickname']='Capital circulant '+c
    h['Description']='Capital circulant : charges (10 au plus) + tuiles de fourrure x prix du castor + parts + palier de la piste Livres. Bouton « Calculer le capital » (haut droite) ou clic droit > Recalculer le capital.'
    h['ColorDiffuse']=COUL[c]; h['CustomMesh']=dict(tpl['CustomMesh'],MeshURL=GH+'sac_part.obj',DiffuseURL=GH+'tok_disc.png?v38',TypeIndex=0)
    h['GMNotes']=json.dumps({'w':0.6,'x':X,'z':Z,'h':0.4,'y3':True,'lock':True,'capd':c},ensure_ascii=False,separators=(', ',': '))
    h['Transform'].update(posX=X,posZ=Z,scaleX=0.6,scaleY=0.6,scaleZ=0.6); h['Locked']=True; objs.append(h)
# 5e. sac des congés en forme de congé
exec(block('rrect'),ns)
os.chdir(R); ns['mesh']('v18/sac_conge','v18/conge_back',ns['rrect'](4,4,396,396,40),36,(200,6)); os.chdir(cwd)
sc=[q for q in objs if q.get('Nickname')=='Sac des congés'][0]
sc['Name']='Custom_Model_Bag'; sc['CustomMesh']=dict(tpl['CustomMesh'],MeshURL=GH+'sac_conge.obj',DiffuseURL=GH+'conge_back.png?v43',TypeIndex=6)
sc['ColorDiffuse']={'r':1.0,'g':1.0,'b':1.0}; sc['MaterialIndex']=3
n=json.loads(sc['GMNotes']); n.pop('rnd',None); n['w']=1.4; sc['GMNotes']=json.dumps(n,ensure_ascii=False,separators=(', ',': '))
# 5f. plateaux et sacs verrouillés, posés à plat : ils tombent sur la table au chargement puis se verrouillent
for q in objs:
    if q['Name'] in ('Bag','Custom_Model_Bag','Custom_Model_Infinite_Bag','Infinite_Bag','Custom_Model') and (q.get('Nickname') or '').startswith(('Capital circulant','Entrepôt','Parts ','Sac ','Expéditions','Marchandises','Eau-de-vie','Grand canot','Moyen canot','Petit canot','Castor','Tuiles','Forts','Missions','Jetons','Marqueurs','Zones','Coureurs','Guide','Interpr','Hivernant')) or q['Name'] in ('Bag','Custom_Model_Bag','Custom_Model_Infinite_Bag','Infinite_Bag') or (q.get('Nickname') or '').startswith('Plateau du joueur'):
        q['Locked']=True
        try: n=json.loads(q.get('GMNotes') or '')
        except Exception: n=None
        if isinstance(n,dict) and 'x' in n: n['lock']=True; n['drop']=True; q['GMNotes']=json.dumps(n,ensure_ascii=False,separators=(', ',': '))
# 5g. aimantation : marqueurs de soupçon et cartes
def snapf(os_):
    for q in os_:
        if q['Name'] in ('Card','Deck') or (q.get('Nickname') or '').startswith('Soupçon'): q['Snap']=True
        snapf(q.get('ContainedObjects',[]))
snapf(objs)
# 5h. textures : ₶ sur les sacs de parts, œil sur les jetons de soupçon
from PIL import ImageDraw, ImageFont
base=Image.open(R+'img/v18/tok_disc.png').convert('RGBA')
t=base.copy(); dr=ImageDraw.Draw(t); f=ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSerif.ttf',120)
dr.text((100,104),'₶',font=f,fill=(55,48,40,255),anchor='mm'); t.save(R+'img/v18/part_lt.png')
for q in objs:
    if (q.get('Nickname') or '').startswith('Parts '): q['CustomMesh']['DiffuseURL']=GH+'part_lt.png?v43'
os.chdir(R); ns['mesh']('v18/sac_part_lt','v18/part_lt',circP,16,(100,3)); os.chdir(cwd)
for q in objs:
    if (q.get('Nickname') or '').startswith('Parts '): q['CustomMesh']['MeshURL']=GH+'sac_part_lt.obj'
t=base.copy(); dr=ImageDraw.Draw(t); W2=6
dr.arc((34,58,166,178),200,340,fill=(55,48,40,255),width=W2); dr.arc((34,22,166,142),20,160,fill=(55,48,40,255),width=W2)
dr.ellipse((76,76,124,124),fill=(55,48,40,255)); dr.ellipse((90,86,102,98),fill=(244,244,244,255)); t.save(R+'img/v18/tok_oeil.png')
for q in objs:
    if (q.get('Nickname') or '').startswith('Soupçon'): q['CustomImage']['ImageURL']=GH+'tok_oeil.png?v43'
# 5i. Rivière : cases ramenées à la taille des cartes (63,5 x 88)
tb=Image.open(R+'img/v18/table_v17.png').convert('RGB'); BG=(35,27,21)
CWp,CHp=round(3.5*94.0257),round(3.5*88/63.5*94.0257)
for (x0,y0,x1,y1) in ((31,579,389,1128),(32,1192,388,1680),(32,1765,388,2252),(32,2337,388,2825),(31,2908,389,3399)):
    cut=tb.crop((x0,y0,x1+1,y1+1)).resize((CWp,CHp),Image.LANCZOS); cx_,cy_=(x0+x1)//2,(y0+y1)//2
    ImageDraw.Draw(tb).rectangle((x0-4,y0-4,x1+4,y1+4),fill=BG); tb.paste(cut,(cx_-CWp//2,cy_-CHp//2))
tb.save(R+'img/v18/table_v17r.png')
for q in objs:
    if q.get('Nickname')=='Table du castor':
        for kk in ('ImageURL','ImageSecondaryURL'): q['CustomImage'][kk]=GH+'table_v17r.png?v43'
# 5j. congés v41 (taille du jeton coureur des bois, 1,4) et cartes Expédition v4
import re as _re
def maj(os_):
    for q in os_:
        ci=q.get('CustomImage')
        if ci and 'c40_' in (ci.get('ImageURL') or ''):
            for kk in ('ImageURL','ImageSecondaryURL'):
                if ci.get(kk): ci[kk]=_re.sub(r'c40_([a-z0-9_]+)\.png\?v\d+',r'c41_\1.png?v43',ci[kk])
            n=json.loads(q.get('GMNotes') or '{}'); n['w']=1.4; n['d']=1.4; q['GMNotes']=json.dumps(n,ensure_ascii=False,separators=(', ',': '))
        for cd in (q.get('CustomDeck') or {}).values():
            m=_re.match(r'.*/exp_(rouge|bleu|vert)\.png\?v\d+$',cd.get('FaceURL',''))
            if m: cd['FaceURL']=GH+f'exp_v4_{m.group(1)}.png?v43'
        maj(q.get('ContainedObjects',[]))
maj(objs)
# 5k. canots v2 des joueurs (coque low-poly, lettre sur les flancs) et sacs de canots
LB={'grand':150/692,'petit':116/452,'coureur':92/332}
def canots(os_):
    for q in os_:
        for st in [q]+list((q.get('States') or {}).values()):
            cm=st.get('CustomMesh') or {}
            m=_re.search(r'/canot3d_(grand|petit|coureur)(_couche)?\.obj$',cm.get('MeshURL') or '')
            if not m: continue
            key=m.group(1); cm['MeshURL']=GH+f'canot4_{key}{m.group(2) or ""}.obj'
            t=_re.search(r'/cn_(rouge|bleu|vert)_(grand|petit|coureur)(?:_([ABC]))?\.png',cm.get('DiffuseURL') or '')
            if t: cm['DiffuseURL']=GH+(f'cn4_{t.group(1)}_{key}_{t.group(3)}.png?v44' if t.group(3) else f'cn4_{t.group(1)}_{key}_sac.png?v44')
            try: n=json.loads(st.get('GMNotes') or '')
            except Exception: n=None
            if isinstance(n,dict) and 'w' in n: n['d']=round(n['w']*LB[key],4); st['GMNotes']=json.dumps(n,ensure_ascii=False,separators=(', ',': '))
        canots(q.get('ContainedObjects',[]))
canots(objs)
# 5l. cartes navire et distillerie : points d'aimantation posés par le script (positions monde)
for q in objs:
    nk=q.get('Nickname') or ''
    if nk.startswith(('Carte de navire','Carte de distillerie')):
        xs_=[523,657,791,926,1060] if 'navire' in nk else [559,720,879,1040]
        q.pop('AttachedSnapPoints',None)
        n=json.loads(q['GMNotes']); n['snapw']=[[round((px/1200-0.5)*4.2,3),round(-(352/640-0.5)*2.24,3),0] for px in xs_]
        q['GMNotes']=json.dumps(n,ensure_ascii=False,separators=(', ',': '))
# 5m. jetons de soupçon : œil blanc (celui de la carte « +1 soupçon ») sur fond de couleur
def oeil(col):
    t=Image.new('RGBA',(200,200),(0,0,0,0)); dr=ImageDraw.Draw(t)
    dr.ellipse((4,4,196,196),fill=col,outline=(42,36,24,255),width=8)
    def q(p0,p1,p2,n=24): return [((1-u)**2*p0[0]+2*(1-u)*u*p1[0]+u*u*p2[0],(1-u)**2*p0[1]+2*(1-u)*u*p1[1]+u*u*p2[1]) for u in [i/n for i in range(n+1)]]
    k=2.3; ox,oy=100-35*k,100-22*k; P=lambda x,y:(ox+x*k,oy+y*k)
    dr.polygon(q(P(4,22),P(35,-6),P(66,22))+q(P(66,22),P(35,50),P(4,22))[1:],fill=(247,240,220,255))
    c=P(35,22); r=10*k; dr.ellipse((c[0]-r,c[1]-r,c[0]+r,c[1]+r),fill=tuple(int(v*.55) for v in col[:3])+(255,))
    return t
for c in COLS:
    rgb=tuple(round(COUL[c][k]*255) for k in 'rgb')+(255,)
    oeil(rgb).save(R+f'img/v18/tok_oeil_{c}.png')
    for q in objs:
        if q.get('Nickname')=='Soupçon '+c: q['CustomImage']['ImageURL']=GH+f'tok_oeil_{c}.png?v45'; q['ColorDiffuse']={'r':1.0,'g':1.0,'b':1.0}
# 5n. marqueurs Livres et Crédit carrés
def carre(col,txt=None,S=160):
    t=Image.new('RGBA',(S,S),(0,0,0,0)); dr=ImageDraw.Draw(t)
    dr.rounded_rectangle((3,3,S-4,S-4),radius=18,fill=col,outline=tuple(int(v*.5) for v in col[:3])+(255,),width=9)
    dr.rounded_rectangle((22,22,S-23,S-23),radius=10,outline=tuple(min(255,int(v+(255-v)*.45)) for v in col[:3])+(255,),width=4)
    if txt: dr.text((S/2,S/2+2),txt,font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',40),fill=(255,255,255,255),anchor='mm')
    return t
for c in COLS:
    rgb=tuple(round(COUL[c][k]*255) for k in 'rgb')+(255,)
    carre(rgb).save(R+f'img/v18/sq_livres_{c}.png'); carre(rgb,'+30').save(R+f'img/v18/sq_livres_{c}_30.png')
    for q in objs:
        if q.get('Nickname')=='Livres '+c:
            q['CustomImage']['ImageURL']=GH+f'sq_livres_{c}.png?v45'; q['CustomImage']['ImageSecondaryURL']=GH+f'sq_livres_{c}_30.png?v45'; q['CustomImage']['CustomTile']['Type']=3
carre((255,255,255,255)).save(R+'img/v18/tok_carre.png')
for q in objs:
    if (q.get('Nickname') or '').startswith('Crédit '): q['CustomImage']['ImageURL']=GH+'tok_carre.png?v45'
# 5o. pastille du capital : tuile carrée de la taille d'une tuile castor (1,05), à la couleur du joueur
os.chdir(R); ns['mesh']('v18/sac_carre','v18/tok_carre',ns['rrect'](3,3,154,154,18),14,(80,6)); os.chdir(cwd)
for q in objs:
    if (q.get('Nickname') or '').startswith('Capital circulant '):
        q['CustomMesh']['MeshURL']=GH+'sac_carre.obj'; q['CustomMesh']['DiffuseURL']=GH+'tok_carre.png?v45'
        n=json.loads(q['GMNotes']); n['w']=1.05; q['GMNotes']=json.dumps(n,ensure_ascii=False,separators=(', ',': '))
        q['Transform'].update(scaleX=1.05,scaleY=1.05,scaleZ=1.05)
# 5p. jetons Guide / Interprète / Hivernant agrandis pour remplir l'ovale Voyageur ; sac Expéditions des coureurs renommé
def voy(os_):
    for q in os_:
        if q.get('Nickname') in ('Guide','Interprète','Hivernant'):
            n=json.loads(q['GMNotes']); n['w']=0.82; n['d']=1.18; q['GMNotes']=json.dumps(n,ensure_ascii=False,separators=(', ',': '))
        voy(q.get('ContainedObjects',[]))
voy(objs)
for q in objs:
    nk=q.get('Nickname') or ''
    if nk.startswith('Expéditions · Petit canot (coureurs des bois)'): q['Nickname']=nk.replace('Petit canot (coureurs des bois)','Coureurs des bois')
# 6. cartes au format 63,5 x 88
def cards(os_):
    for q in os_:
        try: n=json.loads(q.get('GMNotes') or '')
        except Exception: n=None
        if isinstance(n,dict) and q['Name'] in ('Card','Deck'):
            if n.get('w')==3.5 and n.get('d')==4.9: n['d']=round(3.5*88/63.5,3)
            elif n.get('w')==2.45 and n.get('d')==3.43: n['d']=round(2.45*88/63.5,3)
            q['GMNotes']=json.dumps(n,ensure_ascii=False,separators=(', ',': '))
        cards(q.get('ContainedObjects',[]))
cards(objs)
# 7. script : compteurs des mini-sacs + capital circulant
t=[q for q in objs if q.get('Nickname')=='Table du castor'][0]['Transform']
im2=Image.open(R+'img/v18/table_v17.png'); TW=2*t['scaleX']; L=t['posX']-TW/2; k=im2.size[0]/TW
LUA=f'''

-- Capital circulant (livret) : charges (10 au plus) + tuiles de fourrure x prix du castor + parts + palier de la piste Livres.
-- Ce qui est en expédition ne compte pas. Les sacs d'entrepôt affichent leur contenu à chaque entrée / sortie ;
-- le capital se recalcule avec le bouton « Calculer le capital » (haut droite de l'écran) ou clic droit sur le compteur.
local LIV0, PRIX4, PAS = {round(L+1096.9/k,3)}, {round(L+4019.6/k,3)}, {round(108.6/k,4)}
local COUL = {{{', '.join(f'["{c}"] = {{{COUL[c]["r"]:.3f}, {COUL[c]["g"]:.3f}, {COUL[c]["b"]:.3f}}}' for c in COLS)}}}
local NOMS = {{["marchandises"] = "Marchandises", ["eau-de-vie"] = "Eau-de-vie", ["moyen canot"] = "Moyens canots", ["grand canot"] = "Grands canots", ["castor"] = "Fourrures"}}
local function palier(n) if n >= 25 then return 15 elseif n >= 20 then return 14 elseif n >= 15 then return 12 elseif n >= 10 then return 9 elseif n >= 5 then return 5 end return 0 end
local function arrondi(v) return math.floor(v + 0.5) end
function rien() end
local function sac(o) local g = o.getGMNotes() or "" if g:find('"pm"', 1, true) then local n = notes(o) if n and n.pm then return n end end end
local function afficheSac(b, n)
  local q = b.getQuantity()
  b.setName("Entrepôt · " .. (NOMS[n.k] or n.k) .. " (" .. n.pm .. ") : " .. q)
  local ok, bs = pcall(function() return b.getButtons() end)
  if ok and bs and #bs > 0 then b.editButton({{index = 0, label = tostring(q)}}) return q end
  local sc = 1 / b.getScale().x
  b.createButton({{click_function = "rien", function_owner = Global, label = tostring(q), position = {{0, 0.11, 0.77}},
    scale = {{sc, sc, sc}}, width = 340, height = 300, font_size = 260,
    color = {{0.16, 0.14, 0.09}}, font_color = {{0.96, 0.92, 0.84}}, hover_color = {{0.16, 0.14, 0.09}}, press_color = {{0.16, 0.14, 0.09}}}})
  return q
end
local function capital()
  local sacs, cpt, parts, cartes, livres, prix = {{}}, {{}}, {{}}, {{}}, {{}}, nil
  for _, o in ipairs(getObjects()) do
    local nm = o.getName()
    local n = sac(o)
    if n then sacs[n.pm] = sacs[n.pm] or {{}}; sacs[n.pm][n.k] = afficheSac(o, n)
    elseif nm:find("^Capital circulant ") then cpt[nm:sub(19)] = o
    elseif nm:find("^Part ") then table.insert(parts, o)
    elseif nm:find("^Carte de navire") or nm:find("^Carte de distillerie") then table.insert(cartes, o)
    elseif nm:find("^Livres ") then livres[nm:sub(8)] = o
    elseif nm == "Prix du castor" then prix = o end
  end
  local p = 0
  if prix then p = math.max(1, math.min(8, 4 + arrondi((prix.getPosition().x - PRIX4 * F) / (PAS * F)))) end
  for c, ct in pairs(cpt) do
    local q = sacs[c] or {{}}
    local charges = math.min(10, (q["marchandises"] or 0) + (q["eau-de-vie"] or 0))
    local np = 0
    for _, pt in ipairs(parts) do
      if pt.getName() == "Part " .. c then
        local pp = pt.getPosition()
        for _, ca in ipairs(cartes) do
          local bb = ca.getBounds()
          if math.abs(pp.x - bb.center.x) <= bb.size.x / 2 and math.abs(pp.z - bb.center.z) <= bb.size.z / 2 then np = np + 1 break end
        end
      end
    end
    local nl = 0
    if livres[c] then nl = math.max(0, arrondi((livres[c].getPosition().x - LIV0 * F) / (PAS * F))) end
    local total = tostring(charges + (q["castor"] or 0) * p + np + palier(nl))
    local cc = COUL[c] or {{0.16, 0.14, 0.09}}
    local ok, bs = pcall(function() return ct.getButtons() end)
    if ok and bs and #bs > 0 then ct.editButton({{index = 0, label = total}})
    else
      local sc = 1 / ct.getScale().x
      ct.createButton({{click_function = "boutonCapital", function_owner = Global, label = total, position = {{0, 0.11, 0}},
        scale = {{sc, sc, sc}}, width = 0, height = 0, font_size = 520, tooltip = "Recalculer le capital",
        color = cc, font_color = {{1, 1, 1}}, hover_color = cc, press_color = cc}})
    end
  end
end
function majCapital() pcall(capital) end
function boutonCapital() majCapital() end
local function majSac(c) Wait.frames(function() if c and not c.isDestroyed() then local n = sac(c) if n then afficheSac(c, n) end end end, 1) end
-- Cartes Expédition : points d'aimantation du congé (ou du coureur) et des voyageurs, posés quand la carte arrive sur la table.
local EXPSNAP = {{grand = {{{{195.0, 283.0}}, {{493.0, 283.0}}, {{695.0, 283.0}}, {{897.0, 283.0}}, {{165.0, 585.5}}, {{345.0, 585.5}}, {{525.0, 585.5}}, {{705.0, 585.5}}, {{885.0, 585.5}}}}, moyen = {{{{195.0, 283.0}}, {{560.3, 283.0}}, {{829.7, 283.0}}, {{345.0, 585.5}}, {{525.0, 585.5}}, {{705.0, 585.5}}}}, coureur = {{{{191.0, 424.0}}}}}}
local function snapsExp(o)
  if not o or o.isDestroyed() or o.type ~= "Card" then return end
  local nm = o.getName()
  if not nm:find("^Expédition ") then return end
  local pts = nm:find("Grand canot") and EXPSNAP.grand or (nm:find("Moyen canot") and EXPSNAP.moyen or EXPSNAP.coureur)
  local b = o.getBounds(); local sp = {{}}
  for _, p in ipairs(pts) do
    local w = {{b.center.x + (p[1] / 1050 - 0.5) * b.size.x, b.center.y + b.size.y / 2, b.center.z - (p[2] / 750 - 0.5) * b.size.z}}
    table.insert(sp, {{position = o.positionToLocal(w), rotation_snap = false}})
  end
  pcall(function() o.setSnapPoints(sp) end)
end
local function snapsTous() for _, o in ipairs(getObjects()) do pcall(snapsExp, o) end end
local function snapsW()
  for _, o in ipairs(getObjects()) do
    local g = o.getGMNotes() or ""
    if g:find('"snapw"', 1, true) then
      local n = notes(o)
      if n and n.snapw then
        local p, sp = o.getPosition(), {{}}
        local bb = o.getBounds(); local top = bb.center.y + bb.size.y / 2
        for _, v in ipairs(n.snapw) do
          table.insert(sp, {{position = o.positionToLocal({{p.x + v[1] * F, top, p.z + v[2] * F}}), rotation = {{0, 0, 0}}, rotation_snap = v[3] == 1}})
        end
        pcall(function() o.setSnapPoints(sp) end)
      end
    end
  end
end
local ancienSortie = onObjectLeaveContainer
function onObjectLeaveContainer(c, o) if ancienSortie then ancienSortie(c, o) end majSac(c)
  Wait.condition(function() Wait.time(function() pcall(snapsExp, o) end, 0.6) end, function() return o.isDestroyed() or not o.spawning end, 10)
end
function onObjectEnterContainer(c, o) majSac(c) end
local function menus()
  for _, o in ipairs(getObjects()) do
    if o.getName():find("^Capital circulant ") then pcall(function() o.addContextMenuItem("Recalculer le capital", function() majCapital() end) end) end
  end
end
Wait.time(function() menus(); majCapital(); snapsTous(); snapsW() end, 4)
'''
OLD='      if not m[1].isDestroyed() and not m[2].lock then m[1].setLock(false) end'
assert OLD in d['LuaScript']
d['LuaScript']=d['LuaScript'].replace(OLD,'      if not m[1].isDestroyed() and (not m[2].lock or m[2].drop) then m[1].setLock(false) end\n    end\n    Wait.time(function()\n      for _, m2 in ipairs(moved) do if m2[2].drop and not m2[1].isDestroyed() then m2[1].setLock(true) end end\n    end, 3)\n    for _, m in ipairs({}) do')
d['LuaScript']=d['LuaScript'].rstrip('\n')+LUA
d['XmlUI']='<Button id="capital" onClick="boutonCapital" rectAlignment="UpperRight" offsetXY="-20 -70" width="200" height="40" fontSize="18" color="#2A2418" textColor="#F4EBD6">Calculer le capital</Button>'
json.dump(d,open(P,'w'),ensure_ascii=False,indent=2)
print('ok',len(objs),'LIV0',round(L+1096.9/k,3),'PRIX4',round(L+4019.6/k,3),'PAS',round(108.6/k,4))
