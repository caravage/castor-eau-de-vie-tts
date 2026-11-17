# Polices locales (v3.53) : IM Fell English, IM Fell English SC, Alegreya Sans, depuis plateau_hd/node_modules/@fontsource.
# Remplace les liens Google Fonts : sans réseau, le rendu retombait sur une police de repli (Liberation Serif).
import base64, os
F = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'plateau_hd/node_modules/@fontsource')
def _f(fam, pkg, w, st):     # police incluse en data: (les pages créées par set_content ne peuvent pas charger de file://)
    d = base64.b64encode(open(f'{F}/{pkg}/files/{pkg}-latin-{w}-{st}.woff2', 'rb').read()).decode()
    return f"@font-face{{font-family:'{fam}';font-weight:{w};font-style:{st};src:url(data:font/woff2;base64,{d})}}"
CSS = ''.join([_f('IM Fell English SC', 'im-fell-english-sc', 400, 'normal'),
               _f('IM Fell English', 'im-fell-english', 400, 'normal'), _f('IM Fell English', 'im-fell-english', 400, 'italic')]
              + [_f('Alegreya Sans', 'alegreya-sans', w, s) for w in (400, 500, 700) for s in ('normal', 'italic')])
POL = f"<style>{CSS}</style>"
CHROME = '/usr/bin/google-chrome' if os.path.exists('/usr/bin/google-chrome') else None
