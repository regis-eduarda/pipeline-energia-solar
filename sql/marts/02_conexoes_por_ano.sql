-- Pergunta 2: como as conexões cresceram ano a ano?
--
-- Usa a data de atualização cadastral (a ANEEL não publica a data de conexão
-- neste arquivo). Sistemas sem data ficam de fora. O último ano do arquivo
-- não está completo, por isso a coluna ano_completo.
create or replace table marts.conexoes_por_ano as
with por_ano as (
    select
        year(data_cadastro)     as ano,
        count(*)                as novos_sistemas,
        sum(potencia_kw)        as potencia_kw
    from refined.gd_empreendimentos
    where data_cadastro is not null
    group by 1
)
select
    ano,
    novos_sistemas,
    round(potencia_kw / 1000, 1)                                        as nova_potencia_mw,
    round(sum(potencia_kw) over (order by ano) / 1000, 1)               as potencia_acumulada_mw,
    round(100.0 * (novos_sistemas / lag(novos_sistemas) over (order by ano) - 1), 1)
                                                                        as variacao_sistemas_pct,
    ano < (select max(year(data_cadastro)) from refined.gd_empreendimentos) as ano_completo
from por_ano
order by ano;
