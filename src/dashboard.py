"""Gera dashboard/painel.html a partir dos marts.

O painel lê só a camada de indicadores. Aqui só tem select e order by: nenhuma
conta é feita no Python nem no navegador. Os dados vão como JSON dentro do HTML,
então o arquivo abre sozinho, sem servidor.
"""
import json
from pathlib import Path

import duckdb

from banco import BANCO, RAIZ

PASTA = RAIZ / "dashboard"

CONSULTAS = {
    "uf": """
        select uf, regiao, watts_por_habitante, potencia_mw, posicao
        from marts.potencia_por_uf order by posicao
    """,
    "ano": """
        select ano, novos_sistemas, nova_potencia_mw, ano_completo
        from marts.conexoes_por_ano where ano >= 2014 order by ano
    """,
    "mes": """
        select strftime(mes, '%Y-%m') as mes, novos_sistemas, nova_potencia_mw
        from marts.conexoes_por_mes order by mes
    """,
    "classe": """
        select regiao, classe, potencia_mw, participacao_pct, ordem
        from marts.classe_por_regiao_resumo order by regiao, ordem
    """,
}


def carregar(con: duckdb.DuckDBPyConnection) -> dict[str, list[dict]]:
    dados = {}
    for nome, sql in CONSULTAS.items():
        cur = con.execute(sql)
        colunas = [c[0] for c in cur.description]
        dados[nome] = [dict(zip(colunas, linha)) for linha in cur.fetchall()]
    return dados


def main() -> None:
    con = duckdb.connect(str(BANCO), read_only=True)
    dados = carregar(con)
    con.close()

    modelo = (PASTA / "modelo.html").read_text(encoding="utf-8")
    html = modelo.replace("/*DADOS*/null", json.dumps(dados, ensure_ascii=False))
    saida = PASTA / "painel.html"
    saida.write_text(html, encoding="utf-8")
    print(f"{saida.relative_to(RAIZ)} gerado ({len(html) / 1000:.0f} KB)")


if __name__ == "__main__":
    main()
