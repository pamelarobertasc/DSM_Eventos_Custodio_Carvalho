from flask import Blueprint, render_template, request, redirect

from Models.evento import Evento
from DAO.evento_dao import EventoDAO


evento_bp = Blueprint("evento", __name__)


@evento_bp.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        evento = Evento(
            nome=request.form["nome"],
            data=request.form["data"],
            local=request.form["local"]
        )

        EventoDAO.salvar(evento)

        return redirect("/")

    eventos = EventoDAO.listar()

    return render_template("index.html", eventos=eventos)


@evento_bp.route("/eventos")
def listar_eventos_texto():

    eventos = EventoDAO.listar()

    texto = ""

    for evento in eventos:
        texto += f"{evento.id} - {evento.nome} - {evento.data} - {evento.local}<br>"

    return texto
