from sqlalchemy import func

from config.database import session
from models.models import Transacciones, Kardex, Productos
from services import producto_service


def agregar_transacciones(transaccion_db: Transacciones):
    for detalle in transaccion_db.detalle_transacciones:
        kardex_db = Kardex()
        kardex_db.uuid = transaccion_db.uuid
        kardex_db.fecha = func.now()
        if transaccion_db.tipo_transaccion_id == 1:
            kardex_db.cantidad = -detalle.cantidad
        elif transaccion_db.tipo_transaccion_id == 2:
            kardex_db.cantidad = detalle.cantidad
        kardex_db.tipo_transaccion = transaccion_db.tipo_transaccion_id
        kardex_db.productos_id = detalle.producto.id
        session.add(kardex_db)
        session.commit()
        session.refresh(kardex_db)


def listar_kardex_por_producto_sku(sku: str):
    producto: Productos = producto_service.buscar_producto_por_sku(sku)
    return session.query(Kardex).filter(Kardex.productos_id == producto.id).all()

