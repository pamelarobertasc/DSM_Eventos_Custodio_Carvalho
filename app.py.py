from flask import Flask
app = Flask(__name__)

@app.route("/")
def inicio():
    return "Olá, mundo!"

@app.route("/sobre")
def sobre():
    return "Gestão de Eventos DW2"

@app.route("/eventos")
def eventos():
    return "Lista de Eventos aqui"

if __name__ == "__main__":
    app.run(debug=True)
