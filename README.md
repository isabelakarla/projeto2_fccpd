🌟 Projeto 2 da disciplina de Fundamentos da Computação Concorrente, Paraelela e Distribúida no curso de ADS da CESAR School. 🌟

Este repositório contém as soluções para a atividade prática que será utilizada como composição da nota da AV2 da disciplina.

⚙️ Tecnologias Principais
Docker: Conteinerização de serviços.

Docker Compose: Orquestração e gerenciamento de ambientes multi-container.

Python: Linguagem usada na implementação dos serviços.

SQLite e PostgreeSQL: Bancos de Dados utilizados.

🧩 Desafios Concluídos (1 a 4)
As soluções para os desafios abaixo estão organizadas em seus respectivos diretórios: /desafio1, /desafio2, /desafio3 e /desafio4.


📦 Desafio 1: Containers em Rede (Flask e Cliente cURL)

🎯 Objetivo

Criar e demonstrar a comunicação funcional entre dois containers Docker (um Servidor Web e um Cliente que realiza requisições) conectados através de uma rede Docker customizada.

🧱 Arquitetura e Estrutura

Este desafio utiliza o Docker Compose para orquestrar dois serviços:

server: Um servidor web simples em Python/Flask.

client: Um cliente que realiza requisições HTTP para o servidor.

A comunicação é estabelecida pela rede minha_rede, definida no docker-compose.yml, que permite o Service Discovery entre os containers.

Componentes

Arquivo/Pasta

Descrição

app.py

Aplicação Python Flask que retorna a mensagem de saudação.

Dockerfile (na raiz)

Define a imagem do servidor (server), instalando Python e Flask.

client/Dockerfile

Define a imagem do cliente (client), baseada em Alpine com o curl instalado.

docker-compose.yml

Arquivo de orquestração que define os dois serviços e a rede customizada.

⚙️ Decisões Técnicas

1. Servidor (server)

Tecnologia: Python 3.11 e Flask.

Endpoint: A rota base (/) retorna a string "Olá do servidor Flask no container!".

Configuração: O Flask é configurado para rodar em host="0.0.0.0" e port=8080, garantindo que ele escute em todas as interfaces de rede dentro do container, permitindo o acesso via rede Docker.

2. Cliente (client)

Base: Imagem alpine por ser leve e eficiente.

Comunicação: Utiliza curl para fazer requisições.

Fluxo: O comando CMD roda um loop infinito (while true) que realiza uma requisição para http://server:8080 a cada 3 segundos. O nome do host, server, é resolvido automaticamente pelo Docker Compose, graças à rede customizada.

3. Rede Customizada (minha_rede)

A rede minha_rede é explicitamente definida com o driver bridge no docker-compose.yml.

networks:
  minha_rede:
    driver: bridge


Isso assegura que o Docker Compose crie uma rede isolada, à qual ambos os serviços são anexados, facilitando a comunicação interna pelo nome do serviço (server).

🔄 Funcionamento e Fluxo de Comunicação

O fluxo de comunicação ocorre da seguinte forma:

O serviço server inicia e expõe a porta 8080 dentro da rede minha_rede.

O serviço client inicia (com depends_on garantindo que o server comece primeiro).

O CMD do client envia uma requisição GET periódica para o endereço interno http://server:8080.

O server recebe a requisição, processa e envia a resposta.

O client imprime a resposta no seu log de saída, confirmando a troca de mensagens.


💾 Desafio 2: Volumes e Persistência (SQLite)

🎯 Objetivo

Demonstrar o uso de Volumes Nomeados do Docker para garantir a persistência dos dados de um banco de dados SQLite, desacoplando o ciclo de vida do dado do ciclo de vida do container.

🧱 Arquitetura e Estrutura

Este desafio utiliza um único serviço definido no Docker Compose:

db_app: Um container que executa um script Python para inicializar um banco de dados SQLite, inserir um registro e, em seguida, ler e exibir todos os registros existentes.

Componentes

Arquivo/Pasta

Descrição

app.py

Script principal em Python que manipula o banco de dados SQLite.

Dockerfile

Define a imagem para o serviço db_app, baseado em Python 3.10.

docker-compose.yml

Arquivo que define o serviço, o mapeamento do volume e o nome do container.

⚙️ Decisões Técnicas

1. Mecanismo de Persistência (Volume Nomeado)

A decisão crucial é utilizar um Volume Nomeado (dados_sqlite) e mapeá-lo para o diretório /data dentro do container, onde o arquivo do banco de dados (meubanco.db) é criado.

services:
  db_app:
    volumes:
      - dados_sqlite:/data
# ...
volumes:
  dados_sqlite:


2. Script app.py (Fluxo de Dados)

O script app.py foi desenhado para provar a persistência em cada execução:

Criação do Banco: O arquivo meubanco.db é criado no caminho persistente /data/meubanco.db.

Inicialização: A tabela registros é criada (se não existir).

Inserção de Teste: Um registro ("Dado persistido!") é inserido no banco toda vez que o container é iniciado.

Comprovação: Todos os registros são lidos e impressos no log.

Se o volume estiver funcionando corretamente, ao reiniciar o container, os logs mostrarão o registro da execução anterior mais o novo registro da execução atual.

🔄 Funcionamento e Prova de Persistência

A persistência é demonstrada quando o container é removido e recriado, mas o volume permanece intacto.

Fluxo de Persistência:

Primeira Execução: O container db_app é criado. O volume dados_sqlite é criado no host. O app.py insere o Registro 1. O log exibe 1 registro.

Remoção do Container: O container db_app é parado e removido. O volume dados_sqlite (com o Registro 1) continua existindo no host.

Segunda Execução (Recriação): O container db_app é recriado. Ele monta o volume existente. O app.py encontra o Registro 1 e insere o Registro 2. O log desta vez exibe 2 registros.

A presença de registros de execuções anteriores no log da nova execução comprova a eficácia do volume nomeado.



🔗 Desafio 3: Docker Compose Orquestrando Serviços (Web, DB e Cache)

🎯 Objetivo

Utilizar o Docker Compose para criar e orquestrar três serviços interdependentes (web, db e cache), garantindo a comunicação correta entre eles e o uso de variáveis de ambiente e volumes.

🧱 Arquitetura e Estrutura

A arquitetura consiste em três serviços conectados por uma rede interna, sendo o serviço web o ponto de entrada que consome os outros dois serviços (db e cache).

Componentes

Arquivo/Pasta

Serviço

Tecnologia/Função

web/app.py

web

Aplicação Python/Flask para testar a conectividade com DB e Cache.

web/Dockerfile

web

Define a imagem do serviço Web, instalando Flask, Psycopg2 e Redis.

docker-compose.yml

Todos

Define a orquestração dos 3 serviços, rede (minha_rede), dependências e volumes.

(Imagem postgres:15)

db

PostgreSQL (Banco de Dados).

(Imagem redis:7)

cache

Redis (Serviço de Cache).

⚙️ Decisões Técnicas

1. Orquestração e Dependências

O docker-compose.yml define os três serviços, garantindo a ordem de inicialização e a comunicação:

depends_on: O serviço web só é inicializado após o db e o cache terem iniciado. Embora não garanta que os serviços internos estejam prontos (health check), é uma boa prática inicial para ordenar a subida.

Rede Interna: A rede minha_rede é usada. O Flask acessa o PostgreSQL usando o hostname db e o Redis usando o hostname cache.

2. Conectividade e Variáveis de Ambiente

O serviço web se conecta aos outros serviços utilizando variáveis de ambiente definidas no docker-compose.yml:

# Trecho de app.py:
conn = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host="db", # Hostname é o nome do serviço no Compose
    port=5432
)
# Conexão com o Redis:
r = redis.Redis(host="cache", port=6379)


As variáveis de conexão do PostgreSQL (usuário, senha, banco) são passadas como environment para os serviços web e db, garantindo que ambos usem as mesmas credenciais.

3. Persistência

Um volume nomeado (dados_postgres) é utilizado para o serviço db, garantindo que os dados do PostgreSQL persistam mesmo se o container db for removido e recriado.

🔄 Funcionamento e Fluxo

O fluxo é iniciado quando o cliente (navegador) acessa o endpoint do serviço web:

O cliente faz uma requisição para http://localhost:8888/.

O serviço web (Flask) é acionado.

Conexão DB: O web se conecta ao db (PostgreSQL) na porta 5432, executa uma consulta de versão (SELECT version();) e coleta o resultado.

Conexão Cache: O web se conecta ao cache (Redis) na porta 6379, insere uma chave/valor de teste, e lê a mensagem.

Resposta: O web retorna uma página HTML que exibe o status e a versão dos serviços db e cache, confirmando a comunicação bem-sucedida entre os três containers.

🔄 Desafio 4: Microsserviços Independentes (Comunicação HTTP)

🎯 Objetivo

Criar dois microsserviços independentes (service_a e service_b), cada um com seu próprio container, e demonstrar a comunicação síncrona via requisições HTTP entre eles.

🧱 Arquitetura e Estrutura

A solução consiste em dois serviços Python/Flask isolados, orquestrados pelo Docker Compose:

service_a (Serviço de Dados): Fornece uma lista de usuários em formato JSON.

service_b (Serviço Consumidor): Faz uma requisição HTTP para o service_a, processa a resposta e exibe os dados formatados.

Componentes

Arquivo/Pasta

Serviço

Tecnologia/Função

service_a/app.py

service_a

Flask: expõe o endpoint /users com dados estáticos.

service_a/Dockerfile

service_a

Define a imagem, instalando apenas Flask.

service_b/app.py

service_b

Flask: utiliza a biblioteca requests para consumir o service_a.

service_b/Dockerfile

service_b

Define a imagem, instalando Flask e requests.

docker-compose.yml

Ambos

Orquestra a execução, define portas e dependências.

⚙️ Decisões Técnicas e Arquitetura

1. Isolamento e Dockerfiles

Cada microsserviço reside em seu próprio diretório (service_a e service_b) e possui um Dockerfile dedicado. Isso garante o isolamento completo do runtime e das dependências, cumprindo o princípio de microsserviços.

2. Microsserviço A (service_a)

Função: Atua como fonte de dados (Data Service).

Endpoint: /users.

Porta Interna: 5000.

Resposta: Retorna um objeto JSON contendo uma lista de dicionários com campos id, nome e ativo_desde.

3. Microsserviço B (service_b)

Função: Atua como serviço consumidor (Integration/Display Service).

Dependência: Utiliza a biblioteca requests para realizar a chamada HTTP ao serviço service_a.

Comunicação: O Flask utiliza o nome do serviço (hostname) definido no Compose, http://service_a:5000/users, para a comunicação interna.

Processamento: Recebe o JSON, itera sobre ele e constrói um HTML formatado #(<h1>, <ul>, <li>)# para o cliente final.

4. Orquestração e Comunicação no Compose

O docker-compose.yml simplifica a rede e a descoberta de serviço:

Service Discovery: O Compose coloca ambos os serviços na mesma rede default, permitindo que service_b use o nome do serviço service_a como hostname.

Mapeamento de Portas:

service_a: Mapeado para 5001:5000 (Porta externa 5001).

service_b: Mapeado para 5002:5000 (Porta externa 5002).

Dependência: O depends_on: - service_a no service_b garante que o serviço de dados esteja em processo de inicialização antes que o consumidor tente subir.

🔄 Fluxo de Comunicação

Um cliente (navegador/cURL) acessa o service_b pela porta mapeada 5002 (Ex: http://localhost:5002/).

O service_b recebe a requisição e imediatamente realiza uma requisição interna (GET) para http://service_a:5000/users.

O service_a responde com a lista de usuários em JSON.

O service_b recebe, decodifica o JSON e gera o HTML de exibição.

O service_b retorna o HTML final formatado ao cliente.

<p align="center">Made with ❤️ by Isabela Karla</p>
