from sqlalchemy import Column, Integer
from app import db
from app.models.producto import Producto

class Heladeria(db.Model):
    __tablename__ = 'heladeria'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ventas_del_dia = db.Column(db.Integer, default=0)
    
    def __init__(self):
        self.ventas_del_dia = 0
        self.productos = []
        
    def agregar_producto(self, producto):
        if len(self.productos) < 4:
            self.productos.append(producto)
    
    def mejor_producto(self):
        return max(self.productos, key= lambda p: p.calcular_rentabilidad(p.ingredientes))
    
    def vender(self, producto):
        if producto in self.productos:
            ingredientes_disponibles = all(ing.inventario >= 1 for ing in producto.ingredientes)
            if ingredientes_disponibles:
                for ing in producto.ingredientes:
                    ing.inventario -= 1
                self.ventas_del_dia += producto.precio_publico
                return True
        return False
    
            