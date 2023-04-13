from sqlalchemy import func

from config.database import session
from enums.tipo_transaccion_enum import TipoTransaccionEnum
from models.models import Transacciones, Kardex


def agregar_transacciones(transaccion_db: Transacciones):
    kardex_db = Kardex()
    for detalle in transaccion_db.detalle_transacciones:
        kardex_db.fecha = func.now()
        kardex_db.cantidad = detalle.cantidad
        kardex_db.costo = detalle.subtotal / detalle.cantidad
        kardex_db.productos_id = detalle.producto.id
        session.add(kardex_db)
