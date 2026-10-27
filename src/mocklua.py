import json,sys
from lupa import LuaRuntime
from PIL import Image, ImageChops, ImageDraw
save=json.load(open('Castor_et_eau-de-vie.json'))
L=LuaRuntime(unpack_returned_tuples=True); G=L.globals()
L.execute('''
JSON={decode=function(s) return pyjson(s) end, encode=function(t) return "{}" end}
Tables={getTableObject=function() return {getBounds=function() return {size={x=86,y=2,z=58},center={x=0,y=0,z=0}} end} end}
Wait={time=function(f,t) f() end, condition=function(f,c,t,tf) f() end, frames=function(f) f() end}
function broadcastToAll() end
function mk(notes,bx,bz)
  local o={pos=nil,sc={x=1,y=1,z=1},lock=true}
  o.getGMNotes=function() return notes end
  o.setLock=function(v) o.lock=v end
  o.setRotation=function(r) end
  o.getBoundsNormalized=function() return {size={x=bx*o.sc.x,y=0.2,z=bz*o.sc.z}} end
  o.getScale=function() return o.sc end
  o.setScale=function(s) o.sc={x=s[1],y=s[2],z=s[3]} end
  o.setPosition=function(p) o.pos=p end
  o.isDestroyed=function() return false end
  o.loading_custom=false o.spawning=false
  return o
end''')
def dec(s):
    v=json.loads(s) if s else None
    return L.table_from(v) if isinstance(v,dict) else v
G.pyjson=dec
objs=[]
for o in save['ObjectStates']:
    if o['Name']=='HandTrigger': continue
    if o['Name'].startswith('Custom_Model'):
        nn=json.loads(o['GMNotes']); r=nn.get('d',nn['w'])/nn['w']; objs.append((o,G.mk(o['GMNotes'],1,r),(1,r))); continue
    base={'Custom_Tile':(2,2),'Custom_Token':(9,9),'Card':(2.2,3.0),'Deck':(2.2,3.0)}.get(o['Name'],(1.5,1.5))
    objs.append((o,G.mk(o.get('GMNotes',''),*base),base))
G.getObjects=lambda: L.table_from([x[1] for x in objs]); G.Hands=L.eval('{getHands=function() return {} end}')
L.execute(save['LuaScript']); G.onLoad('')
im0=Image.open('img/table_full.png'); W=im0.width//2; H=im0.height//2
board=objs[0]; bw=board[2][0]*board[1].sc.x; bd=board[2][1]*board[1].sc.z
print('plateau %.1f x %.1f sur table 86 x 58, rapport %.3f / %.3f'%(bw,bd,bw/bd,W/H))
px=W/bw
out=Image.new('RGB',(W,H),'#3B3026'); bg=im0.convert('RGBA').resize((W,H)); out.paste(bg,(0,0),bg)
for o,lo,base in objs[1:]:
    if not lo.pos: continue
    w=base[0]*lo.sc.x; d=base[1]*lo.sc.z; cx=lo.pos[1]*px+W/2; cy=-lo.pos[3]*px+H/2
    ci=o.get('CustomImage')
    name=list(o['CustomDeck'].values())[0]['BackURL'] if o['Name']=='Deck' else (ci['ImageURL'] if ci else (o['CustomMesh']['DiffuseURL'] or None if 'CustomMesh' in o else None))
    if name:
        im=Image.open('img/'+name.split('/')[-1]).convert('RGBA')
        if '/cn_' in name: im=im.crop((0,0,im.width,im.height//2))
        if o['Name']=='Deck' and o['Transform']['rotZ']==0:  # faceup : carte du dessus
            cdk=list(o['CustomDeck'].values())[0]; cid=o['ContainedObjects'][0]['CardID']%100; sh=Image.open('img/'+cdk['FaceURL'].split('/')[-1]).convert('RGBA')
            cw,ch=sh.width//cdk['NumWidth'],sh.height//cdk['NumHeight']; im=sh.crop(((cid%cdk['NumWidth'])*cw,(cid//cdk['NumWidth'])*ch,(cid%cdk['NumWidth']+1)*cw,(cid//cdk['NumWidth']+1)*ch))
        im=im.resize((max(1,int(w*px)),max(1,int(d*px))))
        c=o['ColorDiffuse']
        if min(c.values())<1:
            t=Image.new('RGBA',im.size,(int(c['r']*255),int(c['g']*255),int(c['b']*255),255)); im=Image.composite(ImageChops.multiply(im,t),im,im.split()[3])
        out.paste(im,(int(cx-w*px/2),int(cy-d*px/2)),im)
    else: ImageDraw.Draw(out).rectangle([cx-w*px/2,cy-d*px/2,cx+w*px/2,cy+d*px/2],outline='white',width=2)
out.save('mock_lua.png')
