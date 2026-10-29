-- Um sistema de geração distribuída por linha, só com as colunas que as
-- perguntas usam.
--
-- O que muda em relação ao raw:
--   * CPF/CNPJ, nome do titular e CEP ficam de fora. A ANEEL já publica os dois
--     primeiros mascarados (***.477.072-**), mas nenhuma pergunta usa eles;
--   * a classe de consumo perde espaços sobrando ("REBR " virava uma classe a mais);
--   * datas com ano antes de 2000 viram nulo (56 sistemas vêm com 1900, que é
--     data de preenchimento e não data real);
--   * sistemas com potência 0 saem (6 no arquivo de 10/2026).
--
-- A ANEEL não publica a data de conexão neste arquivo. A data que existe é a
-- de atualização cadastral, usada aqui como aproximação (ver README).
create or replace table refined.gd_empreendimentos as
select
    CodEmpreendimento               as cod_empreendimento,
    CodMunicipioIbge                as cod_municipio,
    NomAgente                       as distribuidora,
    trim(DscClasseConsumo)          as classe_consumo,
    SigTipoGeracao                  as tipo_geracao,
    DscPorte                        as porte,
    DscModalidadeHabilitado         as modalidade,
    MdaPotenciaInstaladaKW          as potencia_kw,
    case
        when year(DthAtualizaCadastralEmpreend) >= 2000 then DthAtualizaCadastralEmpreend
    end                             as data_cadastro
from raw.aneel_gd
where MdaPotenciaInstaladaKW > 0;
