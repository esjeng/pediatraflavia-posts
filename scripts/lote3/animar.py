"""Anima o avatar ilustrado da Dra. Flávia (PNG transparente enviado pelo Edilson).
Movimentos sutis: respiração/balanço, piscadas e balanço dos cabelos. Loop de 6 s a 30 fps."""
import math, subprocess, shutil, sys
from pathlib import Path
import numpy as np, cv2

FPS, T = 30, 6
N = FPS * T
SRC = cv2.imread('src/avatar.png', cv2.IMREAD_UNCHANGED)  # BGRA
H, W = SRC.shape[:2]
OUT = Path('out'); OUT.mkdir(exist_ok=True)

# ---------- máscara do cabelo (peso do balanço) ----------
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
alpha = SRC[..., 3].astype(np.float32) / 255
b, g, r = [SRC[..., i].astype(np.float32) for i in range(3)]
lum = 0.299 * r + 0.587 * g + 0.114 * b
sat = (np.max(SRC[..., :3], 2).astype(np.float32) - np.min(SRC[..., :3], 2)) / 255
# rosto + pescoço fora (elipse) e jaleco claro fora
face = ((xx - 560) / 175) ** 2 + ((yy - 360) / 260) ** 2 < 1
neck = (xx > 480) & (xx < 680) & (yy > 450) & (yy < 720)
coat = (lum > 215) & (sat < 0.12)
hair = (alpha > 0.05) & ~face & ~neck & ~coat & (yy > 120)
w = hair.astype(np.float32)
w = cv2.GaussianBlur(w, (0, 0), 9)
w *= np.clip((yy - 200) / 800, 0, 1) ** 1.2          # balança mais nas pontas
w[face | neck] = 0
w = cv2.GaussianBlur(w, (0, 0), 4)

# ---------- pálpebras ----------
EYES = [  # centro x, centro y, raio x, raio y, cor da pele
    (487, 306, 40, 17, (129, 160, 225)),
    (628, 296, 42, 17, (142, 175, 237)),
]


def eyelid(img, k):
    """k = 0 (aberto) a 1 (fechado)."""
    if k <= 0:
        return img
    lay = img.copy()
    m = np.zeros((H, W), np.float32)
    for cx, cy, rx, ry, col in EYES:
        top = cy - ry
        bottom = top + int(2 * ry * k) + 2
        cv2.ellipse(m, (cx, cy), (rx, ry), 0, 0, 360, 1, -1)
        m[:max(0, top - 4)] = m[:max(0, top - 4)]  # noop
        band = np.zeros_like(m); band[top - 6:bottom, cx - rx - 6:cx + rx + 6] = 1
        mm = m * band
        lay[mm > 0, 0], lay[mm > 0, 1], lay[mm > 0, 2] = col
        if k > 0.7:  # linha dos cílios do olho fechado
            cv2.ellipse(lay, (cx, cy + 2), (rx - 2, 7), 0, 10, 170, (40, 55, 80, 255), 3, cv2.LINE_AA)
        m = np.zeros((H, W), np.float32)
        m += mm
        soft = cv2.GaussianBlur(mm, (0, 0), 2.2)[..., None]
        img = (img * (1 - soft) + lay * soft).astype(np.uint8)
    return img


def blink(t):
    for t0 in (1.6, 4.4):
        d = abs(t - t0)
        if d < 0.12:
            return min(1.0, (0.12 - d) / 0.07)
    return 0.0


def frame(i):
    t = i / FPS
    ph = 2 * math.pi * t / T
    # cabelo: deslocamento horizontal ondulado
    dx = (5.0 * np.sin(2 * ph + yy / 140.0) * w).astype(np.float32)
    dy = (1.5 * np.cos(2 * ph + yy / 160.0) * w).astype(np.float32)
    img = cv2.remap(SRC, xx + dx, yy + dy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
    img = eyelid(img, blink(t))
    # respiração: leve escala ancorada embaixo + balanço
    s = 1 + 0.006 * math.sin(2 * ph)
    rot = 0.6 * math.sin(ph)
    M = cv2.getRotationMatrix2D((W / 2, H), rot, s)
    M[1, 2] += -3 * math.sin(2 * ph)
    return cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))


# ---------- fundos ----------
def fundo(cw, ch, cy, r):
    bg = np.zeros((ch, cw, 3), np.uint8); bg[:] = (240, 244, 248)  # creme (BGR)
    gy, gx = np.mgrid[0:ch, 0:cw]
    glow = np.exp(-(((gx - cw * .5) / (cw * .7)) ** 2 + ((gy - ch * .4) / (ch * .6)) ** 2))
    bg = (bg * (0.96 + 0.04 * glow[..., None]) + 255 * 0.04 * glow[..., None]).clip(0, 255).astype(np.uint8)
    lay = bg.copy()
    cv2.circle(lay, (cw // 2, cy), r, (234, 227, 169), -1, cv2.LINE_AA)            # aqua A9E3EA
    cv2.circle(lay, (int(cw * .83), int(cy - r * .72)), int(r * .2), (199, 165, 245), -1, cv2.LINE_AA)  # rosa
    cv2.circle(lay, (int(cw * .16), int(cy + r * .55)), int(r * .12), (199, 165, 245), -1, cv2.LINE_AA)
    return lay


FORMATOS = {
    'quadrado': dict(cw=1080, ch=1080, h=1040, cy=560, r=430),   # perfil / post
    'vertical': dict(cw=1080, ch=1920, h=1500, cy=1150, r=520),  # story / Reels
}


def compor(fr, f, bg):
    h = f['h']; wv = int(W * h / H)
    a = cv2.resize(fr, (wv, h), interpolation=cv2.INTER_AREA)
    out = bg.copy(); x0 = (f['cw'] - wv) // 2; y0 = f['ch'] - h
    al = a[..., 3:4].astype(np.float32) / 255
    roi = out[y0:y0 + h, x0:x0 + wv]
    out[y0:y0 + h, x0:x0 + wv] = (roi * (1 - al) + a[..., :3] * al).astype(np.uint8)
    return out


if __name__ == '__main__':
    only = sys.argv[1:] or ['todos']
    bgs = {k: fundo(f['cw'], f['ch'], f['cy'], f['r']) for k, f in FORMATOS.items()}
    dirs = {k: Path(f'_f_{k}') for k in list(FORMATOS) + ['alfa']}
    for d in dirs.values():
        shutil.rmtree(d, ignore_errors=True); d.mkdir()
    for i in range(N):
        fr = frame(i)
        cv2.imwrite(str(dirs['alfa'] / f'{i:04d}.png'), cv2.resize(fr, (W // 2 * 2 - 128, int(H * (W // 2 * 2 - 128) / W) // 2 * 2)))
        for k, f in FORMATOS.items():
            cv2.imwrite(str(dirs[k] / f'{i:04d}.jpg'), compor(fr, f, bgs[k]), [cv2.IMWRITE_JPEG_QUALITY, 95])
    run = lambda *a: subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *a], check=True)
    for k in FORMATOS:
        run('-framerate', str(FPS), '-i', f'_f_{k}/%04d.jpg', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18',
            '-movflags', '+faststart', str(OUT / f'avatar-dra-flavia-{k}.mp4'))
    run('-framerate', str(FPS), '-i', '_f_alfa/%04d.png', '-c:v', 'libvpx-vp9', '-pix_fmt', 'yuva420p', '-b:v', '3M',
        '-auto-alt-ref', '0', str(OUT / 'avatar-dra-flavia-transparente.webm'))
    run('-framerate', str(FPS), '-i', '_f_quadrado/%04d.jpg', '-vf',
        'fps=15,scale=540:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=160[p];[b][p]paletteuse=dither=bayer',
        '-loop', '0', str(OUT / 'avatar-dra-flavia.gif'))
    shutil.copy('_f_quadrado/0000.jpg', OUT / 'avatar-dra-flavia-quadrado.jpg')
    print('ok')
