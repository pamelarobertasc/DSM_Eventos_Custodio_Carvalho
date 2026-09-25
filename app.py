from flask import Flask
from Controllers.evento_controller import evento_bp
from Controllers.site_controller import site_bp

app = Flask(__name__)
app.register_blueprint(evento_bp)
app.register_blueprint(site_bp)

if __name__ == "__main__":
    app.run(debug=True)
