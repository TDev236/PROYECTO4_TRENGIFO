from flask import Flask
from config import Config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()



def create_app():
    app = Flask(__name__, template_folder=os.path.abspath('app/views'))
    app.config.from_object(Config)
    
    app.secret_key = "super_secreto"
    #Aqui se debe inicializar la base de datos y el login manager
    db.init_app(app)
    migrate.init_app(app,db)
    login_manager.init_app(app)
    
    #Aqui va la configuracion de LoginManager
    login_manager.login_view = "auth.login" # con testo redirigimos a la vista del login si no esta autenticado
    
    
    from app.models.user import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    from app.models.ingrediente import Ingrediente, Base, Complemento
    from app.models.heladeria import Heladeria
    from app.models.producto import Producto
    
    #Aqui registramos el controlador
    from app.routes.auth import auth_bp #esta es l ruta de la autenticacion
    from app.routes.productos import productos_bp
    from app.routes.heladeria_routes import heladeria_bp
    app.register_blueprint(heladeria_bp, url_prefix='/')
    app.register_blueprint(productos_bp, url_prefix='/productos')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    return app