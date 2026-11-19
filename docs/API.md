# Documentação da API — Eventos Acadêmicos

## Endereço da aplicação

Durante a execução local:

http://127.0.0.1:5000

As rotas abaixo usam esse endereço como base.

## Autenticação

A API exige uma sessão autenticada.

Crie uma conta em /cadastro e entre em /login.
O navegador envia o cookie da sessão nas requisições ao sistema.

Consultas sem autenticação recebem status 401 e uma mensagem JSON.

## Proteção das operações de escrita

O cadastro exige o cabeçalho X-CSRF-Token.

O valor do token está na página autenticada:

```html
<meta name="csrf-token" content="TOKEN_DA_SESSAO">
```

O JavaScript da aplicação lê esse valor e o envia automaticamente.

Token ausente ou inválido recebe status 400.
A verificação do token acontece antes da verificação de login.

## Consultar todos os eventos

### Requisição

```http
GET /api/eventos
```

### Resposta de sucesso — 200

```json
[
    {
        "id": 1,
        "nome": "Feira Acadêmica",
        "data": "2026-11-20",
        "local": "Fatec",
        "vagas": 10
    }
]
```

Quando não existem eventos, a resposta é uma lista vazia:

```json
[]
```

## Consultar um evento

### Requisição

```http
GET /api/eventos/1
```

O número no endereço corresponde ao ID do evento.

### Resposta de sucesso — 200

```json
{
    "id": 1,
    "nome": "Feira Acadêmica",
    "data": "2026-11-20",
    "local": "Fatec",
    "vagas": 10
}
```

### Evento inexistente — 404

```json
{
    "erro": "Evento não encontrado."
}
```

## Cadastrar um evento

### Requisição

```http
POST /api/eventos
Content-Type: application/json
X-CSRF-Token: TOKEN_DA_SESSAO
```

### Corpo JSON

```json
{
    "nome": "Feira Acadêmica",
    "data": "2026-11-20",
    "local": "Fatec",
    "vagas": 10
}
```

### Campos

| Campo | Tipo | Regra |
|---|---|---|
| nome | Texto | Obrigatório, até 120 caracteres |
| data | Texto | Obrigatório, data válida no formato ano-mês-dia |
| local | Texto | Opcional, até 120 caracteres |
| vagas | Inteiro | Opcional, maior ou igual a zero e dentro do intervalo aceito pelo SQLite |

O campo local pode ser omitido ou enviado como texto vazio.
Vagas pode ser omitido, enviado como null ou texto vazio.
A validação também aceita vagas como texto contendo um inteiro,
para compartilhar as regras com o formulário HTML.

### Resposta de sucesso — 201

Retorna o evento criado, incluindo o ID gerado pelo banco.

O cabeçalho Location informa o endereço de consulta do novo evento.
Exemplo:

```http
Location: /api/eventos/1
```

### Dados inválidos — 400

Exemplo de resposta:

```json
{
    "erro": "Informe uma data válida."
}
```

Outros exemplos de entrada recusada:

- Nome vazio.
- Nome ou local com mais de 120 caracteres.
- Quantidade negativa ou decimal de vagas.
- Corpo JSON inválido.
- Token da sessão ausente ou inválido.

## Resumo das respostas

| Status | Significado |
|---|---|
| 200 | Consulta realizada |
| 201 | Evento criado |
| 400 | Dados ou token inválidos |
| 401 | Consulta sem autenticação |
| 404 | Evento não encontrado |

## Edição e exclusão

A edição e a exclusão usam as rotas de formulário HTML:

| Método | Rota | Ação |
|---|---|---|
| GET | /editar/ID | Abre o formulário preenchido |
| POST | /editar/ID | Salva as alterações |
| POST | /excluir/ID | Exclui o evento |

Essas operações exigem login e os envios exigem token CSRF.
A exclusão exige perfil admin. Usuário comum recebe status 403.
Após uma alteração bem-sucedida, o servidor redireciona com status 303.

## Integração externa — ViaCEP

A consulta de endereço é feita pelo JavaScript do navegador:

```http
GET https://viacep.com.br/ws/01001000/json/
```

O endereço retornado aparece na página e preenche o campo Local.
A pessoa pode ajustar o local antes de cadastrar o evento.

São tratados:

- CEP com formato inválido.
- CEP inexistente.
- Endereço incompleto na resposta.
- Falha de conexão ou tempo de espera excedido.

A consulta aguarda até dez segundos.

Documentação oficial do serviço:

https://viacep.com.br/

## Verificações realizadas durante o desenvolvimento

- Consulta autenticada da lista.
- Consulta de ID inexistente.
- Recusa de consulta sem login.
- Cadastro válido com resposta 201.
- Recusa de vagas negativas com resposta 400.
- Cadastro e atualização da lista com fetch.
- Consulta de CEP válido, inexistente e incompleto.
- Mensagem de falha com o servidor parado.
- Recuperação da consulta após reiniciar o servidor.
- Cadastro tradicional com JavaScript desativado.