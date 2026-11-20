"""Gera o Lote 3 (22/11 a 05/12/2026) no estilo com avatar da Dra. Flávia.
Uso: python3 gen_lote3.py [pasta ...]   (sem argumentos gera tudo)"""
import json, math, subprocess, sys, shutil
from pathlib import Path
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
import conteudo as C

B = Path(__file__).resolve().parent
OUT = B / 'out'; OUT.mkdir(exist_ok=True)
TMP = B / 'tmp'; TMP.mkdir(exist_ok=True)
FE = json.load(open(B / 'node_modules/@iconify-json/fluent-emoji/icons.json'))['icons']
AVATAR = (B / 'src/avatar.png').as_uri()
LOGO = (B / 'marca/logo.png').as_uri()
FPS = 30


def em(n, s):
    return f'<svg viewBox="0 0 32 32" width="{s}" height="{s}">{FE[n]["body"]}</svg>'


CSS = '''*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Poppins,sans-serif;color:#2D3142;background:transparent}
.s{width:1080px;position:relative;overflow:hidden;margin-bottom:20px}
.bg{background:linear-gradient(180deg,#FBF7F4 0%,#FBEFF3 55%,#FCE6EE 100%)}
.bA{position:absolute;left:-170px;top:-190px;width:430px;height:430px;border-radius:50%;background:#8EDCE6;opacity:.85}
.arc{position:absolute;left:-120px;top:-60px;width:760px;height:300px;border-radius:50%;border:2px solid transparent;border-bottom-color:rgba(245,165,199,.6)}
.circ{position:absolute;border-radius:50%;background:#C9EEF2}
.bP{position:absolute;right:-150px;bottom:-170px;width:420px;height:420px;border-radius:50%;background:#F5A5C7}
.dots{position:absolute;display:grid;grid-template-columns:repeat(3,10px);gap:14px}.dots i{width:8px;height:8px;border-radius:50%;background:#F5A5C7;opacity:.7}
.ht{position:absolute;color:#EF8FB8;font-size:30px}
.av{position:absolute;left:50%;bottom:-10px;transform:translateX(-50%)}
.top{position:absolute;top:44px;left:0;right:0;text-align:center}
.top .h{font-size:34px;font-weight:700}
.top .r{font-size:19px;font-weight:500;color:#5E6272;letter-spacing:.03em;margin-top:2px}
.tag{display:inline-block;font-weight:700;border-radius:24px;padding:10px 30px 14px;line-height:1.1;white-space:nowrap}
.aq{background:#A9E3EA}.pk{background:#F5A5C7;color:#fff}.nv{background:#2D3142;color:#fff}
.el{position:absolute}
.card{display:flex;align-items:center;gap:26px;background:#fff;border-radius:30px;padding:20px 30px;box-shadow:0 12px 30px rgba(45,49,66,.10)}
.card .ic{flex:none;width:84px;height:84px;border-radius:24px;background:#FCE9F1;display:flex;align-items:center;justify-content:center}
.card .t{font-size:36px;line-height:1.25;font-weight:500}
.card .t b{font-weight:700}
.big{font-size:84px;font-weight:700;line-height:1.08;letter-spacing:-.01em;text-align:center;white-space:nowrap}
.big .p{color:#EF8FB8}
.c{position:absolute;left:0;right:0;display:flex;flex-direction:column;align-items:center;text-align:center}
.sub{font-size:28px;color:#5E6272;font-weight:500}
.noav .card{padding:26px 36px;gap:32px;border-radius:34px}
.noav .card .ic{width:104px;height:104px;border-radius:28px}.noav .card .ic svg{width:74px;height:74px}
.noav .card .t{font-size:42px}
.noav .big{font-size:100px}.noav .c.el > svg{width:180px;height:180px}
.noav .sub{font-size:32px}
.noav div.el:not(.c) > .tag{font-size:60px!important}.r.noav div.el:not(.c) > .tag{font-size:68px!important}
.r.noav .card .t{font-size:48px}.r.noav .card .ic{width:118px;height:118px}.r.noav .card .ic svg{width:84px;height:84px}
.r.noav .big{font-size:112px}.r.noav .c.el > svg{width:210px;height:210px}
.thumb{border-radius:28px;box-shadow:0 24px 60px rgba(45,49,66,.25);border:8px solid #fff}
'''
FIT = '''for(const e of document.querySelectorAll('.fit')){let f=parseFloat(getComputedStyle(e).fontSize);
 const m=+e.dataset.max||940; while(e.scrollWidth>m&&f>20){f-=2;e.style.fontSize=f+'px'}}'''

TOPO = '<div class="top"><div class="h">@pediatraflavia</div><div class="r">Dra. Flávia Lopes · CRM-MG 62325 · RQE 37384</div></div>'
LOGO_CRM = (f'<div class="c" style="top:{{y}}px"><img src="{LOGO}" style="height:{{h}}px">'
            '<div class="sub" style="font-size:21px;margin-top:8px;color:#2D3142">CRM-MG 62325 · RQE 37384 · @pediatraflavia</div></div>')


def fundo(H, avatar=True, av_h=690, topo=True, circ=True):
    cy = H - 230 if H == 1350 else H - 470
    r = 430 if H == 1350 else 470
    d = ('<div class="dots" style="left:60px;bottom:40px">' + '<i></i>' * 9 + '</div>'
         '<div class="dots" style="right:70px;top:150px">' + '<i></i>' * 9 + '</div>')
    hy = 560 if H == 1350 else 880
    hearts = f'<div class="ht" style="left:60px;top:{hy}px">&#9829;</div><div class="ht" style="right:80px;top:{hy+40}px">&#9829;</div>'
    av = f'<img class="av" src="{AVATAR}" style="height:{av_h}px">' if avatar else ''
    cc = f'<div class="circ" style="left:{540-r}px;top:{cy-r}px;width:{2*r}px;height:{2*r}px"></div>' if circ else ''
    return (f'<div class="bA"></div><div class="arc"></div>{cc}'
            f'<div class="bP"></div>{d}{hearts}{av}' + (TOPO if topo else ''))


# ---------------- elementos (cada um é um bloco posicionado) ----------------
def els_capa(p, H):
    e, l1, l2, tg = p['capa']
    y0 = 150 if H == 1350 else 210
    sub = 'arraste e descubra &#128073;' if H == 1350 else 'a pediatra explica &#128071;'
    return [f'<div class="c el" style="top:{y0}px">{em(e, 130)}</div>',
            f'<div class="c el" style="top:{y0+150}px"><div class="big fit">{l1}</div><div class="big p fit" style="color:#EF8FB8">{l2}</div></div>',
            f'<div class="c el" style="top:{y0+375}px"><div class="tag nv fit" data-max="900" style="font-size:44px;transform:rotate(-2deg)">{tg}</div></div>',
            f'<div class="c el" style="top:{y0+478}px"><div class="sub">{sub}</div></div>']


def els_lista(titulo, cls, itens, H):
    y0 = 170 if H == 1350 else 230
    out = [f'<div class="el" style="left:80px;top:{y0}px"><div class="tag {cls}" style="font-size:52px">{titulo}</div></div>']
    out += [f'<div class="el card" data-k="{k}" style="left:80px;right:80px"><div class="ic">{em(i, 58)}</div><div class="t">{t}</div></div>'
            for k, (i, t) in enumerate(itens)]
    return out


def els_veredito(p, H):
    v, txt = p['veredito']
    y0 = 200
    return [f'<div class="c el" style="top:{y0}px"><div class="tag pk" style="font-size:120px;padding:10px 60px 22px;transform:rotate(-3deg)">{v}!</div></div>',
            f'<div class="el card" style="left:80px;right:80px;top:{y0+250}px"><div class="ic">{em("light-bulb", 58)}</div><div class="t">{txt}</div></div>']


def els_final(H):
    y0 = 160 if H == 1350 else 230
    return [LOGO_CRM.format(y=y0 - 120 if H == 1350 else y0, h=110 if H == 1350 else 150),
            f'<div class="c el" style="top:{y0+(70 if H == 1350 else 240)}px">{em("sparkling-heart", 100)}</div>',
            f'<div class="c el" style="top:{y0+(190 if H == 1350 else 360)}px"><div class="big" style="font-size:66px">Curta, compartilhe<br>e <span class="p">siga</span></div></div>',
            f'<div class="c el" style="top:{y0+(355 if H == 1350 else 525)}px"><div class="tag nv" style="font-size:44px">@pediatraflavia</div></div>',
            f'<div class="c el" style="top:{y0+(450 if H == 1350 else 620)}px"><div class="sub">para mais dicas &#128150;</div></div>']


LAYOUT_JS = '''(H)=>{for(const s of document.querySelectorAll('section')){
 const noav=s.classList.contains('noav');
 const cards=[...s.querySelectorAll('.card[data-k]')];
 if(cards.length){
  const hdr=s.querySelector('.el'); let y=hdr.offsetTop+hdr.offsetHeight+(noav?44:36);
  const n=cards.length, gap=noav?(n>=4?22:30):(n>=4?16:22);
  if(n>=4&&!noav) cards.forEach(c=>{c.style.padding='16px 28px';c.querySelector('.t').style.fontSize='33px'});
  for(const c of cards){c.style.top=y+'px'; y+=c.offsetHeight+gap}
  const av=s.querySelector('.av'); if(av){const h=Math.max(430,Math.min(690,H-y+10)); av.style.height=h+'px'}
 }
 if(noav){const els=[...s.querySelectorAll(':scope > .el')];
  let yy=0; els.forEach((e,k)=>{ if(k){const p=els[k-1];
     const g=(e.classList.contains('card')&&p.classList.contains('card'))?(els.length>5?22:30):(e.classList.contains('card')?44:34);
     yy+=p.offsetHeight+g} e.style.top=yy+'px'});
  const vis=e=>{let r=e.getBoundingClientRect();for(const d of e.querySelectorAll('*')){const q=d.getBoundingClientRect();if(q.width&&q.height)r={top:Math.min(r.top,q.top),bottom:Math.max(r.bottom,q.bottom)}}return r};
  const sr=s.getBoundingClientRect();
  let t=1e9,b=-1e9; for(const e of els){const r=vis(e);t=Math.min(t,r.top-sr.top);b=Math.max(b,r.bottom-sr.top)}
  const a0=150,a1=H-90; let d=(a0+a1)/2-(t+b)/2; d=Math.max(d,a0-t);
  for(const e of els) e.style.top=(e.offsetTop+d)+'px';
 }
}}'''


NOAV = '<!--NOAV-->'


def pagina(secoes, H, bg=True):
    return ('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>' + CSS + '</style></head><body>' +
            ''.join(f'<section class="s{" bg" if bg else ""}{" noav" if s.startswith(NOAV) else ""}{" r" if H == 1920 else ""}" id="s{i}" style="height:{H}px">{s}</section>' for i, s in enumerate(secoes)) +
            '</body></html>')


def abrir(pw, html, nome, H):
    f = TMP / f'{nome}.html'; f.write_text(html, encoding='utf-8')
    pg = pw.new_page(viewport={'width': 1080, 'height': H})
    pg.goto(f.as_uri()); pg.wait_for_timeout(500); pg.evaluate(FIT); pg.evaluate(LAYOUT_JS, H)
    return pg


# ---------------- carrossel ----------------
def carrossel(pw, p):
    H = 1350
    sem = lambda: NOAV + fundo(H, avatar=False, circ=False)
    secs = [sem() + ''.join(els_capa(p, H))]
    if p.get('veredito'):
        secs.append(sem() + ''.join(els_veredito(p, H)))
    for t, cls, its in p['telas']:
        secs.append(sem() + ''.join(els_lista(t, cls, its, H)))
    fin = fundo(H, topo=False) + ''.join(els_final(H))
    secs.append(fin)
    dst = OUT / p['pasta']; dst.mkdir(exist_ok=True)
    pg = abrir(pw, pagina(secs, H), p['pasta'], H)
    files = []
    for i in range(len(secs)):
        png = TMP / '_s.png'; pg.locator(f'#s{i}').screenshot(path=str(png))
        f = dst / f"{p['prefixo']}-{i+1:02d}.jpg"; Image.open(png).convert('RGB').save(f, quality=92); files.append(f)
    pg.close()
    ims = [Image.open(f).convert('RGB') for f in files]
    ims[0].save(dst / 'slides.pdf', save_all=True, append_images=ims[1:], resolution=150)
    cols = 4; rows = math.ceil(len(ims) / cols)
    sh = Image.new('RGB', (cols * 310 + 10, rows * 385 + 10), '#cfcfcf')
    for k, im in enumerate(ims): sh.paste(im.resize((300, 375)), (10 + (k % cols) * 310, 10 + (k // cols) * 385))
    sh.save(dst / 'preview.jpg', quality=88)
    story(pw, files[0], dst / 'story.jpg', reels=False)
    (dst / 'legenda.txt').write_text(p['legenda'].strip() + '\n', encoding='utf-8')
    return [f.name for f in files]


def story(pw, capa, saida, reels):
    H = 1920
    if reels:
        th = f'<img class="thumb" src="{Path(capa).as_uri()}" style="height:920px;transform:rotate(-3deg)">'
        t1, t2, tx = '&#127916; Reels novo', 'no feed!', '&#128073; Toque no perfil e assista'
    else:
        th = f'<img class="thumb" src="{Path(capa).as_uri()}" style="width:700px;transform:rotate(-3deg)">'
        t1, t2, tx = '&#128204; Post novo', 'no feed!', '&#128073; Toque no perfil e confira'
    sub2 = 'com a Dra. Flávia' if reels else 'arraste para o lado no post'
    html = pagina([fundo(H, avatar=False, topo=False, circ=False) +
                   f'<div class="c" style="top:150px"><div class="tag aq" style="font-size:62px">{t1}</div></div>'
                   f'<div class="c" style="top:270px"><div class="tag pk" style="font-size:56px;transform:rotate(-2deg)">{t2}</div></div>'
                   f'<div class="c" style="top:{410 if not reels else 400}px">{th}</div>'
                   f'<div class="c" style="top:1400px"><div class="card" style="font-size:40px;font-weight:700;padding:22px 44px">{tx}</div></div>'
                   f'<div class="c" style="top:1515px"><div class="sub">{sub2}</div></div>'
                   + LOGO_CRM.format(y=1600, h=150)], H)
    pg = abrir(pw, html, 'story', H)
    png = TMP / '_st.png'; pg.locator('#s0').screenshot(path=str(png)); pg.close()
    Image.open(png).convert('RGB').save(saida, quality=92)


# ---------------- Reels ----------------
RH, AH = 1920, 1000
BGNPY = TMP / 'bg_avatar.npy'


def base_avatar(pw):
    """180 quadros (loop 6 s) de fundo + avatar animado, cacheados em disco."""
    if BGNPY.exists():
        return np.load(BGNPY, mmap_mode='r')
    pg = abrir(pw, pagina([fundo(RH, avatar=False)], RH), 'bgreels', RH)
    png = TMP / '_bg.png'; pg.locator('#s0').screenshot(path=str(png)); pg.close()
    bg = np.array(Image.open(png).convert('RGB'))
    import os, cv2
    cwd = os.getcwd(); os.chdir(B); sys.path.insert(0, str(B)); import animar as AV; os.chdir(cwd)
    AW = int(AV.W * AH / AV.H); x0 = (1080 - AW) // 2; y0 = RH - AH + 10
    arr = np.lib.format.open_memmap(BGNPY, mode='w+', dtype=np.uint8, shape=(AV.N, RH, 1080, 3))
    for i in range(AV.N):
        fr = cv2.resize(AV.frame(i), (AW, AH), interpolation=cv2.INTER_AREA)
        a = fr[..., 3:4].astype(np.float32) / 255; rgb = fr[..., 2::-1].astype(np.float32)
        out = bg.copy(); y1 = min(RH, y0 + AH); hh = y1 - y0
        roi = out[y0:y1, x0:x0 + AW].astype(np.float32)
        out[y0:y1, x0:x0 + AW] = (roi * (1 - a[:hh]) + rgb[:hh] * a[:hh]).astype(np.uint8)
        arr[i] = out
    arr.flush(); del arr
    return np.load(BGNPY, mmap_mode='r')


def camadas(pw, p):
    """Para cada cena: duração e lista de (camada RGBA recortada, x, y, atraso)."""
    cenas = [('capa', els_capa(p, RH), 5.0, [0.1, 0.35, 0.9, 1.4])]
    for t, cls, its in p['telas']:
        n = len(its)
        dur = 6.5 if n == 1 else 4.5 + n
        cenas.append((t, els_lista(t, cls, its, RH), dur, [0.15] + [0.6 + 0.9 * k for k in range(n)]))
    cenas.append(('fim', els_final(RH), 4.5, [0.1, 0.4, 0.7, 1.0, 1.3]))
    secs = [(NOAV if k < len(cenas) - 1 else '') + ''.join(e) for k, (_, e, _, _) in enumerate(cenas)]
    pg = abrir(pw, pagina(secs, RH, bg=False), p['pasta'] + '-ov', RH)
    res = []
    for si, (nome, els, dur, dl) in enumerate(cenas):
        lay = []
        n_el = pg.evaluate(f"document.querySelector('#s{si}').children.length")
        for k in range(n_el):
            bb = pg.evaluate(f'''()=>{{const s=document.querySelector('#s{si}');const ch=[...s.children];
              ch.forEach((c,j)=>c.style.visibility=j=={k}?'visible':'hidden');
              const sr=s.getBoundingClientRect();
              let r=ch[{k}].getBoundingClientRect();
              for(const d of ch[{k}].querySelectorAll('*')){{const q=d.getBoundingClientRect();if(q.width&&q.height){{r={{left:Math.min(r.left,q.left),top:Math.min(r.top,q.top),right:Math.max(r.right,q.right),bottom:Math.max(r.bottom,q.bottom)}}}}}}
              return [r.left-sr.left,r.top-sr.top,r.right-sr.left,r.bottom-sr.top]}}''')
            x0, y0 = max(0, int(bb[0]) - 50), max(0, int(bb[1]) - 50)
            x1, y1 = min(1080, int(bb[2]) + 50), min(RH, int(bb[3]) + 60)
            png = TMP / '_l.png'
            sy = pg.evaluate(f"document.querySelector('#s{si}').offsetTop")
            pg.screenshot(path=str(png), omit_background=True,
                          clip=dict(x=x0, y=sy + y0, width=x1 - x0, height=y1 - y0), full_page=True)
            lay.append((Image.open(png).convert('RGBA').copy(), x0, y0, dl[min(k, len(dl) - 1)]))
        res.append((nome, dur, lay))
    pg.close()
    return res


def ease(t):
    t = max(0.0, min(1.0, t)); return 1 - (1 - t) ** 3


BG_SEM = None


def fundo_sem(pw):
    global BG_SEM
    if BG_SEM is None:
        pg = abrir(pw, pagina([fundo(RH, avatar=False, circ=False)], RH), 'bgsem', RH)
        png = TMP / '_bgs.png'; pg.locator('#s0').screenshot(path=str(png)); pg.close()
        BG_SEM = Image.open(png).convert('RGBA')
    return BG_SEM


def reels(pw, p, base):
    dst = OUT / p['pasta']; dst.mkdir(exist_ok=True)
    cenas = camadas(pw, p)
    total = sum(d for _, d, _ in cenas); nf = int(round(total * FPS))
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'1080x{RH}', '-r', str(FPS), '-i', '-',
           '-stream_loop', '-1', '-i', str(B / 'marca/trilha.wav'),
           '-filter_complex', f'[1:a]volume=0.55,afade=t=in:d=0.5,afade=t=out:st={total-1.5:.2f}:d=1.5[a]',
           '-map', '0:v', '-map', '[a]', '-t', f'{total:.2f}',
           '-c:v', 'libx264', '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-crf', '19', '-c:a', 'aac', '-b:a', '128k',
           '-movflags', '+faststart', str(dst / 'reels.mp4')]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    i = 0; capa = None; bs = fundo_sem(pw)
    for si, (nome, dur, lay) in enumerate(cenas):
        n = int(round(dur * FPS)); ultima = si == len(cenas) - 1
        for j in range(n):
            t = j / FPS
            im = Image.fromarray(np.asarray(base[j % len(base)])).convert('RGBA') if ultima else bs.copy()
            fo = 1.0 if t < dur - 0.3 else max(0.0, (dur - t) / 0.3)  # saída da cena
            if si == len(cenas) - 1: fo = 1.0
            for L, x, y, d in lay:
                a = ease((t - d) / 0.4) * fo
                if a <= 0: continue
                Lr = L if a >= 1 else L.copy()
                if a < 1:
                    al = Lr.getchannel('A').point(lambda v, a=a: int(v * a)); Lr.putalpha(al)
                im.alpha_composite(Lr, (x, y + int(round((1 - a) * 40 * (fo >= 1)))))
            if si == 0 and j == int(4.0 * FPS): capa = im.convert('RGB')
            pr.stdin.write(im.convert('RGB').tobytes()); i += 1
    pr.stdin.close(); pr.wait()
    capa.save(dst / 'capa.jpg', quality=92)
    story(pw, dst / 'capa.jpg', dst / 'story.jpg', reels=True)
    (dst / 'legenda.txt').write_text(p['legenda'].strip() + '\n', encoding='utf-8')
    # prévia: 1 quadro por cena
    tt = 0; fr = []
    for nome, dur, _ in cenas:
        fr.append(tt + dur - 0.5); tt += dur
    ims = []
    for k, t in enumerate(fr):
        f = TMP / f'_p{k}.jpg'
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', f'{t:.2f}', '-i', str(dst / 'reels.mp4'), '-frames:v', '1', str(f)], check=True)
        ims.append(Image.open(f).resize((270, 480)))
    sh = Image.new('RGB', (len(ims) * 280 + 10, 500), '#cfcfcf')
    for k, im in enumerate(ims): sh.paste(im, (10 + k * 280, 10))
    sh.save(dst / 'preview.jpg', quality=88)
    return total


if __name__ == '__main__':
    sel = sys.argv[1:]
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        base = None
        for p in C.POSTS:
            if sel and p['pasta'] not in sel: continue
            if p['tipo'] == 'carrossel':
                print(p['pasta'], carrossel(br, p), flush=True)
            else:
                if base is None: base = base_avatar(br)
                print(p['pasta'], f'{reels(br, p, base):.1f}s', flush=True)
        br.close()
