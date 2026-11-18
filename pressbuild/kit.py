# -*- coding: utf-8 -*-
"""Modelo de diseño común para el Press Kit de GFB (alimenta PDF e IDML)."""
import math, random
from PIL import Image

W, H = 960.0, 540.0
import os
HERE = os.path.dirname(os.path.abspath(__file__))
LINKS = HERE + '/Links'
FONTS = HERE + '/Fonts'

# ---------- Paleta (sacada del logo de GFB) ----------
NAVY = '#4B2A3A'
NAVY_D = '#3A1628'
NAVY_DD = '#170D19'
GREEN = '#8F6A1C'
GREEN_D = '#7A2646'
GREEN_L = '#F5DCE5'
SKY = '#B8913A'
SKY_L = '#F1E6C8'
PAPER = '#FBF1F0'
MIST = '#F3DCDF'
INK = '#33273A'
MUTED = '#76697B'
WHITE = '#FFFFFF'

COLORS = {
    'MV_Navy': NAVY, 'MV_NavyDeep': NAVY_D, 'MV_NavyNight': NAVY_DD,
    'MV_Green': GREEN, 'MV_GreenDeep': GREEN_D, 'MV_GreenMist': GREEN_L,
    'MV_Sky': SKY, 'MV_SkyMist': SKY_L, 'MV_Paper': PAPER, 'MV_Mist': MIST,
    'MV_Ink': INK, 'MV_Muted': MUTED, 'MV_White': WHITE,
}
HEX2NAME = {v.upper(): k for k, v in COLORS.items()}

# ---------- Fuentes ----------
FONT_FILES = {
    'serif': 'CormorantGaramond-Medium.ttf',
    'serifi': 'CormorantGaramond-MediumItalic.ttf',
    'serifb': 'CormorantGaramond-SemiBold.ttf',
    'sans': 'Manrope-Regular.ttf',
    'sansb': 'Manrope-SemiBold.ttf',
    'sanse': 'Manrope-ExtraBold.ttf',
    'tenor': 'TenorSans-Regular.ttf',
    'script': 'GreatVibes-Regular.ttf',
}
# (familia, estilo) tal como los ve InDesign
FONT_IDML = {
    'serif': ('Cormorant Garamond', 'Medium'),
    'serifi': ('Cormorant Garamond', 'Medium Italic'),
    'serifb': ('Cormorant Garamond', 'SemiBold'),
    'sans': ('Manrope', 'Regular'),
    'sansb': ('Manrope', 'SemiBold'),
    'sanse': ('Manrope', 'ExtraBold'),
    'tenor': ('Tenor Sans', 'Regular'),
    'script': ('Great Vibes', 'Regular'),
}

# ---------- Estilos de párrafo (se vuelven estilos reales en InDesign) ----------
# nombre: (font, size, leading, color, tracking(1/1000 em), align)
STYLES = {
    'Titulo_XL':   ('serif', 50, 52, NAVY, -5, 'L'),
    'Titulo_L':    ('serif', 38, 41, NAVY, -4, 'L'),
    'Titulo_M':    ('serif', 28, 31, NAVY, -3, 'L'),
    'Titulo_S':    ('serif', 19, 22, NAVY, 0, 'L'),
    'Cita':        ('serifi', 20, 25, NAVY, 0, 'L'),
    'Lema':        ('serifi', 15, 19, MUTED, 0, 'L'),
    'Cuerpo':      ('sans', 10, 16, INK, 0, 'L'),
    'Cuerpo_S':    ('sans', 8.5, 13.5, MUTED, 0, 'L'),
    'Etiqueta':    ('sansb', 7.5, 10, GREEN, 190, 'L'),
    'Etiqueta_B':  ('sansb', 7, 10, NAVY, 150, 'L'),
    'Cifra':       ('serif', 34, 36, NAVY, -3, 'L'),
    'Cifra_Label': ('sansb', 7, 10, MUTED, 90, 'L'),
    'Boton':       ('sansb', 8, 11, WHITE, 140, 'C'),
    'Pie':         ('sansb', 6.5, 9, NAVY, 160, 'L'),
}


def hx(c):
    return c.upper()


# ---------- Geometría ----------
K = 0.5522847498


class P:
    """Trazado: lista de ops en coordenadas de página (y hacia abajo)."""
    def __init__(self):
        self.ops = []

    def M(self, x, y): self.ops.append(('M', x, y)); return self
    def L(self, x, y): self.ops.append(('L', x, y)); return self
    def C(self, a, b, c, d, e, f): self.ops.append(('C', a, b, c, d, e, f)); return self
    def Z(self): self.ops.append(('Z',)); return self

    def anchors_bbox(self):
        xs, ys = [], []
        for op in self.ops:
            if op[0] in 'ML': xs.append(op[1]); ys.append(op[2])
            elif op[0] == 'C': xs.append(op[5]); ys.append(op[6])
        return min(xs), min(ys), max(xs), max(ys)

    def bbox(self):
        """bbox con puntos de control (suficiente para áreas de enlace)."""
        xs, ys = [], []
        for op in self.ops:
            if op[0] in 'ML': xs.append(op[1]); ys.append(op[2])
            elif op[0] == 'C':
                xs += [op[1], op[3], op[5]]; ys += [op[2], op[4], op[6]]
        return min(xs), min(ys), max(xs), max(ys)

    def closed(self):
        return any(o[0] == 'Z' for o in self.ops)


def rect(x, y, w, h):
    return P().M(x, y).L(x + w, y).L(x + w, y + h).L(x, y + h).Z()


def rrect(x, y, w, h, r):
    r = min(r, w / 2, h / 2); k = K * r
    p = P().M(x + r, y)
    p.L(x + w - r, y).C(x + w - r + k, y, x + w, y + r - k, x + w, y + r)
    p.L(x + w, y + h - r).C(x + w, y + h - r + k, x + w - r + k, y + h, x + w - r, y + h)
    p.L(x + r, y + h).C(x + r - k, y + h, x, y + h - r + k, x, y + h - r)
    p.L(x, y + r).C(x, y + r - k, x + r - k, y, x + r, y).Z()
    return p


def ellipse(cx, cy, rx, ry):
    kx, ky = K * rx, K * ry
    p = P().M(cx, cy - ry)
    p.C(cx + kx, cy - ry, cx + rx, cy - ky, cx + rx, cy)
    p.C(cx + rx, cy + ky, cx + kx, cy + ry, cx, cy + ry)
    p.C(cx - kx, cy + ry, cx - rx, cy + ky, cx - rx, cy)
    p.C(cx - rx, cy - ky, cx - kx, cy - ry, cx, cy - ry).Z()
    return p


def circle(cx, cy, r):
    return ellipse(cx, cy, r, r)


def arch(x, y, w, h):
    r = w / 2.0; k = K * r
    p = P().M(x, y + h).L(x, y + r)
    p.C(x, y + r - k, x + r - k, y, x + r, y)
    p.C(x + r + k, y, x + w, y + r - k, x + w, y + r)
    p.L(x + w, y + h).Z()
    return p


def swoosh(ax, ay, bx, by, h1, h2, skew=0.0):
    """Medialuna afilada (eco del remolino del logo). h1/h2: abombado exterior/interior."""
    dx, dy = bx - ax, by - ay
    L = math.hypot(dx, dy)
    nx, ny = dy / L, -dx / L      # normal
    def pt(t, h):
        return (ax + dx * t + nx * h, ay + dy * t + ny * h)
    c1 = pt(0.22 + skew, h1); c2 = pt(0.72 + skew, h1 * 0.75)
    d1 = pt(0.72 + skew, h2 * 0.75); d2 = pt(0.22 + skew, h2)
    p = P().M(ax, ay).C(c1[0], c1[1], c2[0], c2[1], bx, by)
    p.C(d1[0], d1[1], d2[0], d2[1], ax, ay).Z()
    return p


def smooth_closed(points):
    """Catmull-Rom cerrado -> bezier."""
    n = len(points)
    p = P().M(*points[0])
    for i in range(n):
        p0 = points[(i - 1) % n]; p1 = points[i]; p2 = points[(i + 1) % n]; p3 = points[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6.0, p1[1] + (p2[1] - p0[1]) / 6.0)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6.0, p2[1] - (p3[1] - p1[1]) / 6.0)
        p.C(c1[0], c1[1], c2[0], c2[1], p2[0], p2[1])
    p.Z()
    return p


def contour_loops(cx, cy, r0, dr, n, sx=1.0, sy=0.75, seed=1, wob=0.09):
    rnd = random.Random(seed)
    ph1, ph2 = rnd.uniform(0, 6.28), rnd.uniform(0, 6.28)
    loops = []
    for i in range(n):
        r = r0 + dr * i
        pts = []
        for k in range(28):
            th = 2 * math.pi * k / 28
            rr = r * (1 + wob * math.sin(3 * th + ph1 + i * 0.33) + wob * 0.6 * math.sin(5 * th + ph2 - i * 0.21))
            pts.append((cx + rr * sx * math.cos(th), cy + rr * sy * math.sin(th)))
        loops.append(smooth_closed(pts))
    return loops


def leaf(bx, by, ang, length, width):
    dx, dy = math.cos(ang), math.sin(ang)
    nx, ny = -dy, dx
    tx, ty = bx + dx * length, by + dy * length
    p = P().M(bx, by)
    p.C(bx + dx * length * 0.25 + nx * width, by + dy * length * 0.25 + ny * width,
        tx - dx * length * 0.30 + nx * width * 0.55, ty - dy * length * 0.30 + ny * width * 0.55, tx, ty)
    p.C(tx - dx * length * 0.30 - nx * width * 0.55, ty - dy * length * 0.30 - ny * width * 0.55,
        bx + dx * length * 0.25 - nx * width, by + dy * length * 0.25 - ny * width, bx, by).Z()
    return p


def branch(x0, y0, x1, y1, bend):
    """Rama curva (abierta) y puntos+ángulos a lo largo de ella."""
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy)
    c1 = (x0 + dx * 0.33 - dy / L * bend, y0 + dy * 0.33 + dx / L * bend)
    c2 = (x0 + dx * 0.66 - dy / L * bend * 0.6, y0 + dy * 0.66 + dx / L * bend * 0.6)
    p = P().M(x0, y0).C(c1[0], c1[1], c2[0], c2[1], x1, y1)
    def at(t):
        u = 1 - t
        x = u**3 * x0 + 3 * u * u * t * c1[0] + 3 * u * t * t * c2[0] + t**3 * x1
        y = u**3 * y0 + 3 * u * u * t * c1[1] + 3 * u * t * t * c2[1] + t**3 * y1
        tx = 3 * u * u * (c1[0] - x0) + 6 * u * t * (c2[0] - c1[0]) + 3 * t * t * (x1 - c2[0])
        ty = 3 * u * u * (c1[1] - y0) + 6 * u * t * (c2[1] - c1[1]) + 3 * t * t * (y1 - c2[1])
        return x, y, math.atan2(ty, tx)
    return p, at


# ---------- Modelo ----------
class Item:
    def __init__(self, kind, **kw):
        self.kind = kind
        self.__dict__.update(kw)


class Page:
    def __init__(self, name, bg=PAPER):
        self.name = name
        self.bg = bg
        self.items = []

    # formas
    def shape(self, path, fill=None, stroke=None, sw=0.0, a=1.0, link=None, name=None):
        self.items.append(Item('shape', path=path, fill=fill, stroke=stroke, sw=sw, a=a, link=link, name=name))

    def image(self, path, file, fx=0.5, fy=0.5, zoom=1.0, stroke=None, sw=0.0, a=1.0, link=None, name=None):
        self.items.append(Item('image', path=path, file=file, fx=fx, fy=fy, zoom=zoom, stroke=stroke, sw=sw, a=a, link=link, name=name))

    def logo(self, file, x, y, w, link=None, name=None):
        iw, ih = Image.open(f'{LINKS}/{file}').size
        h = w * ih / iw
        self.items.append(Item('image', path=rect(x, y, w, h), file=file, fx=0.5, fy=0.5, zoom=1.0, stroke=None, sw=0, a=1.0, link=link, name=name or file, fit='contain'))
        return h

    def text(self, x, y, w, paras, style='Cuerpo', h=None, align=None, link=None, name=None, color=None, space=6.0):
        """paras: lista de párrafos; párrafo = str | lista de runs (texto, fontkey|None, color|None).
        '\\n' dentro del texto = salto de línea."""
        self.items.append(Item('text', x=x, y=y, w=w, h=h, paras=paras, style=style, align=align, link=link, name=name, color=color, space=space))


def style_of(name):
    return STYLES[name]


def norm_paras(paras):
    out = []
    for p in paras:
        if isinstance(p, str):
            out.append([(p, None, None)])
        else:
            out.append([(r[0], r[1] if len(r) > 1 else None, r[2] if len(r) > 2 else None) for r in p])
    return out


def split_lines(runs):
    """Parte una lista de runs en líneas (por '\\n')."""
    lines = [[]]
    for text, f, c in runs:
        parts = text.split('\n')
        for i, part in enumerate(parts):
            if i > 0:
                lines.append([])
            if part != '':
                lines[-1].append((part, f, c))
    return lines
