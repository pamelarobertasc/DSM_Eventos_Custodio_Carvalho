# Importa as ferramentas para rotas, formulários, mensagens e sessão.
from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

# Permite identificar conflitos, como dois cadastros com o mesmo e-mail.
from sqlalchemy.exc import IntegrityError

# Ferramentas para gerar e conferir o hash da senha.
from werkzeug.security import (
    check_password_hash,
    generate_password_hash,
)

# Importa o DAO e o modelo de usuário.
from dao.usuario_dao import UsuarioDAO
from models.usuario import Usuario


# Cria o grupo de rotas de autenticação.
auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    # POST acontece quando o formulário de cadastro é enviado.
    if request.method == "POST":

        # Lê os campos. Padroniza o e-mail em letras minúsculas.
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")

        # Confere os dados básicos do cadastro.
        if (
            not nome
            or len(nome) > 120
            or len(email) > 120
            or "@" not in email
        ):
            flash("Confira o nome e o e-mail.", "erro")

        # Confere o tamanho da senha também no servidor.
        elif len(senha) < 8 or len(senha) > 128:
            flash(
                "A senha deve ter entre 8 e 128 caracteres.",
                "erro",
            )

        # Evita criar outra conta com o mesmo e-mail.
        elif UsuarioDAO.buscar_por_email(email):
            flash("Esse e-mail já possui uma conta.", "erro")

        else:
            # Cria a conta com o perfil comum definido no modelo.
            # Guarda o hash gerado a partir da senha.
            usuario = Usuario(
                nome=nome,
                email=email,
                senha_hash=generate_password_hash(senha),
            )

            try:
                # Pede ao DAO para gravar a conta.
                UsuarioDAO.salvar(usuario)

            except IntegrityError:
                # Trata uma possível tentativa simultânea de
                # cadastrar o mesmo e-mail.
                flash("Esse e-mail já possui uma conta.", "erro")

            else:
                flash(
                    "Conta criada! Entre com seu e-mail e senha.",
                    "sucesso",
                )

                # Abre a página de login após o cadastro.
                return redirect(
                    url_for("auth.login"),
                    code=303,
                )

    # No GET ou após erro, apresenta o formulário de cadastro.
    # Mantém nome e e-mail digitados para facilitar a correção.
    return render_template(
        "auth.html",
        cadastro=True,
        valores=request.form,
    )


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    # POST acontece quando a pessoa tenta entrar.
    if request.method == "POST":

        # Lê o e-mail e a senha enviados.
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")

        # Busca a conta pelo e-mail.
        usuario = UsuarioDAO.buscar_por_email(email)

        # Só confere a senha se encontrou uma conta.
        if usuario and check_password_hash(
            usuario.senha_hash,
            senha,
        ):
            # Limpa os dados da sessão anterior.
            session.clear()

            # Guarda o ID da pessoa autenticada na sessão.
            session["usuario_id"] = usuario.id

            flash("Você entrou!", "sucesso")

            # Abre a lista de eventos.
            return redirect(
                url_for("evento.index"),
                code=303,
            )

        # Avisa quando o e-mail ou a senha estão incorretos.
        flash("E-mail ou senha inválidos.", "erro")

    # Exibe o mesmo template, configurado como tela de login.
    return render_template(
        "auth.html",
        cadastro=False,
        valores=request.form,
    )


@auth_bp.post("/sair")
def sair():
    # Apaga a identificação e os demais dados da sessão.
    session.clear()

    flash("Você saiu da conta.", "sucesso")

    # Volta à tela de login.
    return redirect(
        url_for("auth.login"),
        code=303,
    )