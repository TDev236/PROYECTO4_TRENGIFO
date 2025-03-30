from flask import Blueprint, request, jsonify, render_template
from app.controllers.heladeria_controller import HeladeriaController
from app.models.producto import Producto, Copa, Malteada
from app import db
from app.auth.decorators import admin_required
from flask_login import current_user

productos_bp = Blueprint("productos", __name__)
heladeria_controller = HeladeriaController()


#esta es la ruta para listar todos los productos
@productos_bp.route("/", methods=["GET"])
def listar_productos():
    productos = Producto.query.all()
    print(productos)
    productos_json = [
        {"id": p.id, "nombre": p.nombre, "precio": p.precio_publico}
        for p in productos
    ]
    
    es_admin = current_user.is_authenticated and current_user.is_admin
    
    print(productos_json)
    return render_template("index.html", productos_menu = productos, es_admin= es_admin)

#Consultar un producto por ID
@productos_bp.route("/<int:producto_id>", methods=["GET"])
def obtener_producto_por_id(producto_id):
    producto = Producto.query.get(producto_id)
    if not producto:
        return jsonify({"error": "producto no encontrado"}), 404
    return jsonify({
        "id": producto.id, 
        "nombre": producto.nombre, 
        "precio": producto.precio_publico,
        "stock": producto.stock
        }), 200

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
    
    #Aqui verificar si el producto tiene ingredientes antes de calcular calorias
    if not producto.ingredientes:
        return jsonify({"error": "El producto no tiene ingredientes asociados"}), 400
    
    calorias = producto.calcular_calorias(producto.ingredientes)
    return jsonify({
        "id": producto.id, 
        "nombre": producto.nombre, 
        "calorias": calorias
        }), 200


#consultar rentabilidad de un producto
@productos_bp.route("/<int:producto_id>/rentabilidad", methods=["GET"])
def obtener_rentabilidad_producto(producto_id):
    producto = Producto.query.get(producto_id)
    
    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404
    
    if not producto.ingredientes:
        return jsonify({
            "error": "El producto no tiene ingredientes asociados"
        }) , 400
    
    rentabilidad = producto.calcular_rentabilidad(producto.ingredientes)
    return jsonify({
        "id": producto.id, 
        "nombre": producto.nombre, 
        "rentabilidad": rentabilidad
        }), 200


# Consultar costo de produccion de un producto
@productos_bp.route("/<int:producto_id>/costo", methods=["GET"])
def obtener_costo_produccion_producto(producto_id):
    producto = Producto.query.get(producto_id)
    if not producto:
        return jsonify({"error": "producto no encontrado"}), 400
    
    if not producto.ingredientes:
        return jsonify({"error": "El producto no tiene ingredientes asociados"}), 400
    
    costo = producto.calcular_costo(producto.ingredientes)
    return jsonify({
        "id": producto.id, 
        "nombre": producto.nombre, 
        "costo_produccion": costo
        }), 200

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
    nombre = request.form.get("nombre")
    precio = request.form.get("precio")
    tipo = request.form.get("tipo")
    stock = request.form.get("stock", 0)
    
    if not nombre or not precio or not tipo:
        return jsonify({"error": "Faltan datos obligatorios"}), 400
    
    if tipo not in ["Copa", "Malteada"]:
        return jsonify({
            "error": "Tipo de producto no valido"
        }) , 400
        
    if tipo == "Copa":
        producto = Copa(nombre = nombre, precio_publico=precio, tipo_vaso=data.get("tipo_vaso", "Vaso estandar"))
    elif tipo == "Malteada":
        producto = Malteada(nombre=nombre, precio_publico=precio, volumen=data.get("volumen", 500))
    
    producto.stock = stock
    from app import db
    db.session.add(producto)
    db.session.commit()
    
    return jsonify({
        "mensaje": "Producto agregado exitosamente"
    }) , 201
    
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
    extra = data.get("extra")
    
    producto = Producto.query.get(id)
    
    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404
    
    if nombre: 
        producto.nombre = nombre
    if precio:
        producto.precio_publico = precio
    
    if isinstance(producto, Copa) and extra:
        producto.tipo_vaso = extra
    elif isinstance(producto, Malteada) and extra:
        producto.volumen = extra
        
    try:
        db.session.commit()
        return jsonify({
            "mensaje": "Producto actualizado exitosamente"
        }), 200
    except Exception as e:
        return jsonify({
            "error": str(e)
        }) , 500
    

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
    