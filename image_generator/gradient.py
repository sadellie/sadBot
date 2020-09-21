"""
COPIED AND PASTED (i added only few lines) FROM https://stackoverflow.com/a/32532502 (Author: martineau)
"""

VIOLET = (46, 0, 107)
VIOLET2 = (60, 0, 89)
VIOLET3 = (0, 0, 0)
TOP = (22, 4, 20)
BOTTOM = (149, 41, 148)
WHITE = (255, 255, 255)

GREY = (25, 25, 25)
GREY_A = (25, 25, 25, 255)
ALPHA = (255, 255, 255, 128)

C1 = (143, 183, 194)
C2 = (193, 247, 251)
C3 = (197, 188, 189)
C4 = (195, 170, 195)
C5 = (195, 170, 195)
C6 = (25, 4, 23)


class Point(object):
    def __init__(self, x, y):
        self.x, self.y = x, y

    @staticmethod
    def from_point(other):
        return Point(other.x, other.y)


class Rect(object):
    def __init__(self, x2, y2, x1=0, y1=0):
        minx, maxx = (x1, x2) if x1 < x2 else (x2, x1)
        miny, maxy = (y1, y2) if y1 < y2 else (y2, y1)
        self.min = Point(minx, miny)
        self.max = Point(maxx, maxy)

    @staticmethod
    def from_points(p1, p2):
        return Rect(p1.x, p1.y, p2.x, p2.y)

    def __str__(self):
        return 'Rect({:d}, {:d}, {:d}, {:d})'.format(self.min.x, self.min.y,
                                                     self.max.x, self.max.x)

    width = property(lambda self: self.max.x - self.min.x)
    height = property(lambda self: self.max.y - self.min.y)


def gradient_color(minval, maxval, val, color_palette):
    max_index = len(color_palette) - 1
    delta = maxval - minval
    if delta == 0:
        delta = 1
    v = float(val - minval) / delta * max_index
    i1, i2 = int(v), min(int(v) + 1, max_index)

    try:
        (r1, g1, b1, a1), (r2, g2, b2, a2) = color_palette[i1], color_palette[i2]
        f = v - i1
        res = int(r1 + f * (r2 - r1)), int(g1 + f * (g2 - g1)), int(b1 + f * (b2 - b1)), int(a1 + f * (a2 - a1))
        return res
    except:
        pass
    (r1, g1, b1), (r2, g2, b2) = color_palette[i1], color_palette[i2]
    f = v - i1
    res = int(r1 + f * (r2 - r1)), int(g1 + f * (g2 - g1)), int(b1 + f * (b2 - b1))
    return res


def horz_gradient(draw, rect, color_func, color_palette):
    minval, maxval = 1, len(color_palette)
    delta = maxval - minval
    for x in range(rect.min.x, rect.max.x + 1):
        f = (x - rect.min.x) / float(rect.width)
        val = minval + f * delta
        color = color_func(minval, maxval, val, color_palette)
        draw.line([(x, rect.min.y), (x, rect.max.y)], fill=color)


def vert_gradient(draw, rect, color_func, color_palette):
    minval, maxval = 1, len(color_palette)
    delta = maxval - minval
    for y in range(rect.min.y, rect.max.y + 1):
        f = (y - rect.min.y) / float(rect.height)
        val = minval + f * delta
        color = color_func(minval, maxval, val, color_palette)
        draw.line([(rect.min.x, y), (rect.max.x, y)], fill=color)
