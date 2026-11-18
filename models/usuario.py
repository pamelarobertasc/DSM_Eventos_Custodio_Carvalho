# Importa o SQLAlchemy compartilhado pelo projeto.
from extensions import db


# Representa uma conta de acesso ao sistema.
class Usuario(db.Model):

    # Identifica cada usuário.
    id = db.Column(db.Integer, primary_key=True)

    # Guarda o nome obrigatório.
    nome = db.Column(db.String(120), nullable=False)

    # Guarda um e-mail obrigatório e único.
    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    # Guarda a senha transformada em hash.
    senha_hash = db.Column(db.String(255), nullable=False)

    # Novas contas recebem o perfil comum.
    perfil = db.Column(
        db.String(20),
        nullable=False,
        default="comum"
    )