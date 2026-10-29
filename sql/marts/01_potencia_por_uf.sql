-- Pergunta 1: quais estados têm mais potência de GD por habitante?
--
-- Potência e população são somadas por UF separadamente e só depois juntadas.
-- Juntar sistema com município e depois somar a população repetiria a população
-- de cada município uma vez por sistema.
create or replace table marts.potencia_por_uf as
with potencia as (
    select
        m.uf,
        count(*)            as sistemas,
        sum(g.potencia_kw)  as potencia_kw
    from refined.gd_empreendimentos g
    join refined.municipios m using (cod_municipio)
    group by m.uf
),
populacao as (
    select uf, any_value(regiao) as regiao, sum(populacao_2022) as populacao_2022
    from refined.municipios
    group by uf
)
select
    p.uf,
    pop.regiao,
    p.sistemas,
    round(p.potencia_kw / 1000, 1)                          as potencia_mw,
    pop.populacao_2022,
    round(p.potencia_kw * 1000 / pop.populacao_2022, 1)     as watts_por_habitante,
    rank() over (order by p.potencia_kw / pop.populacao_2022 desc) as posicao
from potencia p
join populacao pop using (uf)
order by posicao;
