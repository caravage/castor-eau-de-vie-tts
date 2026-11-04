# Canots v2 (4 nov. 2026 : fond intérieur à la couleur du canot, lettre blanche) : coque low-poly (fond plat, flancs plats au milieu = pose stable à plat ET sur le flanc),
# proue et poupe identiques que la poupe + chevrons vers l'avant (sens de marche), lettre sur le fond intérieur et sur les deux flancs.
# Axes OBJ : x = longueur (proue vers +x), y = haut, z = largeur. Longueur totale = 1 (comme canot3d).
import math, os
from PIL import Image, ImageDraw, ImageFont
OUT = os.environ.get('OUT', 'img/v18')
FONT = '/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf'
PC = {'rouge': '#A8322A', 'bleu': '#2F5E8E', 'vert': '#4E7A2C'}
SIZES = {'grand': (692, 150, 96), 'petit': (452, 116, 76), 'coureur': (332, 92, 62)}   # L, B, H : trois tailles nettement différentes (longueurs de canot3d)
S = [-1, -.93, -.8, -.6, -.35, 0, .35, .6, .8, .93, 1]; A_MID = .35; S_IN = .8

def shade(h, f):
    h = h.lstrip('#'); c = [int(h[i:i + 2], 16) for i in (0, 2, 4)]
    return tuple(min(255, max(0, round(v * f if f < 1 else v + (255 - v) * (f - 1)))) for v in c)
INNER = (236, 222, 190)
CREAM, WOOD, WOOD_D, RIM, PITCH = (238, 226, 196), (214, 178, 120), (168, 128, 78), (92, 60, 34), (40, 30, 24)

def geo(L, B, H):
    Lb = .84 * L
    un = lambda s: max(0., (abs(s) - A_MID) / (1 - A_MID))
    w = lambda s: B / 2 * max(0., 1 - un(s) ** 1.6) ** .8
    g = lambda s: H * (1 + (.62 if s > 0 else .62) * un(s) ** 2.5)          # proue et poupe identiques
    yc = lambda s: .30 * H * un(s) ** 3                                       # relevé du fond aux extrémités
    P = {}
    for s in S:
        for sd in (1, -1):
            P['g', s, sd] = (s * L / 2, g(s), sd * w(s))
            P['c', s, sd] = (s * Lb / 2, yc(s), sd * .72 * w(s))
            if abs(s) <= S_IN:
                t = .07 * B
                P['i', s, sd] = (s * L / 2 * .985, g(s) - .03 * H, sd * (w(s) - t))
                P['f', s, sd] = (s * Lb / 2 * .97, .26 * H + yc(s), sd * .72 * w(s) * .78)
    return P, Lb

sub = lambda a, b: tuple(x - y for x, y in zip(a, b))
cross = lambda a, b: (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])

def build(key):
    L, B, H = SIZES[key]; P, Lb = geo(L, B, H); Hm = 1.7 * H
    W = 1024; m = 8; k = (W - 2 * m) / L
    fR, fL = m, m + Hm * k + m; tp = fL + Hm * k + m; bt = tp + B * k + m; TH = math.ceil((bt + B * k + m) / 4) * 4
    def px(region, p):   # point monde -> pixel de la texture
        x, y, z = p
        if region == 'R': return (m + (x + L / 2) * k, fR + (Hm - y) * k)
        if region == 'L': return (m + (L / 2 - x) * k, fL + (Hm - y) * k)
        if region == 'T': return (m + (x + L / 2) * k, tp + (z + B / 2) * k)
        return (m + (x + L / 2) * k, bt + (B / 2 - z) * k)                    # dessous vu d'en bas
    V, VT, F = [], [], []
    vid = {}
    def vert(p):
        if p not in vid: V.append(p); vid[p] = len(V)
        return vid[p]
    def uv(region, p):
        a, b = px(region, p); VT.append((a / W, 1 - b / TH)); return len(VT)
    def tri(a, b, c, region):   # a,b,c dans le sens trigo vu de l'extérieur
        if a == b or b == c or a == c: return
        n = cross(sub(b, a), sub(c, a)); m3 = tuple((a[i] + b[i] + c[i]) / 3 for i in range(3))
        ref = sub((0, 2 * H, 0), m3) if region == 'T' else sub(m3, (0, .5 * H, 0))   # normale : vers la cavité (dessus) / vers l'extérieur (coque)
        if sum(x * y for x, y in zip(n, ref)) < 0: b, c = c, b
        F.append([(vert(p), uv(region, p)) for p in (a, b, c)])
    def quad(a, b, c, d, region): tri(a, b, c, region); tri(a, c, d, region)
    G = lambda s, sd: P['g', s, sd]; C = lambda s, sd: P['c', s, sd]
    for s0, s1 in zip(S, S[1:]):
        quad(G(s0, 1), C(s0, 1), C(s1, 1), G(s1, 1), 'R')                      # flanc +z
        quad(G(s1, -1), C(s1, -1), C(s0, -1), G(s0, -1), 'L')                  # flanc -z
        quad(C(s0, 1), C(s0, -1), C(s1, -1), C(s1, 1), 'B')                    # fond
    SI = [s for s in S if abs(s) <= S_IN]
    I = lambda s, sd: P['i', s, sd]; Fl = lambda s, sd: P['f', s, sd]
    for s0, s1 in zip(SI, SI[1:]):
        for sd in (1, -1):
            a, b, c, d = G(s0, sd), G(s1, sd), I(s1, sd), I(s0, sd)
            quad(a, b, c, d, 'T') if sd < 0 else quad(d, c, b, a, 'T')         # plat-bord
            a, b, c, d = I(s0, sd), I(s1, sd), Fl(s1, sd), Fl(s0, sd)
            quad(a, b, c, d, 'T') if sd < 0 else quad(d, c, b, a, 'T')         # paroi intérieure
        quad(Fl(s0, -1), Fl(s1, -1), Fl(s1, 1), Fl(s0, 1), 'T')                # fond intérieur
    for e in (1, -1):                                                          # pontets d'extrémité + cloison
        se = S_IN * e; outs = [s for s in S if abs(s) >= S_IN and s * e > 0]; outs.sort(key=abs)
        quad(I(se, 1), I(se, -1), Fl(se, -1), Fl(se, 1), 'T') if e > 0 else quad(I(se, -1), I(se, 1), Fl(se, 1), Fl(se, -1), 'T')
        ring = [I(se, -1)] + [G(s, -1) for s in outs] + [G(s, 1) for s in reversed(outs[:-1])] + [I(se, 1)]
        ring = [p for i, p in enumerate(ring) if i == 0 or p != ring[i - 1]]
        cx = sum(p[0] for p in ring) / len(ring); cy = max(p[1] for p in ring) * .97 if False else sum(p[1] for p in ring) / len(ring)
        ctr = (cx, cy, 0.)
        for a, b in zip(ring, ring[1:] + ring[:1]):
            tri(ctr, b, a, 'T') if e > 0 else tri(ctr, a, b, 'T')
    norm = 1 / L
    with open(f'{OUT}/canot4_{key}.obj', 'w') as f:
        f.write(''.join(f'v {x*norm:.5f} {y*norm:.5f} {z*norm:.5f}\n' for x, y, z in V))
        f.write(''.join(f'vt {u:.5f} {w:.5f}\n' for u, w in VT))
        for i, t in enumerate(F):
            a, b, c = (V[p - 1] for p, _ in t); n = cross(sub(b, a), sub(c, a)); ln = math.sqrt(sum(q * q for q in n)) or 1
            f.write(f'vn {n[0]/ln:.4f} {n[1]/ln:.4f} {n[2]/ln:.4f}\n')
        for i, t in enumerate(F):   # deux sens, même normale extérieure (comme les autres modèles du module)
            for tt in (t, t[::-1]): f.write('f ' + ' '.join(f'{a}/{b}/{i+1}' for a, b in tt) + '\n')
    # État couché : même coque tournée sur son flanc -z (lettre du flanc +z vers le haut), posée à y = 0
    g0, c0 = P['g', 0, -1], P['c', 0, -1]; ang = math.atan2(g0[2] - c0[2], g0[1] - c0[1])   # angle du flanc
    th = -(math.pi / 2 + ang)
    R = lambda p: (p[0], p[1] * math.cos(th) - p[2] * math.sin(th), p[1] * math.sin(th) + p[2] * math.cos(th))
    VR = [R(p) for p in V]; y0 = min(p[1] for p in VR); zc = (min(p[2] for p in VR) + max(p[2] for p in VR)) / 2
    VR = [(x, y - y0, z - zc) for x, y, z in VR]
    with open(f'{OUT}/canot4_{key}_couche.obj', 'w') as f:
        f.write(''.join(f'v {x*norm:.5f} {y*norm:.5f} {z*norm:.5f}\n' for x, y, z in VR))
        f.write(''.join(f'vt {u:.5f} {w:.5f}\n' for u, w in VT))
        for t in F:
            a, b, c = (VR[p - 1] for p, _ in t); n = cross(sub(b, a), sub(c, a)); ln = math.sqrt(sum(q * q for q in n)) or 1
            f.write(f'vn {n[0]/ln:.4f} {n[1]/ln:.4f} {n[2]/ln:.4f}\n')
        for i, t in enumerate(F):
            for tt in (t, t[::-1]): f.write('f ' + ' '.join(f'{a}/{b}/{i+1}' for a, b in tt) + '\n')
    return dict(L=L, B=B, H=H, P=P, Lb=Lb, W=W, TH=TH, px=px, k=k, F=F, V=V, VT=VT)

def texture(key, col, letter, G):
    L, B, H, P, px, k = G['L'], G['B'], G['H'], G['P'], G['px'], G['k']
    im = Image.new('RGB', (G['W'], G['TH']), shade(col, .55)); d = ImageDraw.Draw(im)
    base, dark, light = shade(col, 1), shade(col, .62), shade(col, 1.18)
    fnt = lambda sz: ImageFont.truetype(FONT, round(sz))
    def text(c, s, sz, fill, stroke=None, sw=0):
        f = fnt(sz); d.text(c, s, font=f, fill=fill, anchor='mm', stroke_width=sw, stroke_fill=stroke)
    for reg, sd in (('R', 1), ('L', -1)):
        outline = [px(reg, P['g', s, sd]) for s in S] + [px(reg, P['c', s, sd]) for s in reversed(S)]
        d.polygon(outline, fill=base)
        for s0 in (-.6, -.25, .25, .6):                                         # coutures de gomme (écorce)
            x = s0 * L / 2; d.line([px(reg, (x, H * 1.05, 0)), px(reg, (x * .9, 0, 0))], fill=dark, width=max(2, round(k * 2.5)))
        gl = [px(reg, P['g', s, sd]) for s in S]; d.line(gl, fill=RIM, width=round(k * .16 * H), joint='curve')   # plat-bord sombre
        d.line([(x, y + k * .16 * H * .7) for x, y in gl[2:-2]], fill=CREAM, width=max(2, round(k * 3)))          # filet crème
        cy = .44 * H; r = .36 * H; c = px(reg, (0, cy, 0)); lw = max(2, round(k * 3))
        if key == 'coureur':   # signe distinctif du petit canot : médaillon en losange + frise en zigzag sous le plat-bord
            zz = []; n = 14
            for j in range(n + 1):
                x = (-.62 + 1.24 * j / n) * L / 2; zz.append(px(reg, (x, H * (.80 if j % 2 else .66), 0)))
            d.line(zz, fill=CREAM, width=max(3, round(k * 4)), joint='curve')
            q = r * 1.25 * k; d.polygon([(c[0], c[1] - q), (c[0] + q, c[1]), (c[0], c[1] + q), (c[0] - q, c[1])], fill=CREAM, outline=RIM, width=lw)
            text(c, letter, r * k * 1.3, RIM)
        else:
            d.ellipse([c[0] - r * k, c[1] - r * k, c[0] + r * k, c[1] + r * k], fill=CREAM, outline=RIM, width=lw)
            text(c, letter, r * k * 1.5, RIM)
        xa = .54 * L / 2; hh = .34 * H                                           # un seul chevron, large, vers la proue
        pts = [(xa, cy + hh, 0), (xa + .95 * hh, cy, 0), (xa, cy - hh, 0), (xa + .32 * hh, cy, 0)]
        d.polygon([px(reg, p) for p in pts], fill=(250, 244, 228))
    # Dessus : pontets couleur joueur, plat-bord sombre, intérieur en cèdre, membrures, barres, lettre
    outer = [px('T', P['g', s, 1]) for s in S] + [px('T', P['g', s, -1]) for s in reversed(S)]
    d.polygon(outer, fill=base)
    SI = [s for s in S if abs(s) <= S_IN]
    inner = [px('T', P['i', s, 1]) for s in SI] + [px('T', P['i', s, -1]) for s in reversed(SI)]
    d.polygon(outer, outline=RIM, width=round(k * .07 * B))
    d.polygon(inner, fill=base, outline=RIM, width=round(k * .035 * B))   # fond intérieur à la couleur du canot
    flo = [px('T', P['f', s, 1]) for s in SI] + [px('T', P['f', s, -1]) for s in reversed(SI)]
    d.polygon(outer, outline=RIM, width=round(k * .045 * B))
    c = px('T', (0, 0, 0)); h = .55 * B * k
    text(c, letter, h * 1.05, (255, 255, 255), stroke=RIM, sw=max(2, round(h * .04)))   # lettre blanche
    xb = .87 * L / 2; hb = .05 * L                                               # flèche sur le pontet avant
    d.polygon([px('T', (xb + hb * .6, 0, 0)), px('T', (xb - hb * .4, 0, -hb * .55)), px('T', (xb - hb * .15, 0, 0)), px('T', (xb - hb * .4, 0, hb * .55))], fill=CREAM)
    # Dessous
    bot = [px('B', P['c', s, 1]) for s in S] + [px('B', P['c', s, -1]) for s in reversed(S)]
    d.polygon(bot, fill=dark)
    d.line([px('B', (-G['Lb'] / 2, 0, 0)), px('B', (G['Lb'] / 2, 0, 0))], fill=PITCH, width=max(2, round(k * 4)))
    im.save(f'{OUT}/cn4_{col_name(col)}_{key}_{letter}.png')
col_name = lambda c: [k for k, v in PC.items() if v == c][0]

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for key in SIZES:
        G = build(key)
        for cn, c in PC.items():
            for le in 'ABC': texture(key, c, le, G)
        print(key, 'tris', len(G['F']), 'verts', len(G['V']), 'tex', G['W'], G['TH'])
