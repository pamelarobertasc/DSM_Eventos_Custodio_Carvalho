# Sistema Web de Gestão de Eventos Acadêmicos

Projeto da disciplina Desenvolvimento Web II, do curso de
Desenvolvimento de Software Multiplataforma da Fatec Porto Ferreira.

Professor Vagner dos Santos.

## Integrantes

- Pâmela Roberta de Souza Custódio
- Adriana Carla Rodrigues Moura

## Objetivo

Desenvolver um sistema web para gerenciar eventos acadêmicos,
aplicando arquitetura MVC, persistência com banco de dados e
versionamento com Git e GitHub.

## Tecnologias

- Python
- Flask
- Flask-SQLAlchemy
- SQLite
- HTML e Jinja
- Git e GitHub

## Como executar no Windows

### 1. Obter o projeto

```powershell
git clone https://github.com/pamelarobertasc/DSM_Eventos_Custodio_Carvalho.git
cd DSM_Eventos_Custodio_Carvalho
```

### 2. Criar o ambiente virtual

```powershell
py -m venv venv
```

### 3. Instalar as dependências

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 4. Iniciar a aplicação

```powershell
.\venv\Scripts\python.exe app.py
```

Abra http://127.0.0.1:5000 no navegador.

Para encerrar o servidor, pressione Ctrl+C no terminal.

## Estrutura do projeto

| Caminho | Responsabilidade |
|---|---|
| app.py | Inicializa o Flask, registra as rotas e prepara o banco |
| extensions.py | Disponibiliza a instância compartilhada do SQLAlchemy |
| controllers/ | Recebe as requisições e coordena as operações |
| models/ | Define Evento, Participante e Inscricao |
| dao/ | Concentra o acesso aos dados dos eventos |
| templates/ | Contém os formulários e a listagem |
| data/ | Guarda o exemplo anterior de dados em memória |
| docs/DER.md | Documenta as entidades e seus relacionamentos |
| requirements.txt | Lista as dependências |
| .gitignore | Define os arquivos ignorados pelo Git |

## Banco de dados

A aplicação utiliza SQLite no arquivo instance/eventos.db.

Na inicialização, as tabelas ausentes são criadas pelo SQLAlchemy.
Para o banco antigo de eventos, a aplicação acrescenta a coluna vagas
caso ela ainda não exista.

Faça uma cópia do banco antes de atualizar uma instalação existente.

O ambiente virtual, os arquivos de cache e o banco local são ignorados
pelo Git. Cada instalação cria seu próprio ambiente e banco.

## Modelagem

O sistema possui três entidades:

- Evento, com nome, data, local e quantidade de vagas.
- Participante, com nome e e-mail único.
- Inscricao, que associa um participante a um evento.

O mesmo participante pode ter somente uma inscrição por evento.

Consulte o diagrama e as regras em [docs/DER.md](docs/DER.md).

## Funcionalidades implementadas

- Cadastro de eventos.
- Listagem dos eventos cadastrados.
- Edição de nome, data, local e vagas.
- Exclusão de eventos.
- Validação dos campos no servidor.
- Persistência dos dados após reiniciar a aplicação.
- Modelos e relacionamentos de participantes e inscrições.

## Rotas disponíveis

| Método | Endereço | Funcionamento |
|---|---|---|
| GET | / | Exibe o formulário e a lista de eventos |
| POST | / | Valida e cadastra um evento |
| GET | /eventos | Exibe o formulário e a lista de eventos |
| POST | /eventos | Valida e cadastra um evento |
| GET | /editar/ID | Exibe o formulário do evento escolhido |
| POST | /editar/ID | Valida e salva as alterações |
| POST | /excluir/ID | Exclui o evento escolhido |
| GET | /sobre | Exibe a identificação do projeto |

Substitua ID pelo identificador do evento.

Após uma escrita bem-sucedida, a aplicação redireciona para a lista
com o código HTTP 303.

Dados inválidos recebem resposta 400.
Um evento inexistente nas rotas de edição ou exclusão recebe resposta 404.

## Roteiro de teste manual

1. Cadastre dois eventos com datas válidas.
2. Edite o nome e as vagas de um deles.
3. Exclua o outro evento.
4. Reinicie o servidor.
5. Confira se o evento restante mantém as alterações.
6. Tente cadastrar um evento com quantidade negativa de vagas.
7. Acesse /editar/999999 e confira a resposta para um ID inexistente.

## Escopo atual

A interface realiza o CRUD de eventos.

Participante e Inscricao estão representados nos modelos do banco.
As telas dessas entidades e a validação do limite de inscrições por
vagas ainda estão pendentes.

Sessões, autenticação, AJAX, API externa e deploy serão desenvolvidos
nas próximas etapas do projeto.

## SQL direto e ORM

No SQL direto, o código escreve comandos como INSERT e SELECT.
Com o ORM, os registros são representados por objetos Python.

O EventoDAO concentra as operações de banco. O controller chama
seus métodos para cadastrar, consultar, atualizar e excluir eventos.