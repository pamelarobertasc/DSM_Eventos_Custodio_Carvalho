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
