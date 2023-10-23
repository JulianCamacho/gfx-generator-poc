import math, sys
from PIL import Image

W, H = 640, 480
FILL = (0, 0, 0)

fb = None

def fixed_color(color):
    for c in color[:3]:
        c = abs(int(c * (1 << 8)))
        yield (c & 255) | (255 if (c & (1 << 8)) else 0)

def fixed(p):
    pos, color = p
    w = pos
    pos = tuple(int(c / pos[3] * (1 << 13)) for c in pos[:3])
    return (pos, tuple(fixed_color(color)))

def bounding(p0, p1, p2):
    minx = max(min(p0[0][0], p1[0][0], p2[0][0]), (-W // 2) << 4)
    maxx = min(max(p0[0][0], p1[0][0], p2[0][0]), (W // 2) << 4)
    miny = max(min(p0[0][1], p1[0][1], p2[0][1]), (-H // 2) << 4)
    maxy = min(max(p0[0][1], p1[0][1], p2[0][1]), (H // 2) << 4)
    return (minx, miny, maxx, maxy)

def edge_fn(p, q):
    p, q = p[0], q[0]

    # https://www.scratchapixel.com/lessons/3d-basic-rendering/rasterization-practical-implementation/rasterization-stage.html
    a, b = p[1] - q[1], -(p[0] - q[0])
    c = lambda x, y: (x - q[0]) * a + (y - q[1]) * b
    return c

def raster(p0, p1, p2, msaa=True):
    global fb

    minx, miny, maxx, maxy = bounding(p0, p1, p2)

    if msaa:
        samples = ((-5, 10), (11, 2), (-7, -4))
    else:
        samples = ((0, 0),)

    edge_a, edge_b, edge_c = edge_fn(p0, p1), edge_fn(p1, p2), edge_fn(p2, p0)
    for x in range(minx // 16 * 16, maxx + 16, 16):
        for y in range(miny // 16 * 16, maxy + 16, 16):
            count = 0

            for sx, sy in samples:
                ax = x + sx
                ay = y + sy
                if edge_a(ax, ay) >= 0 and edge_b(ax, ay) >= 0 and edge_c(ax, ay) >= 0:
                    count += 1

            if count > 0:
                yield (x >> 4, y >> 4, count if msaa else 3)

def translate(x, y, z):
    return ((1, 0, 0, x),
            (0, 1, 0, y),
            (0, 0, 1, z),
            (0, 0, 0, 1))

def scale(x, y, z):
    return ((x, 0, 0, 0),
            (0, y, 0, 0),
            (0, 0, z, 0),
            (0, 0, 0, 1))

def rotate(x, y, z, angle):
    mag = math.hypot(x, y, z)
    x /= mag
    y /= mag
    z /= mag

    angle = math.radians(angle)
    c, s = math.cos(angle), math.sin(angle)

    return ((x * x * (1 - c) + c,     x * y * (1 - c) - z * s, x * z * (1 - c) + y * s, 0),
            (y * x * (1 - c) + z * s, y * y * (1 - c) + c,     y * z * (1 - c) - x * s, 0),
            (x * z * (1 - c) - y * s, y * z * (1 - c) + x * s, z * z * (1 - c) + c,     0),
            (0,                       0,                       0,                       1))

def frustum(left, right, bottom, top, near, far):
    # https://docs.gl/gl3/glFrustum

    l, r, b, t, n, f = left, right, bottom, top, near, far
    return ((2 * n / (r - l), 0,               (r + l) / (r - l),  0),
            (0,               2 * n / (t - b), (t + b) / (t - b),  0),
            (0,               0,               -(f + n) / (f - n), -2 * f * n / (f - n)),
            (0,               0,               -1                , 0))

def mat_mat(a, b):
    n = lambda: range(len(a))
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in n()) for j in n()) for i in n())

def mat_vec(mat, vec):
    return tuple(sum(a * b for a, b in zip(r, vec)) for r in mat)

def backend(a, f, w):
    tri = (((-1.0, -1.0, 1, 1.0), (1.0, 0.0, 0.0, 0.0)),
           (( 1.0, -1.0, 1, 1.0), (0.0, 1.0, 0.0, 0.0)),
           (( 0.0,  1.0, 3, 1.0), (0.0, 0.0, 1.0, 0.0)))

    m = frustum(-w, w, -w, w, -5, 5)
    m = mat_mat(m, rotate(1, 0, 0, a))
    m = mat_mat(m, scale(f, f, f))

    tri = tuple((mat_vec(m, p), c) for p, c in tri)

    tri = tuple(fixed(p) for p in tri)
    for x, y, frac in raster(*tri):
        if -W // 2 <= x < W // 2 and -H // 2 <= y < H // 2:
            x += W // 2
            y = H // 2 - y - 1
            fb[y * W + x] = (255 * frac // 3, 255 * frac // 3, 255 * frac // 3)

imgs = []

def do_frame(a, f, w):
    global fb, imgs
    fb = [FILL] * W * H
    backend(a, f, w)

    image = Image.new('RGB', (W, H))
    image.putdata(fb)
    imgs.append(image)

a, f, w = int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])
for n in range(100):
    do_frame(n * a, f, w)

imgs[0].save('out.gif',
             save_all=True,
             append_images=imgs[1:],
             duration=100,
             loop=0)
