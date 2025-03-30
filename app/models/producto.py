from app import db
from abc import ABC, abstractmethod, ABCMeta
from app.models.asociaciones import producto_ingrediente



class IProducto(ABC):
    @abstractmethod
    def calcular_costo(self):
        pass
    
    @abstractmethod
    def calcular_calorias(self):
        pass
    
    
    @abstractmethod
    def calcular_rentabilidad(self):
        pass


class Producto(db.Model):
    __tablename__ = 'productos'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False)
    precio_publico = db.Column(db.Float, nullable=False)
    
    ingredientes = db.relationship("Ingrediente", secondary=producto_ingrediente, back_populates="productos")
    
    def __init__(self, nombre, precio_publico):
        self.nombre = nombre
        self.precio_publico = precio_publico
    
    def calcular_costo(self, ingredientes):
        raise NotImplementedError
    
    def calcular_calorias(self, ingredientes):
        raise NotImplementedError
    
    def calcular_rentabilidad(self, ingredientes):
        raise NotImplementedError

class Copa(Producto):
    def __init__(self, nombre, precio_publico, tipo_vaso):
        super().__init__(nombre, precio_publico)
        self.tipo_vaso = tipo_vaso
    
    def calcular_costo(self, ingredientes):
        return sum(ingrediente.precio for ingrediente in ingredientes)
    
    def calcular_calorias(self, ingredientes):
        return round(sum(ingrediente.calorias for ingrediente in ingredientes) * 0.95, 2)
    
    def calcular_rentabilidad(self, ingredientes):
        return self.precio_publico - self.calcular_costo(ingredientes)

class Malteada(Producto):
    def __init__(self, nombre, precio_publico, volumen):
        super().__init__(nombre, precio_publico)
        self.volumen = volumen
    
    def calcular_costo(self, ingredientes):
        return sum(ingrediente.precio for ingrediente in ingredientes) + 500
    
    def calcular_calorias(self, ingredientes):
        return sum(ingrediente.calorias for ingrediente in ingredientes) + 200
    
    def calcular_rentabilidad(self, ingredientes):
        return self.precio_publico - self.calcular_costo(ingredientes)
