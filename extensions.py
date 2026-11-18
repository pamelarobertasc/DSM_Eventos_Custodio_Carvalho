# Importa a ferramenta que conecta os modelos ao banco.
from flask_sqlalchemy import SQLAlchemy

# Cria uma única instância para compartilhar entre os arquivos.
# A conexão com a aplicação será configurada no app.py.
db = SQLAlchemy()