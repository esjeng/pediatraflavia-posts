"""Lote 3 (22/11 a 05/12/2026) — conteúdo dos posts no estilo com avatar.
Cada lista: (emoji Fluent, texto com <b>). Ritmo dos Reels: abertura 5 s; lista 4,5 s + 1 s por item; texto 6,5 s; final 4,5 s."""

FIM = """❤️ Curta, compartilhe e siga @pediatraflavia para mais dicas!

🩺 Atendimento pediátrico domiciliar em BH, Lagoa Santa e região. Agende pelo WhatsApp, link na bio."""

POSTS = [
# ------------------------------------------------------------------ 23/11 Reels convulsão febril
dict(data='2026-11-23', tipo='reels', pasta='reels-13-convulsao-febril', palavra='CONVULSÃO',
 tema='Convulsão com febre: o que fazer (e o que não fazer)',
 capa=('face-with-thermometer', 'Convulsão', 'com febre?', 'Saiba o que fazer'),
 telas=[
  ('O que é?', 'aq', [('thermometer', 'Crise que acontece com a <b>febre</b>, mais comum entre <b>6 meses e 5 anos</b>'),
                      ('check-mark-button', 'Assusta muito, mas costuma <b>passar sozinha</b> em poucos minutos')]),
  ('Durante a crise', 'pk', [('bed', 'Deite a criança <b>de lado</b>, em lugar seguro'),
                             ('hourglass-not-done', '<b>Marque o tempo</b> da crise'),
                             ('prohibited', '<b>Nada na boca</b> e não segure os movimentos')]),
  ('Não faça', 'pk', [('shower', 'Banho frio ou <b>álcool</b> no corpo'),
                      ('baby-bottle', 'Dar <b>líquido ou remédio</b> pela boca durante a crise')]),
  ('Ligue 192 se', 'nv', [('alarm-clock', 'Durar <b>mais de 5 minutos</b>'),
                          ('warning', '<b>Dificuldade para respirar</b> ou lábios arroxeados'),
                          ('sleeping-face', 'Não <b>acordar bem</b> depois da crise')]),
  ('Depois', 'aq', [('stethoscope', 'Toda <b>primeira crise</b> precisa de avaliação médica'),
                    ('telephone-receiver', 'Converse com o pediatra sobre <b>como controlar a febre</b>')]),
 ],
 story=('Convulsão com febre?', 'Saiba o que fazer &#128680;'),
 legenda=f"""Convulsão com febre: o que fazer? 🚨 Salve este vídeo!

A convulsão febril acontece com a febre e é mais comum entre 6 meses e 5 anos. Assusta muito, mas costuma passar sozinha em poucos minutos.

Durante a crise:
✔️ deite a criança de lado, em lugar seguro
✔️ marque o tempo da crise
✔️ nada na boca e não segure os movimentos

Não faça: banho frio, álcool no corpo ou dar líquido e remédio pela boca durante a crise.

🚨 Ligue 192 se a crise durar mais de 5 minutos, se houver dificuldade para respirar ou lábios arroxeados, ou se a criança não acordar bem depois.

Toda primeira crise precisa de avaliação médica. Converse com o pediatra sobre como controlar a febre.

{FIM}

#pediatra #pediatrabh #pediatralagoasanta #convulsaofebril #febre #primeirossocorros #maedeprimeiraviagem #maternidade #dicasdepediatra"""),

# ------------------------------------------------------------------ 24/11 Carrossel prematuridade
dict(data='2026-11-24', tipo='carrossel', pasta='2026-11-24-novembro-roxo-prematuridade', prefixo='prematuro', palavra='PREMATURO',
 tema='Novembro Roxo: prematuridade e idade corrigida',
 capa=('purple-heart', 'Novembro Roxo:', 'bebê prematuro', 'o que é a idade corrigida?'),
 telas=[
  ('Quem é prematuro?', 'aq', [('baby-medium-light', 'Bebê que nasce <b>antes de 37 semanas</b> de gestação'),
                               ('purple-heart', 'Novembro Roxo é o mês de <b>conscientização</b> sobre a prematuridade')]),
  ('Idade corrigida', 'pk', [('spiral-calendar', 'É a idade que o bebê teria se tivesse nascido com <b>40 semanas</b>'),
                             ('straight-ruler', 'Usada para avaliar <b>crescimento e desenvolvimento</b> até cerca de <b>2 anos</b>')]),
  ('Como calcular', 'aq', [('abacus', 'Idade atual <b>menos</b> as semanas que faltaram para 40'),
                           ('light-bulb', 'Ex.: nasceu com <b>32 semanas</b> (8 antes) e tem 6 meses → <b>4 meses corrigidos</b>')]),
  ('Atenção', 'pk', [('syringe', '<b>Vacinas</b> seguem a idade de nascimento, não a corrigida'),
                     ('soap', '<b>Mãos lavadas</b> e menos aglomeração nos primeiros meses'),
                     ('stethoscope', 'Acompanhamento <b>regular</b> com o pediatra')]),
 ],
 legenda=f"""Novembro Roxo: o mês de conscientização sobre a prematuridade 💜

É considerado prematuro o bebê que nasce antes de 37 semanas de gestação.

Idade corrigida é a idade que o bebê teria se tivesse nascido com 40 semanas. Ela é usada para avaliar o crescimento e o desenvolvimento até cerca de 2 anos.

Como calcular: idade atual menos as semanas que faltaram para 40. Exemplo: nasceu com 32 semanas (8 antes) e hoje tem 6 meses → 4 meses de idade corrigida.

Atenção:
✔️ as vacinas seguem a idade de nascimento, não a corrigida
✔️ mãos lavadas e menos aglomeração nos primeiros meses
✔️ acompanhamento regular com o pediatra

📌 Salve e envie para uma família de prematuro.

{FIM}

#pediatra #pediatrabh #pediatralagoasanta #novembroroxo #prematuridade #prematuro #idadecorrigida #maternidade #dicasdepediatra"""),

# ------------------------------------------------------------------ 25/11 Reels dengue
dict(data='2026-11-25', tipo='reels', pasta='reels-14-dengue-criancas', palavra='DENGUE',
 tema='Dengue em criança: sinais de alerta',
 capa=('mosquito', 'Dengue em criança:', 'sinais de alerta', 'Atenção quando a febre baixa'),
 telas=[
  ('Sintomas comuns', 'aq', [('thermometer', '<b>Febre alta</b> de início súbito'),
                             ('face-with-head-bandage', 'Dor no corpo, na cabeça e <b>atrás dos olhos</b>'),
                             ('red-circle', '<b>Manchas</b> vermelhas na pele')]),
  ('Atenção!', 'pk', [('hourglass-not-done', 'Os sinais de alarme costumam surgir quando a <b>febre baixa</b>, entre o 3º e o 7º dia')]),
  ('Sinais de alarme', 'nv', [('face-vomiting', '<b>Vômitos</b> que não param ou <b>dor de barriga</b> forte'),
                              ('drop-of-blood', '<b>Sangramento</b> de nariz ou gengiva'),
                              ('sleeping-face', 'Muito <b>sonolenta</b>, irritada ou mole'),
                              ('cold-face', 'Mãos e pés <b>frios</b>, tontura ou pouco xixi')]),
  ('Em casa', 'aq', [('cup-with-straw', 'Muito <b>líquido</b>: água, soro, sucos naturais'),
                     ('prohibited', 'Nada de <b>AAS nem anti-inflamatório</b>'),
                     ('stethoscope', 'Febre? Procure <b>avaliação médica</b>')]),
 ],
 story=('Dengue em criança', 'Sinais de alerta &#129439;'),
 legenda=f"""Dengue em criança: conheça os sinais de alerta 🦟

Sintomas comuns: febre alta de início súbito, dor no corpo, na cabeça e atrás dos olhos e manchas vermelhas na pele.

⚠️ Atenção: os sinais de alarme costumam aparecer quando a febre baixa, entre o 3º e o 7º dia. Não é hora de relaxar!

🚨 Procure atendimento imediatamente se houver:
✔️ vômitos que não param ou dor de barriga forte
✔️ sangramento de nariz ou gengiva
✔️ criança muito sonolenta, irritada ou mole
✔️ mãos e pés frios, tontura ou pouco xixi

Em casa: muito líquido (água, soro, sucos naturais) e nada de AAS nem anti-inflamatório. Teve febre? Procure avaliação médica.

E não esqueça: elimine água parada e use repelente adequado para a idade.

{FIM}

#pediatra #pediatrabh #pediatralagoasanta #dengue #denguenacrianca #saudeinfantil #maedeprimeiraviagem #maternidade #dicasdepediatra"""),

# ------------------------------------------------------------------ 26/11 Carrossel brotoeja
dict(data='2026-11-26', tipo='carrossel', pasta='2026-11-26-brotoeja-miliaria', prefixo='brotoeja', palavra='BROTOEJA',
 tema='Brotoeja (miliária): como aliviar no calor',
 capa=('hot-face', 'Brotoejas', 'no calor?', 'como aliviar a miliária'),
 telas=[
  ('O que é?', 'aq', [('sweat-droplets', 'Bolinhas causadas pelo <b>suor preso</b> na pele'),
                      ('baby-medium-light', 'Comum no <b>pescoço, costas, peito</b> e dobrinhas')]),
  ('Como aliviar', 'pk', [('t-shirt', 'Roupas <b>leves</b> de algodão, sem excesso'),
                          ('bathtub', '<b>Banho morno</b> e secar bem as dobrinhas'),
                          ('wind-face', 'Ambiente <b>fresco e ventilado</b>')]),
  ('Evite', 'aq', [('lotion-bottle', '<b>Cremes e óleos</b> grossos na região'),
                   ('prohibited', 'Remédios ou pomadas <b>por conta própria</b>')]),
  ('Procure o pediatra se', 'nv', [('thermometer', 'Vier com <b>febre</b>'),
                                   ('red-circle', 'As bolinhas tiverem <b>pus</b> ou ficarem doloridas'),
                                   ('hourglass-not-done', 'Não melhorar em <b>3 a 4 dias</b> mesmo no fresco')]),
 ],
 legenda=f"""Brotoejas no calor? 🥵 Pode ser miliária!

São bolinhas causadas pelo suor preso na pele, muito comuns no pescoço, nas costas, no peito e nas dobrinhas dos bebês.

Como aliviar:
✔️ roupas leves de algodão, sem excesso de camadas
✔️ banho morno e secar bem as dobrinhas
✔️ ambiente fresco e ventilado

Evite cremes e óleos grossos na região e remédios ou pomadas por conta própria.

⚠️ Procure o pediatra se vier com febre, se as bolinhas tiverem pus ou ficarem doloridas, ou se não melhorar em 3 a 4 dias mesmo no fresco.

{FIM}

#pediatra #pediatrabh #pediatralagoasanta #brotoeja #miliaria #calor #peledobebe #maternidade #dicasdepediatra"""),

# ------------------------------------------------------------------ 27/11 Reels cólica
dict(data='2026-11-27', tipo='reels', pasta='reels-15-colica', palavra='CÓLICA',
 tema='Cólica do bebê: o que ajuda de verdade',
 capa=('loudly-crying-face', 'Cólica', 'do bebê?', 'O que ajuda de verdade'),
 telas=[
  ('É fase!', 'aq', [('spiral-calendar', 'Começa nas <b>primeiras semanas</b> e costuma melhorar até os <b>3 a 4 meses</b>'),
                     ('crescent-moon', 'Choro forte, muitas vezes no <b>fim da tarde</b>')]),
  ('O que ajuda', 'pk', [('people-hugging', '<b>Colo</b>, contato pele a pele e balanço suave'),
                         ('raised-hand-medium-light', '<b>Massagem</b> na barriga e bicicletinha'),
                         ('musical-notes', 'Ambiente <b>calmo</b>, luz baixa e som suave')]),
  ('Evite', 'aq', [('teacup-without-handle', '<b>Chás</b> e remédios sem orientação'),
                   ('red-heart', 'Se cuidar também: <b>peça ajuda</b> e reveze com alguém')]),
  ('Procure o pediatra se', 'nv', [('thermometer', '<b>Febre</b> ou vômitos'),
                                   ('baby-bottle', '<b>Recusa</b> mamar ou não ganha peso'),
                                   ('warning', 'Choro <b>diferente</b> do habitual ou que não acalma')]),
 ],
 story=('Cólica do bebê?', 'O que ajuda &#128118;'),
 legenda=f"""Cólica do bebê: o que ajuda de verdade? 👶

A cólica começa nas primeiras semanas e costuma melhorar até os 3 a 4 meses. O choro é forte e muitas vezes aparece no fim da tarde.

O que ajuda:
✔️ colo, contato pele a pele e balanço suave
✔️ massagem na barriga e bicicletinha com as perninhas
✔️ ambiente calmo, luz baixa e som suave

Evite chás e remédios sem orientação. E cuide de você também: peça ajuda e reveze com alguém. 💛

⚠️ Procure o pediatra se houver febre, vômitos, recusa para mamar, pouco ganho de peso ou choro diferente do habitual, que não acalma.

{FIM}

#pediatra #pediatrabh #pediatralagoasanta #colicadobebe #colica #recemnascido #maedeprimeiraviagem #maternidade #dicasdepediatra"""),

# ------------------------------------------------------------------ 28/11 Carrossel mito banho depois de comer
dict(data='2026-11-28', tipo='carrossel', pasta='2026-11-28-mito-banho-depois-comer', prefixo='congestao', palavra='CONGESTÃO',
 tema='Mito ou verdade: banho depois de comer dá congestão?', mito=True,
 capa=('bathtub', 'Banho depois de comer', 'dá congestão?', 'mito ou verdade'),
 veredito=('MITO', 'Não existe "congestão" causada por banho depois de comer. A criança pode tomar banho e entrar na piscina sem esperar horas.'),
 telas=[
  ('Mas atenção', 'pk', [('hamburger', 'Depois de uma refeição <b>pesada</b>, nadar forte pode dar <b>desconforto</b>'),
                         ('face-vomiting', 'Na dúvida, prefira brincadeiras <b>mais calmas</b> logo após comer')]),
  ('O que importa de verdade', 'nv', [('eyes', 'Um adulto <b>olhando o tempo todo</b>, sem celular'),
                                      ('ring-buoy', 'Colete adequado: <b>boia não é babá</b>'),
                                      ('sun', '<b>Protetor solar</b>, chapéu e muita água')]),
 ],
 legenda=f"""Banho depois de comer dá congestão? 🛁 MITO!

Não existe "congestão" causada por banho depois de comer. A criança pode tomar banho e entrar na piscina sem precisar esperar horas.

Mas atenção: depois de uma refeição pesada, nadar forte pode dar desconforto. Na dúvida, prefira brincadeiras mais calmas logo após comer.

O que importa de verdade na água:
✔️ um adulto olhando o tempo todo, sem celular
✔️ colete adequado: boia não é babá
✔️ protetor solar, chapéu e muita água

{FIM}

#pediatra #pediatrabh #pediatralagoasanta #mitoouverdade #piscina #segurancanaagua #verao #maternidade #dicasdepediatra"""),

# ------------------------------------------------------------------ 29/11 Carrossel desfralde
dict(data='2026-11-29', tipo='carrossel', pasta='2026-11-29-desfralde-sinais', prefixo='desfralde', palavra='DESFRALDE',
 tema='Desfralde: 5 sinais de que é hora',
 capa=('toilet', 'Desfralde:', '5 sinais de que é hora', 'sem pressa e sem pressão'),
 telas=[
  ('5 sinais', 'aq', [('hourglass-not-done', 'Fica <b>seco por 2 horas</b> ou mais'),
                      ('speaking-head', '<b>Avisa</b> que fez ou que vai fazer'),
                      ('eyes', 'Mostra <b>interesse</b> pelo banheiro'),
                      ('jeans', 'Tenta <b>tirar a roupa</b> sozinho'),
                      ('ear', 'Entende <b>pedidos simples</b>')]),
  ('Quando?', 'pk', [('spiral-calendar', 'Em geral entre <b>18 meses e 3 anos</b>: cada criança tem o seu tempo')]),
  ('Dicas', 'aq', [('teddy-bear', 'Penico ou redutor <b>sem pressão</b>'),
                   ('clapping-hands-medium-light', '<b>Elogie</b> as tentativas; escapes são normais'),
                   ('crescent-moon', 'A <b>noite</b> costuma vir depois do dia')]),
 ],
 legenda=f"""Desfralde: 5 sinais de que é hora 🚽

1️⃣ fica seco por 2 horas ou mais
2️⃣ avisa que fez ou que vai fazer
3️⃣ mostra interesse pelo banheiro
4️⃣ tenta tirar a roupa sozinho
5️⃣ entende pedidos simples

Em geral acontece entre 18 meses e 3 anos, e cada criança tem o seu tempo.

Dicas: penico ou redutor sem pressão, elogie as tentativas (escapes são normais!) e lembre que a noite costuma vir depois do dia.

Na dúvida, converse com o pediatra na consulta. 💛

{FIM}

#pediatra #pediatrabh #pediatralagoasanta #desfralde #tirarafralda #desenvolvimentoinfantil #maedeprimeiraviagem #maternidade #dicasdepediatra"""),

# ------------------------------------------------------------------ 30/11 Reels chupeta
dict(data='2026-11-30', tipo='reels', pasta='reels-16-chupeta', palavra='CHUPETA',
 tema='Chupeta: quando e como tirar',
 capa=('baby-bottle', 'Chupeta:', 'quando tirar?', 'Sem trauma'),
 telas=[
  ('Quando?', 'aq', [('spiral-calendar', 'O ideal é tirar até os <b>2 a 3 anos</b>'),
                     ('tooth', 'Depois disso aumenta o risco de alterar <b>dentes e fala</b>')]),
  ('Como tirar', 'pk', [('hourglass-not-done', '<b>Aos poucos</b>: primeiro só para dormir'),
                        ('teddy-bear', 'Troque por <b>colo</b>, naninha e rotina'),
                        ('speech-balloon', '<b>Converse</b> e envolva a criança na decisão')]),
  ('Evite', 'aq', [('honey-pot', 'Passar <b>açúcar, mel ou pimenta</b> na chupeta'),
                   ('prohibited', 'Tirar em meio a <b>grandes mudanças</b> (irmão, escola, mudança)')]),
 ],
 story=('Chupeta: quando tirar?', 'A pediatra explica &#128118;'),
 legenda=f"""Chupeta: quando e como tirar? 👶

O ideal é tirar até os 2 a 3 anos. Depois disso aumenta o risco de alterar os dentes e a fala.

Como tirar:
✔️ aos poucos: primeiro deixe só para dormir
✔️ troque por colo, naninha e rotina
✔️ converse e envolva a criança na decisão

Evite passar açúcar, mel ou pimenta na chupeta e evite tirar em meio a grandes mudanças, como a chegada de um irmão, o início da escola ou uma mudança de casa.

Paciência: alguns dias de choro são normais. 💛

{FIM}

#pediatra #pediatrabh #pediatralagoasanta #chupeta #tirarachupeta #desenvolvimentoinfantil #maedeprimeiraviagem #maternidade #dicasdepediatra"""),

# ------------------------------------------------------------------ 01/12 Carrossel queimadura solar
dict(data='2026-12-01', tipo='carrossel', pasta='2026-12-01-queimadura-solar', prefixo='solar', palavra='QUEIMADURA',
 tema='Dezembro Laranja: queimadura de sol na criança, o que fazer',
 capa=('sun', 'Queimadura', 'de sol?', 'o que fazer · Dezembro Laranja'),
 telas=[
  ('Na hora', 'aq', [('house', 'Saia do sol e vá para a <b>sombra</b>'),
                     ('droplet', '<b>Compressas frias</b> e banho em água fresca'),
                     ('cup-with-straw', 'Ofereça bastante <b>líquido</b>')]),
  ('Não faça', 'pk', [('butter', '<b>Manteiga</b>, pasta de dente ou receitas caseiras'),
                      ('prohibited', '<b>Estourar</b> as bolhas')]),
  ('Procure o pediatra se', 'nv', [('baby-medium-light', 'For um bebê com <b>menos de 1 ano</b>'),
                                   ('red-circle', '<b>Bolhas</b> grandes ou em uma área extensa'),
                                   ('thermometer', '<b>Febre</b>, calafrios, vômitos ou muito abatido')]),
  ('Previna', 'aq', [('lotion-bottle', '<b>Protetor</b> a partir dos 6 meses, reaplicado a cada 2 h'),
                     ('billed-cap', '<b>Chapéu</b>, roupa com proteção UV e sombra'),
                     ('alarm-clock', 'Evite o sol das <b>10h às 16h</b>')]),
 ],
 legenda=f"""Queimadura de sol na criança: o que fazer? ☀️ Dezembro Laranja é o mês de prevenção do câncer de pele.

Na hora:
✔️ saia do sol e vá para a sombra
✔️ compressas frias e banho em água fresca
✔️ ofereça bastante líquido

Não faça: manteiga, pasta de dente ou receitas caseiras, e não estoure as bolhas.

⚠️ Procure o pediatra se for um bebê com menos de 1 ano, se houver bolhas grandes ou em área extensa, ou febre, calafrios, vômitos ou criança muito abatida.

Previna: protetor a partir dos 6 meses, reaplicado a cada 2 horas, chapéu, roupa com proteção UV, sombra e nada de sol das 10h às 16h.

{FIM}

#pediatra #pediatrabh #pediatralagoasanta #dezembrolaranja #queimadurasolar #protetorsolar #verao #maternidade #dicasdepediatra"""),

# ------------------------------------------------------------------ 02/12 Reels tosse
dict(data='2026-12-02', tipo='reels', pasta='reels-17-tosse', palavra='TOSSE',
 tema='Tosse na criança: quando se preocupar',
 capa=('face-with-medical-mask', 'Tosse:', 'quando se preocupar?', 'Sinais de alerta'),
 telas=[
  ('Tosse é defesa', 'aq', [('microbe', 'Ajuda a <b>limpar</b> as vias respiratórias'),
                            ('hourglass-not-done', 'Depois de um resfriado pode durar <b>2 a 3 semanas</b>')]),
  ('O que ajuda', 'pk', [('droplet', '<b>Lavagem nasal</b> com soro'),
                         ('cup-with-straw', 'Muita <b>água</b> ao longo do dia'),
                         ('honey-pot', '<b>Mel</b> só depois de 1 ano'),
                         ('prohibited', 'Xarope para tosse só <b>com orientação</b>')]),
  ('Procure atendimento se', 'nv', [('wind-face', 'Respiração <b>rápida</b> ou costelas afundando'),
                                    ('cold-face', 'Lábios <b>arroxeados</b> ou chiado no peito'),
                                    ('thermometer', '<b>Febre</b> por mais de 3 dias'),
                                    ('baby-medium-light', 'Bebê com <b>menos de 3 meses</b>')]),
 ],
 story=('Tosse na criança?', 'Quando se preocupar &#128567;'),
 legenda=f"""Tosse na criança: quando se preocupar? 😷

A tosse é uma defesa do corpo: ajuda a limpar as vias respiratórias. Depois de um resfriado, ela pode durar de 2 a 3 semanas.

O que ajuda:
✔️ lavagem nasal com soro
✔️ muita água ao longo do dia
✔️ mel, só depois de 1 ano
✔️ xarope para tosse, só com orientação

🚨 Procure atendimento se houver respiração rápida, costelas afundando ao respirar, lábios arroxeados, chiado no peito, febre por mais de 3 dias ou se for um bebê com menos de 3 meses.

{FIM}

#pediatra #pediatrabh #pediatralagoasanta #tosse #resfriado #saudeinfantil #maedeprimeiraviagem #maternidade #dicasdepediatra"""),

# ------------------------------------------------------------------ 03/12 Carrossel mãos-pés-boca
dict(data='2026-12-03', tipo='carrossel', pasta='2026-12-03-maos-pes-boca', prefixo='mpb', palavra='MÃOS-PÉS-BOCA',
 tema='Doença mãos-pés-boca: sinais e cuidados',
 capa=('raised-hand-medium-light', 'Mãos, pés', 'e boca', 'sinais e cuidados da virose'),
 telas=[
  ('O que é?', 'aq', [('microbe', 'Virose <b>comum</b> em crianças pequenas, principalmente em creches'),
                      ('people-hugging', 'Passa por <b>contato</b>, saliva, secreções e fezes')]),
  ('Sinais', 'pk', [('thermometer', '<b>Febre</b> e mal-estar'),
                    ('drooling-face', '<b>Aftas</b> na boca: dói para comer'),
                    ('red-circle', 'Bolinhas nas <b>mãos, pés</b> e bumbum')]),
  ('Cuidados', 'aq', [('soft-ice-cream', 'Alimentos <b>frios e pastosos</b>'),
                      ('cup-with-straw', 'Muita <b>hidratação</b>'),
                      ('soap', '<b>Lave as mãos</b>, inclusive depois de trocar fraldas')]),
  ('Procure o pediatra se', 'nv', [('cup-with-straw', 'Não consegue <b>beber</b> ou faz pouco xixi'),
                                   ('thermometer', '<b>Febre</b> por mais de 3 dias'),
                                   ('sleeping-face', 'Muito <b>sonolenta</b> ou irritada')]),
 ],
 legenda=f"""Doença mãos-pés-boca: sinais e cuidados ✋🦶👄

É uma virose comum em crianças pequenas, principalmente em creches. Passa por contato, saliva, secreções e fezes.

Sinais:
✔️ febre e mal-estar
✔️ aftas na boca, que doem para comer
✔️ bolinhas nas mãos, nos pés e no bumbum

Cuidados: alimentos frios e pastosos, muita hidratação e mãos bem lavadas, inclusive depois de trocar fraldas. A volta à creche deve ser combinada com o pediatra.

⚠️ Procure o pediatra se a criança não conseguir beber, fizer pouco xixi, tiver febre por mais de 3 dias ou estiver muito sonolenta ou irritada.

{FIM}

#pediatra #pediatrabh #pediatralagoasanta #maospesboca #virose #creche #saudeinfantil #maternidade #dicasdepediatra"""),

# ------------------------------------------------------------------ 04/12 Reels medir febre
dict(data='2026-12-04', tipo='reels', pasta='reels-18-medir-febre', palavra='TERMÔMETRO',
 tema='Febre: como medir a temperatura do jeito certo',
 capa=('thermometer', 'Como medir', 'a febre?', 'Do jeito certo'),
 telas=[
  ('Use', 'aq', [('thermometer', 'Termômetro <b>digital</b> (nada de mercúrio)'),
                 ('raised-hand-medium-light', 'Mão na testa <b>não é confiável</b>')]),
  ('Passo a passo', 'pk', [('droplet', '<b>Seque</b> a axila'),
                           ('hourglass-not-done', 'Mantenha o braço junto ao corpo até <b>apitar</b>'),
                           ('bathtub', 'Não meça logo <b>depois do banho</b> ou com muita roupa')]),
  ('É febre quando', 'aq', [('chart-increasing', 'A temperatura na axila chega a <b>37,8 °C</b> ou mais')]),
  ('Procure atendimento', 'nv', [('baby-medium-light', 'Bebê com <b>menos de 3 meses</b> com febre'),
                                 ('hourglass-not-done', 'Febre por <b>mais de 3 dias</b>'),
                                 ('sleeping-face', 'Criança <b>abatida</b> mesmo sem febre')]),
 ],
 story=('Como medir a febre?', 'Do jeito certo &#127777;&#65039;'),
 legenda=f"""Febre: como medir a temperatura do jeito certo? 🌡️

Use termômetro digital (nada de mercúrio). Mão na testa não é confiável!

Passo a passo:
✔️ seque a axila
✔️ mantenha o braço junto ao corpo até o termômetro apitar
✔️ não meça logo depois do banho ou com a criança muito agasalhada

É febre quando a temperatura na axila chega a 37,8 °C ou mais.

⚠️ Procure atendimento se for um bebê com menos de 3 meses com febre, se a febre durar mais de 3 dias ou se a criança estiver abatida, mesmo sem febre.

{FIM}

#pediatra #pediatrabh #pediatralagoasanta #febre #termometro #saudeinfantil #maedeprimeiraviagem #maternidade #dicasdepediatra"""),

# ------------------------------------------------------------------ 05/12 Carrossel festas e engasgo
dict(data='2026-12-05', tipo='carrossel', pasta='2026-12-05-festas-engasgo', prefixo='festas', palavra='FESTAS',
 tema='Festas de fim de ano: alimentos que engasgam os pequenos',
 capa=('christmas-tree', 'Ceia de fim de ano:', 'cuidado com o engasgo', 'alimentos de risco para os pequenos'),
 telas=[
  ('Risco antes dos 4 anos', 'pk', [('grapes', '<b>Uva</b> e tomate-cereja inteiros'),
                                    ('peanuts', '<b>Castanhas</b>, nozes e amendoim'),
                                    ('popcorn', '<b>Pipoca</b> e balas duras'),
                                    ('hot-dog', '<b>Salsicha</b> em rodelas')]),
  ('Como oferecer', 'aq', [('kitchen-knife', 'Corte uva e salsicha <b>no comprido</b>, em pedaços pequenos'),
                           ('chair', 'Criança <b>sentada</b>, sem correr comendo'),
                           ('eyes', 'Sempre com um <b>adulto</b> por perto')]),
  ('Na festa', 'pk', [('wrapped-gift', 'Petiscos <b>longe do alcance</b> dos pequenos'),
                      ('telephone-receiver', 'Engasgo grave? Ligue <b>192</b> e faça a manobra certa para a idade')]),
 ],
 legenda=f"""Ceia de fim de ano: cuidado com o engasgo! 🎄

Alimentos de risco antes dos 4 anos:
⚠️ uva e tomate-cereja inteiros
⚠️ castanhas, nozes e amendoim
⚠️ pipoca e balas duras
⚠️ salsicha em rodelas

Como oferecer:
✔️ corte uva e salsicha no comprido, em pedaços pequenos
✔️ criança sentada, sem correr comendo
✔️ sempre com um adulto por perto

Na festa, deixe os petiscos longe do alcance dos pequenos. Engasgo grave? Ligue 192 e faça a manobra certa para a idade (veja o nosso Reels sobre engasgo no perfil).

📌 Salve e envie para quem vai estar na ceia com as crianças!

{FIM}

#pediatra #pediatrabh #pediatralagoasanta #engasgo #natal #segurancainfantil #festasdefimdeano #maternidade #dicasdepediatra"""),
]
