# Tech Challenge Fase 1 · Case NPS Preditivo

Pós-graduação FIAP em Ciência de Dados com IA.

## Objetivo

Entender o que leva um cliente a dar uma nota baixa depois de uma compra e onde a operação pode agir.
O trabalho cobre o entendimento do negócio, a definição da target (`nps_score`) e uma análise exploratória com foco em negócio.
O modelo preditivo (item opcional) entra se o prazo permitir.

## Base de dados

`data/raw/desafio_nps_fase_1.csv` · 2.500 pedidos, 19 colunas, sem nulos nem duplicados.

| Grupo | Colunas |
|---|---|
| Cliente | `customer_id`, `customer_age`, `customer_region`, `customer_tenure_months` |
| Pedido | `order_id`, `order_value`, `items_quantity`, `discount_value`, `payment_installments` |
| Logística | `delivery_time_days`, `delivery_delay_days`, `freight_value`, `delivery_attempts` |
| Atendimento | `customer_service_contacts`, `resolution_time_days`, `complaints_count` |
| Resultado | `nps_score` (target), `repeat_purchase_30d`, `csat_internal_score` |

A base original não é alterada. Tudo que é derivado vai para `data/processed/`.

## Documentos

- [`reports/01_negocio_e_target.md`](reports/01_negocio_e_target.md): entendimento do negócio (item 1) e definição da target (item 2).
- [`notebooks/01_preparacao_e_eda.ipynb`](notebooks/01_preparacao_e_eda.ipynb): preparação da base e análise exploratória (item 3).

## Metodologia

1. **Qualidade:** checagem de nulos, duplicados e linhas que se contradizem. As linhas inconsistentes são **sinalizadas** (`flag_*`), não removidas.
2. **Target:** `nps_score` é fracionado (0 a 10). Regra de corte, sem arredondar: **detrator < 7**, **neutro de 7 até < 9**, **promotor ≥ 9**. NPS = % promotores − % detratores.
3. **Vazamento:** `repeat_purchase_30d` (igual a 1 exatamente quando a nota é ≥ 8) e `csat_internal_score` (momento de medição desconhecido) ficam fora de qualquer modelo para evitar vazamento (`src/prep.py`, `LEAKAGE_COLS`).
4. **EDA com foco em negócio:** correlação de Spearman, cortes por dias de atraso, atendimento e perfil do cliente, com testes simples de apoio (Kruskal-Wallis, Mann-Whitney).

## Principais achados

- 84% dos pedidos são detratores e o NPS é cerca de −80.
- O atraso na entrega é o maior fator (Spearman −0,59); o tempo total de entrega não pesa, então o cliente reage à promessa não cumprida.
- O percentual de detratores sobe de 52% sem atraso para 88% com 2 dias e 97% com 3 dias.
- Reclamações (−0,49) e contatos com o atendimento (−0,34) também pesam, e têm pouca ligação com o atraso (correlação de −0,02 e 0,19).
- Região, idade e tempo de casa praticamente não mudam a nota.

São leituras exploratórias de uma base observacional: apontam onde olhar, não provam efeito de uma ação.

## Estrutura

```
.
├── data/
│   ├── raw/          # base original (não editar)
│   └── processed/    # base preparada (gerada pelo notebook)
├── notebooks/
│   └── 01_preparacao_e_eda.ipynb
├── src/
│   └── prep.py       # regra de corte, flags de qualidade, pipeline
├── models/           # modelos treinados (se houver)
├── reports/
│   ├── 01_negocio_e_target.md   # itens 1 e 2: negócio e definição da target
│   └── figures/      # gráficos usados nos slides
├── environment.yml
├── requirements.txt
└── .pre-commit-config.yaml
```

## Como reproduzir

Com conda:

```bash
conda env create -f environment.yml
conda activate nps-fase1
jupyter lab
```

Ou com venv:

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter lab
```

Abra `notebooks/01_preparacao_e_eda.ipynb` e rode todas as células. O notebook lê `data/raw/`, salva `data/processed/nps_preparado.csv` e os gráficos em `reports/figures/`.

Opcional, para padronizar o código de `src/`:

```bash
pre-commit install
```

## Limitações

- Não há coluna de data: não é possível dividir treino e teste por período nem ver tendência. Um eventual modelo usa divisão aleatória estratificada.
- A base parece sintética (padrões muito regulares). As conclusões valem para esta base.
- Correlação não é causa.

## Autoria

Giovana Pereira · trabalho individual.
