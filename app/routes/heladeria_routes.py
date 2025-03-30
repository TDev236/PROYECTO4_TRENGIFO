from flask import Blueprint, request, jsonify, render_template, session, flash, redirect, url_for
from app.controllers.heladeria_controller import HeladeriaController
from flask_login import current_user

heladeria_bp = Blueprint('heladeria', __name__)
controller = HeladeriaController()

@heladeria_bp.route("/")
def home():
    if not current_user.is_authenticated:
        flash('Debes inciar sesion primero', 'warning')
        return redirect(url_for('auth.login'))
    return render_template("index.html")

@heladeria_bp.route('/agregar_producto', methods=['POST'])
def agregar_producto():
    data = request.json
    controller.agregar_producto(data['nombre'], data['precio'], data['tipo'], data['extra'])
    return jsonify({"mensaje": "Producto agreagado"}) , 200


@heladeria_bp.route('/vender', methods = ['POST'])
def vender():
    data = request.json
    vendido = controller.realizar_venta(data['nombre'])
    return jsonify({"vendido": vendido})