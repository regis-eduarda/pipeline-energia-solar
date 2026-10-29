"""Monta a camada refined a partir do raw e mostra as contagens antes/depois."""
from banco import conectar, contar, criar_raw, rodar_sql


def main() -> None:
    con = conectar()
    criar_raw(con)
    rodar_sql(con, "refined")

    print(f"raw.ibge_municipios      {contar(con, 'raw.ibge_municipios'):>9,}")
    print(f"refined.municipios       {contar(con, 'refined.municipios'):>9,}")
    print(f"raw.aneel_gd             {contar(con, 'raw.aneel_gd'):>9,}")
    print(f"refined.gd_empreendimentos {contar(con, 'refined.gd_empreendimentos'):>7,}")
    con.close()


if __name__ == "__main__":
    main()
