"""Gera dados/dados.json (painel público do @pediatraflavia) a partir das respostas
salvas do Windsor.ai e do Gmail.

Uso: python3 scripts/gerar_dados.py <pasta_entrada>
Arquivos esperados na pasta de entrada (resposta da ferramenta, como veio):
  perfil.json   Windsor get_data: username, followers_count, media_count
  diario.json   Windsor get_data: date, reach, views, accounts_engaged, reach_followers,
                reach_non_followers, profile_links_taps (últimos 180 dias)
  cidades.json  Windsor get_data: city, audience_city_size
  publico.json  Windsor get_data: audience_gender_age_name, audience_gender_age_size
  novos.json    Windsor get_data: date, follower_count_1d (últimos 30 dias, até ontem)
  stories.json  Windsor get_data: story_id, story_timestamp, story_reach, story_views, story_replies, story_interactions
  posts.json    Windsor get_data: media_id, timestamp, media_type, media_caption, media_permalink,
                media_reach, media_views, media_saved, media_shares, media_like_count, media_comments_count,
                media_reel_avg_watch_time, media_reel_skip_rate
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
           'reels': '1a144974d4e71fc1', 'reels5': '1a144c436b301612',
           'congresso': '1a14f194cb4f41ff', 'diamedico': '1a150259c0ea27fd'}


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

# Diário: últimos 180 dias, dias sem registro = 0
d_in = {str(r.get('date'))[:10]: r for r in rows('diario.json')}
diario = []
for i in range(179, -1, -1):
    d = (hoje - timedelta(days=i)).isoformat()
    r = d_in.get(d, {})
    diario.append({'data': d, 'alcance': int(num(r.get('reach'))), 'visualizacoes': int(num(r.get('views'))),
                   'contas_engajadas': int(num(r.get('accounts_engaged'))),
                   'alcance_seguidores': int(num(r.get('reach_followers'))),
                   'alcance_nao_seguidores': int(num(r.get('reach_non_followers'))),
                   'cliques_link_perfil': int(num(r.get('profile_links_taps')))})


def resumo(dias):
    return {k: sum(x[k] for x in dias) for k in ['alcance', 'visualizacoes', 'contas_engajadas', 'alcance_seguidores',
                                               'alcance_nao_seguidores', 'cliques_link_perfil']}


resumo_30d, resumo_90d, resumo_180d = resumo(diario[-30:]), resumo(diario[-90:]), resumo(diario)

# Público
cidades = []
for r in rows('cidades.json'):
    c = str(r.get('city') or '')
    nome, _, uf = c.partition(', ')
    cidades.append({'cidade': nome, 'estado': uf.replace(' (state)', ''), 'seguidores': int(num(r.get('audience_city_size')))})
cidades.sort(key=lambda x: -x['seguidores'])
GEN = {'F': 'Feminino', 'M': 'Masculino', 'U': 'Não informado'}
publico = []
for r in rows('publico.json'):
    g, _, faixa = str(r.get('audience_gender_age_name') or '').partition('.')
    publico.append({'genero': GEN.get(g, g), 'faixa_etaria': faixa, 'seguidores': int(num(r.get('audience_gender_age_size')))})
publico.sort(key=lambda x: (x['genero'], x['faixa_etaria']))
por_faixa = {}
for x in publico:
    por_faixa[x['faixa_etaria']] = por_faixa.get(x['faixa_etaria'], 0) + x['seguidores']
publico_faixa = [{'faixa_etaria': k, 'seguidores': v} for k, v in sorted(por_faixa.items())]
por_gen = {}
for x in publico:
    por_gen[x['genero']] = por_gen.get(x['genero'], 0) + x['seguidores']
publico_genero = [{'genero': k, 'seguidores': v} for k, v in por_gen.items()]

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
                  'taxa_engajamento': round(100 * inter / alc, 1) if alc else 0,
                  'reels_tempo_medio_assistido': r.get('media_reel_avg_watch_time'), 'reels_taxa_pulo': r.get('media_reel_skip_rate'),
                  'legenda': leg})
posts.sort(key=lambda p: p['data_hora'][6:8] + p['data_hora'][3:5] + p['data_hora'][:2] + p['data_hora'][9:], reverse=True)
melhores = sorted(posts, key=lambda p: p['alcance'], reverse=True)[:10]
por_formato = []
for f in ['Reels', 'Carrossel', 'Imagem']:
    g = [p for p in posts if p['formato'] == f]
    if g:
        a = sum(p['alcance'] for p in g)
        por_formato.append({'formato': f, 'posts': len(g), 'alcance_medio': round(a / len(g)),
                            'taxa_engajamento': round(100 * sum(p['interacoes'] for p in g) / a, 1) if a else 0})

# Stories: a API só dá os últimos dias; mantém o histórico já publicado no arquivo anterior
anterior = {}
try:
    anterior = json.load(open(os.path.join(RAIZ, 'dados', 'dados.json'), encoding='utf-8'))
except Exception:
    pass
st = {x['id']: x for x in anterior.get('stories', [])}
for r in rows('stories.json'):
    if not r.get('story_id'):
        continue
    t = local(r['story_timestamp'])
    st[str(r['story_id'])] = {'id': str(r['story_id']), 'data': t.strftime('%Y-%m-%d'), 'data_hora': t.strftime('%d/%m/%y %H:%M'),
                              'alcance': int(num(r.get('story_reach'))), 'visualizacoes': int(num(r.get('story_views'))),
                              'respostas': int(num(r.get('story_replies'))), 'interacoes': int(num(r.get('story_interactions'))),
                              'data_hora_iso': t.isoformat()}
stories = sorted(st.values(), key=lambda x: x.get('data_hora_iso', x['data']), reverse=True)

# Seguidores: a API não guarda histórico do total, então cada execução grava o total do dia
# (a última execução do dia fica como fechamento) e acumula os novos seguidores por dia.
hist = {x['data']: x['seguidores'] for x in anterior.get('seguidores_historico', [])}
if perfil['seguidores'] > 0:
    hist[hoje.isoformat()] = perfil['seguidores']
seguidores_historico = [{'data': d, 'seguidores': v} for d, v in sorted(hist.items())]
nv = {x['data']: x['novos'] for x in anterior.get('novos_seguidores', [])}
for r in rows('novos.json'):
    d = str(r.get('date'))[:10]
    if d and d < hoje.isoformat() and r.get('follower_count_1d') is not None:
        nv[d] = int(num(r.get('follower_count_1d')))
novos_seguidores = [{'data': d, 'novos': v} for d, v in sorted(nv.items())]


def crescimento(n):
    ini = (hoje - timedelta(days=n)).isoformat()
    pts = [x for x in seguidores_historico if x['data'] >= ini]
    novos = [x for x in novos_seguidores if x['data'] >= ini]
    c = {'horizonte_dias': n, 'seguidores_atual': perfil['seguidores'],
         'novos_seguidores': sum(x['novos'] for x in novos), 'dias_com_novos': len(novos)}
    if pts:
        c.update({'data_inicio': pts[0]['data'], 'seguidores_inicio': pts[0]['seguidores'],
                  'variacao': perfil['seguidores'] - pts[0]['seguidores'],
                  'variacao_pct': round(100 * (perfil['seguidores'] - pts[0]['seguidores']) / pts[0]['seguidores'], 2) if pts[0]['seguidores'] else 0,
                  'dias_com_total': len(pts), 'periodo_completo': pts[0]['data'] <= (hoje - timedelta(days=n - 1)).isoformat()})
        # Deixaram de seguir (estimativa) = novos no mesmo intervalo - variação do total
        nv_int = sum(x['novos'] for x in novos_seguidores if pts[0]['data'] <= x['data'] < hoje.isoformat())
        c['deixaram_de_seguir_estimado'] = max(0, nv_int - c['variacao'])
    c['serie'] = pts
    return c


crescimento_seguidores = {'30d': crescimento(30), '90d': crescimento(90), '180d': crescimento(180)}

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
    ini_leg = p.get('legenda_inicio') or ''
    pub = any(x['data'] == p['data'] and x['formato'] in tipos and x['legenda'].startswith(ini_leg) for x in posts)
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
ASSUNTO = {'carrosseis': 'Carrosséis Lavagem nasal e Marcos do 1º ano', 'carrossel19': 'Carrossel Introdução alimentar',
           'reels': 'Reels Bebê de 4 meses', 'reels5': '5 Reels novos (21/10 a 04/11)',
           'congresso': 'Reels Congresso de Pediatria (18/10)',
           'diamedico': 'Reels Dia do Médico (18/10)'}
aprovacoes = []
for nome, ms in msgs.items():
    for m in ms:
        t = datetime.strptime(str(m.get('date'))[:19], '%Y-%m-%dT%H:%M:%S').replace(tzinfo=timezone.utc).astimezone(BRT)
        txt = re.split(r'Atenciosamente|\bEm \d{1,2} de |&gt;|>|-----', str(m.get('snippet') or ''), flags=re.I)[0].strip()
        aprovacoes.append({'conversa': ASSUNTO.get(nome, nome), 'data_hora': t.strftime('%d/%m/%y %H:%M'), 'resposta': txt, 'data_hora_iso': t.isoformat()})
aprovacoes.sort(key=lambda x: x['data_hora_iso'], reverse=True)
cont = lambda *s: sum(1 for x in programacao if x['situacao'] in s)
resumo_prog = {'agendados': cont('Agendado'), 'aguardando_aprovacao': cont('Aguardando aprovação', 'Ajustes pedidos'),
               'sem_conteudo': cont('Sem conteúdo', 'Não publicado'), 'publicados': cont('Publicado')}

out = {
    'atualizado_em': agora.isoformat(timespec='seconds'),
    'atualizado_em_texto': agora.strftime('%d/%m/%y %H:%M'),
    'perfil': perfil, 'resumo_30d': resumo_30d, 'resumo_90d': resumo_90d, 'resumo_180d': resumo_180d, 'diario': diario,
    'publico_cidades': cidades, 'publico_genero_idade': publico, 'publico_faixa_etaria': publico_faixa,
    'publico_genero': publico_genero,
    'seguidores_historico': seguidores_historico, 'novos_seguidores': novos_seguidores,
    'crescimento_seguidores': crescimento_seguidores, 'stories': stories, 'aprovacoes': aprovacoes,
    'por_formato': por_formato, 'melhores_posts': melhores, 'posts': posts,
    'programacao': programacao, 'resumo_programacao': resumo_prog,
}
os.makedirs(os.path.join(RAIZ, 'dados'), exist_ok=True)
json.dump(out, open(os.path.join(RAIZ, 'dados', 'dados.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok', out['atualizado_em_texto'], len(posts), 'posts,', len(programacao), 'itens na agenda', resumo_prog)
