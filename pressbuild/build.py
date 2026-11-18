# -*- coding: utf-8 -*-
"""Reconstruye el Press Kit de Mivelle con todas las fotos de /fotos."""
import os, re, sys, math, subprocess, glob
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from PIL import Image
import pages7 as P7, render_pdf as RP

# Piezas con ficha propia (nombre de archivo -> datos)
BASE = [
    ('Amarillo', 'Amarillo', 'Bolso con asa superior', '#FBF0C9', .55),
    ('Rosa', 'Rosa', 'Clutch con cadena', '#FADCE6', .55),
    ('Cristal transparente', 'Cristal\ntransparente', 'Bolso con cadena dorada', '#EEE9F2', .5),
    ('Naranja', 'Naranja', 'Bolso con cadena dorada', '#FBE0C4', .5),
    ('Amorette', 'Amorette', 'Corazón rojo y ámbar', '#F9D7D4', .55),
    ('Rojo', 'Rojo', 'Bolso con cadena larga', '#F7D2D6', .5),
    ('Ciruela', 'Ciruela', 'Bolso con cadena dorada', '#EBD0DE', .5),
    ('Rosa wristlet', 'Rosa wristlet', 'Cartera de muñeca', '#FAD9E4', .5),
    ('Negro wristlet', 'Negro wristlet', 'Cartera de muñeca', '#E6DEE5', .5),
    ('Azul cielo', 'Azul cielo', 'Bolso con asa superior', '#D8EEF5', .6),
    ('Ámbar', 'Ámbar', 'Mini tote con cadena', '#F8DFB8', .55),
    ('Magenta', 'Magenta', 'Clutch con cadena', '#F2CFE3', .6),
]
EXT = ('.jpg', '.jpeg', '.png', '.webp')


def added_time(path):
    try:
        out = subprocess.run(['git', 'log', '--diff-filter=A', '--format=%ct', '--', path], cwd=ROOT, capture_output=True, text=True).stdout.split()
        return int(out[-1]) if out else 0
    except Exception:
        return 0


def tint_of(im):
    sm = im.convert('RGB').resize((1, 1), Image.LANCZOS).getpixel((0, 0))
    mix = tuple(int(255 - (255 - c) * .28) for c in sm)
    return '#%02X%02X%02X' % mix


def nice(fn):
    return re.sub(r'[_-]+', ' ', os.path.splitext(fn)[0]).strip()


files = {}
for fn in os.listdir(f'{ROOT}/fotos'):
    if fn.lower().endswith(EXT):
        files[os.path.splitext(fn)[0]] = fn
pieces = []
used = set()
for key, name, forma, tint, fy in BASE:
    if key in files:
        pieces.append([key, files[key], name, forma, tint, fy]); used.add(key)
new = sorted([k for k in files if k not in used], key=lambda k: (added_time(f'fotos/{files[k]}'), k))
for k in new:
    pieces.append([k, files[k], nice(files[k]), 'Hecho a mano', None, .5])

os.makedirs(f'{HERE}/Links', exist_ok=True)
PIECES = []
for i, (key, fn, name, forma, tint, fy) in enumerate(pieces):
    im = Image.open(f'{ROOT}/fotos/{fn}'); im = im.convert('RGB'); im.thumbnail((1600, 1600))
    out = f'foto_{i + 1:02d}.jpg'; im.save(f'{HERE}/Links/{out}', quality=85)
    PIECES.append((out, name, forma, tint or tint_of(im), fy))

N = len(PIECES); NC = max(1, math.ceil(N / 6)); P0 = 8 + NC; TOTAL = P0 + N + 7
P7.PIECES[:] = PIECES; P7.P0 = P0; P7.TOTAL = TOTAL
P7.TOC[:] = [('Biografía', 3), ('Esencia', 4), ('Misión, visión y valores', 5), ('Mensaje de la fundadora', 6), ('Galería', 7), ('Catálogo', 8), ('Piezas, una por una', P0),
             ('En conjunto', P0 + N), ('Paleta de colores', P0 + N + 1), ('Logros y reconocimientos', P0 + N + 2), ('Datos de prensa', P0 + N + 3),
             ('Comunicado de prensa', P0 + N + 4), ('Materiales para prensa', P0 + N + 5), ('Redes y contacto', P0 + N + 6)]
ROM = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']
pages = [P7.p_cover(), P7.p_toc(), P7.p_bio(), P7.p_essence(), P7.p_mission(), P7.p_founder(), P7.p_gallery()]
pages += [P7.p_cat(ROM[k], 8 + k) for k in range(NC)]
pages += [P7.piece_page(i) for i in range(N)]
pages += [P7.p_group(), P7.p_palette(), P7.p_achievements(), P7.p_press(), P7.p_release(), P7.p_materials(), P7.p_contact(), P7.p_close()]
assert len(pages) == TOTAL, (len(pages), TOTAL)


def fix(o, n):
    if isinstance(o, str):
        return re.sub(r'^\d+ / \d+$', f'{n} / {TOTAL}', o)
    if isinstance(o, list):
        return [fix(x, n) for x in o]
    if isinstance(o, tuple):
        return tuple(fix(x, n) if isinstance(x, str) else x for x in o)
    return o


for idx, pg in enumerate(pages):
    for it in pg.items:
        if getattr(it, 'kind', '') == 'text' and getattr(it, 'paras', None) is not None:
            it.paras = fix(it.paras, idx + 1)

outline = [('Portada', 1, 0), ('Contenido', 2, 0)] + [(t, n, 0) for t, n in P7.TOC] + [('Cierre', TOTAL, 0)]
for i, p in enumerate(PIECES):
    outline.append((f'Pieza {i + 1:02d} · {p[1].replace(chr(10), " ")}', P0 + i, 1))
outline.sort(key=lambda o: o[1])
out = f'{ROOT}/Mivelle-Press-Kit.pdf'
w = RP.render({'pages': pages, 'outline': outline}, out, 'Mivelle · Press Kit 2026', 'Mivelle', 'Press kit de Mivelle', 'Mivelle, handbags, República Dominicana')
print(f'{N} piezas, {TOTAL} páginas ->', out)
if w: print('\n'.join(w))
