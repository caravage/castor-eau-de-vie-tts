# Deux dés : dé des zones (2 faces bleu Lac Supérieur, 2 vert Lacs d'en haut, 2 rouge Lacs d'en bas) et dé sec / gras (4 faces sec, 2 faces gras).
# Faces égales sur faces opposées du cube : la valeur lue ne dépend pas du sens des axes à l'import.
import sys
from PIL import Image, ImageDraw, ImageFont
R=sys.argv[1]   # racine du dépôt
S=256; FONT=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif-BoldItalic.ttf',44)
ZC={'bleu':(47,67,115),'vert':(88,128,60),'rouge':(150,58,38)}
def face(col,gras=None):
    t=Image.new('RGB',(S,S),col); d=ImageDraw.Draw(t)
    d.rectangle((0,0,S-1,S-1),outline=tuple(int(v*.55) for v in col),width=10)
    if gras is None: return t
    cx,cy=S/2,S/2-22; rx,ry=48,64; ink=(42,24,10)
    d.line((cx,cy-ry-18,cx,cy+ry+18),fill=ink,width=8); d.line((cx-rx-20,cy,cx+rx+20,cy),fill=ink,width=8)
    d.ellipse((cx-rx,cy-ry,cx+rx,cy+ry),fill=(92,58,26) if gras else (139,90,43),outline=ink,width=7)
    d.ellipse((cx-rx+14,cy-ry+16,cx+rx-14,cy+ry-16),outline=(240,224,190),width=3)
    d.text((cx,S-34),'Gras' if gras else 'Sec',font=FONT,fill=(42,24,10),anchor='mm')
    return t
def atlas(faces,nom):   # ordre : +Y, -Y, +Z, -Z, +X, -X (repère OBJ)
    A=Image.new('RGB',(3*S,2*S))
    for i,f in enumerate(faces): A.paste(f,((i%3)*S,(i//3)*S))
    A.save(R+f'img/v18/{nom}.png')
atlas([face(ZC[c]) for c in ('bleu','bleu','vert','vert','rouge','rouge')],'de_zones')
PARCH=(234,218,182)
atlas([face(PARCH,g) for g in (1,1,0,0,0,0)],'de_castor')
# faces du cube (repère OBJ) : normale N, droite Rt, haut U avec Rt x U = N (même chiralité que les jetons, lisibles dans TTS)
def cross(a,b): return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
FACES=[(N,Rt,cross(N,Rt)) for N,Rt in (((0,1,0),(1,0,0)),((0,-1,0),(1,0,0)),((0,0,1),(1,0,0)),((0,0,-1),(-1,0,0)),((1,0,0),(0,0,-1)),((-1,0,0),(0,0,1)))]
V=[];VT=[];VN=[];FF=[]
for i,(N,Rt,U) in enumerate(FACES):
    assert cross(Rt,U)==N
    u0,v0=(i%3)/3,1-(i//3+1)/2; du,dv=1/3,1/2; e=0.004
    VN.append(N); n=len(VN); idx=[]
    for (a,b) in ((-1,-1),(1,-1),(1,1),(-1,1)):   # (droite, haut)
        p=tuple(0.5*N[k]+0.5*a*Rt[k]+0.5*b*U[k] for k in range(3)); V.append(p)
        VT.append((u0+e+(a+1)/2*(du-2*e),v0+e+(b+1)/2*(dv-2*e))); idx.append(len(V))
    q=idx; FF+= [(q[0],q[1],q[2],n),(q[0],q[2],q[3],n),(q[2],q[1],q[0],n),(q[3],q[2],q[0],n)]
with open(R+'img/v18/de_zones.obj','w') as f:
    f.write(''.join(f'v {x} {y} {z}\n' for x,y,z in V)+''.join(f'vt {u:.5f} {w:.5f}\n' for u,w in VT)+''.join(f'vn {x} {y} {z}\n' for x,y,z in VN))
    f.write(''.join(f'f {a}/{a}/{n} {b}/{b}/{n} {c}/{c}/{n}\n' for a,b,c,n in FF))
print('ok')
