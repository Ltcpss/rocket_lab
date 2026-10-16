# Atividade Orquestração
Atividade prática de engenharia de dados focada na implementação de arquitetura em camadas (Medalhão), tratamento avançado de dados e orquestração de pipelines analíticos no Databricks.

## Conteúdo da Pasta
```
.
├── 01_Landing_to_Bronze
├── 02_Bronze_to_Silver
├── 03_Silver_to_Gold
├── job.yaml
├── execução_job.png
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
- Essa pasta é uma cópia da entrega da atividade de arquitetura medalhão, entregue em `2-arquitetura_medalhao`. Contém algumas mudanças como: junção do notebook `00_setup.ipynb` e `01_bronze.ipynb`, renomeação de todos os notebooks e inclusão de registros da execução do job. 


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