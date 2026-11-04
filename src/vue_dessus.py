import json, os, sys
from PIL import Image, ImageDraw, ImageFont
R='/tmp/claude-0/-home-claude/3c5a2878-065c-5165-9c41-6d23b49bdcf8/scratchpad/repo/'
d=json.load(open(R+'Castor_et_eau-de-vie.json'))
S=28; X0,X1,Z0,Z1=-36,44,-41,47
Wp,Hp=int((X1-X0)*S),int((Z1-Z0)*S)
C=Image.new('RGB',(Wp,Hp),(40,40,40)); dr=ImageDraw.Draw(C)
try: F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',13)
except: F=None
P=lambda X,Z:((X-X0)*S,(Z1-Z)*S)
def img_of(o):
    u=(o.get('CustomImage') or {}).get('ImageURL','')
    if not u: return None
    p=R+'img/v18/'+u.split('/')[-1].split('?')[0]
    return Image.open(p).convert('RGBA') if os.path.exists(p) else None
order=sorted(d['ObjectStates'],key=lambda o:(o.get('Nickname')!='Tapis de jeu', o.get('Nickname')!='Table du castor', o['Name'] not in ('Custom_Tile',)))
for o in order:
    t=o['Transform']; X,Z=t['posX'],t['posZ']; n=o.get('Nickname',''); nm=o['Name']
    im=img_of(o)
    if nm=='Custom_Tile' and im is not None:
        w=2*t['scaleX']; h=2*t['scaleZ']*im.height/im.width
        tp=o['CustomImage'].get('CustomTile',{}).get('Type',0)
        im2=im.resize((max(1,int(w*S)),max(1,int(h*S))),Image.LANCZOS)
        if tp==1:
            m=Image.new('L',im2.size,0); a,b=im2.size; ImageDraw.Draw(m).polygon([(a/2,0),(a,b/4),(a,3*b/4),(a/2,b),(0,3*b/4),(0,b/4)],fill=255); im2.putalpha(m)
        px,py=P(X,Z); C.paste(im2,(int(px-im2.width/2),int(py-im2.height/2)),im2)
    elif nm=='Custom_Token' and im is not None:
        im2=im.resize((22,22)) ; px,py=P(X,Z); C.paste(im2,(int(px-11),int(py-11)),im2)
    elif nm in ('HandTrigger',): continue
    else:
        px,py=P(X,Z)
        col={'Deck':(200,180,140),'Bag':(120,90,160),'Infinite_Bag':(90,120,170),'Custom_Model_Bag':(140,110,80),'Custom_Model_Infinite_Bag':(80,140,120),'Die_6':(230,230,230),'Die_6_Rounded':(30,30,30),'Counter':(200,200,60),'PlayerPawn':(220,80,80),'Custom_Model':(170,170,170)}.get(nm,(255,0,255))
        r=10 if 'Bag' in nm else 8
        if nm=='Deck': dr.rectangle([px-26,py-36,px+26,py+36],fill=col,outline='black')
        else: dr.ellipse([px-r,py-r,px+r,py+r],fill=col,outline='black')
        if nm in ('Deck','Bag','Infinite_Bag') or (nm.startswith('Custom_Model') and 'canot' not in n.lower()):
            dr.text((px-30,py+12),n[:18],fill='white',font=F)
C.save(sys.argv[1]); C.resize((Wp//2,Hp//2),Image.LANCZOS).save(sys.argv[1].replace('.png','_small.png'))
dr=ImageDraw.Draw(C)
for o in d['ObjectStates']:
    for sp in o.get('AttachedSnapPoints',[]) or []:
        t=o['Transform']; X=t['posX']-sp['Position']['x']*t['scaleX']; Z=t['posZ']-sp['Position']['z']*t['scaleZ']
        px,py=P(X,Z); dr.ellipse([px-5,py-5,px+5,py+5],outline=(220,0,0),width=2)
C.save(sys.argv[1]); C.resize((Wp//2,Hp//2),Image.LANCZOS).save(sys.argv[1].replace('.png','_small.png'))
