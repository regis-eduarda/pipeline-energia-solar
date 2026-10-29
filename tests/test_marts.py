from conftest import linhas


def test_watts_por_habitante_sem_repetir_populacao(con):
    # MT: 10 + 5 + 15 = 30 kW para 1000 habitantes = 30 W/hab.
    # Se a população fosse somada depois do join com os sistemas, Cuiabá
    # contaria duas vezes (2000 hab) e o resultado cairia.
    # PR: 20 + 30 = 50 kW para 2000 habitantes = 25 W/hab.
    assert linhas(
        con,
        "select uf, sistemas, watts_por_habitante, posicao from marts.potencia_por_uf order by posicao",
    ) == [("MT", 3, 30.0, 1), ("PR", 2, 25.0, 2)]


def test_potencia_por_uf_fecha_com_a_refined(con):
    assert linhas(con, "select sum(sistemas) from marts.potencia_por_uf") == linhas(
        con, "select count(*) from refined.gd_empreendimentos"
    )


def test_conexoes_por_ano_deixa_de_fora_sem_data(con):
    assert linhas(con, "select ano, novos_sistemas from marts.conexoes_por_ano order by ano") == [
        (2022, 1),
        (2023, 2),
        (2024, 1),
    ]


def test_ultimo_ano_marcado_como_incompleto(con):
    assert linhas(
        con, "select ano from marts.conexoes_por_ano where not ano_completo"
    ) == [(2024,)]


def test_conexoes_por_mes(con):
    assert linhas(con, "select mes::varchar, novos_sistemas from marts.conexoes_por_mes order by mes") == [
        ("2022-12-01", 1),
        ("2023-01-01", 1),
        ("2023-03-01", 1),
        ("2024-06-01", 1),
    ]


def test_participacao_por_regiao(con):
    assert linhas(
        con,
        "select regiao, classe_consumo, participacao_pct from marts.classe_por_regiao "
        "order by regiao, classe_consumo",
    ) == [
        ("Centro-Oeste", "Residencial", 50.0),
        ("Centro-Oeste", "Rural", 50.0),
        ("Sul", "Comercial", 60.0),
        ("Sul", "REBR", 40.0),
    ]
