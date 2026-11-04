import json, re, math, copy
from PIL import Image, ImageDraw
D='/tmp/claude-0/-home-claude/3c5a2878-065c-5165-9c41-6d23b49bdcf8/scratchpad/'
R=D+'repo/'; IMG=R+'img/v18/'
T=Image.open(IMG+'table_full.png').convert('RGB'); M=Image.open(D+'carte_etendue_2x.png').convert('RGB').crop((0,0,2800*2,3000))
PU=4600/42.68; s=PU/(4401/51.34); k=2.934; OPU=4401/51.34
def crop(b,f=1.0):
    im=T.crop(b); return im.resize((round(im.width*s*f),round(im.height*s*f)),Image.LANCZOS)
u=lambda v: round(v*PU)
mapw=M.width/PU; maph=M.height/PU
CAL=(int(255*k),int(30*k),int(1455*k),int(172*k)); f=(M.width-0.5*PU)/((CAL[2]-CAL[0])*s)
cal=crop(CAL,f); TRK=(int(430*k),int(180*k),int(1290*k),int(258*k)); trk=crop(TRK)
BOT=(740,2425,4120,2870); bot=crop(BOT); RIV=(0,0,600,2925); riv=crop(RIV)
x0=7.6; y=0.5
ycal=y; y+=cal.height/PU+0.3; ytrk=y; y+=trk.height/PU+0.5; ymap=y; y+=maph+0.4; ybot=y; y+=bot.height/PU+0.5
H=y; W=x0+mapw; xtrk=x0+(mapw-0.5-trk.width/PU)/2; yriv=(H-riv.height/PU)/2
C=Image.new('RGB',(u(W),u(H)),(34,51,47)); dr=ImageDraw.Draw(C)
dr.rounded_rectangle([u(7.2),u(0.2),u(W)+u(1),u(H-0.2)],radius=u(0.5),fill=(230,218,182))
rb=T.getpixel((60,2915)); dr.rectangle([0,0,riv.width-1,u(H)],fill=rb); C.paste(riv,(0,u(yriv)))
C.paste(cal,(u(x0),u(ycal))); C.paste(trk,(u(xtrk),u(ytrk))); C.paste(M,(u(x0),u(ymap))); C.paste(bot,(u(x0),u(ybot)))
C=C.resize((5600,round(5600*C.height/C.width)),Image.LANCZOS); C.save(IMG+'table_v17.png',optimize=True)
print('plateau',round(W,2),round(H,2))
# --- jetons hexagonaux (carré plein : la découpe hex de TTS donne le bord)
lys=Image.open(D+'vision/fort_hex.png').convert('RGBA')
def full(src,bg):
    im=Image.new('RGBA',(256,256),bg); c=src.resize((236,236),Image.LANCZOS); im.alpha_composite(c,(10,10)); return im
full(Image.open(D+'vision/fort_hex.png').convert('RGBA'),(255,255,255,255)).save(IMG+'fort_hex.png')
full(Image.open(D+'vision/mission_hex.png').convert('RGBA'),(30,26,22,255)).save(IMG+'mission_hex.png')
# --- module
P=R+'Castor_et_eau-de-vie.json'; d=json.load(open(P))
OL,OT=-2.96-51.34/2, 1.8+51.34*2925/4401/2
NL=-2.96-W/2; NB=-15.26; NT=NB+H; NC=(NL+W/2, NT-H/2)
def old_px(X,Z): return ((X-OL)*OPU,(OT-Z)*OPU)
def new_xz(ux,uy): return (NL+ux, NT-uy)
def band(tx,ty,b,ox,oy,ff=1.0): return new_xz(ox+(tx-b[0])*ff/OPU, oy+(ty-b[1])*ff/OPU)
src=open(D+'artifact-files/f7b65138-ad7d-4d14-8f1a-e534080bf5d7/project/Main.dc.html').read()
cart={}
for m in re.finditer(r'<div style="position: absolute; left: ([-\d.]+)px; top: ([-\d.]+)px; width: 313.6px; height: 264.0px; box-sizing: border-box; border-radius: 15.1px;',src):
    nm=re.search(r'>([^<>]{3,40})</div>',src[m.end():m.end()+3000]).group(1).strip()
    cart[nm]=(float(m.group(1)),float(m.group(2)))
print('comptoirs',cart)
def root_xz(rx,ry): return new_xz(x0+rx*2/PU, ymap+ry*2/PU)
setx=lambda o,X,Z:(o['Transform'].__setitem__('posX',round(X,3)),o['Transform'].__setitem__('posZ',round(Z,3)))
objs=[]; tpl={}; DZ=round(NT-18.86+0.6,2); TAP=None
# sacs de pions rangés au-dessus de la rade de Québec (px racine de la carte)
col=lambda i:2385+i*86
BAGS={'Guides':(col(0),120),'Interprètes':(col(1),120),'Hivernants':(col(2),120),'Coureurs des bois':(col(3),120),'Zones fermées':(col(4),120),
 'Forts français':(col(0),265),'Forts anglais':(col(1),265),'Missions':(col(2),265),'Jetons Abîmé':(col(3),265),'Marqueurs Ravagé':(col(4),265)}
for o in d['ObjectStates']:
    n=o.get('Nickname',''); t=o['Transform']; X,Z=t['posX'],t['posZ']
    if n in ('Carte v15 (test)','Prendre le pas · 1er','Dé du marché'): continue
    if n.startswith('Carte de navire') or n.startswith('Carte de distillerie'):
        xs_=[523,657,791,926,1060] if 'navire' in n else [559,720,879,1040]
        o['AttachedSnapPoints']=[{'Position':{'x':round(-((px/1200)*2-1),4),'y':0.05,'z':round(-(352/640*2-1)*640/1200,4)}} for px in xs_]
    if n=='Table du castor':
        for kk in ('ImageURL','ImageSecondaryURL'): o['CustomImage'][kk]='https://raw.githubusercontent.com/caravage/castor-eau-de-vie-tts/main/img/v18/table_v17.png?v41'
        t['scaleX']=t['scaleZ']=round(W/2,4); setx(o,*NC)
    elif n=='Tapis de jeu':
        TAP=o; continue
    elif n in ('Année','Mois'):
        tx,ty=old_px(X,Z); setx(o,*band(tx,ty,CAL,x0,ycal,f))
    elif n in ('Ravages','Prix du castor'):
        tx,ty=old_px(X,Z); setx(o,*band(tx,ty,TRK,xtrk,ytrk))
    elif n.startswith('Livres ') or n.startswith('Crédit '):
        tx,ty=old_px(X,Z); setx(o,*band(tx,ty,BOT,x0,ybot))
    elif n in BAGS:
        setx(o,*root_xz(*BAGS[n]))
    elif n=='Sac des congés':
        setx(o,*root_xz(1977,496.5))
    elif n in ('Castor sec','Castor gras','Tuiles secrètes'):
        tx,ty=old_px(X,Z); setx(o,*band(tx,ty,RIV,0,yriv))
    elif n in ('Fort français','Mission'):
        tpl[n]=o; continue
    elif n=='Dé du marché':
        i=sum(1 for q in objs if q.get('Nickname')=='Dé du marché'); setx(o,*new_xz(x0+42+i*1.8, ybot+2.6))
    elif n=='Navire de la compagnie':
        setx(o,*root_xz(2376.5,491.5))
    elif Z>=19.0: t['posZ']=round(Z+DZ,3)
    elif X>=23.0 and Z>-20.5: t['posX']=round(X+5.5,3)
    objs.append(o)
# jetons fort / mission : images hex + mise en place sur les comptoirs
def hexify(o,img):
    o['CustomImage']['ImageURL']=o['CustomImage']['ImageSecondaryURL']=f'https://raw.githubusercontent.com/caravage/castor-eau-de-vie-tts/main/img/v18/{img}?v41'
    o['CustomImage']['CustomTile']['Type']=1
for o in objs:
    if o.get('Nickname')=='Forts anglais':
        for c in o['ContainedObjects']: hexify(c,'fort_uk_hex.png')
    if o.get('Nickname') in ('Forts français','Missions'):
        for c in o['ContainedObjects']: hexify(c,'fort_hex.png' if 'Fort' in c.get('Nickname','') else 'mission_hex.png')
for n in tpl: hexify(tpl[n],'fort_hex.png' if n=='Fort français' else 'mission_hex.png')
# tapis rogné à droite sur le contenu
xs=[q['Transform']['posX'] for q in objs if q['Name']!='HandTrigger']
zs=[q['Transform']['posZ'] for q in objs if q['Name']!='HandTrigger']
xl,xr=-34.5,max(xs)+3.5; zb,zt=-39.6,max(zs)+4.0
TAP['Transform']['scaleX']=round((xr-xl)/2,3); TAP['Transform']['scaleZ']=round((zt-zb)/2/(1491/1600),3); setx(TAP,(xl+xr)/2,(zb+zt)/2)
objs.insert(0,TAP)
print('tapis',round(xl,1),round(xr,1),round(zb,1),round(zt,1),'DZ',DZ)
# répartition des sacs de peaux (livret, Répartition des sacs ; Tuiles cachées)
def retag(bag,src,dst,n):
    for q in objs:
        if q.get('Nickname')!=bag: continue
        for c in q['ContainedObjects']:
            if n==0: break
            ci=c['CustomImage']; fr=ci['ImageURL'].split('/')[-1].split('?')[0]; bk=ci.get('ImageSecondaryURL','').split('/')[-1].split('?')[0]
            if (fr,bk)==src:
                ci['ImageURL']=ci['ImageURL'].replace(src[0],dst[0]); ci['ImageSecondaryURL']=ci['ImageSecondaryURL'].replace(src[1],dst[1]); n-=1
retag('Castor sec',('tile_G2_sec.png','tile_G2_gras.png'),('tile_G1_sec.png','tile_G1_gras.png'),3)
retag('Castor sec',('tile_G3_sec.png','tile_G3_gras.png'),('tile_G1_sec.png','tile_G1_gras.png'),1)
retag('Castor gras',('tile_gras_neutre.png','tile_S2_gras.png'),('tile_gras_neutre.png','tile_S1_gras.png'),2)
retag('Tuiles secrètes',('hid_fur2.png','hid_back.png'),('hid_fur1.png','hid_back.png'),1)
retag('Tuiles secrètes',('hid_fur3.png','hid_back.png'),('hid_fur1.png','hid_back.png'),1)
# sacs de jetons en forme de jeton (comme les voyageurs et les coureurs)
GH='https://raw.githubusercontent.com/caravage/castor-eau-de-vie-tts/main/img/v18/'
MESH={'Forts français':('sac_fort_fr','fort_hex.png?v41',1.1547),'Forts anglais':('sac_fort_uk','fort_uk_hex.png?v41',1.1547),'Missions':('sac_mission','mission_hex.png?v41',1.1547),
 'Jetons Abîmé':('sac_abime','abime.png?v38',1.0),'Marqueurs Ravagé':('sac_ravage','ravage.png?v38',1.0),'Zones fermées':('sac_zone_fermee','zone_fermee.png?v39',1.0)}
for q in objs:
    nk=q.get('Nickname')
    if nk in MESH and q['Name']=='Infinite_Bag':
        m,img,asp=MESH[nk]
        q['Name']='Custom_Model_Infinite_Bag'
        q['CustomMesh']={'MeshURL':GH+m+'.obj','DiffuseURL':GH+img,'NormalURL':'','ColliderURL':'','Convex':True,'MaterialIndex':3,'TypeIndex':7,'CastShadows':True}
        q['Bag']={'Order':0}; q['MaterialIndex']=3
        n=json.loads(q['GMNotes']); n['w']=1.2; n['d']=round(1.2*asp,3); n.pop('ry',None); n['h']=0.6; q['GMNotes']=json.dumps(n,ensure_ascii=False,separators=(', ',': '))
        t=q['Transform']; t['rotY']=180; q['ColorDiffuse']={'r':1.0,'g':1.0,'b':1.0}
    if (nk or '').startswith('Part '): q['Snap']=True
    if nk in MESH or nk=='Coureurs des bois':
        for c in q.get('ContainedObjects') or []:
            cn=json.loads(c.get('GMNotes') or '{}'); cn['face']='up'; c['GMNotes']=json.dumps(cn,ensure_ascii=False,separators=(', ',': '))
    if nk=='Castor gras': q['ColorDiffuse']={'r':round(190/255,4),'g':round(165/255,4),'b':round(120/255,4)}
    if nk=='Sac des congés':
        n=json.loads(q['GMNotes']); n['w']=1.0; q['GMNotes']=json.dumps(n,ensure_ascii=False,separators=(', ',': ')); q['Transform']['scaleX']=q['Transform']['scaleZ']=0.5
# zones de main centrées sur les plateaux des joueurs
PB={q['Nickname'].split()[-1]:q['Transform']['posX'] for q in objs if (q.get('Nickname') or '').startswith('Plateau du joueur')}
CMAP={'Red':'rouge','Blue':'bleu','Green':'vert'}
for q in objs:
    if q['Name']=='HandTrigger' and CMAP.get(q.get('FogColor')) in PB:
        pb=[r for r in objs if r.get('Nickname')=='Plateau du joueur '+CMAP[q['FogColor']]][0]; pn=json.loads(pb['GMNotes'])
        x=pn['x']; z=round(pn['z']-pn['d']/2-2.0,3)   # zone de 4 de profondeur collée sous le plateau, de sa largeur
        q['Transform']['posX']=round(x,3); q['Transform']['posZ']=z; q['Transform']['scaleX']=pn['w']
        n=json.loads(q['GMNotes']); n['x']=round(x,3); n['z']=z; n['hw']=pn['w']; q['GMNotes']=json.dumps(n,ensure_ascii=False,separators=(', ',': '))
# parts : 20 par joueur
import hashlib
used={q.get('GUID') for q in objs}
for col in ('rouge','bleu','vert'):
    parts=[q for q in objs if q.get('Nickname')==f'Part {col}']
    for i in range(20-len(parts)):
        c=copy.deepcopy(parts[0]); g=hashlib.md5(f'part{col}{i}'.encode()).hexdigest()[:6]
        while g in used: g=hashlib.md5((g+'x').encode()).hexdigest()[:6]
        used.add(g); c['GUID']=g; c['Transform']['posY']=round(c['Transform']['posY']+0.1*(i+1),3); objs.append(c)
# points d'aimantation globaux (script Lua) : pistes, tours, rades
lua=d['LuaScript']; line=[l for l in lua.split('\n') if l.startswith('local SNAP =')][0]
old=[tuple(map(float,q)) for q in re.findall(r'\{(-?[\d.]+),(-?[\d.]+)\}', line)]
new=[]
for X,Z in old:
    tx,ty=old_px(X,Z)
    if TRK[0]<=tx<=TRK[2] and TRK[1]<=ty<=TRK[3]: new.append(band(tx,ty,TRK,xtrk,ytrk))
    elif CAL[0]<=tx<=CAL[2] and CAL[1]<=ty<=CAL[3]: new.append(band(tx,ty,CAL,x0,ycal,f))
    elif 2720<=tx<=3452 and 1552<=ty<=2146: new.append(root_xz(2325+(tx-2726)*452.6/720, 396+(ty-1558)*452.6/720))
    elif 3510<=tx<=4244 and 1552<=ty<=2146:
        if tx-3510<380: new.append(root_xz(2534.9+(tx-3516)*242.7/386, 817+(ty-1558)*242.7/386))
newline=line.split('=')[0]+'= {'+','.join('{%.3f,%.3f}'%q for q in new)+'}'+(line[line.index('}   --'):][1:] if '}   --' in line else '')
d['LuaScript']=lua.replace(line,newline); print('snaps',len(old),'->',len(new))
# notes de mise en place (GMNotes) alignées sur les nouvelles positions
for q in objs:
    g=q.get('GMNotes') or ''
    try: n=json.loads(g)
    except Exception: continue
    if not isinstance(n,dict) or 'x' not in n: continue
    n['x']=round(q['Transform']['posX'],3); n['z']=round(q['Transform']['posZ'],3)
    if q.get('Nickname')=='Table du castor': n['w']=round(W,3); n['d']=round(H,3)
    if q.get('Nickname')=='Tapis de jeu': n['w']=round(xr-xl,3); n['d']=round(zt-zb,3)
    q['GMNotes']=json.dumps(n,ensure_ascii=False,separators=(', ',': '))
d['ObjectStates']=objs
json.dump(d,open(P,'w'),ensure_ascii=False,indent=2)
json.dump({'W':W,'H':H,'NL':NL,'NT':NT},open(D+'v17_geom.json','w'))
print('ok', len(objs))
