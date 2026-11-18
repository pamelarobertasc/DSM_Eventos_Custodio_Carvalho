# Importa o Flask para criar a aplicação web.
from flask import Flask

# Ferramentas para conferir e atualizar o banco antigo.
from sqlalchemy import event, inspect, text

# Importa a instância compartilhada do SQLAlchemy.
from extensions import db

# Importa os modelos para o SQLAlchemy conhecer as três tabelas.
from models.evento import Evento
from models.participante import Participante
from models.inscricao import Inscricao

# Importa os grupos de rotas da aplicação.
from controllers.evento_controller import evento_bp
from controllers.site_controller import site_bp


# Cria a aplicação Flask.
app = Flask(__name__)

# Define o banco SQLite dentro da pasta instance.
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///eventos.db"

# Desativa o acompanhamento extra de alterações do SQLAlchemy.
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Conecta a instância do SQLAlchemy à aplicação.
db.init_app(app)

# Registra as rotas dos controllers.
app.register_blueprint(evento_bp)
app.register_blueprint(site_bp)


# Abre o contexto necessário para trabalhar com o banco.
with app.app_context():

    # Executa esta função a cada nova conexão com o SQLite.
    @event.listens_for(db.engine, "connect")
    def ativar_chaves(conexao, registro):

        # Cria um cursor para executar um comando no banco.
        cursor = conexao.cursor()

        # Ativa a verificação das chaves estrangeiras no SQLite.
        cursor.execute("PRAGMA foreign_keys = ON")

        # Fecha o cursor depois de executar o comando.
        cursor.close()

    # Cria as tabelas que ainda não existem.
    db.create_all()

    # Consulta os nomes das colunas da tabela evento.
    colunas = {
        coluna["name"]
        for coluna in inspect(db.engine).get_columns("evento")
    }

    # Acrescenta vagas se o banco veio da versão antiga.
    if "vagas" not in colunas:

        # Abre uma transação e confirma se o comando funcionar.
        with db.engine.begin() as conexao:

            # Adiciona a coluna preservando os eventos cadastrados.
            conexao.execute(
                text("ALTER TABLE evento ADD COLUMN vagas INTEGER")
            )


# Inicia o servidor quando você executa python app.py.
if __name__ == "__main__":
    app.run(debug=True)