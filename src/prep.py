"""Preparação da base NPS: regra de corte, flags de qualidade e leitura.

As regras ficam aqui para que notebooks, slides e o eventual modelo usem
exatamente a mesma definição.
"""

from pathlib import Path

import numpy as np
import pandas as pd

RAW_PATH = Path("data/raw/desafio_nps_fase_1.csv")
PROCESSED_PATH = Path("data/processed/nps_preparado.csv")

# Regra de corte (decisão do grupo, sem arredondar a nota):
#   detrator  : nota <  7
#   neutro    : 7 <= nota < 9
#   promotor  : nota >= 9
CUT_DETRATOR = 7.0
CUT_PROMOTOR = 9.0

# Colunas que NÃO podem entrar em nenhum modelo que preveja nps_score.
LEAKAGE_COLS = ["repeat_purchase_30d", "csat_internal_score"]


def load_raw(path: Path = RAW_PATH) -> pd.DataFrame:
    """Lê a base bruta sem alterar nenhum valor."""
    return pd.read_csv(path)


def classify_nps(score: pd.Series) -> pd.Series:
    """Classifica a nota em detrator / neutro / promotor pela regra de corte."""
    return pd.Series(
        np.select(
            [score < CUT_DETRATOR, score < CUT_PROMOTOR],
            ["detrator", "neutro"],
            default="promotor",
        ),
        index=score.index,
        name="nps_class",
    )


def nps_value(classes: pd.Series) -> float:
    """NPS = % promotores - % detratores, em pontos (-100 a 100)."""
    shares = classes.value_counts(normalize=True)
    return 100 * (shares.get("promotor", 0.0) - shares.get("detrator", 0.0))


def add_quality_flags(df: pd.DataFrame) -> pd.DataFrame:
    """Adiciona colunas booleanas `flag_*` sem remover nenhuma linha."""
    out = df.copy()
    out["flag_atraso_maior_que_prazo"] = (
        out["delivery_delay_days"] > out["delivery_time_days"]
    )
    out["flag_desconto_maior_que_valor"] = out["discount_value"] > out["order_value"]
    out["flag_resolucao_sem_contato"] = (out["resolution_time_days"] > 0) & (
        out["customer_service_contacts"] == 0
    )
    out["flag_reclamacao_sem_contato"] = (out["complaints_count"] > 0) & (
        out["customer_service_contacts"] == 0
    )
    flag_cols = [c for c in out.columns if c.startswith("flag_")]
    out["flag_qualquer"] = out[flag_cols].any(axis=1)
    return out


def prepare(df: pd.DataFrame) -> pd.DataFrame:
    """Pipeline completo: flags de qualidade + classe de NPS."""
    out = add_quality_flags(df)
    out["nps_class"] = classify_nps(out["nps_score"])
    return out
