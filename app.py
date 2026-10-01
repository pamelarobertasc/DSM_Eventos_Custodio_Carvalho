from flask import Flask

from extensions import db

from Controllers.evento_controller import evento_bp
from Controllers.site_controller import site_bp

from Models.evento import Evento

from DAO.evento_dao import EventoDAO


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///eventos.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

app.register_blueprint(evento_bp)
app.register_blueprint(site_bp)


with app.app_context():
    db.create_all()

 #  3 with app.app_context():
 # novo = Evento (
 #       nome="Hackathon",
  #      data="2026-10-01",
   #     local="Lab 3"
    #)

    #db.session.add(novo)
    #db.session.commit()

    #print("Evento cadastrado com sucesso!")

    #eventos = Evento.query.all()

   # evento_id = Evento.query.get(1)

#if evento_id:
 # print("GET:")
 # print(evento_id.id, evento_id.nome, evento_id.data, evento_id.local)
    
#else:
 #   print("Evento com ID 1 não encontrado.")

    #eventos_lab = Evento.query.filter_by(local="Lab 3").all()

   # print("FILTER_BY:")

    #for evento in eventos_lab:
      #  print(
     #       evento.id,
    #        evento.nome,
   #         evento.data,
  #          evento.local
 #       )

#for evento in eventos:
 #   print(evento.id, evento.nome, evento.data, evento.local)

#with app.app_context():

    #evento = Evento(
     #   nome="Workshop ORM",
     #   data="2026-10-15",
     #   local="Lab 2"
    #)

    #EventoDAO.salvar(evento)

    #eventos = EventoDAO.listar()

    #print("EVENTOS CADASTRADOS:")

    #for evento in eventos:
       # print(
            #evento.id,
           # evento.nome,
          #  evento.data,
         #   evento.local
        #)

if __name__ == "__main__":
    app.run(debug=True)
