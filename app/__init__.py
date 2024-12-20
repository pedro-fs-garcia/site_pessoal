from flask import Flask
from .database.database_connection import init_db

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'sua-chave-secreta'

    init_db()

    from .routes import main
    app.register_blueprint(main)

    return app
