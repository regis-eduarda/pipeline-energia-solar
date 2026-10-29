-- Um município por linha, com UF, região e população do Censo 2022.
--
-- A UF e a região vêm de "regiao-imediata", não de "microrregiao": o IBGE parou
-- de preencher microrregião para municípios novos (Boa Esperança do Norte/MT
-- vem com microrregiao nula).
--
-- A tabela do SIDRA traz uma primeira linha de cabeçalho ("Valor"), que o
-- filtro NC = '6' (nível município) deixa de fora.
create or replace table refined.municipios as
select
    m.id                                                        as cod_municipio,
    m.nome                                                      as municipio,
    m."regiao-imediata"."regiao-intermediaria".UF.sigla         as uf,
    m."regiao-imediata"."regiao-intermediaria".UF.regiao.nome   as regiao,
    cast(p.V as bigint)                                         as populacao_2022
from raw.ibge_municipios m
left join raw.ibge_populacao p
    on p.D1C = cast(m.id as varchar)
   and p.NC = '6';
