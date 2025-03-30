from app.models.heladeria import Heladeria
from app.models.producto import Copa, Malteada
from app.models.ingrediente import Base, Complemento
from app import db

class HeladeriaController:
    def __init__(self):
        self.heladeria = Heladeria()
        
    def agregar_producto(self, nombre, precio, tipo, extra):
        if tipo == "copa":
            producto = Copa(nombre, precio, tipo_vaso= extra)
        elif tipo =="malteada":
            producto = Malteada(nombre, precio, volumen = extra)
        else:
            raise ValueError("Tipo de producto no valido")
        
        #aqui la funcion agrega el producto a la db
        db.session.add(producto)
        db.session.commit()
        
        
        self.heladeria.agregar_producto(producto)
    
    def realizar_venta(self, nombre_producto):
        return self.heladeria.vender(nombre_producto)