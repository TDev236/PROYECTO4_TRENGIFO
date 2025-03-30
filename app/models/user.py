from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False) 
    role = db.Column(db.Enum("admin", "empleado", "cliente", name="roles"), nullable=False, default="cliente")
    

    def set_password(self, password):
        """Hash y almacena la contraseña."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifica la contraseña ingresada con la almacenada. """
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        return self.role == "admin"
    
    def is_empleado(self):
        return self.role == "empleado"
    
    def is_cliente(self):
        return self.role == "cliente"
    
    
    def is_authenticated(self):
        return True
    
    def __repr__(self):
        return f'<User {self.username} ({self.role})>'