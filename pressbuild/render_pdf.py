# -*- coding: utf-8 -*-
import os
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from PIL import Image
import kit
from kit import *

for key, fn in FONT_FILES.items():
    pdfmetrics.registerFont(TTFont('MV-' + key, f'{FONTS}/{fn}'))


def sw(text, font, size, tracking=0):
    return pdfmetrics.stringWidth(text, 'MV-' + font, size) + tracking / 1000.0 * size * len(text)


def hexrgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))


_img_cache = {}
def img_size(f):
    if f not in _img_cache:
        _img_cache[f] = Image.open(f'{LINKS}/{f}').size
    return _img_cache[f]


_readers = {}
def _reader(f):
    if f not in _readers:
        _readers[f] = ImageReader(f'{LINKS}/{f}')
    return _readers[f]


def place_image(item):
    """Devuelve (x, y, w, h) de la imagen en coordenadas de página."""
    x0, y0, x1, y1 = item.path.anchors_bbox()
    fw, fh = x1 - x0, y1 - y0
    iw, ih = img_size(item.file)
    if getattr(item, 'fit', 'cover') == 'contain':
        s = min(fw / iw, fh / ih)
        w, h = iw * s, ih * s
        return x0 + (fw - w) / 2, y0 + (fh - h) / 2, w, h
    s = max(fw / iw, fh / ih) * item.zoom
    w, h = iw * s, ih * s
    ox = x0 + fw / 2 - item.fx * w
    oy = y0 + fh / 2 - item.fy * h
    ox = min(x0, max(x1 - w, ox))
    oy = min(y0, max(y1 - h, oy))
    return ox, oy, w, h


WRAP_STYLES = {'Body', 'Small', 'Nm', 'H2', 'Cuerpo', 'Cuerpo_S', 'Lema', 'Cita', 'Cifra_Label'}


def wrap_line(line, font, size, trk, width):
    toks = []
    for t, f, c in line:
        parts = t.split(' ')
        for i, w in enumerate(parts):
            if w == '' and i > 0:
                continue
            toks.append([w + (' ' if i < len(parts) - 1 else ''), f, c])
    # fusiona tokens sin espacio final con el siguiente (palabras partidas por runs)
    lines, cur, cw = [], [], 0.0
    for tk in toks:
        wd = sw(tk[0].rstrip(' '), tk[1] or font, size, trk)
        full = sw(tk[0], tk[1] or font, size, trk)
        if cur and cw + wd > width and tk[0].strip() != '':
            lines.append(cur); cur, cw = [], 0.0
        cur.append((tk[0], tk[1], tk[2])); cw += full
    if cur: lines.append(cur)
    # limpia espacios finales
    out = []
    for ln in lines:
        ln = [(t, f, c) for t, f, c in ln]
        if ln:
            t, f, c = ln[-1]; ln[-1] = (t.rstrip(' '), f, c)
        out.append(ln)
    return out


def text_layout(item):
    """Líneas por párrafo y altura total."""
    fnt, size, lead, col, trk, al = STYLES[item.style]
    paras = norm_paras(item.paras)
    out = []
    total = 0.0
    for i, runs in enumerate(paras):
        lines = split_lines(runs)
        if item.style in WRAP_STYLES:
            wl = []
            for ln in lines:
                wl.extend(wrap_line(ln, fnt, size, trk, item.w))
            lines = wl
        total += (item.space if i > 0 else 0) + lead * len(lines)
        out.append(lines)
    return out, total


def line_width(line, style_font, size, trk):
    w = 0
    for t, f, c in line:
        w += sw(t, f or style_font, size, trk)
    return w


def text_height(item):
    return text_layout(item)[1]


def draw_path(c, path, H_):
    p = c.beginPath()
    for op in path.ops:
        if op[0] == 'M': p.moveTo(op[1], H_ - op[2])
        elif op[0] == 'L': p.lineTo(op[1], H_ - op[2])
        elif op[0] == 'C': p.curveTo(op[1], H_ - op[2], op[3], H_ - op[4], op[5], H_ - op[6])
        elif op[0] == 'Z': p.close()
    return p


def render(doc, out, title, author, subject, keywords):
    c = canvas.Canvas(out, pagesize=(W, H), pageCompression=1, initialFontName='MV-sans', initialFontSize=10)
    c.setTitle(title); c.setAuthor(author); c.setSubject(subject); c.setKeywords(keywords)
    c.setCreator('Mivelle · Press Kit')
    warnings = []
    for pi, page in enumerate(doc['pages'], start=1):
        c.bookmarkPage(f'p{pi}', fit='Fit')
        c.setFillColorRGB(*hexrgb(page.bg)); c.rect(0, 0, W, H, stroke=0, fill=1)
        links = []
        for it in page.items:
            if getattr(it, 'only', None) == 'idml':
                continue
            if it.kind == 'shape':
                c.saveState()
                c.setFillAlpha(it.a); c.setStrokeAlpha(it.a)
                if it.fill: c.setFillColorRGB(*hexrgb(it.fill))
                if it.stroke:
                    c.setStrokeColorRGB(*hexrgb(it.stroke)); c.setLineWidth(it.sw); c.setLineCap(1); c.setLineJoin(1)
                p = draw_path(c, it.path, H)
                c.drawPath(p, stroke=1 if it.stroke else 0, fill=1 if it.fill else 0)
                c.restoreState()
                bb = it.path.bbox()
            elif it.kind == 'image':
                c.saveState()
                c.setFillAlpha(it.a)
                p = draw_path(c, it.path, H)
                c.clipPath(p, stroke=0, fill=0)
                x, y, w, h = place_image(it)
                c.drawImage(_reader(it.file), x, H - y - h, w, h, mask='auto')
                c.restoreState()
                if it.stroke and it.sw:
                    c.saveState(); c.setStrokeColorRGB(*hexrgb(it.stroke)); c.setLineWidth(it.sw); c.setLineJoin(1)
                    c.drawPath(draw_path(c, it.path, H), stroke=1, fill=0); c.restoreState()
                bb = it.path.bbox()
            else:
                fnt, size, lead, col, trk, al = STYLES[it.style]
                if it.color: col = it.color
                al = it.align or al
                lines_by_para, total = text_layout(it)
                y = it.y
                maxw = 0
                for pi2, lines in enumerate(lines_by_para):
                    if pi2 > 0: y += it.space
                    for line in lines:
                        y += lead
                        lw = line_width(line, fnt, size, trk)
                        maxw = max(maxw, lw)
                        if lw > it.w + 0.5:
                            warnings.append(f'p{pi} texto desborda ({lw:.0f}>{it.w:.0f}): {"".join(t for t,_,_ in line)[:50]}')
                        x = it.x if al == 'L' else (it.x + (it.w - lw) / 2 if al == 'C' else it.x + it.w - lw)
                        for t, f, cc in line:
                            ff = f or fnt
                            c.setFillColorRGB(*hexrgb(cc or col))
                            t_obj = c.beginText()
                            t_obj.setTextOrigin(x, H - y)
                            t_obj.setFont('MV-' + ff, size)
                            t_obj.setCharSpace(trk / 1000.0 * size)
                            t_obj.textOut(t)
                            c.drawText(t_obj)
                            x += sw(t, ff, size, trk)
                it.h_actual = total
                bb = (it.x, it.y, it.x + it.w, it.y + (it.h or total))
            lk = getattr(it, 'link', None)
            if lk:
                links.append((bb, lk))
        for (x0, y0, x1, y1), lk in links:
            rect_ = (x0, H - y1, x1, H - y0)
            if lk[0] == 'url':
                c.linkURL(lk[1], rect_, relative=0, thickness=0)
            else:
                c.linkRect('', f'p{lk[1]}', rect_, relative=0, thickness=0, Border='[0 0 0]')
        c.showPage()
    for (t, pg, lvl) in doc.get('outline', []):
        c.addOutlineEntry(t, f'p{pg}', level=lvl, closed=False)
    c.save()
    return warnings
