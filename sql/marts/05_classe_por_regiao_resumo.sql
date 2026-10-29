-- Pergunta 3 resumida para o painel: as quatro classes que somam quase toda a
-- potência e o resto junto em "Outras". Com 9 classes, o gráfico empilhado
-- fica ilegível, e o painel não deve fazer conta, então o agrupamento fica aqui.
--
-- Parte da refined (em kW) e não de marts.classe_por_regiao, que já vem
-- arredondada em MW: somar valores arredondados zerava classes pequenas.
create or replace table marts.classe_por_regiao_resumo as
with base as (
    select
        m.regiao,
        case
            when g.classe_consumo in ('Residencial', 'Comercial', 'Rural', 'Industrial')
                then g.classe_consumo
            else 'Outras'
        end                     as classe,
        sum(g.potencia_kw)      as potencia_kw
    from refined.gd_empreendimentos g
    join refined.municipios m using (cod_municipio)
    group by all
)
select
    regiao,
    classe,
    round(potencia_kw / 1000, 1)                                                as potencia_mw,
    round(100 * potencia_kw / sum(potencia_kw) over (partition by regiao), 1)  as participacao_pct,
    case classe
        when 'Residencial' then 1 when 'Comercial' then 2 when 'Rural' then 3
        when 'Industrial' then 4 else 5
    end                                                                         as ordem
from base
order by regiao, ordem;
