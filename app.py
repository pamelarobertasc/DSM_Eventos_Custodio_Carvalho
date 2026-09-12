from flask import Flask
from Controllers.evento_controller import evento_bp

app = Flask(__name__)
app.register_blueprint(evento_bp)

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/")
def inicio():
    return "Olá, mundo!"

@app.route("/sobre")
def sobre():
    return "Gestão de Eventos - DW2."

@app.route("/eventos")
def eventos():
    return "Lista de eventos aqui."

#Isso é um comentário
#Agora executamos pelos proximos comandos o servidor web 
if __name__ == "__main__":
    app.run(debug=True)