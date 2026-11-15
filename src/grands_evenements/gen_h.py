# Essai format horizontal (700×500) : A = bandeau d'image en haut, B = image à gauche
exec(open(__file__.replace('gen_h.py','gen_h_base.py')).read())
CSSH = """
.planche.h{left:34px;right:34px;top:60px;height:236px}
.planche.g{left:34px;top:34px;width:290px;height:432px;right:auto}
"""
def bandeauH(left=0, width=700):
    return (f"<div class='bandeau' style='left:{left}px;width:{width}px;right:auto'><svg width='{width-68}' height='18' viewBox='0 0 {width-68} 18' style='position:absolute;left:34px;top:0'>"
            f"<path d='M0 9 L{(width-68)/2-102} 9 M{(width-68)/2+102} 9 L{width-68} 9' stroke='{OR}' stroke-width='1'/></svg><span>Grand événement</span></div>")

def cadre():
    return ("<div class='carte'><div class='papier'>" + GRAIN + "<div class='filet'></div><div class='filet2'></div></div>"
            + coin(17, 17, 0) + coin(649, 17, 90) + coin(649, 449, 180) + coin(17, 449, 270))

def img(c, cls):
    return (f"<div class='planche {cls}'><div class='img' style=\"background-image:url('file://{HERE}/sources/{c['img']}');background-size:cover;"
            f"background-position:{c['pos']};transform:scale({c['zoom']});transform-origin:{c['pos']}\"></div><div class='vign'></div></div>")

def ornH(top, cx, w):
    return (f"<svg style='position:absolute;left:{cx-w}px;top:{top}px' width='{2*w}' height='18' viewBox='0 0 {2*w} 18'>"
            f"<path d='M0 9 L{w-22} 9 M{w+22} 9 L{2*w} 9' stroke='{OR}' stroke-width='1'/><circle cx='0' cy='9' r='1.8' fill='{OR}'/><circle cx='{2*w}' cy='9' r='1.8' fill='{OR}'/>"
            f"<path d='M{w} 2 L{w+7} 9 L{w} 16 L{w-7} 9 Z' fill='{BORDEAUX}'/><path d='M{w-12} 9 L{w-17} 5 L{w-22} 9 L{w-17} 13 Z M{w+12} 9 L{w+17} 5 L{w+22} 9 L{w+17} 13 Z' fill='{OR}'/></svg>")

def carteA(c, fs_eff):
    b = cadre() + bandeauH() + img(c, 'h')
    b += f"<div class='titre' style='top:314px;font-size:34px'>{E(c['titre'])}</div>" + ornH(354, 350, 190)
    b += f"<div class='effet' style='left:60px;right:60px;top:378px;font-size:{fs_eff}px'>{E(c['effet'])}</div>"
    return b + "</div>"

def carteB(c, fs_eff):
    b = cadre() + img(c, 'g') + bandeauH(330, 370)
    b += f"<div class='titre' style='left:344px;right:30px;top:150px;font-size:34px'>{E(c['titre'])}</div>" + ornH(196, 515, 130)
    b += f"<div class='effet' style='left:352px;right:40px;top:226px;font-size:{fs_eff}px'>{E(c['effet'])}</div>"
    return b + "</div>"

C = {c['id']: c for c in CARTES}
essais = [('A_incendie', carteA, dict(C['incendie'], pos='50% 40%', zoom=1.0), 18.5),
          ('A_guerre', carteA, dict(C['guerre'], pos='45% 38%', zoom=1.15), 21),
          ('A_lachine', carteA, dict(C['lachine'], pos='54% 20%', zoom=1.3), 21),
          ('B_lachine', carteB, dict(C['lachine'], pos='50% 28%', zoom=1.38), 21)]
for nom, f, c, fs in essais:
    p = f"{HERE}/html/h_{nom}.html"
    open(p, 'w').write(f"<!doctype html><html><head><meta charset='utf-8'><link rel='stylesheet' href='file://{FONTS}'><style>{CSS}{CSSH}</style></head><body>{f(c, fs)}</body></html>")
    subprocess.run(['google-chrome', '--headless=new', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files', '--force-device-scale-factor=2',
                    '--default-background-color=00000000', '--virtual-time-budget=4000', f"--screenshot={HERE}/png/h_{nom}.png", '--window-size=700,500', f'file://{p}'],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
print('ok')
