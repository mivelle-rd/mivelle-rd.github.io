# -*- coding: utf-8 -*-
import math, random
from kit import *
import render_pdf as RP

IG = 'https://www.instagram.com/mivelle.rd/'
WAL = 'https://wa.me/18496079595?text=Hola%20Mivelle%2C%20quiero%20informaci%C3%B3n%20sobre%20sus%20carteras.'
TOTAL = 29
IVORY = '#FBF1F0'; IVORY2 = '#F3DCDF'; BROWN = '#4B2A3A'; DARK = '#3A1628'; PLATE = '#DDB95F'; PLATE_L = '#EBD08A'
GOLD_D = '#8F6A1C'; RED = '#C2456B'; AMBER = '#E39B1D'; ROSE = '#E87BA4'; SKYB = '#79CBE3'; PLUM = '#7B2253'
MUT = '#86707A'
STYLES.update({
    'Huge':   ('tenor', 70, 74, BROWN, -10, 'L'),
    'H1':     ('tenor', 40, 44, BROWN, -6, 'L'),
    'H2':     ('tenor', 26, 30, BROWN, -4, 'L'),
    'Quote':  ('tenor', 32, 38, RED, -5, 'L'),
    'Lab':    ('sansb', 7.2, 10, GOLD_D, 200, 'L'),
    'Body':   ('sans', 9.6, 15.5, BROWN, 0, 'L'),
    'Small':  ('sans', 8, 12.5, MUT, 0, 'L'),
    'Nm':     ('tenor', 15, 18, BROWN, 0, 'L'),
    'Num':    ('tenor', 11, 14, GOLD_D, 60, 'L'),
    'Big':    ('tenor', 46, 50, BROWN, -6, 'L'),
    'Phone':  ('tenor', 50, 54, PLATE, -4, 'L'),
    'Pie2':   ('sansb', 6.5, 9, BROWN, 160, 'L'),
    'Script': ('script', 40, 44, RED, 0, 'L'),
    'ScriptL': ('script', 46, 50, RED, 0, 'L'),
    'Chip':   ('sansb', 6.8, 9, BROWN, 120, 'C'),
})
STYLES.update({
    'Seccion':        ('sansb', 7.2, 10, GOLD_D, 200, 'L'),
    'Seccion_Oscura': ('sansb', 7.2, 10, PLATE, 200, 'L'),
    'Pieza_Titulo':   ('tenor', 40, 44, BROWN, -6, 'L'),
    'Indice_N1':      ('sansb', 8.5, 12, BROWN, 140, 'L'),
    'Indice_N2':      ('tenor', 11, 14, BROWN, 0, 'L'),
})
WRAP = RP.WRAP_STYLES


def sec(pg, text, x=54, y=20, dark=False):
    """Etiqueta de sección: alimenta el índice automático de InDesign."""
    pg.text(x, y, 330, [text], 'Seccion_Oscura' if dark else 'Seccion', name='Seccion')


def R(x, y, w, h): return rect(x, y, w, h)


def pill(pg, x, y, w, h, label, fill, tcolor, link=None, name=None, stroke=None):
    pg.shape(rrect(x, y, w, h, h / 2), fill=fill, stroke=stroke, sw=1.0 if stroke else 0, link=link, name=name)
    fnt, size, lead, col, trk, al = STYLES['Boton']
    tw = RP.sw(label, fnt, size, trk)
    tx = x + (w - tw - 18) / 2
    pg.text(tx - 2, y + h / 2 - 8.0, tw + 6, [label], 'Boton', align='L', color=tcolor)
    ax = tx + tw + 5; ay = y + h / 2
    pg.shape(P().M(ax, ay).L(ax + 10, ay), stroke=tcolor, sw=1.2)
    pg.shape(P().M(ax + 6.4, ay - 3.2).L(ax + 10, ay).L(ax + 6.4, ay + 3.2), stroke=tcolor, sw=1.2)


def plate(pg, x, y, w, h, text, style, link=None, name=None, tcol=BROWN):
    """Placa dorada de Mivelle (cápsula con orificio) — eco de la placa de las carteras."""
    pg.shape(rrect(x, y, w, h, h / 2), fill=PLATE, link=link, name=name)
    pg.shape(rrect(x + 3, y + 3, w - 6, h - 6, (h - 6) / 2), stroke=PLATE_L, sw=1.0, a=.9)
    pg.shape(circle(x + w - h / 2, y + h / 2, h * 0.075), fill=BROWN, a=.85)
    pg.text(x + 24, y + h * 0.16, w - h, [text], style, color=tcol, name=(name or 'Placa') + ' texto')


def foot(pg, n, dark=False, x=54):
    c = '#F2EDE9' if dark else BROWN
    pg.text(x, 513, 400, ['MIVELLE  ·  HANDBAGS  ·  REPÚBLICA DOMINICANA'], 'Pie2', color=c)
    pg.text(806, 513, 100, [f'{n} / {TOTAL}'], 'Pie2', align='R', color=PLATE if dark else GOLD_D)
    pg.items[-1].only = 'pdf'


def lab(pg, x, y, t, color=GOLD_D, w=300):
    pg.shape(P().M(x, y).L(x + 28, y), stroke=color, sw=1.2)
    pg.text(x + 38, y - 5, w, [t], 'Lab', color=color)


def beads(pg, specs, a=.55):
    for cx, cy, r, col in specs:
        pg.shape(circle(cx, cy, r), fill=col, a=a)
        pg.shape(circle(cx - r * .28, cy - r * .3, r * .22), fill=WHITE, a=.55)


# ===== 1 PORTADA =====
def p_cover():
    pg = Page('Portada', IVORY)
    beads(pg, [(70, 470, 46, RED), (130, 505, 26, AMBER), (24, 420, 20, ROSE), (410, 60, 30, SKYB), (440, 500, 36, AMBER), (900, 20, 40, PLUM)], .5)
    pg.shape(rrect(452, 28, 454, 484, 227), fill=IVORY2)
    pg.image(rrect(452, 28, 454, 484, 227), 'p06.jpg', fx=.5, fy=.54, zoom=1.0, name='Foto portada')
    pg.shape(rrect(452, 28, 454, 484, 227), stroke=PLATE, sw=2.2)
    lab(pg, 54, 70, 'PRESS KIT  ·  2026')
    pg.shape(rrect(54, 104, 380, 138, 69), fill=WHITE, a=.96, link=('page', 2), name='Capsula logo')
    pg.shape(rrect(54, 104, 380, 138, 69), stroke=PLATE, sw=1.6)
    pg.logo('logo_mivelle_real.png', 104, 124, 280, link=('page', 2), name='Logo Mivelle')
    pg.text(54, 258, 360, ['HANDBAGS  ·  BORN IN A BEAUTIFUL CORNER OF THE DOMINICAN REP.'], 'Lab')
    pg.text(54, 282, 380, [[('Crafted to elevate\nyour style.', None)]], 'ScriptL', name='Lema')
    pg.text(54, 404, 330, ['Carteras hechas a mano con cuentas de cristal. Tienda online.'], 'Body', name='Subtitulo')
    pill(pg, 54, 446, 190, 32, 'VER EL CATÁLOGO', BROWN, IVORY, link=('page', 8), name='Boton catalogo')
    pill(pg, 258, 446, 150, 32, 'TIENDA ONLINE', IVORY, BROWN, stroke=BROWN, name='Chip')
    pg.text(806, 513, 100, [f'1 / {TOTAL}'], 'Pie2', align='R', color=GOLD_D)
    pg.items[-1].only = 'pdf'
    return pg



def cap(pg, x, y, w, h, f, fx=.5, fy=.5, name='Foto', link=None, frame=True):
    """Foto en cápsula (eco de la placa dorada)."""
    if frame:
        pg.shape(rrect(x - 14, y + 14, w, h, w / 2), stroke=PLATE, sw=1.4, a=.95)
    pg.image(rrect(x, y, w, h, w / 2), f, fx=fx, fy=fy, stroke=WHITE, sw=5, link=link, name=name)


# ===== PIEZAS =====
PIECES = [  # foto, nombre, forma, tinte, fy
    ('p01.jpg', 'Amarillo', 'Bolso con asa superior', '#FBF0C9', .55),
    ('p02.jpg', 'Rosa', 'Clutch con cadena', '#FADCE6', .55),
    ('p03.jpg', 'Cristal\ntransparente', 'Bolso con cadena dorada', '#EEE9F2', .5),
    ('p05.jpg', 'Naranja', 'Bolso con cadena dorada', '#FBE0C4', .5),
    ('p06.jpg', 'Amorette', 'Corazón rojo y ámbar', '#F9D7D4', .55),
    ('p07.jpg', 'Rojo', 'Bolso con cadena larga', '#F7D2D6', .5),
    ('p09.jpg', 'Ciruela', 'Bolso con cadena dorada', '#EBD0DE', .5),
    ('p10.jpg', 'Rosa wristlet', 'Cartera de muñeca', '#FAD9E4', .5),
    ('p11.jpg', 'Negro wristlet', 'Cartera de muñeca', '#E6DEE5', .5),
    ('p12.jpg', 'Azul cielo', 'Bolso con asa superior', '#D8EEF5', .6),
    ('p14.jpg', 'Ámbar', 'Mini tote con cadena', '#F8DFB8', .55),
    ('p15.jpg', 'Magenta', 'Clutch con cadena', '#F2CFE3', .6),
]
P0 = 10   # primera página de pieza
CAT_P = {1: 6, 2: 7}


def piece_page(i):
    f, name, forma, tint, fy_ = PIECES[i]
    n = P0 + i
    pg = Page(f'Pieza {i + 1:02d} · {name.replace(chr(10), " ")}', tint)
    left = i % 2 == 0
    px = 90 if left else 560
    tx = 520 if left else 70
    beads(pg, [(tx + 380, 70, 30, WHITE), (tx + 420, 120, 14, WHITE), (tx - 10, 480, 24, WHITE)], .6)
    cap(pg, px, 40, 310, 440, f, fy=fy_, name='Foto pieza')
    pg.text(tx, 70, 300, [f'N.º {i + 1:02d}'], 'Script', color=RED)
    pg.text(tx, 124, 440, [name.replace('\n', ' ')], 'Pieza_Titulo', name='Titulo')
    pg.text(tx, 178 if len(name) < 16 else 178, 360, [forma], 'Nm', color=RED)
    pg.text(tx, 220, 330, ['Una pieza de la colección Mivelle: hecha a mano con cuentas de cristal, pensada para elevar tu estilo.'], 'Body')
    y = 292
    for l, v in [('COLOR', name.replace('\n', ' ') if (forma == 'Hecho a mano' or i == 2) else name.replace('\n', ' ').split(' ')[0]), ('FORMA', forma), ('HECHO', 'A mano, con cuentas de cristal')]:
        pg.shape(P().M(tx, y).L(tx + 330, y), stroke=BROWN, sw=0.5, a=.25)
        pg.text(tx, y + 11, 90, [l], 'Lab')
        pg.text(tx + 90, y + 8, 240, [v], 'Nm')
        y += 38
    pg.shape(P().M(tx, y).L(tx + 330, y), stroke=BROWN, sw=0.5, a=.25)
    msg = f'Hola Mivelle, quiero información sobre la cartera {name.replace(chr(10), " ")} (N.º {i + 1:02d}).'
    from urllib.parse import quote
    pill(pg, tx, 418, 160, 30, 'DISPONIBLE', None, BROWN, stroke=BROWN, link=('url', 'https://wa.me/18496079595?text=' + quote(msg)), name='Boton Disponible')
    # navegación
    prev_p = n - 1 if i > 0 else 8
    next_p = n + 1 if i < len(PIECES) - 1 else P0 + len(PIECES)
    pg.text(tx, 470, 110, ['‹ ANTERIOR'], 'Pie2', link=('page', prev_p), name='Anterior')
    pg.text(tx + 110, 470, 110, ['CATÁLOGO'], 'Pie2', link=('page', 8), name='Catalogo')
    pg.text(tx + 220, 470, 110, ['SIGUIENTE ›'], 'Pie2', link=('page', next_p), name='Siguiente')
    foot(pg, n, x=(54 if not left else 54))
    return pg


# ===== CONTENIDO =====
TOC = [('Biografía', 3), ('Esencia', 4), ('Misión, visión y valores', 5), ('Mensaje de la fundadora', 6), ('Galería', 7), ('Catálogo', 8), ('Piezas, una por una', 10),
       ('En conjunto', 22), ('Paleta de colores', 23), ('Logros y reconocimientos', 24), ('Datos de prensa', 25),
       ('Comunicado de prensa', 26), ('Materiales para prensa', 27), ('Redes y contacto', 28)]


TOC_IDML = [('BIOGRAFÍA', 1, 3), ('ESENCIA', 1, 4), ('MISIÓN, VISIÓN Y VALORES', 1, 5), ('MENSAJE DE LA FUNDADORA', 1, 6), ('GALERÍA', 1, 7),
            ('CATÁLOGO · PARTE I', 1, 8), ('CATÁLOGO · PARTE II', 1, 9)] + \
           [(p[1].replace(chr(10), ' '), 2, P0 + i) for i, p in enumerate(PIECES)] + \
           [('EN CONJUNTO', 1, 22), ('PALETA DE COLORES', 1, 23), ('LOGROS Y RECONOCIMIENTOS', 1, 24), ('DATOS DE PRENSA', 1, 25),
            ('COMUNICADO DE PRENSA', 1, 26), ('MATERIALES PARA PRENSA', 1, 27), ('REDES Y CONTACTO', 1, 28)]


def p_toc():
    pg = Page('Contenido', IVORY)
    beads(pg, [(60, 500, 38, ROSE), (900, 500, 44, SKYB), (500, 520, 24, RED)], .35)
    for cx, cy, r, f, fy_ in [(790, 74, 58, 'p07.jpg', .5), (884, 150, 36, 'p12.jpg', .6), (698, 138, 32, 'p02.jpg', .55)]:
        pg.image(circle(cx, cy, r), f, fx=.5, fy=fy_, stroke=PLATE, sw=3, name='Burbuja')
    pg.text(54, 70, 300, ['Todo en un vistazo'], 'Script', color=RED)
    pg.text(54, 118, 520, ['Contenido'], 'Big', name='Titulo')
    n0 = len(pg.items)
    for i, (t, n) in enumerate(TOC):
        col, row = i // 7, i % 7
        x = 54 + col * 432; y = 176 + row * 46
        lk = ('page', n)
        pg.shape(rrect(x, y, 420, 38, 19), fill=WHITE, a=.92, link=lk, name=f'Placa {t}')
        pg.shape(rrect(x, y, 420, 38, 19), stroke=PLATE, sw=1.3, link=lk)
        pg.shape(circle(x + 19, y + 19, 13), fill=PLATE, link=lk)
        pg.text(x + 4, y + 12, 30, [f'{i + 1:02d}'], 'Nm', align='C', link=lk)
        pg.text(x + 46, y + 10, 290, [t], 'Nm', link=lk)
        pg.text(x + 330, y + 14, 70, [f'PÁG. {n}'], 'Lab', align='R', link=lk)
    for it in pg.items[n0:]:
        it.only = 'pdf'
    toc = pg.text(54, 176, 800, [lab for lab, _, _ in TOC_IDML], 'Indice_N1', name='TOC', space=0)
    pg.items[-1].only = 'idml'
    pg.items[-1].cols = 2
    pg.items[-1].h = 280
    pg.items[-1].pstyles = ['Indice_N1' if l == 1 else 'Indice_N2' for _, l, _ in TOC_IDML]
    pg.items[-1].pnums = [str(n) for _, _, n in TOC_IDML]
    foot(pg, 2)
    return pg


def p_bio():
    pg = Page('Biografía', IVORY)
    cap(pg, 70, 40, 300, 440, 'p01.jpg', fy=.55, name='Foto biografia')
    beads(pg, [(880, 60, 36, AMBER), (930, 120, 18, ROSE)], .45)
    pg.text(430, 66, 300, ['Nuestra historia'], 'Script')
    sec(pg, 'BIOGRAFÍA', 430)
    pg.text(430, 110, 480, [[('Nacida en un rincón\nhermoso de ', None), ('RD.', None, RED)]], 'H1', name='Titulo')
    pg.text(430, 204, 215, ['Mivelle es una marca de handbags nacida en un rincón hermoso de República Dominicana. Cada pieza está hecha a mano con cuentas de cristal, con cadena dorada y una placa con el nombre de la marca.'], 'Body')
    pg.text(666, 204, 240, ['La marca fue fundada por Skarlen Montaño y se creó con una idea clara: elevar tu estilo. Mivelle empezó como un proyecto propio y hoy es una empresa: una tienda online que ya ha vendido varias de sus piezas.'], 'Body')
    plate(pg, 430, 350, 476, 80, 'Crafted to elevate your style.', 'H2', name='Placa cita')
    pg.text(430, 446, 476, ['MIVELLE BY SKARLEN MONTAÑO  ·  FUNDADORA'], 'Lab')
    foot(pg, 3, x=430)
    return pg


def p_essence():
    pg = Page('Esencia', IVORY)
    beads(pg, [(60, 60, 30, ROSE), (900, 480, 40, AMBER)], .4)
    pg.text(54, 54, 300, ['Lo que nos define'], 'Script')
    sec(pg, 'ESENCIA')
    pg.text(54, 100, 800, [[('Tres detalles, ', None), ('una misma esencia.', None, RED)]], 'H1', name='Titulo')
    cols = [('Hecho a mano', 'Cada bolso se arma pieza por pieza, cuenta por cuenta.', 'p03.jpg', .5),
            ('Cristal', 'Cuentas que juegan con la luz y llenan de color cada pieza.', 'p10.jpg', .5),
            ('Detalle dorado', 'Cadena dorada y una placa con el nombre Mivelle en cada cartera.', 'p05.jpg', .5)]
    for i, (t, d, f, fy_) in enumerate(cols):
        x = 54 + i * 290
        cap(pg, x + 10, 170, 150, 240, f, fy=fy_, name=f'Foto esencia {i + 1}', frame=False)
        pg.shape(circle(x + 85, 428, 5), fill=PLATE)
        pg.text(x, 440, 270, [t], 'Nm', align='C' if False else 'L')
        pg.text(x, 462, 250, [d], 'Small')
    foot(pg, 4)
    return pg


def p_gallery():
    pg = Page('Galería', DARK)
    pg.text(54, 62, 300, ['Galería'], 'Script', color=PLATE)
    sec(pg, 'GALERÍA', 54, 20, True)
    pg.text(54, 110, 220, [[('Color y\ncristal en\ncada ', None), ('detalle.', None, PLATE)]], 'H2', color=IVORY, name='Titulo')
    pg.text(54, 222, 190, ['Piezas de Mivelle en exteriores, interiores y estudio.'], 'Body', color='#E7D5DD')
    pill(pg, 54, 284, 150, 28, 'VER CATÁLOGO', PLATE, BROWN, link=('page', 8), name='Boton catalogo')
    tiles = [('p07.jpg', .5), ('p02.jpg', .55), ('p15.jpg', .6), ('p03.jpg', .5), ('p11.jpg', .6), ('p09.jpg', .5), ('p14.jpg', .55), ('p12.jpg', .6)]
    cw, ch, g = 168, 268, 4
    for i, (f, fy_) in enumerate(tiles):
        pg.image(R(280 + (i % 4) * (cw + g), (i // 4) * (ch + g), cw, ch), f, fx=.5, fy=fy_, name=f'Galeria {i + 1}')
    foot(pg, 7, dark=True)
    return pg


def p_cat(part, n):
    pg = Page(f'Catálogo parte {part}', IVORY)
    k = ['I','II','III','IV','V','VI','VII','VIII','IX','X'].index(part)
    start = 6 * k
    items = PIECES[start:start + 6]
    beads(pg, [(900, 40, 30, ROSE), (936, 90, 14, AMBER)], .4)
    pg.text(54, 40, 420, [f'Catálogo · Parte {part}'], 'Script')
    sec(pg, f'CATÁLOGO · PARTE {part}')
    pg.text(54, 84, 600, [[('Elige la ', None), ('tuya.', None, RED)]] if part == 'I' else [[('Más piezas, ', None), ('más color.', None, RED)]], 'H1', name='Titulo')
    cw, ch, gx, gy = 276, 178, 12, 12
    for i, (f, name, forma, tint, fy_) in enumerate(items):
        x = 54 + (i % 3) * (cw + gx); y = 140 + (i // 3) * (ch + gy)
        pp = ('page', P0 + start + i)
        pg.shape(rrect(x, y, cw, ch, 22), fill=WHITE, a=.95, link=pp, name=f'Tarjeta {start + i + 1}')
        pg.shape(rrect(x, y, cw, ch, 22), stroke=IVORY2, sw=1.0)
        pg.image(rrect(x + 9, y + 9, 106, ch - 18, 53), f, fx=.5, fy=fy_, link=pp, name=f'Cartera {start + i + 1}')
        tx = x + 128
        pg.text(tx, y + 16, 130, [f'N.º {start + i + 1:02d}'], 'Num')
        pg.text(tx, y + 32, 140, [name], 'Nm', link=pp)
        pg.text(tx, y + (78 if (len(name) > 12) else 58), 140, [forma], 'Small')
        pill(pg, tx, y + ch - 62, 136, 24, 'VER PIEZA', IVORY, BROWN, link=pp, name=f'Ver pieza {start + i + 1}', stroke=BROWN)
        pill(pg, tx, y + ch - 34, 136, 24, 'DISPONIBLE', None, BROWN, stroke=BROWN, link=('url', 'https://wa.me/18496079595?text=' + __import__('urllib.parse', fromlist=['quote']).quote('Hola Mivelle, quiero pedir la cartera ' + name.replace(chr(10), ' ') + '. ¿Está disponible?')), name=f'Pidela {start + i + 1}')
    foot(pg, n)
    return pg


def p_group():
    pg = Page('En conjunto', IVORY)
    pg.master = 'B'
    pg.image(R(0, 0, 480, 540), 'p13.jpg', fx=.5, fy=.6, name='Conjunto 1')
    pg.image(R(484, 0, 476, 270), 'p08.jpg', fx=.5, fy=.55, name='Conjunto 2')
    pg.shape(R(484, 274, 476, 266), fill=DARK)
    pg.text(520, 306, 300, ['En conjunto'], 'Script', color=PLATE)
    sec(pg, 'EN CONJUNTO', 520, 284, True)
    pg.text(520, 346, 400, [[('Una familia\nde ', None), ('colores.', None, PLATE)]], 'H2', color=IVORY, name='Titulo')
    pg.text(520, 414, 360, ['Las piezas de Mivelle conviven entre sí: mismos detalles dorados, cada una con su propio color.'], 'Body', color='#E7D5DD')
    pill(pg, 520, 462, 190, 28, 'ESCRIBIR POR WHATSAPP', PLATE, BROWN, link=('url', WAL), name='Boton WhatsApp')
    pill(pg, 722, 462, 160, 28, 'VER EN INSTAGRAM', IVORY, BROWN, link=('url', IG), name='Boton Instagram')
    pg.text(806, 513, 100, [f'22 / {TOTAL}'], 'Pie2', align='R', color=IVORY)
    pg.items[-1].only = 'pdf'
    return pg


def p_palette():
    pg = Page('Paleta de colores', IVORY)
    pg.text(54, 40, 300, ['Todos los tonos'], 'Script')
    sec(pg, 'PALETA DE COLORES')
    pg.text(54, 84, 700, [[('Paleta de ', None), ('colores.', None, RED)]], 'H1', name='Titulo')
    r = 56
    for i, (f, name, forma, tint, fy_) in enumerate(PIECES[:12]):
        cx = 54 + r + (i % 6) * 142; cy = 220 + (i // 6) * 175 + 20
        pp = ('page', P0 + i)
        pg.shape(circle(cx, cy, r + 8), fill=tint, link=pp)
        pg.image(circle(cx, cy, r), f, fx=.5, fy=fy_ + 0.05 if fy_ < .6 else fy_, stroke=WHITE, sw=3.5, link=pp, name=f'Color {i + 1}')
        pg.text(cx - 66, cy + r + 14, 132, [name.replace('\n', ' ')], 'Small', align='C', link=pp)
    foot(pg, 23)
    return pg


def p_press():
    pg = Page('Datos de prensa', IVORY)
    cap(pg, 60, 40, 190, 440, 'p10.jpg', name='Foto prensa')
    pg.text(330, 62, 300, ['En pocas líneas'], 'Script')
    sec(pg, 'DATOS DE PRENSA', 330)
    pg.text(330, 108, 600, [[('Datos de ', None), ('prensa.', None, RED)]], 'H1', name='Titulo')
    facts = [('Handbags', 'CATEGORÍA'), ('RD', 'ORIGEN · REPÚBLICA DOMINICANA'), ('A mano', 'CUENTAS DE CRISTAL Y CADENA DORADA'), ('Online', 'TIENDA ONLINE · VENTAS')]
    for k, (b, l) in enumerate(facts):
        x = 330 + (k % 2) * 300; y = 176 + (k // 2) * 106
        pg.shape(rrect(x, y, 276, 90, 45), fill=WHITE, a=.95)
        pg.shape(rrect(x, y, 276, 90, 45), stroke=PLATE, sw=1.2)
        pg.text(x + 34, y + 14, 220, [b], 'Big')
        pg.text(x + 34, y + 68, 230, [l], 'Lab')
    y = 396
    for l, v in [('MARCA', 'Mivelle'), ('FUNDADORA', 'Skarlen Montaño'), ('CONTACTO', '849-607-9595  ·  @mivelle.rd')]:
        pg.shape(P().M(330, y).L(906, y), stroke=BROWN, sw=0.5, a=.25)
        pg.text(330, y + 9, 110, [l], 'Lab')
        pg.text(450, y + 6, 440, [v], 'Body')
        y += 32
    foot(pg, 25, x=330)
    return pg


def p_contact():
    pg = Page('Redes y contacto', DARK)
    pg.image(R(0, 0, 300, 540), 'p08.jpg', fx=.3, fy=.55, name='Foto contacto')
    pg.shape(rrect(350, 36, 150, 64, 32), fill=WHITE, a=.97)
    pg.logo('logo_mivelle_real.png', 366, 44, 118, link=('page', 1), name='Logo Mivelle')
    pg.text(530, 56, 300, ['Escríbenos'], 'Script', color=PLATE)
    sec(pg, 'REDES Y CONTACTO', 350, 16, True)
    pg.text(350, 108, 520, [[('Hablemos', None), ('.', None, PLATE)]], 'Big', color=IVORY, name='Titulo')
    pg.text(350, 166, 520, ['Escanea un código o toca el botón para escribirnos o ver las piezas de Mivelle.'], 'Body', color='#E7D5DD')
    cards = [('qr_instagram.png', 'INSTAGRAM', '@mivelle.rd', ('url', IG), 'ABRIR INSTAGRAM'),
             ('qr_whatsapp.png', 'WHATSAPP', '849-607-9595', ('url', WAL), 'ABRIR WHATSAPP')]
    for k, (qr, l, big, lk, cta) in enumerate(cards):
        x = 350 + k * 290
        pg.shape(rrect(x, 200, 276, 222, 28), fill=IVORY, link=lk, name='Tarjeta ' + l)
        pg.image(R(x + 20, 220, 100, 100), qr, fx=.5, fy=.5, stroke=WHITE, sw=1, link=lk, name='QR ' + l)
        pg.text(x + 134, 224, 130, [l], 'Lab')
        pg.text(x + 134, 242, 136, [big], 'Nm', link=lk)
        pg.text(x + 134, 272, 130, ['Escanea con la cámara de tu teléfono.'], 'Small')
        pg.shape(P().M(x + 20, 338).L(x + 256, 338), stroke=BROWN, sw=0.5, a=.2)
        pill(pg, x + 20, 360, 236, 30, cta, BROWN, IVORY, link=lk, name='Boton ' + l)
    pill(pg, 350, 442, 566, 38, 'ESCRÍBELO POR WHATSAPP  ·  849-607-9595', PLATE, BROWN, link=('url', WAL), name='Boton Escribelo')
    foot(pg, 28, dark=True, x=350)
    return pg


def p_close():
    pg = Page('Cierre', DARK)
    pg.image(R(0, 0, 960, 540), 'p13.jpg', fx=.5, fy=.62, name='Foto cierre')
    pg.shape(R(0, 0, 960, 540), fill=DARK, a=.62)
    pg.shape(circle(480, 112, 78), fill=WHITE, a=.97, link=('page', 1), name='Circulo logo')
    pg.logo('logo_mivelle_real.png', 408, 92, 144, link=('page', 1), name='Logo Mivelle')
    pg.text(60, 214, 840, [[('Crafted to\nelevate your style.', None)]], 'Huge', color=WHITE, align='C', name='Titulo')
    pg.text(130, 380, 700, ['Handbags nacidas en República Dominicana.'], 'H2', color='#F0E2E8', align='C')
    pill(pg, 366, 440, 228, 32, 'SÍGUENOS EN INSTAGRAM', PLATE, BROWN, link=('url', IG), name='Boton Instagram')
    pg.text(806, 513, 100, [f'{TOTAL} / {TOTAL}'], 'Pie2', align='R', color=WHITE)
    pg.items[-1].only = 'pdf'
    return pg


def logo_card(pg, x, y, w, h, link=('page', 1)):
    pg.shape(rrect(x, y, w, h, h / 2 if h < 120 else 24), fill=WHITE, a=.97, link=link, name='Tarjeta logo')
    pg.shape(rrect(x, y, w, h, h / 2 if h < 120 else 24), stroke=PLATE, sw=1.3)
    lw = min(w - 60, (h - 24) * 938 / 360)
    pg.logo('logo_mivelle_real.png', x + (w - lw) / 2, y + (h - lw * 360 / 938) / 2, lw, link=link, name='Logo Mivelle')


def p_mission():
    pg = Page('Misión, visión y valores', IVORY)
    beads(pg, [(900, 60, 34, ROSE), (60, 500, 30, AMBER)], .4)
    pg.text(54, 44, 420, ['Lo que nos mueve'], 'Script')
    sec(pg, 'MISIÓN, VISIÓN Y VALORES')
    pg.text(54, 90, 850, [[('Misión, visión ', None), ('y valores.', None, RED)]], 'H1', name='Titulo')
    cards = [('MISIÓN', 'Crear handbags hechas a mano, con cuentas de cristal, que eleven el estilo de quien las lleva.'),
             ('VISIÓN', 'Ser una marca dominicana de carteras reconocida por su color, su detalle y su origen: un rincón hermoso de República Dominicana.'),
             ('VALORES', 'Hecho a mano  ·  Color  ·  Detalle dorado  ·  Origen dominicano')]
    for i, (t, d) in enumerate(cards):
        x = 54 + i * 290
        pg.shape(rrect(x, 170, 276, 200, 28), fill=WHITE, a=.95)
        pg.shape(rrect(x, 170, 276, 200, 28), stroke=PLATE, sw=1.2)
        pg.shape(circle(x + 36, 206, 8), fill=PLATE)
        pg.text(x + 54, 201, 200, [t], 'Lab')
        pg.text(x + 28, 232, 222, [d], 'Nm')
    logo_card(pg, 54, 396, 300, 100)
    pg.text(384, 418, 520, [[('Mivelle, by Skarlen Montaño.', None)]], 'H2', name='Fundadora')
    pg.text(384, 456, 520, ['Fundadora y creadora de las piezas de la marca.'], 'Small')
    foot(pg, 5)
    return pg


def p_founder():
    pg = Page('Mensaje de la fundadora', IVORY)
    beads(pg, [(60, 70, 30, ROSE), (900, 490, 40, AMBER), (930, 440, 16, ROSE)], .4)
    pg.image(R(0, 0, 330, 540), 'p15.jpg', fx=.5, fy=.55, name='Foto fundadora')
    pg.text(390, 54, 420, ['Mensaje de la fundadora'], 'Script')
    sec(pg, 'MENSAJE DE LA FUNDADORA', 390)
    pg.text(390, 100, 520, [[('Hecho con ', None), ('cariño.', None, RED)]], 'H1', name='Titulo')
    pg.text(390, 170, 500, ['Mivelle empezó como algo mío: un proyecto personal, armado pieza por pieza. Hoy es una empresa, una tienda online, y cada cartera que sale de nuestras manos lleva ese mismo cuidado.',
                            'Mivelle nació en un rincón hermoso de República Dominicana y la creamos para que cada mujer eleve su estilo. Gracias por ser parte de este camino.'], 'Nm')
    pg.shape(P().M(390, 372).L(520, 372), stroke=PLATE, sw=1.4)
    pg.text(390, 386, 400, ['Skarlen Montaño'], 'ScriptL', color=RED)
    pg.text(390, 444, 400, ['FUNDADORA DE MIVELLE'], 'Lab')
    foot(pg, 6, x=390)
    return pg


def p_achievements():
    pg = Page('Logros y reconocimientos', IVORY)
    beads(pg, [(900, 50, 32, ROSE), (936, 100, 14, AMBER)], .4)
    pg.text(54, 40, 420, ['Lo que hemos logrado'], 'Script')
    sec(pg, 'LOGROS Y RECONOCIMIENTOS')
    pg.text(54, 86, 850, [[('Logros y ', None), ('reconocimientos.', None, RED)]], 'H1', name='Titulo')
    hitos = [('Empresa', 'De proyecto propio a empresa', 'Mivelle empezó como algo personal y hoy es una empresa que gira en torno a las carteras de cristal hechas a mano.'),
             ('Online', 'Tienda online', 'La marca opera como tienda online: sus clientes ven las piezas y piden por Instagram y WhatsApp.'),
             ('Ventas', 'Primeras ventas', 'Mivelle ya ha vendido varias de sus carteras y otras piezas.'),
             ('12 piezas', 'Colección propia', 'Doce piezas en catálogo, cada una con su color, su cadena dorada y la placa de la marca.')]
    for i, (big, t, d) in enumerate(hitos):
        x = 54 + (i % 2) * 290; y = 168 + (i // 2) * 168
        pg.shape(rrect(x, y, 276, 150, 30), fill=WHITE, a=.95)
        pg.shape(rrect(x, y, 276, 150, 30), stroke=PLATE, sw=1.2)
        pg.text(x + 26, y + 16, 230, [big], 'Big')
        pg.text(x + 26, y + 76, 230, [t.upper()], 'Lab')
        pg.text(x + 26, y + 92, 230, [d], 'Small')
    cap(pg, 668, 60, 210, 420, 'p11.jpg', fy=.55, name='Foto logros')
    foot(pg, 24)
    return pg


def p_release():
    pg = Page('Comunicado de prensa', IVORY)
    beads(pg, [(920, 40, 28, ROSE), (948, 86, 12, AMBER)], .4)
    pg.shape(R(0, 0, 250, 540), fill=DARK)
    sec(pg, 'COMUNICADO DE PRENSA', 34, 44, True)
    pg.text(34, 112, 190, ['PARA PUBLICACIÓN\nINMEDIATA'], 'Lab', color=IVORY)
    pg.text(34, 160, 190, ['República Dominicana, noviembre de 2026'], 'Small', color='#E7D5DD')
    pg.shape(P().M(34, 250).L(216, 250), stroke=PLATE, sw=.8, a=.7)
    pg.text(34, 266, 190, ['CONTACTO DE PRENSA'], 'Lab', color=PLATE)
    pg.text(34, 284, 190, ['Mivelle by Skarlen Montaño'], 'Nm', color=IVORY)
    pg.text(34, 332, 190, ['849-607-9595\n@mivelle.rd'], 'Body', color='#E7D5DD')
    pill(pg, 34, 396, 176, 28, 'ESCRIBIR POR WHATSAPP', PLATE, BROWN, link=('url', WAL), name='Boton WhatsApp')
    pg.text(290, 48, 620, [[('De proyecto propio a empresa: ', None), ('handbags de cristal hechas a mano en República Dominicana', None, RED)]], 'H2', name='Titulo')
    pg.text(290, 150, 300, ['Mivelle, una marca de handbags fundada por Skarlen Montaño, pasó de ser un proyecto propio a convertirse en una empresa: una tienda online que ya ha vendido varias de sus carteras y otras piezas. La marca nació en un rincón hermoso de República Dominicana con una idea clara: crear carteras que eleven el estilo de quien las lleva.',
                            'Mivelle se encuentra en Instagram como @mivelle.rd. Para entrevistas, fotografías o información de la colección, la marca atiende por WhatsApp en el 849-607-9595.'], 'Body')
    pg.text(616, 150, 290, ['Cada pieza está hecha a mano con cuentas de cristal y lleva cadena dorada y una placa con el nombre de la marca. La colección incluye bolsos con asa superior, clutches, minis y carteras de muñeca, en colores como rojo, rosa, azul cielo, ámbar, ciruela, amarillo y negro, además de una pieza en cristal transparente y Amorette, un modelo en forma de corazón.'], 'Body')
    pg.shape(rrect(290, 372, 616, 100, 22), fill=WHITE, a=.95)
    pg.shape(rrect(290, 372, 616, 100, 22), stroke=PLATE, sw=1.2)
    pg.text(314, 388, 300, ['ACERCA DE MIVELLE'], 'Lab')
    pg.text(314, 406, 570, ['Mivelle es una empresa dominicana, con tienda online, de handbags hechas a mano con cuentas de cristal. Crafted to elevate your style.'], 'Body')
    pg.text(314, 444, 300, ['###'], 'Lab')
    foot(pg, 26, x=290)
    return pg


def p_materials():
    pg = Page('Materiales para prensa', IVORY)
    beads(pg, [(900, 50, 32, ROSE), (936, 100, 14, AMBER)], .4)
    pg.text(54, 40, 420, ['Para periodistas y medios'], 'Script')
    sec(pg, 'MATERIALES PARA PRENSA')
    pg.text(54, 86, 850, [[('Materiales ', None), ('para prensa.', None, RED)]], 'H1', name='Titulo')
    logo_card(pg, 54, 160, 330, 150)
    pg.text(54, 322, 330, ['Logo oficial'], 'Nm')
    pg.text(54, 344, 330, ['Mivelle by Skarlen Montaño.'], 'Small')
    for i, f in enumerate(['p06.jpg', 'p12.jpg', 'p02.jpg', 'p14.jpg', 'p15.jpg', 'p09.jpg']):
        x = 420 + (i % 3) * 164; y = 160 + (i // 3) * 112
        pg.image(rrect(x, y, 152, 100, 18), f, fx=.5, fy=.55, stroke=WHITE, sw=3, name=f'Muestra {i + 1}')
    pg.text(420, 388, 490, ['Fotografías de la colección'], 'Nm')
    pg.text(420, 410, 490, ['Las 12 piezas del catálogo y las fotos de conjunto.'], 'Small')
    items = ['Logo oficial de la marca', 'Fotografías de las 12 piezas', 'Fotos de conjunto de la colección', 'Datos de prensa y comunicado (este documento)']
    for i, t in enumerate(items):
        pg.shape(circle(60, 380 + i * 22 + 5, 4), fill=PLATE)
        pg.text(72, 380 + i * 22, 320, [t], 'Body')
    pill(pg, 54, 474, 230, 28, 'SOLICITAR POR WHATSAPP', PLATE, BROWN, link=('url', 'https://wa.me/18496079595?text=Hola%20Mivelle%2C%20quiero%20solicitar%20los%20materiales%20de%20prensa.'), name='Boton materiales')
    pill(pg, 296, 474, 160, 28, 'VER EN INSTAGRAM', BROWN, IVORY, link=('url', IG), name='Boton Instagram')
    foot(pg, 27, x=480)
    return pg


def build_doc():
    pages = [p_cover(), p_toc(), p_bio(), p_essence(), p_mission(), p_founder(), p_gallery(), p_cat('I', 8), p_cat('II', 9)]
    pages += [piece_page(i) for i in range(12)]
    pages += [p_group(), p_palette(), p_achievements(), p_press(), p_release(), p_materials(), p_contact(), p_close()]
    assert len(pages) == TOTAL, len(pages)
    outline = [('Portada', 1, 0), ('Contenido', 2, 0)] + [(t, n, 0) for t, n in TOC] + [('Cierre', 29, 0)]
    for i, p in enumerate(PIECES):
        outline.append((f'Pieza {i + 1:02d} · {p[1].replace(chr(10), " ")}', P0 + i, 1))
    outline.sort(key=lambda o: o[1])
    return {'pages': pages, 'outline': outline}
