from abc import ABC, abstractmethod
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from app import db
from app.models.asociaciones import producto_ingrediente

class Ingrediente(db.Model):
    __tablename__ = 'ingredientes'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(250), nullable=False, unique=True)
    precio = db.Column(db.Float, nullable=False)
    calorias = db.Column(db.Integer, nullable=False)
    inventario = db.Column(db.Integer, default=0)
    es_vegetariano = db.Column(db.Boolean, nullable=False)
    
    tipo = db.Column(db.String(250), nullable=False)
    
    productos = db.relationship('Producto', secondary=producto_ingrediente, back_populates= 'ingredientes')
    
    def __init__(self, nombre, precio, calorias, inventario, es_vegetariano):
        self.nombre = nombre
        self.precio = precio
        self.calorias = calorias
        self.inventario = inventario
        self.es_vegetariano = es_vegetariano
        
    def es_sano(self):
        return self.calorias < 100 or self.es_vegetariano
    
    
class Base(Ingrediente):
    __tablename__ = 'base'
    id = db.Column(db.Integer, db.ForeignKey('ingredientes.id'), primary_key=True)
    sabor = db.Column(db.String(250), nullable= False)
    
    
    
    def abastecer(self):
        self.inventario += 5

class Complemento(Ingrediente):
    __tablename__ = 'complemento'
    id = db.Column(db.Integer, db.ForeignKey('ingredientes.id'), primary_key=True)
    
    
    def abastecer(self):
        self.inventario += 10
    
    def renovar_inventario(self):
        self.inventario = 0