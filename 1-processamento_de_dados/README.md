# Atividade PySpark — Rocket Lab Engenharia de Dados

Atividade prática de introdução ao **PySpark**, desenvolvida no **Databricks** como parte do programa Rocket Lab Engenharia de Dados. O notebook trabalha com `join`, criação e alteração de colunas, agregações com `groupBy` e funções de janela (`Window`), usando três bases de dados públicas: jogadores do FIFA Ultimate Team, bandas de metal e Pokémon.

**Autora:** Leticia Pessôa Machado

## Conteúdo do repositório

```
.
├── RL_Dados_2026_2_Atividade_PySpark.ipynb   # notebook com a resolução
└── README.md
```

## Bases de dados

| Base | Tabela no Databricks | 
|---|---|
| Bandas de metal | `workspace.default.metal_bands` | 
| Pokémon | `workspace.default.pokemon_data` | 
| Jogadores FUT | `workspace.default.fut_players_data` | 

Os arquivos CSV **não estão incluídos** neste repositório. Para reproduzir o trabalho, é preciso carregá-los como tabelas (ver abaixo).

## O que foi resolvido

| Parte | Descrição | Técnicas |
|---|---|---|
| Exercício 1.1 | Leitura da base de jogadores | `spark.table` |
| Exercício 1.2 | Nacionalidade dos jogadores "The Bests" (dribbling e shooting > 90) | `filter`, `join` (left) |
| Exercício 2 | País com maior overall médio e overall médio do Brasil | `groupBy`, `agg`, `avg` |
| Exercício 2.1 | Classificação dos jogadores por faixa de overall | `when` / `otherwise` |
| Desafio | Dream Team do Brasil na formação 4-4-2 | `Window`, `row_number`, `join` |
| Desafio Bônus | O mesmo time, sem repetir jogadores | `Window`, `row_number` |

### Decisões de implementação

- **Formação como dado.** As vagas de cada grupo (`Goleiro`, `Defesa`, `Meio`, `Ataque`) ficam em uma lista de tuplas, transformada em DataFrame e ligada por `join`. Para mudar a formação, basta alterar os números.
- **Lógica reaproveitável.** O ranking por grupo e o filtro de vagas ficam na função `montar_dream_team`, usada tanto no Desafio quanto no Bônus.
- **Desafio Bônus.** Um jogador pode ter várias cartas na base. O critério é manter a de **maior overall** de cada jogador, identificado por `player_extended_name` (nome completo). As alternativas foram descartadas porque `player_id` é único por carta, `base_id` separa cartas da mesma pessoa e `player_name` mistura pessoas diferentes.

## Como executar

1. Criar uma conta no [Databricks](https://www.databricks.com/) e conectar o notebook ao compute **Serverless**.
2. Carregar cada CSV em *Catalog → workspace → default → Create → Table*, com os nomes da tabela acima e a primeira linha como cabeçalho.
3. Importar o notebook (*Workspace → Import*) ou clonar este repositório como **Git folder**.
4. Executar as células de cima para baixo.

## Tecnologias

- Python
- PySpark (`pyspark.sql`, `functions`, `Window`)
- Databricks

## Aviso

O enunciado e o material do curso pertencem ao programa Rocket Lab da V(dev) e são confidenciais. Este repositório contém apenas a resolução da atividade.
