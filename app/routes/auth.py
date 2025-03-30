from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from app import db, login_manager
from app.models.user import User


auth_bp = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(user_id):
    if user_id.isdigit():
        return User.query.get(int(user_id))
    return None

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('heladeria.home'))
        else:
            flash('Usuario o contraseña incorrectos', 'error')
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        email = request.form['email']
        role = request.form.get('role', 'cliente')
         
        #Validar si el correo ya existe
        if User.query.filter_by(email=email).first():
            flash('El correo ya esta registrado', 'error')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(username=username).first():
            flash('El usuario ya existe', 'error')
            return redirect(url_for('auth.register'))
        
        #Determinar los valores de es_admin y es_empleado
        es_admin = role == 'admin'
        es_empleado = role == 'empleado'
        
        # Crear usuario con su rol
        new_user = User(
            username = username,
            email = email,
            password_hash = password,
            role=role,
        )
        
        db.session.add(new_user)
        db.session.commit()
        flash('Usuario creado con exito. Continua', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')