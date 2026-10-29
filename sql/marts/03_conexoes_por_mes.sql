-- Pergunta 2, de perto: mês a mês entre 2021 e 2024, para ver o que aconteceu
-- em volta de janeiro de 2023, quando a Lei 14.300/2022 passou a valer para
-- quem conectasse depois.
create or replace table marts.conexoes_por_mes as
select
    cast(date_trunc('month', data_cadastro) as date) as mes,
    count(*)                                as novos_sistemas,
    round(sum(potencia_kw) / 1000, 1)       as nova_potencia_mw
from refined.gd_empreendimentos
where data_cadastro >= date '2021-01-01'
  and data_cadastro <  date '2025-01-01'
group by all
order by 1;
