# Permite registrar a data e a hora da inscrição em UTC.
from datetime import datetime, timezone

# Usa a instância compartilhada do SQLAlchemy.
from extensions import db


# Liga um participante a um evento.
class Inscricao(db.Model):

    # Identifica cada inscrição.
    id = db.Column(db.Integer, primary_key=True)

    # Guarda o ID de um participante existente.
    participante_id = db.Column(
        db.Integer,
        db.ForeignKey("participante.id"),
        nullable=False
    )

    # Guarda o ID de um evento existente.
    evento_id = db.Column(
        db.Integer,
        db.ForeignKey("evento.id"),
        nullable=False
    )

    # Preenche a data e a hora ao inserir uma nova inscrição.
    data_inscricao = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    # Permite acessar a pessoa por inscricao.participante.
    participante = db.relationship(
        "Participante",
        back_populates="inscricoes"
    )

    # Permite acessar o evento por inscricao.evento.
    evento = db.relationship(
        "Evento",
        back_populates="inscricoes"
    )

    # Impede duas inscrições da mesma pessoa no mesmo evento.
    __table_args__ = (
        db.UniqueConstraint(
            "participante_id",
            "evento_id",
            name="inscricao_unica"
        ),
    )