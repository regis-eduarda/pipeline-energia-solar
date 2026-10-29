-- Pergunta 3: quanto da potência vem de cada classe de consumo em cada região?
--
-- A região vem do IBGE (refined.municipios), não da coluna de região da ANEEL,
-- para todas as tabelas usarem o mesmo nome ("Centro-Oeste", com hífen).
create or replace table marts.classe_por_regiao as
with base as (
    select
        m.regiao,
        g.classe_consumo,
        count(*)            as sistemas,
        sum(g.potencia_kw)  as potencia_kw
    from refined.gd_empreendimentos g
    join refined.municipios m using (cod_municipio)
    group by 1, 2
)
select
    regiao,
    classe_consumo,
    sistemas,
    round(potencia_kw / 1000, 1)                                                as potencia_mw,
    round(100 * potencia_kw / sum(potencia_kw) over (partition by regiao), 1)  as participacao_pct
from base
order by regiao, potencia_kw desc;
