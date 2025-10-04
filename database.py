from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email_verificado = db.Column(db.Boolean, default=False)
    rol = db.Column(db.String(50), default='usuario')

class Categoria(db.Model):
    __tablename__ = 'categorias'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    productos = db.relationship('Producto', backref='categoria', lazy=True)

class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    imagen_principal = db.Column(db.String(255))
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    imagenes = db.relationship('ProductoImagen', backref='producto', lazy=True)

class ProductoImagen(db.Model):
    __tablename__ = 'producto_imagenes'
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    url = db.Column(db.String(255), nullable=False)

class Pedido(db.Model):
    __tablename__ = 'pedidos'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    total = db.Column(db.Float, nullable=False)
    pago_id = db.Column(db.String(120))  

    # Datos de contacto/envío
    email = db.Column(db.String(120), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(50), nullable=False)
    codigo_postal = db.Column(db.String(10), nullable=False)
    provincia = db.Column(db.String(100), nullable=False)
    ciudad = db.Column(db.String(100), nullable=False)
    barrio = db.Column(db.String(100), nullable=False)
    calle = db.Column(db.String(120),nullable=False)
    numero_calle = db.Column(db.String(20))
    departamento = db.Column(db.String(50))

    # Para retiro por otra persona
    retira_otro = db.Column(db.Boolean, default=False)
    nombre_retira = db.Column(db.String(100))
    apellido_retira = db.Column(db.String(100))

    productos = db.relationship('PedidoItem', backref='pedido', lazy=True)


class PedidoItem(db.Model):
    __tablename__ = 'pedido_items'
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    cantidad = db.Column(db.Integer, default=1)
    precio_unitario = db.Column(db.Float, nullable=False)

    producto = db.relationship('Producto', lazy=True)
