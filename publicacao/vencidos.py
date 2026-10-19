"""Publicador do Instagram: lista o que está na hora de publicar.

Uso (na tarefa agendada):
  curl -sL https://raw.githubusercontent.com/esjeng/pediatraflavia-posts/main/publicacao/vencidos.py | python3 - --conta pediatraflavia
Opcional para teste: --agora 2026-10-20T12:30

Lê publicacao/agenda.json do repositório da conta (via API do GitHub, sem cache) e imprime um JSON
com os itens cujo horário está na janela [agora - 35 min, agora + 10 min], já com a ação e os
parâmetros do Windsor.ai prontos (e alternativas, se o link principal falhar).
Itens sem "aprovado": true são listados em "bloqueados" e não devem ser publicados.
"""
import argparse, json, urllib.request
from datetime import datetime, timedelta, timezone

CONTAS = {
    'pediatraflavia': {'repo': 'esjeng/pediatraflavia-posts', 'conta_ig': '17841404417503785'},
    'raquetada': {'repo': 'esjeng/raquetada-posts', 'conta_ig': '17841444170180102'},
}
BRT = timezone(timedelta(hours=-3))


def get(url, accept=None):
    req = urllib.request.Request(url, headers={'User-Agent': 'publicador', **({'Accept': accept} if accept else {})})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode('utf-8')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--conta', required=True, choices=CONTAS)
    ap.add_argument('--agora')
    ap.add_argument('--antes', type=int, default=35)
    ap.add_argument('--depois', type=int, default=10)
    a = ap.parse_args()
    cfg = CONTAS[a.conta]
    agora = datetime.fromisoformat(a.agora).replace(tzinfo=BRT) if a.agora else datetime.now(BRT)
    try:
        agenda = json.loads(get(f"https://api.github.com/repos/{cfg['repo']}/contents/publicacao/agenda.json",
                                'application/vnd.github.raw'))
    except Exception:
        agenda = json.loads(get(f"https://raw.githubusercontent.com/{cfg['repo']}/main/publicacao/agenda.json"))
    ini, fim = agora - timedelta(minutes=a.antes), agora + timedelta(minutes=a.depois)
    itens, bloqueados = [], []
    for it in agenda.get('itens', []):
        q = datetime.fromisoformat(it['quando'])
        if not (ini <= q <= fim):
            continue
        if not it.get('aprovado'):
            bloqueados.append({'id': it['id'], 'descricao': it.get('descricao', '')})
            continue
        sha, pasta = it['sha'], it['pasta'].strip('/')
        raw = lambda f: f"https://raw.githubusercontent.com/{cfg['repo']}/{sha}/{pasta}/{f}"
        cdn = lambda f: f"https://cdn.jsdelivr.net/gh/{cfg['repo']}@{sha}/{pasta}/{f}"
        legenda = get(raw(it['legenda'])).rstrip('\n') if it.get('legenda') else None
        t = it['tipo']
        if t == 'carrossel':
            acao = 'create_carousel_post'
            p = {'image_urls': [raw(f) for f in it['imagens']], 'caption': legenda}
            alts = [{'image_urls': [cdn(f) for f in it['imagens']], 'caption': legenda}]
        elif t == 'reels':
            acao = 'create_video_post'
            p = {'video_url': raw(it['video']), 'cover_url': raw(it['capa']), 'share_to_feed': True, 'caption': legenda}
            alts = [dict(p, video_url=cdn(it['video']))]
        elif t == 'story':
            acao = 'create_story'
            if it.get('video'):
                p = {'video_url': raw(it['video'])}
                alts = [{'video_url': cdn(it['video'])}] + ([{'image_url': raw(it['imagem'])}] if it.get('imagem') else [])
            else:
                p = {'image_url': raw(it['imagem'])}
                alts = [{'image_url': cdn(it['imagem'])}]
        else:
            continue
        itens.append({'id': it['id'], 'descricao': it.get('descricao', ''), 'quando': it['quando'],
                      'action': acao, 'params': p, 'alternativas': alts})
    print(json.dumps({'conta': a.conta, 'connector': 'instagram', 'account': cfg['conta_ig'],
                      'agora': agora.isoformat(timespec='minutes'), 'itens': itens, 'bloqueados': bloqueados},
                     ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
