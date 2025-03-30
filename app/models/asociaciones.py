from app import db

#tabla donde se relacionana muchos a muchos
producto_ingrediente = db.Table(
    "producto_ingrediente",
    db.Column('producto_id', db.Integer, db.ForeignKey('productos.id'), primary_key=True),
    db.Column('ingrediente_id', db.Integer, db.ForeignKey('ingredientes.id'), primary_key=True)
)