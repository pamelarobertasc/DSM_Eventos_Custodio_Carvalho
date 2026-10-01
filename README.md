# DSM_Eventos_Custodio_Carvalho

Sistema Web de Gestão de Eventos Acadêmicos

Projeto Integrador — Desenvolvimento Web II (DW2)
CST em Desenvolvimento de Software Multiplataforma — Fatec Porto Ferreira

## Integrantes

- Custódio
- Carvalho

*(se os nomes completos forem diferentes dos sobrenomes usados no repositório, é só atualizar aqui)*

## Como executar o projeto

1. Clone o repositório:
   ```
   git clone URL_DO_REPOSITORIO
   cd nome-do-repositorio
   ```

2. Crie e ative o ambiente virtual:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
   (no macOS/Linux: `source venv/bin/activate`)

3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

4. Execute a aplicação:
   ```
   python app.py
   ```

5. Acesse no navegador: `http://127.0.0.1:5000`

## Estrutura do projeto

```
DSM_Eventos_Custodio_Carvalho/
├── app.py                        # inicia a aplicação Flask
├── requirements.txt              # dependências do projeto
├── .gitignore                    # arquivos que o Git deve ignorar
├── models/
│   └── evento.py                 # entidade Evento
├── controllers/
│   ├── evento_controller.py      # rotas de listar/cadastrar evento
│   └── site_controller.py        # rotas gerais do site (ex.: /sobre)
├── data/
│   └── memoria.py                # armazenamento em memória (temporário)
└── templates/
    └── index.html                # página de listagem e cadastro
```

## Status atual (Etapa 1)

- [x] Projeto organizado em MVC
- [x] Rotas de listar e cadastrar eventos (dados em memória, ainda não persistentes)
- [ ] Persistência em banco de dados (Etapa 2)

## Etapa 2 — Persistência com ORM

Nesta etapa, o projeto passou a utilizar o **Flask-SQLAlchemy** como ORM (Object-Relational Mapping) para realizar a comunicação entre a aplicação Python e o banco de dados SQLite.

O modelo `Evento` foi convertido para uma classe ORM, permitindo que os objetos Python sejam associados aos registros da tabela no banco de dados.

### Configuração do banco de dados

A aplicação utiliza SQLite como banco de dados e o Flask-SQLAlchemy para realizar o mapeamento objeto-relacional.

A criação das tabelas é realizada através do comando:

```python
db.create_all()
```

Os registros são persistidos utilizando:

```python
db.session.add(evento)
db.session.commit()
```

### Consultas utilizando ORM

Foram realizadas consultas utilizando os métodos do SQLAlchemy:

```python
Evento.query.all()
```

Retorna todos os eventos cadastrados.

```python
Evento.query.get(1)
```

Busca um evento pelo seu identificador.

```python
Evento.query.filter_by(local="Lab 3").all()
```

Busca os eventos de acordo com o local informado.

### Data Access Object (DAO)

Foi criada a classe `EventoDAO` para organizar o acesso aos dados.

O DAO possui os seguintes métodos:

* `salvar(evento)` — adiciona o evento ao banco de dados e confirma a transação.
* `listar()` — retorna todos os eventos cadastrados.

O fluxo da aplicação passou a ser:

```text
Controller
    ↓
EventoDAO
    ↓
SQLAlchemy (ORM)
    ↓
SQLite
```

Dessa forma, o Controller não precisa realizar diretamente as operações de persistência no banco de dados.

## SQL direto x ORM

### SQL direto

No acesso tradicional ao banco de dados, a aplicação utiliza comandos SQL diretamente.

Exemplo de inserção:

```sql
INSERT INTO evento (nome, data, local)
VALUES ('Workshop ORM', '2026-10-15', 'Lab 2');
```

Exemplo de consulta:

```sql
SELECT * FROM evento;
```

Nesse modelo, o desenvolvedor precisa escrever manualmente os comandos SQL utilizados pela aplicação.

### ORM

Com o ORM, os registros do banco podem ser representados por objetos Python.

Exemplo:

```python
evento = Evento(
    nome="Workshop ORM",
    data="2026-10-15",
    local="Lab 2"
)
```

Depois, o objeto pode ser persistido utilizando:

```python
db.session.add(evento)
db.session.commit()
```

As consultas também podem ser realizadas utilizando os recursos do SQLAlchemy:

```python
Evento.query.all()
```

### Comparação

| SQL direto                                    | ORM                                               |
| --------------------------------------------- | ------------------------------------------------- |
| Utiliza comandos SQL diretamente              | Utiliza objetos e classes Python                  |
| O desenvolvedor escreve as consultas SQL      | O SQLAlchemy gera as consultas necessárias        |
| Maior contato com a linguagem SQL             | Abstrai parte da comunicação com o banco          |
| Exige conhecimento de SQL nas operações       | Permite trabalhar principalmente com Python       |
| Pode resultar em mais código SQL na aplicação | Integra o acesso aos dados ao modelo da aplicação |

## Vantagens do ORM

O uso do ORM no projeto proporciona:

* Redução da necessidade de escrever SQL manualmente.
* Utilização de objetos Python para representar os registros.
* Maior organização do acesso aos dados.
* Facilidade de manutenção do código.
* Separação da lógica de acesso aos dados através do DAO.
* Integração entre os modelos da aplicação e as tabelas do banco de dados.

## Status atual (Etapa 2)

* [x] Flask-SQLAlchemy instalado
* [x] `requirements.txt` atualizado
* [x] Modelo `Evento` convertido para ORM
* [x] Banco de dados SQLite configurado
* [x] Tabela criada utilizando `db.create_all()`
* [x] Persistência de eventos utilizando ORM
* [x] Consultas com `all()`, `get()` e `filter_by()`
* [x] `EventoDAO` criado
* [x] Controller integrado ao `EventoDAO`
* [x] Comparação entre SQL direto e ORM documentada

## Alterações realizadas — Etapa 2

Nesta etapa, o projeto foi atualizado para utilizar persistência de dados com banco de dados SQLite e mapeamento objeto-relacional (ORM) utilizando Flask-SQLAlchemy.

### 1. Instalação do ORM

Foi adicionada a biblioteca **Flask-SQLAlchemy** ao projeto e o arquivo `requirements.txt` foi atualizado para registrar a nova dependência.

### 2. Conversão da entidade Evento para ORM

A classe `Evento`, anteriormente utilizada apenas como uma classe Python, foi transformada em um modelo ORM.

O modelo passou a utilizar:

* `db.Model`;
* `db.Column`;
* chave primária `id`;
* campos `nome`, `data` e `local`.

### 3. Configuração do banco de dados

Foi criada a configuração do SQLAlchemy na aplicação Flask, utilizando o banco de dados SQLite.

Também foi criado o arquivo `extensions.py`, responsável por disponibilizar a instância do SQLAlchemy:

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
```

A criação das tabelas é realizada através de:

```python
with app.app_context():
    db.create_all()
```

### 4. Persistência dos eventos

Os eventos passaram a ser armazenados no banco de dados utilizando o ORM.

Para inserir um evento são utilizados:

```python
db.session.add(evento)
db.session.commit()
```

Dessa forma, os dados permanecem armazenados mesmo após o encerramento da aplicação.

### 5. Consultas utilizando ORM

Foram realizados testes de consultas utilizando os recursos do SQLAlchemy:

```python
Evento.query.all()
```

Para consultar todos os eventos.

```python
Evento.query.get(1)
```

Para consultar um evento pelo seu identificador.

```python
Evento.query.filter_by(local="Lab 3").all()
```

Para consultar eventos filtrando pelo local.

### 6. Criação do EventoDAO

Foi criada a pasta `DAO` e o arquivo `evento_dao.py`.

O `EventoDAO` possui os métodos:

```python
salvar(evento)
```

Responsável por adicionar e confirmar o evento no banco de dados.

```python
listar()
```

Responsável por consultar e retornar os eventos cadastrados.

### 7. Integração do Controller com o DAO

O `evento_controller.py` foi atualizado para utilizar o `EventoDAO`.

O cadastro passou a utilizar:

```python
EventoDAO.salvar(evento)
```

E a listagem passou a utilizar:

```python
eventos = EventoDAO.listar()
```

Com isso, o Controller deixou de utilizar a lista em memória como fonte principal dos eventos.

O fluxo passou a ser:

```text
Usuário
   ↓
Controller
   ↓
EventoDAO
   ↓
Flask-SQLAlchemy
   ↓
SQLite
```

### 8. Documentação

O `README.md` foi atualizado para documentar:

* configuração do ORM;
* persistência dos dados;
* consultas utilizando SQLAlchemy;
* funcionamento do DAO;
* integração entre Controller e DAO;
* comparação entre SQL direto e ORM.

## Status atual

* [x] Projeto organizado em MVC
* [x] Flask-SQLAlchemy instalado
* [x] `requirements.txt` atualizado
* [x] Modelo `Evento` convertido para ORM
* [x] Banco SQLite configurado
* [x] Tabela criada com `db.create_all()`
* [x] Persistência utilizando ORM
* [x] Consultas com `all()`, `get()` e `filter_by()`
* [x] `EventoDAO` criado
* [x] Controller integrado ao DAO
* [x] README atualizado

