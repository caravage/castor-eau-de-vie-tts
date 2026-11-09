# Ferme du castor v8 (Prix FR 2-10, Dette 0-2, Prospérité 0-4, Caisse, Entrepôt ; 1500 x 1200) et plaquettes des partis (Château, Palais ; 560 x 960).
# Entrée : scratchpad ferme2/ (ferme_recto_v8.png, ferme_geo_v8.json, parti_*_v1.png, partis_geo_v1.json). Sortie : Castor_et_eau-de-vie.json + img/v18/.
import json, copy, hashlib, shutil, sys
S=sys.argv[1]; R=sys.argv[2]
GH='https://raw.githubusercontent.com/caravage/castor-eau-de-vie-tts/main/img/v18/'
P=R+'Castor_et_eau-de-vie.json'; d=json.load(open(P)); objs=d['ObjectStates']
guid=lambda s:hashlib.md5(s.encode()).hexdigest()[:6]
note=lambda n:json.dumps(n,ensure_ascii=False,separators=(', ',': '))
for f in ('ferme_recto_v8.png','parti_chateau_v1.png','parti_palais_v1.png'): shutil.copy(S+f,R+'img/v18/'+f)
# 1. Ferme
fg=json.load(open(S+'ferme_geo_v8.json')); FW,FH,FPX=1500,1200,150.0
pl=[q for q in objs if q.get('Nickname')=='Ferme du castor'][0]; FX,FZ=pl['Transform']['posX'],pl['Transform']['posZ']
pl['CustomImage'].update(ImageURL=GH+'ferme_recto_v8.png',ImageSecondaryURL=GH+'ferme_recto_v8.png')
n=json.loads(pl['GMNotes']); n.update(w=FW/FPX,d=FH/FPX); pl['GMNotes']=note(n)
pl['Description']='Prix en France 2-10 (départ 7) · Politique d’achat · Dette 0-2 · Prospérité 0-4 (départ 1) · Caisse · Entrepôt de Québec.'
fw=lambda px,py:(round(FX+(px-FW/2)/FPX,3),round(FZ-(py-FH/2)/FPX,3))
mk=[q for q in objs if q.get('Nickname')=='Prix en France'][0]
cibles={'Prix en France':fg['pfr'][5],'Politique d’achat':fg['pol'][0],'Prospérité':fg['pro'][1],'Dette':fg['det'][2]}
for nom,(px,py) in cibles.items():
    m=[q for q in objs if q.get('Nickname')==nom]
    if m: m=m[0]
    else: m=copy.deepcopy(mk); m['GUID']=guid('m'+nom); m['Nickname']=nom; objs.append(m)
    X,Z=fw(px,py); nn=json.loads(m['GMNotes']); nn.update(x=X,z=Z); m['GMNotes']=note(nn); m['Transform'].update(posX=X,posZ=Z,posY=2.0)
# 2. Partis
pg=json.load(open(S+'partis_geo_v1.json')); PW,PH=560,960
x0=20.7  # sous l’encart des Antilles (v3.35)
for i,(nom,fich,desc) in enumerate((('Château','parti_chateau_v1.png','Parti du gouverneur : 1 · attribue le premier congé de chaque joueur ; 2 · pour 1 ₶, ajoute un officier à son expédition. Par membre : 1 congé de plus émis. Milice : 2 ₶, +1 défense dans un fort.'),
                                     ('Palais','parti_palais_v1.png','Parti de l’intendant : 1 · attribue le budget de la colonie ; 2 · pour 1 ₶, ajoute un missionnaire à son expédition. Par membre : +1 dé de vérification de la contrebande à Albany. Caisse de la colonie.'))):
    old=[q for q in objs if q.get('Nickname')==nom]
    t=copy.deepcopy(pl); t['GUID']=guid('parti'+nom); t['Nickname']=nom; t['Description']=desc
    t['CustomImage'].update(ImageURL=GH+fich,ImageSecondaryURL=GH+fich)
    X=round(x0+i*(PW/FPX+0.3),3); Z=-12.5
    t['GMNotes']=note({'w':PW/FPX,'d':PH/FPX,'x':X,'z':Z,'h':0.15,'lock':True,'drop':True})
    t['Transform'].update(posX=X,posZ=Z,scaleX=PW/FPX/2,scaleY=1.0,scaleZ=PW/FPX/2); t['Locked']=True
    t.pop('AttachedSnapPoints',None)
    if old: objs[objs.index(old[0])]=t
    else: objs.append(t)
json.dump(d,open(P,'w'),ensure_ascii=False,indent=2)
print('ok',FX,FZ,x0)
