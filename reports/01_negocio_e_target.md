# Entendimento do negócio e definição da target

Tech Challenge Fase 1 · Case NPS Preditivo · itens 1 e 2

Este documento responde às perguntas dos itens 1 e 2 do desafio. É pensamento analítico, não código: os números citados vêm da base `data/raw/desafio_nps_fase_1.csv` (2.500 pedidos) e podem ser reproduzidos em `notebooks/01_preparacao_e_eda.ipynb`.

---

## 1. Entendimento do negócio

### 1.1 Qual problema de negócio está sendo resolvido?

Uma empresa de e-commerce cresceu rápido e passou a lidar com muito mais pedidos, entregas e contatos de clientes. A área de Experiência do Cliente notou algo que os indicadores operacionais não explicam: pedidos que parecem iguais no papel geram clientes promotores e clientes detratores.

Há dois problemas ligados:

- **Não sabemos o que causa a diferença.** Falta saber quais fatores operacionais (pedido, entrega, atendimento) de fato mexem na satisfação.
- **Descobrimos tarde.** O NPS só é coletado depois que a jornada de compra termina. Quando a nota chega, a frustração já aconteceu e o momento de evitá-la passou.

A pergunta que orienta o trabalho é:

> **Quais fatores operacionais mais explicam a nota de satisfação do cliente e que sinais, já conhecidos antes da pesquisa, permitiriam agir a tempo sobre os pedidos com risco de gerar detratores?**

A base mostra que o problema não é pequeno: **84% dos pedidos são detratores e o NPS é cerca de −80**. Vale ressalvar desde já que a base parece sintética (padrões muito regulares), então esse nível extremo não deve ser lido como retrato de uma empresa real.

### 1.2 Por que o NPS é importante para um e-commerce?

O NPS (Net Promoter Score, proposto por Fred Reichheld em 2003) pergunta o quanto o cliente indicaria a empresa e resume a resposta em um número: % de promotores menos % de detratores. É útil no e-commerce por quatro motivos:

- **É simples e comparável.** Um número só, acompanhado ao longo do tempo e entre períodos, canais e regiões.
- **Está ligado a crescimento.** Promotores tendem a comprar de novo e indicar; detratores tendem a deixar de comprar e a falar mal.
- **Ajuda a controlar custo.** Reter e indicar costuma sair mais barato do que adquirir cliente novo em mídia paga.
- **Funciona como alarme.** Uma queda no NPS pode sinalizar o problema antes de ele aparecer em vendas ou em recompra.

Como todo indicador resumido, ele diz *que* algo está errado, não *o que*. Por isso o trabalho precisa cruzar a nota com dados da operação.

### 1.3 Quais áreas se beneficiam desses insights?

| Área | O que a base indica | Ação possível |
|---|---|---|
| **Logística** | Atraso é o maior fator da nota (correlação −0,59). Com 2 dias de atraso, 88% dos pedidos são detratores. | Prometer prazos que se cumprem, avisar o cliente sobre atrasos, priorizar pedidos já atrasados. |
| **Atendimento** | Reclamações (−0,49), contatos (−0,34) e tempo de resolução (−0,19) derrubam a nota. Reclamações e contatos andam juntos (correlação 0,74). | Resolver no primeiro contato, atuar de forma proativa antes de o cliente reclamar. |
| **Produto e pricing** | Valor do pedido, desconto, parcelas e frete ficam entre −0,04 e 0,04. | Nesta base, preço e condições de pagamento **não** parecem ser a alavanca principal da satisfação. |
| **Marketing e CRM** | Região, idade e tempo de casa quase não mudam a nota. | Segmentar por perfil não ajuda. Faz mais sentido agir por evento (atraso, reclamação). |
| **Estratégia e CX** | Sinais de entrega e atendimento estão na base e podem ser acompanhados antes da pesquisa. | Criar um painel de pedidos em risco e acompanhar o % de detratores por faixa de atraso. |

### 1.4 Como o NPS impacta recompra, boca a boca e market share?

Esta é uma reflexão. A base não permite medir esses efeitos, e explico o porquê em cada ponto.

**Recompra.** Promotores tendem a comprar de novo e detratores tendem a sumir, e recompra é a forma mais direta de o NPS virar receita. A base tem a coluna `repeat_purchase_30d`, mas ela vale 1 exatamente quando a nota é 8 ou mais, em todas as linhas. Isso é uma regra, não um comportamento observado, então **não serve como prova** do efeito do NPS na recompra. Além disso, cada cliente aparece uma única vez, o que impede acompanhar a recompra ao longo do tempo.

**Boca a boca.** No digital, o boca a boca se espalha por avaliações em marketplaces, redes sociais e sites de reclamação. Um detrator pode afetar muito mais gente do que o custo de resolver o problema dele. Como o NPS é pergunta de indicação, ele é o indicador interno mais próximo desse efeito, mas a base não traz dado de avaliações públicas.

**Market share.** O efeito é indireto e mais lento: boa experiência gera retenção e indicação, que reduzem o custo de crescer e sustentam participação de mercado. Aqui o NPS é só uma peça, pois preço, variedade e marca também pesam. Não há como medir essa relação com os dados disponíveis.

### 1.5 Que indicadores de mercado complementariam a análise?

| Indicador | Para que serve | Está na base? |
|---|---|---|
| **Benchmark de NPS do setor e de concorrentes** | Dizer se o NPS é bom ou ruim em relação a quem compete (com a mesma metodologia). | Não |
| **SLA logístico** (% de entregas no prazo, dias de atraso médio) | Medir o fator que mais pesa e comparar com a promessa feita. | Parcial (`delivery_delay_days`) |
| **Taxa de contato por pedido e de reclamação** | Dimensionar o volume de problemas no atendimento. | Sim |
| **Tempo de resolução e resolução no primeiro contato** | Medir a qualidade do atendimento. | Parcial (`resolution_time_days`) |
| **Recompra real por coorte** | Verificar se promotores de fato compram mais. | Não |
| **Taxa de resposta da pesquisa** | Saber o quanto a nota representa o conjunto de clientes. | Não |
| **Avaliações públicas e reclamações em sites** | Medir o boca a boca. | Não |
| **Custo de um pedido problemático** (reenvio, atendimento, desconto) | Comparar o custo de prevenir com o de corrigir. | Não |
| **Participação de mercado e concorrência** | Situar a empresa no setor. | Não |

### 1.6 Do problema de negócio ao problema analítico

| | Objetivo de negócio | Objetivo analítico |
|---|---|---|
| **O que se quer** | Reduzir detratores e elevar o NPS. | Explicar a nota com dados operacionais e, se houver modelo, antecipá-la. |
| **Como medir** | NPS, % de detratores, % de pedidos com atraso, taxa de reclamação. | Na EDA: correlações e comparações por faixa. Em um modelo (item 4, opcional): ver abaixo. |

Se o modelo do item 4 for desenvolvido, as métricas devem seguir o **custo do erro**:

- **Classificação (detrator × não detrator).** Deixar passar um detrator significa um cliente insatisfeito sem nenhuma ação. Um alarme falso custa apenas uma ação preventiva à toa (por exemplo, um aviso proativo). Por isso a prioridade é a **revocação (recall) dos detratores**, com precisão aceitável, e o ponto de corte do modelo deve respeitar a capacidade da equipe de agir. Acurácia não serve sozinha: com 84% de detratores, chutar "detrator" sempre já acerta 84%.
- **Regressão (nota de 0 a 10).** MAE e RMSE, que dão o erro médio em pontos de nota, e R² para ver quanto da variação o modelo explica.

---

## 2. Definição da target

### 2.1 Qual variável representa a satisfação do cliente?

**`nps_score`**, a nota de satisfação do cliente, de 0 a 10, presente nos 2.500 pedidos.

### 2.2 Por que ela foi escolhida?

- **Mede a satisfação diretamente**, pela voz do cliente, e é o indicador que a Experiência do Cliente já acompanha.
- **É o resultado que o negócio quer mover.** Tudo o mais na base (entrega, atendimento, pedido) é causa ou contexto.
- **Tem escala de 0 a 10**, que permite tanto tratá-la como número (regressão) quanto agrupá-la em detrator, neutro e promotor (classificação).

As outras duas candidatas foram descartadas como alvo:

| Variável | Por que não é o alvo |
|---|---|
| `csat_internal_score` | É um score interno, de origem não explicada no enunciado, com 462 zeros e correlação de 0,56 com a nota. Mede algo parecido, e não sabemos quando é medido em relação à nota. |
| `repeat_purchase_30d` | Mede comportamento, não satisfação, e é igual a 1 exatamente quando a nota é 8 ou mais. |

### 2.3 Em que momento da jornada a informação é coletada?

Segundo o enunciado, a nota é coletada **depois da experiência de compra, no encerramento da jornada**. Isso tem uma consequência prática: qualquer variável usada para explicar ou prever a nota precisa existir **antes** dela.

Pedido, entrega e atendimento cumprem isso. Mas há um ponto de atenção. Contatos, reclamações e tempo de resolução acontecem no pós-venda. Se a ideia for avisar a equipe logo no despacho, esses dados ainda não existem. Será preciso definir **em que ponto da jornada a previsão é feita** e usar só o que já se sabe até ali. A base não tem datas nem horários, então não dá para conferir a ordem dos eventos. Essa é uma limitação.

### 2.4 Regra de corte: detrator, neutro e promotor

Pela convenção do NPS, detrator é nota de 0 a 6, neutro 7 e 8, promotor 9 e 10. Como a nota desta base é **fracionada** (101 valores distintos, só 17% inteiros), adotamos a mesma convenção **sem arredondar**:

| Classe | Regra | Pedidos | % | Nota média |
|---|---|---|---|---|
| Detrator | nota < 7 | 2.109 | 84,4% | 3,65 |
| Neutro | 7 ≤ nota < 9 | 281 | 11,2% | 7,79 |
| Promotor | nota ≥ 9 | 110 | 4,4% | 9,61 |

**NPS = 4,4% − 84,4% = −80 pontos.**

A regra importa: se a nota fosse arredondada para inteiro antes da classificação, o NPS iria para cerca de −73. Isso porque 134 pedidos (de 6,5 a 6,99) passariam de detrator a neutro e 46 (de 8,5 a 8,99) de neutro a promotor. A mesma regra deve ser usada nos slides e em qualquer modelo.

### 2.5 Existe risco de usar essa variável de forma inadequada?

Sim. Os principais:

1. **Vazamento (leakage).** `repeat_purchase_30d` é a nota em outra forma e `csat_internal_score` tem relação forte com ela e momento de medição desconhecido. Usá-las para prever a nota daria um modelo aparentemente perfeito e inútil na prática. Ficam **fora** de qualquer modelo.
2. **Viés de resposta.** O NPS vem de quem respondeu. Quem responde pode ser diferente de quem não responde, e a taxa de resposta não é conhecida.
3. **Desbalanceamento.** São 84% de detratores e só 110 promotores. Um modelo de três classes teria poucos exemplos de promotor, e a acurácia enganaria. Recomenda-se agrupar em **detrator × não detrator** ou usar regressão, dividir os dados de forma estratificada e olhar as métricas por classe.
4. **Piso da escala e origem da nota.** 158 pedidos (6,3%) têm nota exatamente 0, bem acima das notas vizinhas, o que sugere que a nota é cortada no piso da escala. Nota fracionada também não é comum em pesquisa real (que costuma ser inteira). Pode ser uma média de respostas, um cálculo ou dado simulado. Vale confirmar com a origem dos dados.
5. **Nota individual não é o NPS da empresa.** O NPS é um índice calculado sobre um grupo. Em cada pedido, o que existe é uma nota. Falar em "NPS de um cliente" é um atalho que pode confundir.
6. **Correlação não é causa.** A base é observacional. Os fatores identificados indicam onde olhar, não provam que corrigi-los vai elevar a nota.
7. **Qualidade dos dados.** 673 linhas (27%) têm alguma inconsistência, como atraso maior que o tempo total de entrega. Elas foram sinalizadas e mantidas.
8. **Uso sobre pessoas.** Uma nota prevista serve para priorizar uma ação de cuidado com o cliente, não para penalizar cliente ou atendente.
9. **Mudança ao longo do tempo.** Se a empresa melhorar a logística, a relação entre atraso e nota muda, e um modelo treinado antes deixa de valer. Exigiria monitoramento.

---

## 3. O que vem a seguir

Com a target definida, a EDA (item 3) responde o que mais gera detratores, onde está o ponto de ruptura e que perfil de cliente tem nota mais alta ou mais baixa. O resultado está em `notebooks/01_preparacao_e_eda.ipynb` e vai virar a história dos slides.
