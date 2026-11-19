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



## SQL direto e ORM

No SQL direto, o código escreve comandos como INSERT e SELECT.
Com o ORM, os registros são representados por objetos Python.

O EventoDAO concentra as operações de banco. O controller chama
seus métodos para cadastrar, consultar, atualizar e excluir eventos.

## Etapa 3 — Sessão e autenticação

- Cadastro de usuários com e-mail único.
- Senhas armazenadas em hash.
- Login e logout.
- Proteção das rotas de eventos por autenticação.
- Perfil comum pode cadastrar, listar e editar eventos.
- Perfil admin também pode excluir eventos.
- Mensagens de sucesso e erro.
- Contador de visitas associado à sessão.
- Contador de acessos durante a execução do servidor.
- Preferência de tema armazenada em cookie por 30 dias.
- Formulários protegidos com token CSRF.
- Templates com estrutura compartilhada em base.html.

### Criar uma conta

Abra http://127.0.0.1:5000/cadastro e preencha os dados.
Novas contas recebem o perfil comum.

### Promover uma conta a administrador

Após cadastrar a conta, execute na raiz do projeto:

```powershell
.\venv\Scripts\python.exe -m flask --app app tornar-admin EMAIL_DA_CONTA
```

Substitua EMAIL_DA_CONTA pelo e-mail cadastrado no sistema.

A chave de assinatura da sessão fica em instance/secret_key.
Esse arquivo e o banco local são ignorados pelo Git.

## Etapa 4 — API e requisições assíncronas

- Consulta de eventos em JSON.
- Cadastro pela API com validação no servidor.
- Cadastro e atualização da lista com fetch.
- Mensagens para erros de validação e falhas de conexão.
- Cadastro tradicional disponível com JavaScript desativado.
- Consulta à API externa ViaCEP para preencher o local do evento.

### Rotas adicionais

| Método | Endereço | Funcionamento |
|---|---|---|
| GET e POST | /cadastro | Cria uma conta |
| GET e POST | /login | Autentica o usuário |
| POST | /sair | Encerra a sessão |
| POST | /tema | Guarda a preferência de tema |
| GET | /api/eventos | Retorna todos os eventos em JSON |
| GET | /api/eventos/ID | Retorna um evento em JSON |
| POST | /api/eventos | Recebe JSON e cadastra um evento |

### Cadastro pela API

Exemplo de corpo JSON:

```json
{
    "nome": "Feira Acadêmica",
    "data": "2026-11-20",
    "local": "Fatec",
    "vagas": 10
}
```

O cadastro exige autenticação e o cabeçalho X-CSRF-Token.
O token está na tag meta csrf-token da página autenticada.
O JavaScript do sistema envia esse cabeçalho automaticamente.

Nome e data são obrigatórios.
Local e vagas podem ser omitidos.
Vagas deve ser uma quantidade inteira não negativa.

### Respostas da API

| Código | Significado |
|---|---|
| 200 | Consulta realizada |
| 201 | Evento criado |
| 400 | Dados inválidos ou token de sessão inválido |
| 401 | Consulta sem autenticação |
| 404 | Evento não encontrado |

O cadastro bem-sucedido retorna o evento criado e o cabeçalho
Location com seu endereço de consulta.

### Integração externa

O sistema consulta https://viacep.com.br/ws/CEP/json/.

O endereço retornado aparece na tela e preenche o campo Local.
O usuário pode ajustar o texto antes de cadastrar.

A consulta trata CEP incompleto, CEP inexistente e falha de conexão.

Documentação do serviço: https://viacep.com.br/

### Conferência manual

- Cadastrar, entrar e sair de uma conta.
- Conferir permissões de usuário comum e admin.
- Cadastrar, editar, excluir e verificar persistência.
- Conferir mensagens, contadores e tema.
- Consultar a API com e sem autenticação.
- Consultar um ID inexistente.
- Cadastrar pela API com dados válidos e inválidos.
- Cadastrar e atualizar a lista sem recarregar a página.
- Cadastrar pelo formulário com JavaScript desativado.
- Parar o servidor e conferir a mensagem de falha na atualização.
- Reiniciar o servidor e consultar novamente.
- Consultar CEP válido, inexistente e incompleto.

## Próxima etapa

Publicação da aplicação, fluxo com branches e pull request,
e revisão da documentação para a entrega final.