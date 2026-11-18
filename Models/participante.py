# Usa a instância compartilhada do SQLAlchemy.
from extensions import db


# Representa uma pessoa que pode se inscrever nos eventos.
class Participante(db.Model):

    # Identifica cada participante.
    id = db.Column(db.Integer, primary_key=True)

    # Nome obrigatório do participante.
    nome = db.Column(db.String(120), nullable=False)

    # E-mail obrigatório. unique impede e-mails repetidos.
    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    # Liga o participante às inscrições que ele realizou.
    # Ao excluir o participante, suas inscrições são excluídas.
    inscricoes = db.relationship(
        "Inscricao",
        back_populates="participante",
        cascade="all, delete-orphan"
    )