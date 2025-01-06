from flask import Flask
from flask_login import LoginManager
from .database.database_connection import init_db
from .models.user import User

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'sua-chave-secreta'

    init_db()

    from .routes.main_routes import main
    from .routes.admin_routes import admin
    app.register_blueprint(main)
    app.register_blueprint(admin)

    app.secret_key = 'sua_chave_secreta'
    login_manager.init_app(app)
    login_manager.login_view = 'home' #Redireciona usuários não autenticados para a página home

    return app


@login_manager.user_loader
def load_user(username, password = ""):
    return User(password, username)