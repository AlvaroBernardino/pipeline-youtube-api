# Pipeline YouTube API - Projeto de Engenharia de Dados

Este projeto tem como objetivo construir um pipeline completo para ingestão, transformação e exportação de dados da YouTube Data API usando OAuth 2.0, PySpark, Databricks e Google Cloud Platform (GCP).

## Estrutura do Projeto

- `/data`  
  Pasta destinada a armazenar dados brutos (raw) coletados da API. **Não versionar essa pasta** para evitar subir dados grandes ou sensíveis.

- `/notebooks`  
  Contém notebooks Jupyter ou Databricks para limpeza, transformação e análise dos dados.

- `/scripts`  
  Scripts Python responsáveis pela ingestão dos dados da API, processamento e integrações com outras plataformas.

- `/config`  
  Arquivos de configuração, como `client_secret.json` para autenticação OAuth. **Este arquivo deve ser ignorado pelo Git** por questões de segurança.

- `.gitignore`  
  Arquivo que define quais arquivos ou pastas o Git deve ignorar.

- `requirements.txt`  
  Lista das bibliotecas Python necessárias para executar os scripts.

- `README.md`  
  Documentação principal do projeto.

```bash
pip install -r requirements.txt
