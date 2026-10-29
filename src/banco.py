"""Conexão com o DuckDB e funções que as etapas do pipeline usam."""
from pathlib import Path

import duckdb

RAIZ = Path(__file__).resolve().parent.parent
RAW = RAIZ / "data" / "raw"
BANCO = RAIZ / "data" / "pipeline.duckdb"
SQL = RAIZ / "sql"


def conectar(caminho: Path | str = BANCO) -> duckdb.DuckDBPyConnection:
    con = duckdb.connect(str(caminho))
    for schema in ("raw", "refined", "marts"):
        con.execute(f"create schema if not exists {schema}")
    return con


def criar_raw(con: duckdb.DuckDBPyConnection, pasta: Path = RAW) -> None:
    """A camada raw são só views apontando para os arquivos baixados.

    Nada é copiado nem alterado: se o arquivo mudar, a view mostra o arquivo novo.
    """
    con.execute(f"""
        create or replace view raw.aneel_gd as
        select * from read_parquet('{(pasta / "aneel_gd.parquet").as_posix()}')
    """)
    con.execute(f"""
        create or replace view raw.ibge_municipios as
        select * from read_json_auto('{(pasta / "ibge_municipios.json").as_posix()}')
    """)
    con.execute(f"""
        create or replace view raw.ibge_populacao as
        select * from read_json_auto('{(pasta / "ibge_populacao_2022.json").as_posix()}')
    """)


def rodar_sql(con: duckdb.DuckDBPyConnection, camada: str) -> list[str]:
    """Executa os .sql de sql/<camada>/ em ordem alfabética e devolve os nomes."""
    arquivos = sorted((SQL / camada).glob("*.sql"))
    for arquivo in arquivos:
        con.execute(arquivo.read_text(encoding="utf-8"))
    return [a.stem for a in arquivos]


def contar(con: duckdb.DuckDBPyConnection, tabela: str) -> int:
    return con.execute(f"select count(*) from {tabela}").fetchall()[0][0]
