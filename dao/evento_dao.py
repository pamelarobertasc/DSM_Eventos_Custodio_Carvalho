# Importa a conexão compartilhada com o banco.
from extensions import db

# Importa o modelo que representa os eventos.
from models.evento import Evento


# Concentra as operações de banco relacionadas aos eventos.
class EventoDAO:

    @staticmethod
    def confirmar():
        # Tenta confirmar as alterações no banco.
        try:
            db.session.commit()

        # Se houver erro, desfaz a transação e informa a falha.
        except Exception:
            db.session.rollback()
            raise

    @staticmethod
    def salvar(evento):
        # Prepara um novo evento para inserção.
        db.session.add(evento)

        # Confirma a gravação.
        EventoDAO.confirmar()

    @staticmethod
    def listar():
        # Seleciona todos os eventos, ordenados pelo ID.
        consulta = db.select(Evento).order_by(Evento.id)

        # Executa a consulta e devolve os objetos encontrados.
        return db.session.scalars(consulta).all()

    @staticmethod
    def buscar_por_id(id):
        # Busca um evento pelo ID. Retorna None se ele não existir.
        return db.session.get(Evento, id)

    @staticmethod
    def atualizar(evento, nome, data, local, vagas):
        # Substitui os valores do evento pelos dados recebidos.
        evento.nome = nome
        evento.data = data
        evento.local = local
        evento.vagas = vagas

        # Confirma as alterações no banco.
        EventoDAO.confirmar()

    @staticmethod
    def excluir(evento):
        # Marca o evento para exclusão.
        db.session.delete(evento)

        # Confirma a exclusão no banco.
        EventoDAO.confirmar()