"""Monta a camada de indicadores (marts) a partir da refined."""
from banco import conectar, contar, rodar_sql


def main() -> None:
    con = conectar()
    for tabela in rodar_sql(con, "marts"):
        nome = tabela.split("_", 1)[1]
        print(f"marts.{nome:<22} {contar(con, f'marts.{nome}'):>5} linhas")
    con.close()


if __name__ == "__main__":
    main()
