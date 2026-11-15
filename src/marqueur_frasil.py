# Marqueur « Frasil » (400 × 400) : rayures du calendrier (mois de frasil), flocon et mot « Frasil ». Posé sur un mois par Grand Hiver.
import subprocess, os
F = os.path.abspath('src/plateau_hd/node_modules/@fontsource/im-fell-english-sc/files/im-fell-english-sc-latin-400-normal.woff2')
br = ''.join(f"<line x1='200' y1='170' x2='{200+92*__import__('math').cos(a)}' y2='{170+92*__import__('math').sin(a)}' stroke='#2A3A55' stroke-width='14' stroke-linecap='round'/>"
             for a in [k * 1.0471976 for k in range(6)])
import math
pts = ''
for k in range(6):
    a = k * math.pi / 3; mx, my = 200 + 58 * math.cos(a), 170 + 58 * math.sin(a)
    for s in (-1, 1):
        b = a + s * 0.75; pts += f"<line x1='{mx}' y1='{my}' x2='{mx + 30 * math.cos(b)}' y2='{my + 30 * math.sin(b)}' stroke='#2A3A55' stroke-width='10' stroke-linecap='round'/>"
SVG = f"""<svg xmlns='http://www.w3.org/2000/svg' width='400' height='400' viewBox='0 0 400 400'>
<style>@font-face{{font-family:SC;src:url(file://{F})}}</style>
<defs><pattern id='h' width='34' height='34' patternUnits='userSpaceOnUse' patternTransform='rotate(45)'><rect width='34' height='34' fill='#D3E2EA'/>
<rect x='0' width='8' height='34' fill='#96A5BC'/><rect x='17' width='6' height='34' fill='#FFFFFF'/></pattern></defs>
<rect x='10' y='10' width='380' height='380' rx='58' fill='url(#h)' stroke='#2A2418' stroke-width='14'/>
<circle cx='200' cy='170' r='112' fill='#EEF4F7' opacity='.85'/>{br}{pts}
<rect x='70' y='300' width='260' height='66' rx='14' fill='#EEF4F7' stroke='#2A2418' stroke-width='4'/>
<text x='200' y='348' text-anchor='middle' font-family='SC' font-size='50' fill='#2A2418'>Frasil</text></svg>"""
open('/tmp/frasil.svg', 'w').write(SVG)
subprocess.run(['google-chrome', '--headless=new', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files', '--default-background-color=00000000',
                '--window-size=400,400', '--screenshot=img/v18/frasil.png', 'file:///tmp/frasil.svg'], capture_output=True)
