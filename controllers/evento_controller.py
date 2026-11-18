# Permite verificar se a data recebida é válida.
from datetime import date

# Importa as ferramentas usadas nas rotas.
from flask import (
    Blueprint,
    abort,
    redirect,
    render_template,
    request,
    url_for,
)

# Importa as operações do banco e o modelo Evento.
from dao.evento_dao import EventoDAO
from models.evento import Evento


# Cria o grupo de rotas dos eventos.
evento_bp = Blueprint("evento", __name__)


def ler_campos():
    # Lê os campos enviados e remove espaços das pontas.
    nome = request.form.get("nome", "").strip()
    data = request.form.get("data", "").strip()
    local = request.form.get("local", "").strip()
    vagas = request.form.get("vagas", "").strip()

    # Confere o nome obrigatório e o tamanho dos textos.
    if not nome or len(nome) > 120 or len(local) > 120:
        raise ValueError(
            "Informe o nome e use até 120 caracteres no nome e no local."
        )

    # Verifica a data e padroniza para ano-mês-dia.
    try:
        data = date.fromisoformat(data).isoformat()
    except ValueError:
        raise ValueError("Informe uma data válida.")

    # Converte vagas para inteiro. Campo vazio vira None.
    try:
        vagas = int(vagas) if vagas else None
    except ValueError:
        raise ValueError("Vagas deve ser um número inteiro.")

    # Impede quantidade negativa de vagas.
    if vagas is not None and vagas < 0:
        raise ValueError("Vagas deve ser zero ou um número positivo.")

    # Entrega os campos validados em um dicionário.
    return {
        "nome": nome,
        "data": data,
        "local": local,
        "vagas": vagas,
    }


def mostrar_formulario(erro=None, evento=None, editar=False):
    # Escolhe a página de cadastro ou de edição.
    pagina = "editar.html" if editar else "index.html"

    # Entrega ao HTML os dados necessários para montar a página.
    return render_template(
        pagina,
        evento=evento,
        eventos=EventoDAO.listar(),
        erro=erro,
        valores=request.form,
    )


@evento_bp.route("/", methods=["GET", "POST"])
def index():
    # POST acontece quando o formulário de cadastro é enviado.
    if request.method == "POST":
        try:
            campos = ler_campos()
        except ValueError as erro:
            # Mostra o erro e mantém os valores digitados.
            return mostrar_formulario(str(erro)), 400

        # Os ** distribuem o dicionário pelos atributos do Evento.
        evento = Evento(**campos)

        # Grava o evento no banco.
        EventoDAO.salvar(evento)

        # Após cadastrar, pede ao navegador para abrir a lista com GET.
        return redirect(url_for("evento.index"), code=303)

    # No GET, mostra a lista e o formulário.
    return mostrar_formulario()


@evento_bp.route("/eventos", methods=["GET", "POST"])
def eventos():
    # Disponibiliza a mesma página pelo endereço /eventos.
    return index()


@evento_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    # Busca o evento indicado pelo ID da URL.
    evento = EventoDAO.buscar_por_id(id)

    # Responde 404 quando o evento não existe.
    if evento is None:
        abort(404)

    # POST recebe os dados que a pessoa alterou.
    if request.method == "POST":
        try:
            campos = ler_campos()
        except ValueError as erro:
            return mostrar_formulario(
                erro=str(erro),
                evento=evento,
                editar=True,
            ), 400

        # Atualiza o registro com os campos validados.
        EventoDAO.atualizar(evento, **campos)

        # Volta à lista depois de salvar.
        return redirect(url_for("evento.index"), code=303)

    # No GET, abre o formulário preenchido com o evento.
    return mostrar_formulario(evento=evento, editar=True)


@evento_bp.post("/excluir/<int:id>")
def excluir(id):
    # Busca o evento escolhido para exclusão.
    evento = EventoDAO.buscar_por_id(id)

    # Responde 404 se esse ID não existir.
    if evento is None:
        abort(404)

    # Exclui o evento e confirma a operação no banco.
    EventoDAO.excluir(evento)

    # Volta à lista atualizada.
    return redirect(url_for("evento.index"), code=303)