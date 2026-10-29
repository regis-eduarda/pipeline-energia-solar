# Pipeline de geração distribuída no Brasil

Projeto final da pós (Eng. de Dados Jr.). A ideia é montar um pipeline do zero
com dados públicos da ANEEL e do IBGE sobre geração distribuída, que são os
sistemas pequenos (na maioria painéis solares em telhado) que geram energia
perto de onde ela é consumida e ficam ligados na rede da distribuidora.

## Perguntas

1. Quais estados têm mais potência de geração distribuída **por habitante**?
   O total absoluto favorece estados grandes, então divido pela população.
2. Como as conexões cresceram ano a ano? E o que aconteceu perto da Lei
   14.300/2022, que mudou as regras de compensação para quem conectasse
   depois de janeiro de 2023?
3. Quanto da potência instalada vem de cada classe de consumo (residencial,
   comercial, rural, industrial...) em cada região do país?

## Fontes

- ANEEL – Relação de empreendimentos de geração distribuída (dados abertos)
- IBGE – API de localidades (municípios) e SIDRA, tabela 4709 (população do Censo 2022)

_Em construção._
