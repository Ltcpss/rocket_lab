# Atividade Orquestração
Atividade prática de engenharia de dados focada na implementação de arquitetura em camadas (Medalhão), tratamento e análises de dados no Databricks.

## Conteúdo da Pasta
```
.
├── 00_setup.ipynb
├── 01_bronze.ipynb
├── 02_silver.ipynb
├── 03_gold.ipynb
└── README.md
```

## Base de Dados
| Base | Tabela no Databricks | 
|---|---|
| Informações de filmes | `movies_info` | 
| Dados Financeiros | `movies_financials` | 
| Métricas de Engajamento | `movies_metrics` | 
| Créditos e Tags | `credits_and_tags` | 
| Avaliações de Usuários | `movies_reviews` | 
| Cotação do Dólar (PTAX) | Série temporal contínua obtida via API | 

## O que foi resolvido
## O que foi resolvido
| Parte | Descrição | Técnicas |
|---|---|---|
| **Ingestão (Bronze)** | Carga de arquivos CSV brutos para o Unity Catalog em formato Delta Lake e ingestão automatizada da API PTAX do Banco Central, contendo montagem manual de query string OData, tratamento de exceptions e gerador de mock fiel aos dias úteis. | PySpark (`spark.read.csv`), Delta Lake, Tratamento de API REST (`requests`), Query String OData (`urllib.parse.quote`), Estratégia de Fallback, Mock com Dias Úteis. |
| **Transformação (Silver)** | Limpeza profunda, tipagem segura (modo ANSI), correção de *column shift*, tratamento de datas ambíguas, *forward fill* na cotação do dólar e unificação de entidades. | PySpark, Window Functions, Regex Avançado, `try_cast`, `coalesce`, `unionByName`. |
| **Modelagem e Analytics (Gold)** | Construção de um modelo estrela otimizado (fato, dimensões e tabelas-ponte N:N), chaves substitutas determinísticas e resolução de questões analíticas de negócio. | Star Schema, Modelagem Dimensional, Spark SQL, Funções de Janela (`RANK`), Chaves Substitutas (`row_number`). |
| **Orquestração** | Automação e encadeamento sequencial de ponta a ponta (Bronze ➔ Silver ➔ Gold) garantindo dependências e resiliência na execução. | Databricks Jobs & Pipelines, Definição declarativa (`job.yaml`), Dependências de tarefas. |


## Decisões de implementação
- Tratamento de Anomalias (Column Shift): Uso de validações baseadas em expressões regulares e conversões seguras (try_cast) para impedir que dados corrompidos quebrem o pipeline no modo ANSI do Spark.

- Chaves Substitutas Determinísticas: Utilização de row_number() ordenado em vez de monotonically_increasing_id() na camada Gold, garantindo estabilidade e integridade referencial nas chaves estrangeiras das tabelas-ponte e fatos a cada reexecução.

- Construção Manual da Query String (API OData / BCB): Como o serviço do Banco Central exige caracteres literais específicos (@, $, '), a URL foi montada via urllib.parse.quote com um conjunto restrito de caracteres seguros, evitando a codificação automática incorreta (%40, %24, etc.) pelo cliente HTTP.

- Estratégia de Fallback: Implementação de tratamento de exceções com timeout de 60 segundos e validação de payloads vazios. Caso ocorram bloqueios de rede ou instabilidades no servidor externo, o pipeline aciona automaticamente um mecanismo de simulação.

- Gerador de Mock Fiel ao Comportamento Real: O mock foi projetado para gerar cotações exclusivamente em dias úteis (excluindo fins de semana e feriados) e utiliza uma semente fixa (random.seed(42)). Isso é essencial para que a camada Silver consiga testar corretamente a regra de negócio do forward fill.

## Como executar
1. Certifique-se de que os arquivos CSV de origem estejam carregados no volume correspondente do Unity Catalog (/Volumes/atividade_2_cinedata/raw/inputs).
2. Via Workspace do Databricks: Importe os notebooks 01_Landing_to_Bronze, 02_Bronze_to_Silver e 03_Silver_to_Gold para a pasta do projeto e execute-os sequencialmente.
3. Via Job Automatizado: Utilize o arquivo job.yaml para configurar e disparar a pipeline completa de orquestração diretamente pelo painel de Jobs & Pipelines do Databricks.

## Tecnologia
- Plataforma: Databricks (Serverless Compute)
- Processamento: Apache Spark / PySpark
- Armazenamento / Governança: Delta Lake / Unity Catalog
- Linguagem: Python e Spark SQL

## Aviso
O enunciado e o material do curso pertencem ao programa Rocket Lab da V(dev) e são confidenciais. Este repositório contém apenas a resolução da atividade.