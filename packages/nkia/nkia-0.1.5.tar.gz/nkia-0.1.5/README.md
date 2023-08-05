# Biblioteca de serviços do projeto Biodigital

Bem vindo a biblioteca de serviços do projeto biodigital, aqui você irá encontrar pacotes python criados especialmente para lidar com a massa de dados presente no DataLake Neo4j

## Pacotes

### data_gen

Pacote utilizado para manipular diretamente os dados do Neo4j, como por exemplo, criar e salvar no mongo uma estrutura de DataFrame contendo a informação dos produtos e seus atributos

### database

Usado para fazer as conexões com o banco de dados utilizando as credenciais presentes nas variáveis de ambiente, bem como armazenar algumas querys realizadas no NEO4j.

### incators_gen

Utilizado para geração dos indicadores/relatórios que serão explorados no front end e também na API.

## Como executar

- Instalar os requisitos:
  - ```pip install -r requirements.txt --user```

- Configurar as variáveis de ambiente do Neo4j e iniciar o docker do MongoDB.
- Instalar o pacote de stop words do NLTK
  - ```python -m nltk.downloader stopwords```
- Executar o módulo de interesse, por exemplo:
  - ```python3 src/incators_gen/bi.py```
