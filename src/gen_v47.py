# v3.47 : marqueur Ravagé = wigwam incendié ; compteur Force iroquoise (drapeau haudenosaunee, valeur et boutons − / + en Lua) et jetons Alliance recto / verso (Tortue, Lynx).
import os
from playwright.sync_api import sync_playwright
B = '#F4F1EA'
carres = ''.join(f"<rect x='{x}' y='178' width='44' height='44' fill='none' stroke='{B}' stroke-width='13'/>" for x in (30, 100, 256, 326))
drap = f"""<g fill='{B}'><rect x='78' y='193' width='18' height='14'/><rect x='148' y='193' width='16' height='14'/><rect x='236' y='193' width='16' height='14'/><rect x='304' y='193' width='18' height='14'/>
<path d='M200 120 L226 162 L215 162 L236 200 L222 200 L242 240 L158 240 L178 200 L164 200 L185 162 L174 162 Z'/><rect x='193' y='238' width='14' height='34'/></g>{carres}"""
FORCE = f"""<svg xmlns='http://www.w3.org/2000/svg' width='400' height='400' viewBox='0 0 400 400'><rect width='400' height='400' fill='#4E2A7A'/>
<g transform='translate(200 118) scale(0.82) translate(-200 -196)'>{drap}</g>
<line x1='40' y1='250' x2='360' y2='250' stroke='{B}' stroke-width='3' opacity='.5'/></svg>"""
RAVAGE = """<svg xmlns='http://www.w3.org/2000/svg' width='400' height='400' viewBox='0 0 400 400'><rect width='400' height='400' fill='#7A1F18'/>
<g fill='none' stroke='#CFC6B8' stroke-width='13' stroke-linecap='round' opacity='.8'>
<path d='M170 118 C150 92 190 78 172 52 C160 36 182 24 178 12'/><path d='M222 112 C208 88 240 76 228 50'/></g>
<ellipse cx='200' cy='328' rx='160' ry='14' fill='#4A120D'/>
<g stroke='#3A2414' stroke-width='9' stroke-linecap='round'><line x1='150' y1='170' x2='262' y2='112'/><line x1='250' y1='170' x2='140' y2='112'/></g>
<path d='M70 325 Q72 180 200 165 Q328 180 330 325 Z' fill='#C99A55'/>
<g fill='#B0823F'><path d='M74 300 L326 300 L328 325 L72 325 Z'/><path d='M84 238 L316 238 L320 262 L80 262 Z'/><path d='M112 192 L288 192 L300 212 L100 212 Z'/></g>
<path d='M120 196 Q150 170 200 168 Q244 170 266 192 Q258 214 236 218 Q200 226 160 222 Q130 218 120 196 Z' fill='#24120D'/>
<g fill='#E9A23B'><path d='M132 212 Q128 170 152 150 Q150 176 166 180 Q160 140 188 118 Q186 158 204 166 Q206 134 226 124 Q220 160 240 170 Q246 152 256 148 Q262 186 248 212 Q190 224 132 212 Z'/></g>
<g fill='#F6D277'><path d='M160 212 Q158 186 174 172 Q176 190 188 192 Q186 166 204 152 Q206 184 222 190 Q228 178 236 176 Q238 200 226 214 Z'/></g>
<path d='M180 325 L180 280 Q200 258 220 280 L220 325 Z' fill='#24120D'/>
</svg>"""
FONT = "@font-face{font-family:F;font-style:italic;src:url(node_modules/@fontsource/im-fell-english/files/im-fell-english-latin-400-italic.woff2)}"
def jeton(sym, fond, mot, enc):
    # symbole seul (sans le disque du médaillon), teinté ; enc = couleur du symbole et du mot
    return f"""<html><head><style>{FONT}body{{margin:0}}div.t{{width:400px;height:400px;background:{fond};position:relative;font-family:F}}
img{{position:absolute;left:52px;top:18px;width:296px;height:296px}}p{{position:absolute;margin:0;left:0;right:0;top:300px;text-align:center;font-style:italic;font-size:58px;color:{enc}}}</style></head>
<body><div class='t'><img src='{sym}'><p>{mot}</p></div></body></html>"""
pages = {'force_iroquoise_v47.png': FORCE,
         'alliance_tortue_alliee.png': jeton('sym_tortue_clair.png', '#597733', 'Alliée', '#F1E4C4'),
         'alliance_tortue_neutre.png': jeton('sym_tortue_fonce.png', '#CFDDB4', 'Neutre', '#4A6429'),
         'alliance_lynx_alliee.png': jeton('sym_mishipeshu_clair.png', '#2B426E', 'Alliée', '#F1E4C4'),
         'alliance_lynx_neutre.png': jeton('sym_mishipeshu_fonce.png', '#C3D3E8', 'Neutre', '#2B426E'),
         'ravage_v47.png': RAVAGE}
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 400, 'height': 400})
    for nom, html in pages.items():
        f = os.path.abspath('_' + nom + ('.svg' if html.startswith('<svg') else '.html')); open(f, 'w').write(html)
        pg.goto('file://' + f); pg.wait_for_timeout(300); pg.screenshot(path=nom, clip={'x': 0, 'y': 0, 'width': 400, 'height': 400})
    b.close()
