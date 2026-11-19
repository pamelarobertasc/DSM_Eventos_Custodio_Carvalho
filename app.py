# Bibliotecas para configurações e geração de valores aleatórios.
import os
import secrets
import hmac
from pathlib import Path

# Permite criar um comando para promover uma conta a admin.
import click

# Ferramentas do Flask.
from flask import (
    Flask,
    abort,
    g,
    redirect,
    request,
    session,
    url_for,
    jsonify,
)

# Ferramentas para configurar e atualizar o banco.
from sqlalchemy import event, inspect, text

# Instância compartilhada do SQLAlchemy.
from extensions import db

# Importa os modelos antes de criar as tabelas.
from models.evento import Evento
from models.participante import Participante
from models.inscricao import Inscricao
from models.usuario import Usuario

# Importa os grupos de rotas.
from controllers.evento_controller import evento_bp
from controllers.site_controller import site_bp
from controllers.auth_controller import auth_bp


# Cria a aplicação.
app = Flask(__name__)

# Garante que a pasta local instance exista.
Path(app.instance_path).mkdir(exist_ok=True)

# Define o arquivo que guarda a chave usada para assinar a sessão.
arquivo_chave = Path(app.instance_path) / "secret_key"

# Se não houver chave definida no ambiente, prepara uma chave local.
if not os.environ.get("SECRET_KEY"):
    try:
        # O modo "x" cria o arquivo somente se ele ainda não existir.
        with arquivo_chave.open("x") as arquivo:
            arquivo.write(secrets.token_hex(32))

    except FileExistsError:
        # Se já existe, vamos reutilizar a chave salva.
        pass

# Reutilizar a chave mantém a validade da sessão após reiniciar.
app.secret_key = (
    os.environ.get("SECRET_KEY")
    or arquivo_chave.read_text()
)

# Impede o JavaScript de ler diretamente o cookie da sessão.
app.config["SESSION_COOKIE_HTTPONLY"] = True

# Limita o envio do cookie em requisições vindas de outros sites.
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

# Configura o SQLite.
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///eventos.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Liga o SQLAlchemy à aplicação.
db.init_app(app)

# Registra os controllers.
app.register_blueprint(evento_bp)
app.register_blueprint(site_bp)
app.register_blueprint(auth_bp)


def token_csrf():
    # Cria um token aleatório para os formulários desta sessão.
    if "csrf" not in session:
        session["csrf"] = secrets.token_hex(32)

    # Entrega o token para o template.
    return session["csrf"]


@app.before_request
def carregar_usuario_e_proteger_escritas():
    # Começa a requisição sem uma conta autenticada.
    g.usuario = None

    # Recupera do banco a pessoa identificada pela sessão.
    if session.get("usuario_id"):
        g.usuario = db.session.get(
            Usuario,
            session["usuario_id"],
        )

    # Confere o token antes de aceitar operações de escrita.
    if request.method in ("POST", "PUT", "PATCH", "DELETE"):

        # O token pode vir do JavaScript ou de um formulário HTML.
        recebido = (
            request.headers.get("X-CSRF-Token")
            or request.form.get("csrf_token", "")
        )

        # Lê o token que o servidor guardou na sessão.
        esperado = session.get("csrf", "")

        # Recusa o envio quando o token está ausente ou diferente.
        if not esperado or not hmac.compare_digest(
            str(recebido),
            esperado,
        ):
            # A API informa falhas do token em JSON.
            if request.path.startswith("/api/"):
                return jsonify(
                    erro="Sessão expirada. Atualize a página."
                ), 400
            
            # Os formulários tradicionais recebem a página de erro.
            abort(
                400,
                description=(
                    "Sessão expirada. Atualize a página "
                    "antes de enviar o formulário."
                ),
            )


@app.context_processor
def contexto():
    # Disponibiliza esses valores em todos os templates.
    return {
        "csrf_token": token_csrf,
        "tema": request.cookies.get("tema", "claro"),
        "acessos": app.config.get("ACESSOS", 0),
    }


@app.post("/tema")
def trocar_tema():
    # Recebe a preferência enviada pelos botões da página.
    tema = request.form.get("tema", "")

    # Aceita somente os dois temas disponíveis.
    if tema not in ("claro", "escuro"):
        abort(400)

    # Escolhe para onde voltar após trocar o tema.
    destino = (
        url_for("evento.index")
        if g.usuario
        else url_for("auth.login")
    )

    # Prepara o redirecionamento.
    resposta = redirect(destino, code=303)

    # Guarda a preferência por 30 dias no navegador.
    resposta.set_cookie(
        "tema",
        tema,
        max_age=30 * 86400,
        samesite="Lax",
    )

    return resposta


@app.cli.command("tornar-admin")
@click.argument("email")
def tornar_admin(email):
    # Busca uma conta existente pelo e-mail informado no terminal.
    usuario = db.session.scalar(
        db.select(Usuario).filter_by(
            email=email.strip().lower()
        )
    )

    # Informa quando a conta ainda não foi cadastrada.
    if usuario is None:
        raise click.ClickException(
            "Crie essa conta pela tela de cadastro primeiro."
        )

    # Altera o perfil e confirma no banco.
    usuario.perfil = "admin"
    db.session.commit()

    click.echo("Perfil admin atribuído.")


# Prepara o banco dentro do contexto da aplicação.
with app.app_context():

    # Ativa a verificação das chaves estrangeiras a cada conexão.
    @event.listens_for(db.engine, "connect")
    def ativar_chaves(conexao, registro):
        cursor = conexao.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.close()

    # Cria as tabelas ausentes, incluindo a tabela de usuários.
    db.create_all()

    # Confere as colunas existentes na tabela evento.
    colunas = {
        coluna["name"]
        for coluna in inspect(db.engine).get_columns("evento")
    }

    # Atualiza o banco antigo caso ainda não tenha vagas.
    if "vagas" not in colunas:
        with db.engine.begin() as conexao:
            conexao.execute(
                text(
                    "ALTER TABLE evento "
                    "ADD COLUMN vagas INTEGER"
                )
            )


# Inicia o servidor ao executar este arquivo.
if __name__ == "__main__":
    app.run(debug=True)