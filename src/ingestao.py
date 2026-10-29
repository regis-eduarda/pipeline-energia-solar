"""Baixa os arquivos de origem para data/raw, sem mexer em nada.

A camada raw guarda exatamente o que veio da fonte. Qualquer limpeza
acontece depois, na refined.
"""
from pathlib import Path

import requests

RAW = Path(__file__).resolve().parent.parent / "data" / "raw"

FONTES = {
    # ANEEL - empreendimentos de geração distribuída (licença ODbL)
    "aneel_gd.parquet": (
        "https://dadosabertos.aneel.gov.br/dataset/5e0fafd2-21b9-4d5b-b622-40438d40aba2"
        "/resource/cd29f6eb-e08d-4db7-b6fb-ed6e3b682d27/download/"
        "empreendimento-geracao-distribuida.parquet"
    ),
    # IBGE - lista de municípios com UF e região
    "ibge_municipios.json": "https://servicodados.ibge.gov.br/api/v1/localidades/municipios",
    # IBGE SIDRA - tabela 4709, variável 93 (população residente), Censo 2022
    "ibge_populacao_2022.json": "https://apisidra.ibge.gov.br/values/t/4709/n6/all/v/93/p/2022",
}


def baixar(url: str, destino: Path) -> None:
    with requests.get(url, stream=True, timeout=300) as resp:
        resp.raise_for_status()
        with open(destino, "wb") as f:
            for bloco in resp.iter_content(chunk_size=1024 * 1024):
                f.write(bloco)


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    for nome, url in FONTES.items():
        destino = RAW / nome
        if destino.exists():
            print(f"{nome}: já existe, pulando")
            continue
        print(f"{nome}: baixando...")
        baixar(url, destino)
        print(f"{nome}: {destino.stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
