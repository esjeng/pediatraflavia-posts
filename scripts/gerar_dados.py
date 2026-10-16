"""Gera dados/dados.json (painel público do @pediatraflavia) a partir das respostas
salvas do Windsor.ai e do Gmail.

Uso: python3 scripts/gerar_dados.py <pasta_entrada>
Arquivos esperados na pasta de entrada (resposta da ferramenta, como veio):
  perfil.json   Windsor get_data: username, followers_count, media_count
  diario.json   Windsor get_data: date, reach, views, accounts_engaged (últimos 90 dias)
  posts.json    Windsor get_data: media_id, timestamp, media_type, media_caption, media_permalink,
                media_reach, media_views, media_saved, media_shares, media_like_count, media_comments_count
  gmail_<threadId>.json   Gmail get_thread (MINIMAL), um arquivo por conversa de aprovação
A agenda vem de dados/programacao.json (mantida no repositório).
"""
import json, re, sys, glob, os
from datetime import datetime, timedelta, timezone

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENT = sys.argv[1]
BRT = timezone(timedelta(hours=-3))
DRA = 'pediatraflavia@gmail.com'
THREADS = {'carrosseis': '1a14254e6bf5d439', 'carrossel19': '1a1428a10d8a2223',
           'reels': '1a144974d4e71fc1', 'reels5': '1a144c436b301612'}


def rows(nome):
    p = os.path.join(ENT, nome)
    if not os.path.exists(p):
        return []
    a = json.load(open(p, encoding='utf-8'))
    if isinstance(a, list) and a and isinstance(a[0], dict) and isinstance(a[0].get('text'), str):
        a = json.loads(a[0]['text'])
    if isinstance(a, dict):
        a = a.get('data') or a.get('rows') or a.get('result') or []
    return a


def num(x):
    try:
        return float(x or 0)
    except (TypeError, ValueError):
        return 0.0


agora = datetime.now(BRT)
hoje = agora.date()

# Perfil
pf = (rows('perfil.json') or [{}])[0]
perfil = {'usuario': pf.get('username', 'pediatraflavia'), 'seguidores': int(num(pf.get('followers_count'))),
          'publicacoes': int(num(pf.get('media_count')))}

# Diário: últimos 90 dias, dias sem registro = 0
d_in = {str(r.get('date'))[:10]: r for r in rows('diario.json')}
diario = []
for i in range(89, -1, -1):
    d = (hoje - timedelta(days=i)).isoformat()
    r = d_in.get(d, {})
    diario.append({'data': d, 'alcance': int(num(r.get('reach'))), 'visualizacoes': int(num(r.get('views'))),
                   'contas_engajadas': int(num(r.get('accounts_engaged')))})
ult30 = diario[-30:]
resumo_30d = {'alcance': sum(x['alcance'] for x in ult30), 'visualizacoes': sum(x['visualizacoes'] for x in ult30),
              'contas_engajadas': sum(x['contas_engajadas'] for x in ult30)}


# Posts
def local(ts):
    t = datetime.strptime(str(ts)[:19], '%Y-%m-%dT%H:%M:%S').replace(tzinfo=timezone.utc)
    return t.astimezone(BRT)


FORMATO = {'CAROUSEL_ALBUM': 'Carrossel', 'REELS': 'Reels', 'VIDEO': 'Reels', 'IMAGE': 'Imagem'}
posts = []
for r in rows('posts.json'):
    if not r.get('media_id'):
        continue
    t = local(r['timestamp'])
    alc = int(num(r.get('media_reach')))
    inter = int(num(r.get('media_like_count')) + num(r.get('media_comments_count')) + num(r.get('media_saved')) + num(r.get('media_shares')))
    leg = (r.get('media_caption') or '').replace('�', ' ').strip()
    posts.append({'id': str(r['media_id']), 'data': t.strftime('%Y-%m-%d'), 'data_hora': t.strftime('%d/%m/%y %H:%M'),
                  'formato': FORMATO.get(r.get('media_type'), r.get('media_type')), 'tipo_instagram': r.get('media_type'),
                  'titulo': leg.split('\n')[0][:120], 'link': r.get('media_permalink'),
                  'alcance': alc, 'visualizacoes': int(num(r.get('media_views'))), 'curtidas': int(num(r.get('media_like_count'))),
                  'comentarios': int(num(r.get('media_comments_count'))), 'salvamentos': int(num(r.get('media_saved'))),
                  'compartilhamentos': int(num(r.get('media_shares'))), 'interacoes': inter,
                  'taxa_engajamento': round(100 * inter / alc, 1) if alc else 0})
posts.sort(key=lambda p: p['data_hora'][6:8] + p['data_hora'][3:5] + p['data_hora'][:2] + p['data_hora'][9:], reverse=True)
melhores = sorted(posts, key=lambda p: p['alcance'], reverse=True)[:10]
por_formato = []
for f in ['Reels', 'Carrossel', 'Imagem']:
    g = [p for p in posts if p['formato'] == f]
    if g:
        a = sum(p['alcance'] for p in g)
        por_formato.append({'formato': f, 'posts': len(g), 'alcance_medio': round(a / len(g)),
                            'taxa_engajamento': round(100 * sum(p['interacoes'] for p in g) / a, 1) if a else 0})

# Aprovações (mesma regra do dashboard no Claude)
msgs = {}
for nome, tid in THREADS.items():
    lst = []
    p = os.path.join(ENT, f'gmail_{tid}.json')
    if os.path.exists(p):
        a = json.load(open(p, encoding='utf-8'))
        if isinstance(a, list) and a and isinstance(a[0], dict) and isinstance(a[0].get('text'), str):
            a = json.loads(a[0]['text'])
        lst = [m for m in (a.get('messages') or []) if DRA in str(m.get('sender', '')).lower()]
        lst.sort(key=lambda m: str(m.get('date')))
    msgs[nome] = lst


def own(s):
    return re.split(r'ATENCIOSAMENTE|\bEM \d{1,2} DE |&GT;|>|-----', str(s or '').upper())[0]


def keys(v):
    return [k.strip().upper() for k in (v if isinstance(v, list) else str(v or '').split('|')) if k.strip()]


def decide(ms, ok, story):
    ok = keys(ok)
    st = 'Aguardando'
    for m in ms:
        t = own(m.get('snippet'))
        if story and 'SEM STORY' in t:
            st = 'Sem story'
            continue
        if any(k in t for k in ok):
            st = 'Aprovado'
        elif 'AJUSTE' in t:
            st = 'Ajustes pedidos'
    return st


prog = json.load(open(os.path.join(RAIZ, 'dados', 'programacao.json'), encoding='utf-8'))
programacao = []
for p in sorted(prog, key=lambda x: x['data']):
    ms = msgs.get(p.get('thread'), [])
    ap = p.get('post_fixo') or (decide(ms, p.get('post_ok'), False) if p.get('thread') else '—')
    ast = p.get('story_fixo') or (decide(ms, p.get('story_ok'), True) if p.get('thread') else '—')
    if p.get('story_fixo') and any('SEM STORY' in own(m.get('snippet')) for m in ms):
        ast = 'Sem story'
    tipos = [FORMATO.get(t, t) for t in str(p.get('media_type')).split('|')]
    pub = any(x['data'] == p['data'] and x['formato'] in tipos for x in posts)
    if pub:
        sit = 'Publicado'
    elif p.get('sem_conteudo'):
        sit = 'Sem conteúdo'
    elif p['data'] < hoje.isoformat():
        sit = 'Não publicado'
    elif ap == 'Aprovado':
        sit = 'Agendado'
    elif ap == 'Ajustes pedidos':
        sit = 'Ajustes pedidos'
    else:
        sit = 'Aguardando aprovação'
    programacao.append({'id': p['id'], 'data': p['data'], 'data_texto': p['data'][8:10] + '/' + p['data'][5:7],
                        'dia': p['dia'], 'hora': p['hora'], 'formato': p['formato'], 'tema': p['tema'],
                        'story_hora': p.get('story_hora') or '', 'aprovacao_post': ap, 'aprovacao_story': ast, 'situacao': sit})
cont = lambda *s: sum(1 for x in programacao if x['situacao'] in s)
resumo_prog = {'agendados': cont('Agendado'), 'aguardando_aprovacao': cont('Aguardando aprovação', 'Ajustes pedidos'),
               'sem_conteudo': cont('Sem conteúdo', 'Não publicado'), 'publicados': cont('Publicado')}

out = {
    'atualizado_em': agora.isoformat(timespec='seconds'),
    'atualizado_em_texto': agora.strftime('%d/%m/%y %H:%M'),
    'perfil': perfil, 'resumo_30d': resumo_30d, 'diario': diario,
    'por_formato': por_formato, 'melhores_posts': melhores, 'posts': posts,
    'programacao': programacao, 'resumo_programacao': resumo_prog,
}
os.makedirs(os.path.join(RAIZ, 'dados'), exist_ok=True)
json.dump(out, open(os.path.join(RAIZ, 'dados', 'dados.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok', out['atualizado_em_texto'], len(posts), 'posts,', len(programacao), 'itens na agenda', resumo_prog)
