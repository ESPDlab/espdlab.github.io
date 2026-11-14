"""Draw the hero stills of the homepage (Korea from orbit, with the power grid from OpenStreetMap data).
usage: python tools/gen_art.py media herosite <folder with lines_kr.json, lines_kp.json, points.json> <ne_10m_admin_0_countries.geojson>
writes media/hero.jpg and media/hero-lit.jpg. See README.md, section "첫 화면의 전력망 그림".
The other modes (hero, illus, all) are left over from the design stage and are not used by the site."""
import math, os, random, sys
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

OUT = sys.argv[1]
WHAT = sys.argv[2] if len(sys.argv) > 2 else "all"
SS = 2
BG = (29, 29, 31)          # ink: same as the card surface, so the picture has no visible edge
WHITE = (245, 245, 247)
BLUE = (41, 151, 255)      # primary-on-dark
GREY = (134, 134, 139)
FONT = "C:/Windows/Fonts/seguisb.ttf"


def font(px):
    return ImageFont.truetype(FONT, int(px * SS))


def S(p):
    return (p[0] * SS, p[1] * SS)


def line(d, pts, col, w, cap=True):
    P = [S(p) for p in pts]
    d.line(P, fill=col, width=max(1, int(round(w * SS))), joint="curve")
    if cap and w >= 3:
        r = w * SS / 2
        for x, y in (P[0], P[-1]):
            d.ellipse((x - r, y - r, x + r, y + r), fill=col)


def dashed(d, pts, col, w, on=14, off=10):
    draw, left = True, on
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        L = math.hypot(x1 - x0, y1 - y0)
        pos = 0.0
        while L - pos > 1e-9:
            step = min(left, L - pos)
            if draw:
                a = (x0 + (x1 - x0) * pos / L, y0 + (y1 - y0) * pos / L)
                b = (x0 + (x1 - x0) * (pos + step) / L, y0 + (y1 - y0) * (pos + step) / L)
                line(d, [a, b], col, w, cap=False)
            pos += step
            left -= step
            if left <= 1e-9:
                draw = not draw
                left = on if draw else off


def dot(d, c, r, fill=None, outline=None, w=0):
    x, y = S(c)
    R = r * SS
    d.ellipse((x - R, y - R, x + R, y + R), fill=fill, outline=outline, width=int(w * SS))


def text(d, xy, s, px, col, anchor="la"):
    d.text(S(xy), s, font=font(px), fill=col, anchor=anchor)


def poly(d, pts, fill):
    d.polygon([S(p) for p in pts], fill=fill)


class Art:
    def __init__(self, w, h, bg=BG):
        self.w, self.h = w, h
        self.img = Image.new("RGB", (w * SS, h * SS), bg)

    def layer(self):
        im = Image.new("RGBA", self.img.size, (0, 0, 0, 0))
        return im, ImageDraw.Draw(im)

    def put(self, layer):
        self.img.paste(layer, (0, 0), layer)

    def glow(self, layer, radii=((5, 1.0), (20, 0.7))):
        black = Image.new("RGB", self.img.size, (0, 0, 0))
        black.paste(layer, (0, 0), layer)
        for r, gain in radii:
            b = black.filter(ImageFilter.GaussianBlur(r * SS))
            if gain != 1.0:
                b = b.point(lambda v, g=gain: min(255, int(v * g)))
            self.img = ImageChops.screen(self.img, b)
        self.put(layer)

    def save(self, name, **kw):
        out = self.img.resize((self.w, self.h), Image.LANCZOS)
        out.save(os.path.join(OUT, name), **kw)
        return out


# ---------------------------------------------------------------- research illustrations

def chirp(cx, cy, amp, sigma, f0, f1, span=3.0, n=500):
    pts = []
    for i in range(n + 1):
        t = -span + 2 * span * i / n
        u = i / n
        env = math.exp(-0.5 * t * t)
        phase = 2 * math.pi * (f0 * u + 0.5 * (f1 - f0) * u * u) * (2 * span)
        pts.append((cx + t * sigma, cy - amp * env * math.sin(phase)))
    return pts


def arrow(d, tip, direction, col, size=16, w=5):
    x, y = tip
    s = size * direction
    line(d, [(x - s, y - size * 0.8), (x, y), (x - s, y + size * 0.8)], col, w)


def dim(d, a, b, y, col, tick=14, w=3):
    line(d, [(a, y), (b, y)], col, w)
    line(d, [(a, y - tick), (a, y + tick)], col, w)
    line(d, [(b, y - tick), (b, y + tick)], col, w)


def illus_fault():
    A = Art(1200, 1200)
    L, d = A.layer()
    cy = 560
    # distance bracket
    dim(d, 210, 830, 190, GREY + (255,))
    text(d, (520, 172), "d", 44, WHITE + (255,), "mb")
    # cable: sheath + conductor, broken at the fault
    line(d, [(70, cy), (805, cy)], (74, 74, 79, 255), 30)
    line(d, [(855, cy), (1130, cy)], (74, 74, 79, 255), 30)
    line(d, [(70, cy), (805, cy)], (176, 176, 182, 255), 6)
    line(d, [(855, cy), (1130, cy)], (176, 176, 182, 255), 6)
    # sensor clamp
    d.rounded_rectangle((170 * SS, (cy - 62) * SS, 250 * SS, (cy + 62) * SS), radius=16 * SS, fill=BG + (255,), outline=WHITE + (255,), width=5 * SS)
    line(d, [(190, cy - 28), (230, cy - 28)], WHITE + (255,), 4)
    line(d, [(190, cy), (230, cy)], WHITE + (255,), 4)
    line(d, [(190, cy + 28), (230, cy + 28)], WHITE + (255,), 4)
    text(d, (210, cy + 104), "SENSOR", 24, GREY + (255,), "mm")
    text(d, (830, cy + 104), "FAULT", 24, GREY + (255,), "mm")
    # time trace axis
    line(d, [(110, 990), (1090, 990)], (90, 90, 95, 255), 3)
    dim(d, 250, 760, 1085, GREY + (255,))
    text(d, (505, 1068), "\u0394t", 40, WHITE + (255,), "mb")
    text(d, (1090, 1090), "d = v \u00b7 \u0394t / 2", 34, WHITE + (255,), "rm")
    text(d, (110, 80), "TIME\u2013FREQUENCY DOMAIN REFLECTOMETRY", 24, GREY + (255,), "lm")
    A.put(L)
    # light: fault rings, incident and reflected chirps, time trace
    G, g = A.layer()
    for r, a in ((34, 255), (66, 150), (102, 70)):
        dot(g, (830, cy), r, outline=BLUE + (a,), w=5)
    line(g, [(818, cy - 26), (838, cy - 8), (822, cy + 8), (842, cy + 26)], WHITE + (255,), 5)
    line(g, chirp(450, 380, 78, 58, 0.5, 1.5), BLUE + (255,), 6)
    arrow(g, (690, 380), 1, BLUE + (255,))
    line(g, chirp(560, 750, 40, 58, 1.5, 0.5), WHITE + (235,), 5)
    arrow(g, (330, 750), -1, WHITE + (235,))
    line(g, [(110, 990)] + chirp(250, 990, 70, 34, 0.5, 1.5) + [(650, 990)] + chirp(760, 990, 30, 34, 0.5, 1.5) + [(1090, 990)], BLUE + (255,), 5)
    A.glow(G)
    return A.save("illus_fault.png", optimize=True)


def arc_pts(c, r, a0, a1, n=200):
    return [(c[0] + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)), c[1] + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


def illus_health():
    A = Art(1200, 1200)
    L, d = A.layer()
    c = (600, 450)
    line(d, arc_pts(c, 250, 135, 405), (62, 62, 66, 255), 34)
    text(d, (600, 430), "83", 210, WHITE + (255,), "mm")
    text(d, (600, 580), "HEALTH INDEX", 28, GREY + (255,), "mm")
    text(d, (110, 80), "HEALTH MONITORING", 24, GREY + (255,), "lm")
    # cable strip in segments, two of them degraded
    x0, x1, y = 110, 1090, 990
    n = 14
    seg = (x1 - x0) / n
    bad = {8: 0.55, 9: 0.3}
    for i in range(n):
        a, b = x0 + i * seg + 6, x0 + (i + 1) * seg - 6
        if i in bad:
            d.rounded_rectangle((a * SS, (y - 17) * SS, b * SS, (y + 17) * SS), radius=17 * SS, outline=GREY + (255,), width=4 * SS)
    text(d, (x0, y + 62), "0", 24, GREY + (255,), "lm")
    text(d, (x1, y + 62), "L", 24, GREY + (255,), "rm")
    line(d, [(x0, 880), (x1, 880)], (70, 70, 75, 255), 2)
    A.put(L)
    G, g = A.layer()
    line(g, arc_pts(c, 250, 135, 135 + 270 * 0.83), BLUE + (255,), 34)
    for i in range(n):
        if i not in bad:
            a, b = x0 + i * seg + 6 + 17, x0 + (i + 1) * seg - 6 - 17
            line(g, [(a, y), (b, y)], BLUE + (255,), 34)
    # health profile along the cable, dipping over the degraded span
    prof = []
    for k in range(401):
        x = x0 + (x1 - x0) * k / 400
        u = (x - x0) / (x1 - x0)
        dip = 86 * math.exp(-((u - 0.655) / 0.07) ** 2)
        prof.append((x, 790 + dip + 5 * math.sin(u * 38) + 3 * math.sin(u * 91)))
    line(g, prof, WHITE + (240,), 5)
    A.glow(G)
    return A.save("illus_health.png", optimize=True)


def illus_rul():
    A = Art(1200, 1200)
    L, d = A.layer()
    ax = (60, 60, 64, 255)
    line(d, [(150, 190), (150, 990), (1090, 990)], ax, 3)
    dashed(d, [(150, 820), (1090, 820)], GREY + (255,), 3, 16, 12)
    text(d, (1090, 792), "END OF LIFE", 24, GREY + (255,), "rm")
    dashed(d, [(560, 190), (560, 990)], (90, 90, 95, 255), 3, 8, 10)
    text(d, (560, 1034), "NOW", 24, GREY + (255,), "mm")
    text(d, (110, 80), "REMAINING USEFUL LIFE", 24, GREY + (255,), "lm")
    text(d, (118, 190), "HEALTH", 22, GREY + (255,), "rm")
    text(d, (1090, 1034), "TIME", 22, GREY + (255,), "rm")
    # confidence band of the prediction
    up, lo = [], []
    for k in range(101):
        u = k / 100
        x = 560 + 470 * u
        y = 430 + 390 * (u * 470 / 370) ** 1.8
        hw = 10 + 78 * u
        up.append((x, y - hw))
        lo.append((x, min(985, y + hw)))
    poly(d, up + lo[::-1], BLUE + (46,))
    dim(d, 560, 930, 905, WHITE + (255,))
    text(d, (745, 890), "RUL", 40, WHITE + (255,), "mb")
    A.put(L)
    G, g = A.layer()
    rnd = random.Random(7)
    meas = []
    for k in range(42):
        x = 150 + 410 * k / 41
        meas.append((x, 300 + 130 * ((x - 150) / 410) ** 1.6 + rnd.uniform(-7, 7)))
    line(g, meas, WHITE + (255,), 6)
    for p in meas[::5]:
        dot(g, p, 9, fill=BG + (255,), outline=WHITE + (255,), w=4)
    pred = [(560 + 3.7 * k, 430 + 390 * (k / 100) ** 1.8) for k in range(0, 113)]
    dashed(g, pred, BLUE + (255,), 6, 20, 14)
    dot(g, (930, 820), 15, fill=BLUE + (255,))
    dot(g, (930, 820), 30, outline=BLUE + (150,), w=4)
    A.glow(G)
    return A.save("illus_rul.png", optimize=True)


def tower(d, x, base, h, col, w=4):
    top = base - h
    lf, rf, lt, rt = (x - 46, base), (x + 46, base), (x - 11, top), (x + 11, top)
    line(d, [lf, lt], col, w)
    line(d, [rf, rt], col, w)
    line(d, [lt, rt], col, w)
    n = 6
    for i in range(n):
        a, b = i / n, (i + 1) / n
        la = (lf[0] + (lt[0] - lf[0]) * a, base - h * a)
        rb = (rf[0] + (rt[0] - rf[0]) * b, base - h * b)
        ra = (rf[0] + (rt[0] - rf[0]) * a, base - h * a)
        lb = (lf[0] + (lt[0] - lf[0]) * b, base - h * b)
        line(d, [la, rb], col, 2.5, cap=False)
        line(d, [ra, lb], col, 2.5, cap=False)
    tips = []
    for frac, half in ((0.62, 104), (0.79, 86), (0.95, 66)):
        y = base - h * frac
        line(d, [(x - half, y), (x + half, y)], col, w)
        line(d, [(x - half, y), (x - 14, y - 26)], col, 2.5, cap=False)
        line(d, [(x + half, y), (x + 14, y - 26)], col, 2.5, cap=False)
        for sx in (-half, half):
            line(d, [(x + sx, y), (x + sx, y + 20)], col, 3)
        tips.append((x - half, y + 20, x + half, y + 20))
    return tips


def sag(a, b, s, n=80):
    return [(a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n + s * 4 * (i / n) * (1 - i / n)) for i in range(n + 1)]


def illus_dlr():
    A = Art(1200, 1200)
    L, d = A.layer()
    text(d, (110, 80), "DYNAMIC LINE RATING", 24, GREY + (255,), "lm")
    base = 640
    line(d, [(70, base), (1130, base)], (60, 60, 64, 255), 3)
    tl = tower(d, 300, base, 400, WHITE + (255,))
    tr = tower(d, 900, base, 400, WHITE + (255,))
    for (lx0, ly, lx1, _), (rx0, ry, rx1, _) in zip(tl, tr):
        line(d, sag((lx1, ly), (rx0, ry), 74), (176, 176, 182, 255), 3)
        line(d, sag((lx0 - 300, ly + 10), (lx0, ly), 40)[40:], (176, 176, 182, 255), 3)
        line(d, sag((rx1, ry), (rx1 + 300, ry + 10), 40)[:41], (176, 176, 182, 255), 3)
    # chart frame
    line(d, [(110, 1090), (1090, 1090)], (60, 60, 64, 255), 3)
    for k, lab in enumerate(("0", "6", "12", "18", "24")):
        x = 110 + 245 * k
        line(d, [(x, 1090), (x, 1102)], (60, 60, 64, 255), 3)
        text(d, (x, 1130), lab, 22, GREY + (255,), "mm")
    dashed(d, [(110, 985), (1090, 985)], GREY + (255,), 3, 16, 12)
    text(d, (1090, 1012), "STATIC", 22, GREY + (255,), "rm")
    curve = []
    for k in range(301):
        u = k / 300
        y = 905 - 62 * math.sin(2 * math.pi * (u - 0.08)) - 26 * math.sin(6 * math.pi * u + 1.0) - 12 * math.sin(14 * math.pi * u)
        curve.append((110 + 980 * u, min(y, 978)))
    poly(d, curve + [(1090, 985), (110, 985)], BLUE + (44,))
    text(d, (110, 742), "DYNAMIC", 22, BLUE + (255,), "lm")
    A.put(L)
    G, g = A.layer()
    line(g, curve, BLUE + (255,), 6)
    # sun
    sc = (170, 250)
    dot(g, sc, 34, outline=BLUE + (255,), w=6)
    for k in range(8):
        a = math.radians(45 * k)
        line(g, [(sc[0] + 54 * math.cos(a), sc[1] + 54 * math.sin(a)), (sc[0] + 74 * math.cos(a), sc[1] + 74 * math.sin(a))], BLUE + (255,), 6)
    # wind
    for y, x0, ln in ((330, 520, 190), (372, 470, 250), (414, 540, 160)):
        pts = [(x0 + ln * i / 60, y + 9 * math.sin(i / 60 * math.pi * 2)) for i in range(61)]
        line(g, pts, BLUE + (220,), 5)
        arrow(g, (x0 + ln + 6, y), 1, BLUE + (220,), 11, 5)
    A.glow(G)
    return A.save("illus_dlr.png", optimize=True)


def illus_forecast():
    A = Art(1200, 1200)
    L, d = A.layer()
    text(d, (110, 80), "TIME SERIES FORECASTING", 24, GREY + (255,), "lm")
    rnd = random.Random(3)

    def f(x):
        u = (x - 110) / 980
        return 400 - 80 * math.sin(2 * math.pi * u * 3.0) - 34 * math.sin(2 * math.pi * u * 7.2 + 0.7) - 60 * u

    hist = [(x, f(x) + rnd.uniform(-9, 9)) for x in range(110, 641, 6)]
    fut = [(x, f(x)) for x in range(640, 1091, 6)]
    hist[-1] = (640, f(640))
    up = [(x, y - (8 + 70 * (x - 640) / 450)) for x, y in fut]
    lo = [(x, y + (8 + 70 * (x - 640) / 450)) for x, y in fut]
    poly(d, up + lo[::-1], BLUE + (44,))
    dashed(d, [(640, 190), (640, 600)], (90, 90, 95, 255), 3, 8, 10)
    d.rounded_rectangle((392 * SS, 236 * SS, 640 * SS, 566 * SS), radius=18 * SS, outline=GREY + (255,), width=3 * SS)
    text(d, (516, 208), "INPUT WINDOW", 22, GREY + (255,), "mm")
    text(d, (865, 208), "FORECAST", 22, BLUE + (255,), "mm")
    # network
    layers = [(360, 4), (600, 5), (840, 3)]
    nodes = [[(x, 880 + (i - (n - 1) / 2) * 74) for i in range(n)] for x, n in layers]
    for a, b in zip(nodes, nodes[1:]):
        for p in a:
            for q in b:
                line(d, [p, q], (84, 84, 90, 255), 2, cap=False)
    line(d, [(516, 566), (516, 640), (360, 640), (360, nodes[0][0][1] - 40)], (84, 84, 90, 255), 3)
    line(d, [(840, nodes[2][0][1] - 40), (840, 640), (865, 640), (865, 520)], BLUE + (150,), 3)
    A.put(L)
    G, g = A.layer()
    line(g, hist, WHITE + (255,), 5)
    dashed(g, fut, BLUE + (255,), 6, 20, 14)
    for li, col in enumerate(nodes):
        for i, p in enumerate(col):
            lit = (li + i) % 2 == 0
            dot(g, p, 21, fill=(BLUE + (255,)) if lit else (BG + (255,)), outline=(BLUE if lit else WHITE) + (255,), w=5)
    A.glow(G, radii=((5, 0.9), (18, 0.55)))
    return A.save("illus_forecast.png", optimize=True)


# ---------------------------------------------------------------- hero: Korea from orbit

def unit(lat, lon):
    la, lo = math.radians(lat), math.radians(lon)
    return (math.cos(la) * math.cos(lo), math.cos(la) * math.sin(lo), math.sin(la))


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def dotp(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def norm(a):
    l = math.sqrt(dotp(a, a))
    return (a[0] / l, a[1] / l, a[2] / l)


class Cam:
    """Perspective camera in low orbit south of Korea, looking north past the peninsula to the horizon."""

    def __init__(self, latc, lonc, alt, latt, lont, F, cx, cy):
        self.up0 = unit(latc, lonc)
        self.C = tuple(v * (1 + alt) for v in self.up0)
        self.f = norm(sub(unit(latt, lont), self.C))
        self.r = norm(cross(self.f, self.up0))
        self.u = cross(self.r, self.f)
        self.F, self.cx, self.cy = F, cx, cy
        self.cosr = 1 / (1 + alt)
        self.rho = math.acos(self.cosr)

    def proj(self, lat, lon):
        P = unit(lat, lon)
        c = dotp(P, self.up0)
        if c < math.cos(self.rho - 0.002):          # behind the horizon: slide it onto the limb
            t = norm(sub(P, tuple(c * v for v in self.up0)))
            a = self.rho - 0.002
            P = tuple(math.cos(a) * self.up0[k] + math.sin(a) * t[k] for k in range(3))
        v = sub(P, self.C)
        z = max(dotp(v, self.f), 0.004)
        return (self.cx + self.F * dotp(v, self.r) / z, self.cy - self.F * dotp(v, self.u) / z)

    def visible(self, lat, lon):
        return dotp(unit(lat, lon), self.up0) >= math.cos(self.rho - 0.004)

    def limb(self, n=1440):
        sn = math.sin(self.rho)
        e1 = norm(cross(self.up0, (0, 0, 1)))
        e2 = cross(self.up0, e1)
        pts = []
        for i in range(n):
            a = 2 * math.pi * i / n
            P = tuple(self.cosr * self.up0[k] + sn * (math.cos(a) * e1[k] + math.sin(a) * e2[k]) for k in range(3))
            v = sub(P, self.C)
            z = dotp(v, self.f)
            if z > 0.02:
                x, y = self.cx + self.F * dotp(v, self.r) / z, self.cy - self.F * dotp(v, self.u) / z
                if -6000 < x < 9000:
                    pts.append((x, y))
        return sorted(pts)


def dense(pts, step=0.2, close=True):
    out = []
    seq = pts + [pts[0]] if close else pts
    for (a0, o0), (a1, o1) in zip(seq, seq[1:]):
        n = max(1, int(max(abs(a1 - a0), abs(o1 - o0)) / step))
        for i in range(n):
            out.append((a0 + (a1 - a0) * i / n, o0 + (o1 - o0) * i / n))
    if not close:
        out.append(pts[-1])
    return out


BORDER = [(40.1, 124.4), (40.82, 125.8), (41.15, 126.28), (41.78, 126.88), (41.4, 128.2), (42.0, 128.08), (42.22, 129.2),
          (42.43, 129.75), (42.95, 129.99), (42.55, 130.5), (42.3, 130.7)]
KOREA = [(39.92, 124.35), (39.6, 124.75), (39.3, 125.25), (38.75, 125.15), (38.4, 124.9), (38.1, 124.75), (37.75, 125.1),
         (37.95, 125.6), (37.75, 126.1), (37.6, 126.5), (37.3, 126.6), (37.0, 126.75), (36.95, 126.3), (36.75, 126.13),
         (36.4, 126.45), (36.0, 126.65), (35.6, 126.47), (35.3, 126.35), (34.95, 126.3), (34.7, 126.25), (34.35, 126.45),
         (34.3, 126.75), (34.5, 127.2), (34.7, 127.6), (34.75, 127.95), (34.85, 128.4), (34.85, 128.72), (35.08, 129.05),
         (35.45, 129.38), (36.0, 129.55), (36.1, 129.4), (36.7, 129.45), (37.1, 129.38), (37.6, 129.05), (38.0, 128.72),
         (38.6, 128.38), (39.0, 127.85), (39.25, 127.45), (39.75, 127.55), (39.95, 127.95), (40.1, 128.6), (40.65, 129.25),
         (41.3, 129.75), (41.8, 129.85), (42.25, 130.45)] + BORDER[::-1]
JEJU = [(33.38 + 0.17 * math.sin(a / 24 * 2 * math.pi), 126.55 + 0.42 * math.cos(a / 24 * 2 * math.pi)) for a in range(24)]
MAIN = [(24.5, 118.2), (26.0, 119.7), (27.5, 120.6), (28.8, 121.7), (30.0, 122.1), (30.9, 121.9), (31.7, 121.3), (32.5, 120.9),
        (33.6, 120.5), (34.6, 119.3), (35.1, 119.4), (36.0, 120.3), (36.8, 121.6), (37.4, 122.6), (37.55, 121.4), (37.8, 120.7),
        (37.15, 119.5), (37.7, 118.9), (38.2, 118.0), (39.0, 117.7), (39.2, 118.9), (39.9, 119.6), (40.7, 121.0), (40.9, 121.8),
        (40.3, 122.2), (39.5, 121.4), (38.8, 121.2), (39.2, 122.6), (39.8, 123.8), (39.92, 124.35)] + BORDER + [
        (42.6, 131.2), (43.1, 131.9), (42.8, 132.9), (43.3, 134.7), (44.5, 136.2), (46.0, 138.0), (48.0, 140.2), (51.0, 140.6),
        (53.0, 141.2), (56.0, 137.0), (58.0, 125.0), (56.0, 108.0), (24.5, 108.0)]
KYUSHU = [(33.9, 130.9), (33.6, 130.3), (33.2, 129.6), (32.8, 129.7), (32.6, 130.2), (32.1, 130.2), (31.3, 130.2), (31.0, 130.7),
          (31.4, 131.3), (32.0, 131.5), (32.8, 131.9), (33.3, 131.8), (33.7, 131.6)]
SHIKOKU = [(34.3, 133.9), (33.9, 132.7), (33.3, 132.4), (32.8, 132.9), (33.3, 134.2), (33.9, 134.7)]
HONSHU = [(34.0, 131.0), (34.0, 132.0), (34.3, 132.5), (34.4, 133.5), (34.6, 134.2), (34.6, 135.0), (34.3, 135.2), (33.5, 135.8),
          (34.3, 136.9), (34.6, 137.3), (34.6, 138.2), (35.0, 138.6), (34.6, 138.9), (35.3, 139.6), (35.0, 139.9), (35.7, 140.9),
          (37.0, 141.0), (38.3, 141.5), (39.5, 142.0), (41.4, 141.4), (40.9, 140.3), (40.0, 139.9), (38.5, 139.5), (37.8, 138.9),
          (37.0, 137.0), (37.5, 137.3), (36.9, 136.8), (36.2, 136.1), (35.7, 135.9), (35.6, 135.3), (35.6, 134.2), (35.5, 133.2),
          (35.4, 132.6), (34.9, 132.0), (34.4, 131.2)]
HOKKAIDO = [(41.5, 140.0), (42.9, 140.4), (43.3, 141.3), (45.4, 141.7), (44.3, 143.3), (43.9, 145.0), (43.0, 145.3), (42.9, 144.2),
            (42.0, 143.2), (42.5, 141.8), (42.3, 140.9), (41.8, 141.1)]

NODES = {
    "seoul": (37.56, 126.98, 5), "incheon": (37.45, 126.65, 2.5), "suwon": (37.27, 127.01, 2), "pyeongtaek": (36.99, 127.09, 1.5),
    "dangjin": (36.97, 126.62, 1.5), "taean": (36.90, 126.23, 1), "seosan": (36.78, 126.45, 1), "boryeong": (36.40, 126.49, 1),
    "cheonan": (36.81, 127.15, 1.5), "sejong": (36.50, 127.27, 1), "daejeon": (36.35, 127.38, 2), "cheongju": (36.64, 127.49, 1.5),
    "chungju": (36.99, 127.93, 1), "wonju": (37.34, 127.92, 1), "chuncheon": (37.88, 127.73, 1), "gapyeong": (37.83, 127.51, 1),
    "uijeongbu": (37.74, 127.05, 1.5), "paju": (37.76, 126.78, 1), "gangneung": (37.75, 128.88, 1), "donghae": (37.52, 129.11, 1),
    "samcheok": (37.30, 129.25, 1), "uljin": (37.09, 129.38, 1.5), "taebaek": (37.16, 128.99, 1), "yeongju": (36.81, 128.62, 1),
    "andong": (36.57, 128.73, 1), "sangju": (36.41, 128.16, 1), "gimcheon": (36.14, 128.11, 1), "gumi": (36.12, 128.34, 1.5),
    "daegu": (35.87, 128.60, 2.5), "pohang": (36.02, 129.36, 1.5), "wolsong": (35.71, 129.48, 1.5), "ulsan": (35.54, 129.31, 2),
    "kori": (35.32, 129.29, 1.5), "busan": (35.18, 129.08, 3), "gimhae": (35.23, 128.89, 1.5), "changwon": (35.23, 128.68, 1.5),
    "miryang": (35.50, 128.75, 1), "jinju": (35.18, 128.11, 1), "samcheonpo": (34.91, 128.11, 1), "hadong": (34.95, 127.82, 1),
    "gwangyang": (34.94, 127.70, 1.5), "yeosu": (34.76, 127.66, 1), "suncheon": (34.95, 127.49, 1), "goheung": (34.61, 127.28, 1),
    "gwangju": (35.16, 126.85, 2), "naju": (35.02, 126.71, 1), "mokpo": (34.81, 126.39, 1), "haenam": (34.57, 126.60, 1),
    "jindo": (34.49, 126.26, 1), "hanbit": (35.41, 126.42, 1.5), "jeongeup": (35.57, 126.86, 1), "gunsan": (35.97, 126.74, 1),
    "iksan": (35.95, 126.96, 1), "jeonju": (35.82, 127.15, 1.5), "namwon": (35.41, 127.39, 1), "geochang": (35.69, 127.91, 1),
    "muju": (36.01, 127.66, 1), "yeongdong": (36.17, 127.78, 1), "jeju": (33.50, 126.53, 1.5), "seogwipo": (33.25, 126.56, 1),
    "hallim": (33.41, 126.27, 1), "seongsan": (33.44, 126.91, 1),
    "pyongyang": (39.03, 125.75, 1), "nampo": (38.74, 125.4, 0.6), "sinuiju": (40.1, 124.4, 0.6), "wonsan": (39.15, 127.44, 0.6),
    "hamhung": (39.92, 127.54, 0.7), "chongjin": (41.78, 129.78, 0.6), "kaesong": (37.97, 126.55, 0.5), "kimchaek": (40.67, 129.2, 0.5),
}
EDGES = ("seoul-incheon seoul-suwon seoul-uijeongbu uijeongbu-paju paju-incheon seoul-gapyeong gapyeong-chuncheon suwon-pyeongtaek "
         "pyeongtaek-dangjin dangjin-taean dangjin-seosan seosan-taean seosan-boryeong pyeongtaek-cheonan cheonan-sejong sejong-daejeon "
         "cheonan-cheongju cheongju-daejeon cheongju-chungju chungju-wonju wonju-chuncheon wonju-seoul wonju-gangneung gangneung-donghae "
         "donghae-samcheok samcheok-uljin uljin-taebaek taebaek-yeongju yeongju-andong chungju-yeongju andong-sangju sangju-gimcheon "
         "gimcheon-gumi gumi-daegu daejeon-yeongdong yeongdong-gimcheon daegu-pohang pohang-wolsong wolsong-ulsan ulsan-kori kori-busan "
         "busan-gimhae gimhae-changwon changwon-miryang miryang-daegu miryang-ulsan changwon-jinju jinju-samcheonpo jinju-hadong "
         "hadong-gwangyang gwangyang-yeosu gwangyang-suncheon suncheon-goheung suncheon-gwangju gwangju-naju naju-mokpo mokpo-haenam "
         "haenam-jindo gwangju-hanbit hanbit-jeongeup jeongeup-gwangju jeongeup-jeonju jeonju-iksan iksan-gunsan gunsan-boryeong "
         "jeonju-daejeon jeonju-namwon namwon-suncheon namwon-geochang geochang-daegu geochang-jinju daejeon-muju muju-geochang "
         "uljin-pohang andong-daegu andong-pohang suwon-cheonan incheon-dangjin taebaek-gangneung "
         "jeju-hallim hallim-seogwipo seogwipo-seongsan seongsan-jeju").split()
BACKBONE = "dangjin-suwon uljin-taebaek taebaek-wonju wonju-gapyeong suwon-chungju daejeon-daegu daegu-busan cheonan-daejeon".split()
HVDC = "haenam-jeju jindo-hallim uljin-gapyeong".split()
NORTH = "pyongyang-nampo pyongyang-sinuiju pyongyang-wonsan wonsan-hamhung hamhung-kimchaek kimchaek-chongjin pyongyang-kaesong".split()


def load_osm(d):
    """Real grid from OpenStreetMap (Overpass JSON in folder d): transmission lines by voltage class, substations and plants as dots."""
    import json

    def volt(tags):
        vs = [int(v) for v in (tags.get("voltage") or "").replace(",", ";").split(";") if v.strip().isdigit()]
        return max(vs) if vs else 0

    lines, dots = [], []
    for n in ("lines_kr.json", "lines_kp.json"):
        f = os.path.join(d, n)
        if not os.path.exists(f) or open(f, "rb").read(1) != b"{":
            continue
        for e in json.load(open(f, encoding="utf-8"))["elements"]:
            g = e.get("geometry") or []
            if len(g) < 2:
                continue
            v = volt(e["tags"])   # class: 0 unknown, 1 154 kV, 2 345 kV, 3 765 kV, 4 HVDC
            cls = 4 if e["tags"].get("frequency") == "0" else 3 if v >= 700000 else 2 if v >= 300000 else 1 if v >= 100000 else 0
            lines.append((cls, [(p["lat"], p["lon"]) for p in g]))
    for e in json.load(open(os.path.join(d, "points.json"), encoding="utf-8"))["elements"]:
        t, c = e["tags"], e.get("center") or e
        if t.get("power") == "substation":
            if t.get("substation") == "traction":
                continue
            v = volt(t)
            r = 2.4 if v >= 700000 else 1.9 if v >= 300000 else 1.2 if v >= 100000 else 0.8
        else:
            src = t.get("plant:source") or ""
            r = 0.6 if src in ("solar", "") else 2.6 if src in ("nuclear", "coal") else 1.6
        dots.append((c["lat"], c["lon"], r))
    lines.sort(key=lambda l: l[0])
    return {"lines": lines, "dots": dots}


def load_land(path):
    """Exterior rings as (lat, lon) lists: Korea (south and north) apart from the other land in view."""
    import json
    korea, other = [], []
    for f in json.load(open(path, encoding="utf-8"))["features"]:
        g = f["geometry"]
        for poly in (g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]):
            ring = [(la, lo) for lo, la in poly[0]]
            if max(la for la, lo in ring) < 15 or min(la for la, lo in ring) > 62 or max(lo for la, lo in ring) < 95 or min(lo for la, lo in ring) > 155:
                continue
            (korea if f["properties"].get("ADM0_A3") in ("KOR", "PRK") else other).append(ring)
    return {"korea": korea, "other": other}


def hero(params, name, W=2400, H=1030, G=1.0, real=None):   # G: stroke/dot scale for tighter framings; real: load_osm() result
    cam = Cam(*params)
    rnd = random.Random(11)
    big = (W * SS, H * SS)

    def P(lat, lon):
        x, y = cam.proj(lat, lon)
        return (x * SS, y * SS)

    # space
    space = Image.new("RGB", big, (2, 3, 6))
    sd = ImageDraw.Draw(space)
    for _ in range(1500):
        x, y = rnd.uniform(0, big[0]), rnd.uniform(0, big[1])
        b = int(40 + 215 * rnd.random() ** 3)
        r = rnd.choice((1, 1, 1, 1.4, 1.4, 2.2)) * SS / 2
        sd.ellipse((x - r, y - r, x + r, y + r), fill=(b, b, min(255, b + 18)))
    space = ImageChops.screen(space, space.filter(ImageFilter.GaussianBlur(2 * SS)))

    # globe mask from the horizon arc
    arc = [(x * SS, y * SS) for x, y in cam.limb()]
    mask = Image.new("L", big, 0)
    ImageDraw.Draw(mask).polygon(arc + [(arc[-1][0], 40000), (arc[0][0], 40000)], fill=255)

    globe = Image.new("RGB", big, (5, 8, 15))
    gd = ImageDraw.Draw(globe, "RGBA")
    kmask = None
    if real and real.get("land"):
        for ring in real["land"]["other"]:
            gd.polygon([P(a, o) for a, o in ring], fill=(12, 17, 27))
        kmask = Image.new("L", big, 0)
        kd = ImageDraw.Draw(kmask)
        for ring in real["land"]["korea"]:
            kd.polygon([P(a, o) for a, o in ring], fill=255)
        globe.paste((17, 25, 40), (0, 0), kmask)
    else:
        for land, col in ((MAIN, (12, 17, 27)), (HONSHU, (12, 17, 27)), (KYUSHU, (12, 17, 27)), (SHIKOKU, (12, 17, 27)),
                          (HOKKAIDO, (12, 17, 27)), (KOREA, (17, 25, 40)), (JEJU, (17, 25, 40))):
            gd.polygon([P(a, o) for a, o in dense(land)], fill=col)
    # graticule
    for lat in range(24, 60, 2):
        pts = [P(lat, lon / 4) for lon in range(100 * 4, 150 * 4) if cam.visible(lat, lon / 4)]
        if len(pts) > 1:
            gd.line(pts, fill=(120, 170, 255, 16), width=SS)
    for lon in range(100, 150, 2):
        pts = [P(lat / 4, lon) for lat in range(20 * 4, 60 * 4) if cam.visible(lat / 4, lon)]
        if len(pts) > 1:
            gd.line(pts, fill=(120, 170, 255, 16), width=SS)
    if kmask:   # outline of the whole peninsula and its islands: the rim of the mask
        rim_k = ImageChops.subtract(kmask.filter(ImageFilter.MaxFilter(2 * SS + 1)), kmask).point(lambda v: v * 80 // 255)
        globe.paste((90, 160, 255), (0, 0), rim_k)
    else:
        for land in (KOREA, JEJU):
            pts = [P(a, o) for a, o in dense(land)]
            gd.line(pts + [pts[0]], fill=(90, 160, 255, 70), width=int(1.5 * SS))

    # grid geometry, shared by the resting layer and the lit layer
    def path(e):
        a, b = e.split("-")
        (la0, lo0, _), (la1, lo1, _) = NODES[a], NODES[b]
        j = rnd.uniform(-0.07, 0.07)
        mid = ((la0 + la1) / 2 + j * (lo1 - lo0), (lo0 + lo1) / 2 - j * (la1 - la0))
        return dense([(la0, lo0), mid, (la1, lo1)], 0.05, close=False)

    lines = [(path(e), 1.6) for e in EDGES] + [(path(e), 2.6) for e in BACKBONE]
    hv = [path(e) for e in HVDC]
    north = [path(e) for e in NORTH]
    subs = []
    for pts, _ in lines:
        for _ in range(2):
            subs.append(pts[rnd.randrange(len(pts))])
    spurs = []
    for name_, (la, lo, wgt) in NODES.items():
        for _ in range(int(3 * wgt)):
            q = (la + rnd.gauss(0, 0.16), lo + rnd.gauss(0, 0.2))
            spurs.append(dense([(la, lo), q], 0.05, close=False))
            subs.append(q)

    def draw_real(d, lit):
        k = (1.25 if lit else 1.0) * G
        col = (190, 226, 255) if lit else (41, 151, 255)
        for cls, pts in real["lines"]:
            q = [P(a, o) for a, o in pts]
            if cls == 4:    # HVDC links: brighter
                d.line(q, fill=(255, 255, 255, 255) if lit else (120, 195, 255, 210), width=max(1, int(round(1.5 * k * SS))), joint="curve")
            else:
                d.line(q, fill=col + (((150, 185, 230, 255) if lit else (75, 100, 135, 165))[cls],), width=max(1, int(round((0.8, 1.0, 1.6, 2.4)[cls] * k * SS))), joint="curve")
        for a, o, r in real["dots"]:
            x, y = P(a, o)
            rr = r * k * SS
            d.ellipse((x - rr, y - rr, x + rr, y + rr), fill=(255, 255, 255, 255) if lit else (150, 205, 255, 150 if r < 1 else 215))

    def draw_grid(d, lit):
        if real:
            return draw_real(d, lit)
        c_line = (190, 226, 255, 255) if lit else (41, 151, 255, 135)
        c_node = (255, 255, 255, 255) if lit else (150, 205, 255, 225)
        k = (1.25 if lit else 1.0) * G
        for pts in north:
            d.line([P(a, o) for a, o in pts], fill=c_line[:3] + (255 if lit else 70,), width=int(1.4 * k * SS))
        for pts in spurs:
            d.line([P(a, o) for a, o in pts], fill=c_line[:3] + (230 if lit else 90,), width=int(1.0 * k * SS))
        for pts, w in lines:
            d.line([P(a, o) for a, o in pts], fill=c_line, width=int(w * k * SS), joint="curve")
        for pts in hv:
            q = [P(a, o) for a, o in pts]
            for i in range(0, len(q) - 1, 2):
                d.line(q[i:i + 2], fill=(255, 255, 255, 255) if lit else (170, 215, 255, 230), width=int(2.4 * k * SS))
        for a, o in subs:
            x, y = P(a, o)
            r = 1.7 * k * SS
            d.ellipse((x - r, y - r, x + r, y + r), fill=c_node[:3] + (255 if lit else 170,))
        for name_, (la, lo, wgt) in NODES.items():
            x, y = P(la, lo)
            r = (2.6 + 1.1 * math.sqrt(wgt)) * k * SS
            d.ellipse((x - r, y - r, x + r, y + r), fill=c_node)

    # resting state: grid and facilities visible, softly lit
    rest = Image.new("RGBA", big, (0, 0, 0, 0))
    rd = ImageDraw.Draw(rest)
    for name_, (la, lo, wgt) in NODES.items():      # city-light speckle
        for _ in range(int(55 * wgt * G * G)):
            x, y = P(la + rnd.gauss(0, 0.085 * math.sqrt(wgt)), lo + rnd.gauss(0, 0.105 * math.sqrt(wgt)))
            r = rnd.choice((0.8, 0.8, 1.2)) * SS * G
            rd.ellipse((x - r, y - r, x + r, y + r), fill=(150, 195, 255, rnd.randint(40, 120)))
    draw_grid(rd, False)
    black = Image.new("RGB", big, (0, 0, 0))
    black.paste(rest, (0, 0), rest)
    globe = ImageChops.screen(globe, black.filter(ImageFilter.GaussianBlur(7 * SS)).point(lambda v: min(255, int(v * 1.05))))
    globe.paste(rest, (0, 0), rest)

    def finish(g):
        out = Image.composite(g, space, mask)
        # atmosphere along the horizon
        rim = Image.new("RGB", big, (0, 0, 0))
        ImageDraw.Draw(rim).line(arc, fill=(120, 190, 255), width=4 * SS)
        out = ImageChops.screen(out, rim.filter(ImageFilter.GaussianBlur(3 * SS)))
        out = ImageChops.screen(out, rim.filter(ImageFilter.GaussianBlur(16 * SS)).point(lambda v: min(255, int(v * 3.2))))
        haze = rim.filter(ImageFilter.GaussianBlur(70 * SS)).point(lambda v: min(255, int(v * 7)))
        return ImageChops.screen(out, ImageChops.multiply(haze, Image.merge("RGB", (mask, mask, mask))).point(lambda v: v // 2))

    lit = Image.new("RGB", big, (0, 0, 0))
    draw_grid(ImageDraw.Draw(lit, "RGBA"), True)
    bloom = ImageChops.add(lit, lit.filter(ImageFilter.GaussianBlur(4 * SS)).point(lambda v: min(255, int(v * (0.45 if real else 0.9)))))
    bloom = ImageChops.add(bloom, lit.filter(ImageFilter.GaussianBlur(16 * SS)).point(lambda v: min(255, int(v * (0.3 if real else 1.1)))))
    if real:    # the site's pair: a resting picture and a fully lit one; the page shows the lit one only around the pointer
        halo = lit.filter(ImageFilter.GaussianBlur(60 * SS)).point(lambda v: min(255, int(v * 0.9)))
        for g, n in ((globe, name), (ImageChops.add(ImageChops.add(globe, halo), bloom), name.replace(".jpg", "-lit.jpg"))):
            finish(g).resize((W, H), Image.LANCZOS).save(os.path.join(OUT, n), quality=88)
        return None

    # hover state: facilities near the pointer light up, fading with distance
    cur = cam.proj(36.15, 128.0)
    R = 215 * G * 1.1
    fall =Image.radial_gradient("L").point(lambda v: int(255 * math.exp(-((v / 255) * 2.1) ** 2)))
    fall = fall.resize((int(2 * R * SS), int(2 * R * SS)), Image.LANCZOS)
    m2 = Image.new("L", big, 0)
    m2.paste(fall, (int((cur[0] - R) * SS), int((cur[1] - R) * SS)))
    halo = Image.new("RGB", big, (20, 60, 120))
    globe = ImageChops.add(globe, ImageChops.multiply(halo, Image.merge("RGB", (m2, m2, m2))).point(lambda v: v // 3))
    globe = ImageChops.add(globe, ImageChops.multiply(bloom, Image.merge("RGB", (m2, m2, m2))))

    out = finish(globe)

    # pointer and the radius it lights
    od = ImageDraw.Draw(out, "RGBA")
    cx, cy = cur[0] * SS, cur[1] * SS
    rr = R * 0.62 * SS
    for i in range(72):
        if i % 2 == 0:
            a0, a1 = math.radians(i * 5), math.radians(i * 5 + 5)
            od.line([(cx + rr * math.cos(a0), cy + rr * math.sin(a0)), (cx + rr * math.cos(a1), cy + rr * math.sin(a1))],
                    fill=(255, 255, 255, 110), width=int(1.5 * SS))
    k = 2.3 * SS
    shape = [(0, 0), (0, 17), (4.6, 13), (7.6, 20), (10.4, 18.8), (7.4, 12), (13, 12)]
    od.polygon([(cx + x * k, cy + y * k) for x, y in shape], fill=(255, 255, 255, 255), outline=(10, 10, 12, 255))
    od.line([(cx + x * k, cy + y * k) for x, y in shape + [shape[0]]], fill=(10, 10, 12, 255), width=int(1.6 * SS))
    final = out.resize((W, H), Image.LANCZOS)
    final.save(os.path.join(OUT, name), quality=90)
    return final


os.makedirs(OUT, exist_ok=True)
if WHAT in ("illus", "all"):
    ims = [illus_fault(), illus_health(), illus_rul(), illus_dlr(), illus_forecast()]
    sheet = Image.new("RGB", (1500, 1000), (120, 120, 120))
    for i, im in enumerate(ims):
        sheet.paste(im.resize((496, 496), Image.LANCZOS), (2 + 500 * (i % 3), 2 + 500 * (i // 3)))
    sheet.save(os.path.join(OUT, "_sheet_illus.png"))
if WHAT in ("hero", "all"):
    a = hero((32.9, 127.7, 0.075, 36.3, 127.8, 830.0, 1200.0, 668.0), "hero_grid.jpg")
    a.resize((1200, 515), Image.LANCZOS).save(os.path.join(OUT, "_preview_hero.jpg"), quality=85)
if WHAT == "hero16":   # full-bleed 16:9 hero: Korea larger and right of centre, room for text on the left
    a = hero((32.9, 127.7, 0.075, 36.3, 127.8, 1240.0, 1850.0, 855.0), "hero_grid_wide.jpg", 2560, 1440, 1.3)
    a.resize((1280, 720), Image.LANCZOS).save(os.path.join(OUT, "_preview_hero16.jpg"), quality=80)
if WHAT == "herosite":   # the site's hero pair: grid from OpenStreetMap (argv[3]: folder with the Overpass JSON), land from Natural Earth (argv[4])
    cam_site = (31.8, 127.7, 0.08, 35.9, 127.8, 1400.0, 1850.0, 760.0)   # Jeju and its HVDC links stay in frame
    real = load_osm(sys.argv[3])
    real["land"] = load_land(sys.argv[4])
    hero(cam_site, "hero.jpg", 2560, 1440, 1.3, real=real)
    for n in ("hero.jpg", "hero-lit.jpg"):
        Image.open(os.path.join(OUT, n)).resize((1280, 720), Image.LANCZOS).save(os.path.join(sys.argv[3], "_preview_" + n), quality=80)
