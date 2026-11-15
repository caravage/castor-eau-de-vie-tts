# Marqueur « Zone détruite » (400 × 400, même gabarit que zone_fermee.png) : tête de mort ivoire sur fond noir.
import subprocess
SVG = """<svg xmlns='http://www.w3.org/2000/svg' width='400' height='400' viewBox='0 0 400 400'>
<rect x='10' y='10' width='380' height='380' rx='58' fill='#1D1B17' stroke='#2A2418' stroke-width='14'/>
<g fill='#F1E7C9'>
 <path d='M200 70 C128 70 88 118 88 178 C88 214 104 238 124 252 L124 290 C124 300 132 306 142 306 L258 306 C268 306 276 300 276 290 L276 252 C296 238 312 214 312 178 C312 118 272 70 200 70 Z'/>
 <rect x='150' y='300' width='100' height='34' rx='8'/>
</g>
<g fill='#1D1B17'>
 <ellipse cx='156' cy='186' rx='31' ry='35'/><ellipse cx='244' cy='186' rx='31' ry='35'/>
 <path d='M200 222 L184 258 L216 258 Z'/>
 <rect x='166' y='300' width='9' height='34'/><rect x='195' y='300' width='9' height='34'/><rect x='224' y='300' width='9' height='34'/>
</g></svg>"""
open('/tmp/detruite.svg', 'w').write(SVG)
subprocess.run(['google-chrome', '--headless=new', '--disable-gpu', '--hide-scrollbars', '--default-background-color=00000000', '--window-size=400,400',
                '--screenshot=img/v18/zone_detruite.png', 'file:///tmp/detruite.svg'], capture_output=True)
