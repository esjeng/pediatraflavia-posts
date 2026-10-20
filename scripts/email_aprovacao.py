"""Monta o e-mail de aprovação (HTML) para a Dra. Flávia.

Regra (Edilson, 20/10/2026): cada carrossel vai com UM link que abre todos os slides juntos
(arquivo slides.pdf na pasta do post), e não um link por slide.

Uso:
  1) python3 scripts/email_aprovacao.py pdf posts/<pasta> <prefixo>   -> gera posts/<pasta>/slides.pdf
  2) commit + push; anote o SHA
  3) python3 scripts/email_aprovacao.py html <SHA> lote.json saida.html
     lote.json: {"titulo": "...", "intro": "...", "itens": [{"data": "2026-10-23", "dia": "Sex",
       "pasta": "reels-06-engasgo", "tipo": "reels"|"carrossel", "palavra": "ENGASGO", "tema": "...", "aviso": ""}]}
"""
import html, json, sys
from pathlib import Path

REPO = 'esjeng/pediatraflavia-posts'
RAIZ = Path(__file__).resolve().parent.parent


def pdf(pasta, prefixo):
    from PIL import Image
    d = RAIZ / pasta
    fs = sorted(f for f in d.iterdir() if f.name.startswith(prefixo + '-') and f.suffix == '.jpg' and 'preview' not in f.name)
    ims = [Image.open(f).convert('RGB') for f in fs]
    ims[0].save(d / 'slides.pdf', save_all=True, append_images=ims[1:], resolution=150)
    print(d / 'slides.pdf', len(ims), 'páginas')


def montar(sha, lote):
    raw = lambda pasta, f: f'https://raw.githubusercontent.com/{REPO}/{sha}/posts/{pasta}/{f}'
    cdn = lambda pasta, f: f'https://cdn.jsdelivr.net/gh/{REPO}@{sha}/posts/{pasta}/{f}'  # PDF abre no navegador
    blocos = []
    for it in lote['itens']:
        p, d = it['pasta'], it['data']
        quando = f"{it['dia']} {d[8:]}/{d[5:7]} · 18h (story no mesmo horário)"
        leg = (RAIZ / 'posts' / p / 'legenda.txt').read_text(encoding='utf-8').strip()
        if it['tipo'] == 'reels':
            img, w, fmt = raw(p, 'capa.jpg'), 260, 'Reels'
            links = (f'<a href="{raw(p, "reels.mp4")}">&#9654;&#65039; Assistir o Reels</a> · '
                     f'<a href="{raw(p, "story.mp4")}">Assistir o story</a>')
        else:
            img, w, fmt = raw(p, 'preview.jpg'), 560, 'Carrossel'
            links = (f'<a href="{cdn(p, "slides.pdf")}"><b>&#128196; Ver todos os slides</b></a> · '
                     f'<a href="{raw(p, "story.jpg")}">Ver o story</a>')
        aviso = (f'<p style="background:#FFF4D6;padding:8px 12px;border-radius:8px;font-size:13px">&#9888;&#65039; {it["aviso"]}</p>'
                 if it.get('aviso') else '')
        blocos.append(f'''<div style="border:1px solid #eee;border-radius:14px;padding:16px 18px;margin:18px 0">
<div style="font-size:12px;color:#888;text-transform:uppercase;letter-spacing:.05em">{fmt}</div>
<h3 style="margin:4px 0 6px;color:#2D3142">{html.escape(it['tema'])}</h3>
<div style="font-size:14px;margin-bottom:10px">&#128197; <b>{quando}</b> · Para aprovar: <b style="background:#FCE4EF;padding:2px 8px;border-radius:6px">APROVADO {it['palavra']}</b></div>
{aviso}<a href="{img}"><img src="{img}" width="{w}" style="max-width:100%;border-radius:10px;border:1px solid #eee"></a>
<div style="font-size:14px;margin:8px 0">{links}</div>
<div style="font-size:13px;color:#555;margin-top:8px">Legenda:</div>
<div style="white-space:pre-wrap;font-size:13px;color:#333;background:#FAF7F4;padding:10px 12px;border-radius:8px">{html.escape(leg)}</div>
</div>''')
    return f'''<div style="font-family:Arial,Helvetica,sans-serif;max-width:640px;color:#2D3142">
<h2 style="color:#EF8FB8;margin-bottom:4px">{lote['titulo']}</h2>
<p>{lote['intro']}</p>
<p><b>Para aprovar</b>, responda este e-mail com a palavra de cada post (ex.: <b>APROVADO {lote['itens'][0]['palavra']}</b>) ou <b>APROVADO TODOS</b>.<br>
Para mudanças, escreva <b>AJUSTES</b> e o que alterar. Se não quiser o story de algum post, escreva <b>SEM STORY</b> e o nome do post.</p>
{''.join(blocos)}
<p style="font-size:13px;color:#777">Só publico o que for aprovado.</p></div>'''


if __name__ == '__main__':
    if sys.argv[1] == 'pdf':
        pdf(sys.argv[2], sys.argv[3])
    else:
        Path(sys.argv[4]).write_text(montar(sys.argv[2], json.load(open(sys.argv[3], encoding='utf-8'))), encoding='utf-8')
