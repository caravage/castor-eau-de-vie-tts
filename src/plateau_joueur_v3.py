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
    im.crop((int(x-w/2),int(y-h/2),int(x+w/2),int(y+h/2))).resize((S,S),Image.LANCZOS).save(R+f'img/v18/pm_{SLUG[k]}.png')
    ns['mesh'](f'v18/sac_pm_{SLUG[k]}',f'v18/pm_{SLUG[k]}',circ,20,(S//2,3))
os.chdir(cwd)

def guid(seed):
    used={q.get('GUID') for q in objs}; g=hashlib.md5(seed.encode()).hexdigest()[:6]
    while g in used: g=hashlib.md5((g+'x').encode()).hexdigest()[:6]
    return g
def local(px,py):   # pixel du plateau -> coordonnées locales de la tuile (rotY 180)
    return round(-((px/IW)*2-1),4), round(-((py/IH)*2-1)*(IH/IW),4)
def world(cx,cz,px,py):
    return round(cx+(px-IW/2)/PX,3), round(cz-(py-IH/2)/PX,3)

tpl=[q for q in objs if q.get('Nickname')=='Moyen canot rouge'][0]
mats={c:[q for q in objs if q.get('Nickname')=='Plateau du joueur '+c][0] for c in COLS}
for i,c in enumerate(COLS):
    m=mats[c]
    for kk in ('ImageURL','ImageSecondaryURL'): m['CustomImage'][kk]=GH+f'pmat_v3_{i}.png?v42'
    n=json.loads(m['GMNotes']); n['cap']=c; m['GMNotes']=json.dumps(n,ensure_ascii=False,separators=(', ',': '))
    # 3. points d'aimantation : 4 cartes (avec rotation) + 7 cases de soupçon
    sp=[]
    for (x,y,w,h) in geo['slots'][:4]:
        lx,lz=local(x,y); sp.append({'Position':{'x':lx,'y':0.05,'z':lz},'Rotation':{'x':0,'y':0,'z':0}})
    for (x,y,w,h) in geo['souf']:
        lx,lz=local(x,y); sp.append({'Position':{'x':lx,'y':0.05,'z':lz}})
    m['AttachedSnapPoints']=sp
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
# 5. compteurs de capital placés dans la case « = » ; plateaux, compteurs et sacs verrouillés
for c in COLS:
    m=mats[c]; cx,cz=m['Transform']['posX'],m['Transform']['posZ']
    X,Z=world(cx,cz,geo['ctr'][0][0],geo['ctr'][0][1])
    q=[o for o in objs if o.get('Nickname')=='Capital circulant '+c][0]
    q['Description']='Capital circulant : charges (10 au plus) + tuiles de fourrure x prix du castor + parts + palier de la piste Livres. Calculé automatiquement ; clic droit > Recalculer le capital.'
    q['Transform'].update(posX=X,posZ=Z)
    q['GMNotes']=json.dumps({'w':1.9,'x':X,'z':Z,'h':0.6,'y3':True,'lock':True},ensure_ascii=False,separators=(', ',': '))
for q in objs:
    if q['Name'] in ('Bag','Custom_Model_Bag','Custom_Model_Infinite_Bag','Infinite_Bag','Counter') or (q.get('Nickname') or '').startswith('Plateau du joueur'):
        q['Locked']=True
        try: n=json.loads(q.get('GMNotes') or '')
        except Exception: n=None
        if isinstance(n,dict) and 'x' in n: n['lock']=True; q['GMNotes']=json.dumps(n,ensure_ascii=False,separators=(', ',': '))
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
  b.createButton({{click_function = "rien", function_owner = Global, label = tostring(q), position = {{0, 0.25, 0.77}},
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
    pcall(function() ct.Counter.setValue(charges + (q["castor"] or 0) * p + np + palier(nl)) end)
  end
end
function majCapital() pcall(capital) end
function boutonCapital() majCapital() end
local function majSac(c) Wait.frames(function() if c and not c.isDestroyed() then local n = sac(c) if n then afficheSac(c, n) end end end, 1) end
local ancienSortie = onObjectLeaveContainer
function onObjectLeaveContainer(c, o) if ancienSortie then ancienSortie(c, o) end majSac(c) end
function onObjectEnterContainer(c, o) majSac(c) end
local function menus()
  for _, o in ipairs(getObjects()) do
    if o.getName():find("^Capital circulant ") then pcall(function() o.addContextMenuItem("Recalculer le capital", function() majCapital() end) end) end
  end
end
Wait.time(function() menus(); majCapital() end, 4)
'''
d['LuaScript']=d['LuaScript'].rstrip('\n')+LUA
d['XmlUI']='<Button id="capital" onClick="boutonCapital" rectAlignment="UpperRight" offsetXY="-20 -70" width="200" height="40" fontSize="18" color="#2A2418" textColor="#F4EBD6">Calculer le capital</Button>'
json.dump(d,open(P,'w'),ensure_ascii=False,indent=2)
print('ok',len(objs),'LIV0',round(L+1096.9/k,3),'PRIX4',round(L+4019.6/k,3),'PAS',round(108.6/k,4))
