# Importa o SQLAlchemy criado no extensions.py.
from extensions import db


# Representa a tabela de eventos no banco.
class Evento(db.Model):

    # Identifica cada evento com um número único.
    id = db.Column(db.Integer, primary_key=True)

    # Guarda o nome do evento. O preenchimento é obrigatório.
    nome = db.Column(db.String(120), nullable=False)

    # Guarda a data como texto no formato ano-mês-dia.
    data = db.Column(db.String(10), nullable=False)

    # Guarda o local do evento.
    local = db.Column(db.String(120))

    # Guarda a quantidade de vagas. Pode ficar sem preenchimento.
    vagas = db.Column(db.Integer)

    # Liga um evento às suas inscrições.
    # back_populates conecta essa relação ao atributo "evento"
    # que vamos criar no modelo Inscricao.
    # Ao excluir um evento, suas inscrições também são excluídas.
    inscricoes = db.relationship(
        "Inscricao",
        back_populates="evento",
        cascade="all, delete-orphan"
    )

    # Impede o banco de aceitar uma quantidade negativa de vagas.
    # NULL permite deixar a quantidade sem preenchimento.
    __table_args__ = (
        db.CheckConstraint(
            "vagas IS NULL OR vagas >= 0",
            name="vagas_validas"
        ),
    )