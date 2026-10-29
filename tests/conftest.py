"""Dado inventado, pequeno o bastante para conferir as contas de cabeça.

Os testes rodam num DuckDB em memória: o banco do projeto (data/pipeline.duckdb)
nunca é aberto.

Municípios:
    5103403 Cuiabá/MT                  população 1000
    5101837 Boa Esperança do Norte/MT  sem população (criado depois do Censo)
    4106902 Curitiba/PR                população 2000

Sistemas:
    A1 Cuiabá      Residencial  10 kW  2022-12-10
    A2 Cuiabá      Residencial   5 kW  2023-01-05
    A3 Boa Esp.    Rural        15 kW  2023-03-01
    A4 Curitiba    "REBR "      20 kW  1900-01-01  -> data vira nula
    A5 Curitiba    REBR          0 kW  2023-02-02  -> sai na refined
    A6 Curitiba    Comercial    30 kW  2024-06-01
"""
import pytest

from banco import conectar, rodar_sql


def _uf(sigla: str, regiao: str) -> str:
    return (
        "{'regiao-intermediaria': {'UF': {'sigla': '" + sigla + "', "
        "'regiao': {'nome': '" + regiao + "'}}}}"
    )


@pytest.fixture
def con():
    con = conectar(":memory:")

    con.execute(f"""
        create table raw.ibge_municipios as
        select * from (values
            (5103403, 'Cuiabá',                 {_uf('MT', 'Centro-Oeste')}),
            (5101837, 'Boa Esperança do Norte', {_uf('MT', 'Centro-Oeste')}),
            (4106902, 'Curitiba',               {_uf('PR', 'Sul')})
        ) t(id, nome, "regiao-imediata")
    """)

    con.execute("""
        create table raw.ibge_populacao as
        select * from (values
            ('Nível Territorial (Código)', 'Município (Código)', 'Valor'),
            ('6', '5103403', '1000'),
            ('6', '4106902', '2000')
        ) t(NC, D1C, V)
    """)

    con.execute("""
        create table raw.aneel_gd as
        select * from (values
            ('A1', 5103403, 'Residencial', 10.0, date '2022-12-10'),
            ('A2', 5103403, 'Residencial',  5.0, date '2023-01-05'),
            ('A3', 5101837, 'Rural',       15.0, date '2023-03-01'),
            ('A4', 4106902, 'REBR ',       20.0, date '1900-01-01'),
            ('A5', 4106902, 'REBR',         0.0, date '2023-02-02'),
            ('A6', 4106902, 'Comercial',   30.0, date '2024-06-01')
        ) t(CodEmpreendimento, CodMunicipioIbge, DscClasseConsumo,
            MdaPotenciaInstaladaKW, DthAtualizaCadastralEmpreend),
        lateral (select
            'Distribuidora X'   as NomAgente,
            'UFV'               as SigTipoGeracao,
            'Microgeracao'      as DscPorte,
            'Geracao na propria UC' as DscModalidadeHabilitado,
            '123.456.789-00'    as NumCPFCNPJ,
            'Fulano de Tal'     as NomTitularEmpreendimento
        )
    """)

    rodar_sql(con, "refined")
    rodar_sql(con, "marts")
    yield con
    con.close()


def linhas(con, sql: str) -> list[tuple]:
    return con.execute(sql).fetchall()
