# Marqueur « Raid » (400 × 400, même gabarit que zone_fermee.png) : drapeau haudenosaunee (ceinture d'Hiawatha),
# fond pourpre, quatre carrés reliés et l'arbre de la paix au centre, en blanc.
import subprocess
B = '#F4F1EA'
carres = ''.join(f"<rect x='{x}' y='178' width='44' height='44' fill='none' stroke='{B}' stroke-width='13'/>" for x in (30, 100, 256, 326))
SVG = f"""<svg xmlns='http://www.w3.org/2000/svg' width='400' height='400' viewBox='0 0 400 400'>
<rect x='10' y='10' width='380' height='380' rx='58' fill='#4E2A7A' stroke='#2A2418' stroke-width='14'/>
<g fill='{B}'>
 <rect x='78' y='193' width='18' height='14'/><rect x='148' y='193' width='16' height='14'/><rect x='236' y='193' width='16' height='14'/><rect x='304' y='193' width='18' height='14'/>
 <path d='M200 120 L226 162 L215 162 L236 200 L222 200 L242 240 L158 240 L178 200 L164 200 L185 162 L174 162 Z'/>
 <rect x='193' y='238' width='14' height='34'/>
</g>{carres}</svg>"""
open('/tmp/raid.svg', 'w').write(SVG)
subprocess.run(['google-chrome', '--headless=new', '--disable-gpu', '--hide-scrollbars', '--default-background-color=00000000', '--window-size=400,400',
                '--screenshot=img/v18/raid.png', 'file:///tmp/raid.svg'], capture_output=True)
