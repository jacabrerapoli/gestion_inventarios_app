from sqlalchemy import func

from config.database import session
from models.models import Transacciones, Kardex


def agregar_transacciones(transaccion_db: Transacciones):
    kardex_db = Kardex()
    for detalle in transaccion_db.detalle_transacciones:
        kardex_db.uuid = transaccion_db.uuid
        kardex_db.fecha = func.now()
        kardex_db.cantidad = -detalle.cantidad if transaccion_db.tipo_transaccion_id == 1 else detalle.cantidad
        kardex_db.tipo_transaccion_id = transaccion_db.tipo_transaccion_id
        kardex_db.productos_id = detalle.producto.id
        session.add(kardex_db)
