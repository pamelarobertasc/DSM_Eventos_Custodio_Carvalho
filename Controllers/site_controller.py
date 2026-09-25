from flask import Blueprint

site_bp = Blueprint("site", __name__)

@site_bp.route("/sobre")
def sobre():
    return "Gestão de Eventos - DW2."
