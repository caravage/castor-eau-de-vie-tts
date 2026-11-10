# Prépare carte_src.html (HTML statique) à partir de ../carte_etendue_tts.dc.html :
# runtime retiré, polices locales (fonts.css), images /_blob/<id> → img/<id>.png
import re
s = open('../carte_etendue_tts.dc.html').read()
s = s.replace('<script src="./support.js"></script>', '')
s = re.sub(r'<link rel="stylesheet" href="https://fonts.googleapis[^>]*>', '<link rel="stylesheet" href="fonts.css">', s)
s = re.sub(r'/_blob/([0-9a-f]{32})', r'img/\1.png', s)
s = s.replace('<x-dc>', '<div>').replace('</x-dc>', '</div>').replace('<helmet>', '').replace('</helmet>', '')
s = re.sub(r'<script type="text/x-dc".*?</script>', '', s, flags=re.S)
open('carte_src.html', 'w').write(s)
print('carte_src.html')
