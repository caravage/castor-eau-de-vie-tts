import math, re, os, json
src=open('repo/src/meshes.py').read()
def block(name):
    i=src.index(f'def {name}('); lines=src[i:].split('\n'); out=[lines[0]]
    for l in lines[1:]:
        if l and not l[0].isspace(): break
        out.append(l)
    return '\n'.join(out)
ns={}
exec('import math, json, os\nimport numpy as np, mapbox_earcut as earcut\nfrom PIL import Image\n'+block('mesh')+'\n'+block('rrect'),ns)
os.chdir('repo')
hexp=[(128+128*math.cos(math.radians(a)),128+128*math.sin(math.radians(a))) for a in range(-90,270,60)]
circ=[(110+104*math.cos(2*math.pi*i/48),110+104*math.sin(2*math.pi*i/48)) for i in range(48)]
out={}
out['sac_fort_fr']=ns['mesh']('v18/sac_fort_fr','v18/fort_hex',hexp,26,(128,6))
out['sac_fort_uk']=ns['mesh']('v18/sac_fort_uk','v18/fort_uk_hex',hexp,26,(20,128))
out['sac_mission']=ns['mesh']('v18/sac_mission','v18/mission_hex',hexp,26,(128,6))
out['sac_abime']=ns['mesh']('v18/sac_abime','v18/abime',circ,22,(110,10))
out['sac_ravage']=ns['mesh']('v18/sac_ravage','v18/ravage',ns['rrect'](0,0,220,220,28),22,(110,4))
out['sac_zone_fermee']=ns['mesh']('v18/sac_zone_fermee','v18/zone_fermee',ns['rrect'](4,4,396,396,46),40,(200,8))
print(out)
json.dump(out,open('/tmp/claude-0/-home-claude/3c5a2878-065c-5165-9c41-6d23b49bdcf8/scratchpad/new_meshes.json','w'))
