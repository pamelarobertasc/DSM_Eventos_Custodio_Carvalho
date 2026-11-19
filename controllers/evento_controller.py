# Permite validar a data recebida.
from datetime import date

# Importa as ferramentas usadas pelo controller.
from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

# Importa as operações do banco e o modelo Evento.
from dao.evento_dao import EventoDAO
from models.evento import Evento


# Cria o grupo de rotas de eventos.
evento_bp = Blueprint("evento", __name__)


@evento_bp.before_request
def exigir_login():
    # g.usuario é preenchido no app.py antes de cada requisição.
    # Se não houver usuário autenticado, abre o login.
    if g.usuario is None:
        # Pedidos para a API recebem uma resposta JSON.
        if request.path.startswith("/api/"):
            return jsonify(erro="Entre na sua conta para acessar a API."), 401

        # Pedidos de páginas continuam abrindo a tela de login.
        return redirect(url_for("auth.login"))
    
    # Conta as visitas somente ao abrir a listagem por GET.
    if (
        request.method == "GET"
        and request.endpoint in ("evento.index", "evento.eventos")
    ):
        # Contador individual, associado à sessão do navegador.
        session["visitas"] = session.get("visitas", 0) + 1

        # Contador compartilhado durante a execução deste processo.
        current_app.config["ACESSOS"] = (
            current_app.config.get("ACESSOS", 0) + 1
        )


def ler_campos():
    # Lê os campos enviados e remove espaços das pontas.
    nome = request.form.get("nome", "").strip()
    data = request.form.get("data", "").strip()
    local = request.form.get("local", "").strip()
    vagas = request.form.get("vagas", "").strip()

    # Confere o nome obrigatório e o tamanho dos textos.
    if not nome or len(nome) > 120 or len(local) > 120:
        raise ValueError(
            "Informe o nome e use até 120 caracteres "
            "no nome e no local."
        )

    # Valida a data e padroniza para ano-mês-dia.
    try:
        data = date.fromisoformat(data).isoformat()
    except ValueError:
        raise ValueError("Informe uma data válida.")

    # Campo vazio vira None. Caso preenchido, deve ser inteiro.
    try:
        vagas = int(vagas) if vagas else None
    except ValueError:
        raise ValueError("Vagas deve ser um número inteiro.")

    # Impede quantidade negativa de vagas.
    if vagas is not None and vagas < 0:
        raise ValueError(
            "Vagas deve ser zero ou um número positivo."
        )

    # Entrega os valores validados ao cadastro ou à edição.
    return {
        "nome": nome,
        "data": data,
        "local": local,
        "vagas": vagas,
    }


def mostrar_formulario(erro=None, evento=None, editar=False):
    # Escolhe a página de cadastro ou edição.
    pagina = "editar.html" if editar else "index.html"

    # Entrega os dados necessários ao template.
    return render_template(
        pagina,
        evento=evento,
        eventos=EventoDAO.listar(),
        erro=erro,
        valores=request.form,
    )


@evento_bp.route("/", methods=["GET", "POST"])
def index():
    # POST acontece quando o cadastro é enviado.
    if request.method == "POST":
        try:
            campos = ler_campos()

        except ValueError as erro:
            # Exibe o erro mantendo os valores digitados.
            return mostrar_formulario(str(erro)), 400

        # Cria o objeto com os dados validados.
        evento = Evento(**campos)

        # Grava o evento no banco.
        EventoDAO.salvar(evento)

        # Guarda a mensagem que aparecerá após o redirecionamento.
        flash("Evento cadastrado!", "sucesso")

        # Pede ao navegador para abrir a lista com GET.
        return redirect(
            url_for("evento.index"),
            code=303,
        )

    # GET exibe a listagem e o formulário.
    return mostrar_formulario()


@evento_bp.route("/eventos", methods=["GET", "POST"])
def eventos():
    # Disponibiliza a mesma página pelo endereço /eventos.
    return index()


@evento_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    # Busca o registro indicado pelo ID da URL.
    evento = EventoDAO.buscar_por_id(id)

    # Encerra a requisição se o evento não existir.
    if evento is None:
        abort(404)

    # POST recebe os novos valores do formulário.
    if request.method == "POST":
        try:
            campos = ler_campos()

        except ValueError as erro:
            # Mostra o erro no formulário de edição.
            return mostrar_formulario(
                erro=str(erro),
                evento=evento,
                editar=True,
            ), 400

        # Atualiza os dados no banco.
        EventoDAO.atualizar(evento, **campos)

        # Prepara o aviso de sucesso.
        flash("Evento atualizado!", "sucesso")

        # Volta para a listagem.
        return redirect(
            url_for("evento.index"),
            code=303,
        )

    # GET abre o formulário com os dados atuais.
    return mostrar_formulario(
        evento=evento,
        editar=True,
    )


@evento_bp.post("/excluir/<int:id>")
def excluir(id):
    # Confere a permissão no servidor.
    # Somente uma conta com perfil admin pode excluir.
    if g.usuario.perfil != "admin":
        abort(403)

    # Busca o evento escolhido.
    evento = EventoDAO.buscar_por_id(id)

    # Responde 404 quando o ID não existe.
    if evento is None:
        abort(404)

    # Remove o evento do banco.
    EventoDAO.excluir(evento)

    # Prepara a mensagem para a próxima página.
    flash("Evento excluído!", "sucesso")

    # Abre a lista atualizada.
    return redirect(
        url_for("evento.index"),
        code=303,
    )

# GET devolve todos os eventos em JSON.
@evento_bp.get("/api/eventos")
def api_listar():
    # Consulta os objetos do banco.
    eventos = EventoDAO.listar()

    # Converte cada objeto em dicionário.
    lista = [evento.para_dicionario() for evento in eventos]

    # Gera a resposta JSON com status 200.
    return jsonify(lista)


# GET devolve somente o evento indicado pelo ID.
@evento_bp.get("/api/eventos/<int:id>")
def api_buscar(id):
    # Procura o registro no banco.
    evento = EventoDAO.buscar_por_id(id)

    # Retorna uma mensagem JSON se o ID não existir.
    if evento is None:
        return jsonify(erro="Evento não encontrado."), 404

    # Retorna os dados do evento encontrado.
    return jsonify(evento.para_dicionario())