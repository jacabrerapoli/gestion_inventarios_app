from sqlalchemy import Column, Integer, String, ForeignKey, Float, TIMESTAMP, Text, func
from sqlalchemy.orm import declarative_base, relationship

from config.database import engine

Base = declarative_base()


class Clientes(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True)
    tipo_identificacion = Column(String(50))
    num_identificacion = Column(String(50))
    nombres = Column(String(45))
    apellidos = Column(String(45))
    correo = Column(String(45))
    direccion = Column(String(45))
    telefono = Column(String(45))


class Proveedores(Base):
    __tablename__ = 'proveedores'
    id = Column(Integer, primary_key=True)
    tipo_identificacion = Column(String(45))
    numero_identificacion = Column(String(45))
    nombre_empresa = Column(String(45))
    nombre_representante = Column(String(45))
    apellido_representante = Column(String(45))
    correo = Column(String(45))
    direccion = Column(String(45))
    telefono = Column(String(45))


class Transacciones(Base):
    __tablename__ = 'transacciones'
    id = Column(Integer, primary_key=True)
    uuid = Column(String, unique=True)
    fecha = Column(TIMESTAMP, server_default=func.now())
    total = Column(Float)
    tipo_transaccion_id = Column(Integer, ForeignKey('tipo_transacciones.id'))
    clientes_id = Column(Integer, ForeignKey('clientes.id'))
    proveedor_id = Column(Integer, ForeignKey('proveedores.id'))
    tipo_transaccion = relationship('TipoTransacciones')
    cliente = relationship(Clientes)
    proveedor = relationship(Proveedores)
    detalle_transacciones = relationship('DetalleTransacciones', cascade="all, delete-orphan")


class DetalleTransacciones(Base):
    __tablename__ = 'detalle_transacciones'
    id = Column(Integer, primary_key=True)
    cantidad = Column(Integer)
    subtotal = Column(Float)
    transaccion_id = Column(Integer, ForeignKey('transacciones.id'))
    productos_id = Column(Integer, ForeignKey('productos.id'))
    transaccion = relationship(Transacciones, overlaps="detalle_transacciones")
    producto = relationship('Productos')


class Kardex(Base):
    __tablename__ = 'kardex'
    id = Column(Integer, primary_key=True)
    uuid = Column(String(50))
    tipo_transaccion = Column(Integer)
    productos_id = Column(Integer, ForeignKey('productos.id'))
    cantidad = Column(Integer)
    fecha = Column(TIMESTAMP, server_default=func.now())


class Productos(Base):
    __tablename__ = 'productos'
    id = Column(Integer, primary_key=True)
    sku = Column(String(45))
    nombre = Column(String(45))
    marca = Column(String(45))
    linea = Column(String(45))
    descripcion = Column(Text)
    costo = Column(Float)
    precio = Column(Float)


class TipoTransacciones(Base):
    __tablename__ = 'tipo_transacciones'
    id = Column(Integer, primary_key=True)
    tipo = Column(String(45))


Base.metadata.create_all(engine)
