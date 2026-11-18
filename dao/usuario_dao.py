# Importa a instância compartilhada do SQLAlchemy.
from extensions import db

# Importa o modelo das contas de acesso.
from models.usuario import Usuario


# Concentra as operações de banco relacionadas aos usuários.
class UsuarioDAO:

    @staticmethod
    def buscar_por_email(email):
        # Monta a consulta usando o e-mail recebido.
        consulta = db.select(Usuario).filter_by(email=email)

        # Retorna o usuário encontrado ou None, se ele não existir.
        return db.session.scalar(consulta)

    @staticmethod
    def salvar(usuario):
        # Prepara o novo usuário para inserção.
        db.session.add(usuario)

        try:
            # Confirma a gravação no banco.
            db.session.commit()

        except Exception:
            # Se houver erro, desfaz a transação.
            db.session.rollback()

            # Repassa o erro para o controller tratar.
            raise