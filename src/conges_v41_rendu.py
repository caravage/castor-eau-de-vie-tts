import json
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':400,'height':400})
    pg.goto('file:///tmp/claude-0/-home-claude/3c5a2878-065c-5165-9c41-6d23b49bdcf8/scratchpad/conges41/conges41.html')
    pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(2500)
    pg.evaluate("""()=>{for(const t of document.querySelectorAll('text.fit')){const w=t.getBBox().width; const x=+t.getAttribute('x'); const a=t.getAttribute('text-anchor');
      const lim = a==='start' ? 100-x : 94; if(w>lim){t.setAttribute('font-size', (+t.getAttribute('font-size'))*lim/w);}}
      for(const t of document.querySelectorAll('text.fitp')){const w=t.getBBox().width; if(w>66){t.setAttribute('font-size',(+t.getAttribute('font-size'))*66/w);}}}""")
    ids=pg.evaluate("[...document.querySelectorAll('div[id]')].map(d=>d.id)")
    for i in ids: pg.locator('#'+i).screenshot(path=i+'.png',omit_background=True)
    b.close()
print(len(ids))
