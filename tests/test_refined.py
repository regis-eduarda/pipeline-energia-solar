from conftest import linhas


def test_municipios_nao_ganha_nem_perde_linha(con):
    assert linhas(con, "select count(*) from refined.municipios") == [(3,)]


def test_cabecalho_do_sidra_nao_vira_populacao(con):
    # se a linha "Valor" passasse, o cast para bigint quebraria antes daqui
    assert linhas(con, "select sum(populacao_2022) from refined.municipios") == [(3000,)]


def test_municipio_sem_censo_fica_com_populacao_nula(con):
    assert linhas(
        con, "select populacao_2022 from refined.municipios where cod_municipio = 5101837"
    ) == [(None,)]


def test_uf_e_regiao_vem_do_ibge(con):
    assert linhas(
        con, "select uf, regiao from refined.municipios where cod_municipio = 4106902"
    ) == [("PR", "Sul")]


def test_sistema_com_potencia_zero_sai(con):
    assert linhas(con, "select count(*) from refined.gd_empreendimentos") == [(5,)]
    assert linhas(
        con, "select count(*) from refined.gd_empreendimentos where cod_empreendimento = 'A5'"
    ) == [(0,)]


def test_data_de_1900_vira_nula(con):
    assert linhas(
        con, "select data_cadastro from refined.gd_empreendimentos where cod_empreendimento = 'A4'"
    ) == [(None,)]


def test_classe_perde_espaco_sobrando(con):
    classes = linhas(con, "select distinct classe_consumo from refined.gd_empreendimentos order by 1")
    assert classes == [("Comercial",), ("REBR",), ("Residencial",), ("Rural",)]


def test_dado_pessoal_nao_chega_na_refined(con):
    colunas = {c[0] for c in linhas(con, "describe refined.gd_empreendimentos")}
    assert "NumCPFCNPJ" not in colunas
    assert "NomTitularEmpreendimento" not in colunas
