from flask import Blueprint, request, jsonify, render_template
from app.controllers.heladeria_controller import HeladeriaController
from app.models.producto import Producto
from app import db
from app.auth.decorators import admin_required

productos_bp = Blueprint("productos", __name__)
heladeria_controller = HeladeriaController()


#esta es la ruta para listar todos los productos
@productos_bp.route("/", methods=["GET"])
def listar_productos():
    productos = Producto.query.all()
    productos_json = [
        {"id": p.id, "nombre": p.nombre, "precio": p.precio_publico}
        for p in productos
    ]
    
    print(productos_json)
    return render_template("index.html", productos_json = productos_json)

#Consultar un producto por ID
@productos_bp.route("/<int:producto_id>", methods=["GET"])
def obtener_producto_por_id(producto_id):
    producto = Producto.query.get(producto_id)
    if not producto:
        return jsonify({"error": "producto no encontrado"}), 404
    return jsonify({"id": producto.id, "nombre": producto.nombre, "precio": producto.precio_publico}), 200

#Consultar producto por nombre
@productos_bp.route("/buscar", methods=["GET"])
def obtener_producto_por_nombre():
    nombre= request.args.get("nombre")
    producto = Producto.query.filter_by(nombre=nombre).first()
    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404
    return jsonify({"id": producto.id, "nombre": producto.nombre, "precio": producto.precio_publico}), 200


#Calcular calorias de un producto

@productos_bp.route("/<int:producto_id>/calorias", methods=["GET"])
def obtener_calorias_producto(producto_id):
    producto = Producto.query.get(producto_id)
    
    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404
    
    return jsonify({"id": producto.id, "nombre": producto.nombre, "calorias": producto.calorias}), 200


#consultar rentabilidad de un producto
@productos_bp.route("/<int:producto_id>/rentabilidad", methods=["GET"])
def obtener_rentabilidad_producto(producto_id):
    producto = Producto.query.get(producto_id)
    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404
    rentabilidad = producto.precio_publico - producto.costo_produccion
    return jsonify({"id": producto.id, "nombre": producto.nombre, "rentabilidad": rentabilidad}), 200


# Consultar costo de produccion de un producto
@productos_bp.route("/<int:producto_id>/costo", methods=["GET"])
def obtener_costo_produccion_producto(producto_id):
    producto = Producto.query.get(producto_id)
    if not producto:
        return jsonify({"error": "producto no encontrado"}), 400
    return jsonify({"id": producto.id, "nombre": producto.nombre, "costo_produccion": producto.costo_produccion}), 200

# vender producto por id
@productos_bp.route("/<int:producto_id>/vender", methods=["POST"])
def vender_producto_por_id(producto_id):
    producto = Producto.query.get(producto_id)
    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404
    if producto.stock <=0:
        return jsonify({"error": "no hay stock disponible"}), 400
    
    producto.stock -= 1
    db.session.commit()
    return jsonify({"mensaje": "Venta realizada", "producto": producto.nombre, "stock_restante": producto.stock}), 200

#reabastecer productos por ID
@productos_bp.route("/<int:producto_id>/reabastecer", methods=["POST"])
def reabastecer_producto(producto_id):
    data = request.get_json()
    cantidad = data.get("cantidad", 0)
    
    producto = Producto.query.get(producto_id)
    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 400
    
    producto.stock += cantidad
    db.session.commit()
    return jsonify({"mensaje": "Producto reabastecido", "stock_actual":producto.stock}), 200

#renovar inventario de producto por ID
@productos_bp.route("/<int:producto_id>/renovar", methods=["POST"])
def renovar_inventario_producto(producto_id):
    producto = Producto.query.get(producto_id)
    if not producto:
        return jsonify({"error": "producto no encontrado"}), 404
    
    producto.stock = 10
    db.session.commit()
    return jsonify({"mensaje": "Inventario renovado", "stock_actual": producto.stock}), 200



# ruta pra agregar un nuevo producto
@productos_bp.route("/", methods=["POST"])
@admin_required
def agregar_producto():
    data = request.get_json()
    nombre = data.get("nombre")
    precio = data.get("precio")
    tipo = data.get("tipo")
    extra = data.get("extra")
    
    if not nombre or not precio or not tipo or not extra:
        return jsonify({"error": "Faltan datos obligatorios"}), 400
    
    try:
        heladeria_controller.agregar_producto(nombre, precio, tipo, extra)
        return jsonify({"mensaje": "Producto agregado exitosamente"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
#ruta para vender los produtos
@productos_bp.route("/vender", methods=["POST"])
def vender_producto():
    data = request.get_json()
    nombre = data.get("nombre")
    
    if not nombre:
        return jsonify({"error" : "Obligatorio el nombre del producto"}), 400
    
    resultado = heladeria_controller.realizar_venta(nombre)
    
    if resultado:
        return jsonify({"mensaje": "Venta realizada con exito"})
    else:
        return jsonify({"error": "producto no encontrado o sin stock"}), 400

@productos_bp.route("/<int:id>", methods=["PUT"])
def actualizar_producto(id):
    data = request.get_json()
    nombre = data.get("nombre")
    precio = data.get("precio")
    tipo = data.get("tipo")
    extra = data.get("extra")
    
    producto = Producto.query.get(id)
    
    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404
    
    if nombre: 
        producto.nombre = nombre
    if precio:
        producto.precio_publico = precio
    if tipo:
        producto.tipo = tipo
    if extra:
        producto.extra = extra
        
    try:
        from app import db
        db.session.commit()
        return jsonify({"mensaje": "Producto actualizado exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@productos_bp.route("/<int:id>", methods=["DELETE"])
def eliminar_producto(id):
    producto = Producto.query.get(id)
    
    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404
    
    try:
        from app import db
        db.session.delete(producto)
        db.session.commit()
        return jsonify({"mensaje": "Producto eliminado exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    