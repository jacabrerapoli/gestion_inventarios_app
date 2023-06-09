from sqlalchemy import func

from config.database import session
from dto.transaccion_dto import TransaccionVentaDTO
from enums.tipo_transaccion_enum import TipoTransaccionEnum
from models.models import Clientes, TipoTransacciones, Transacciones, DetalleTransacciones, Productos, Kardex
from services import tipo_transaccion_service, cliente_service, producto_service, kardex_service
from services.kardex_service import agregar_transacciones


def crear_transaccion_venta(trasaccion_dto: TransaccionVentaDTO):
    # Buscar tipo de transacción
    tipo = tipo_transaccion_service.buscar_tipo_transaccion_por_tipo(TipoTransaccionEnum.VENTA.value)

    # Buscar cliente por tipo y número de identificación
    cliente_dto = trasaccion_dto.cliente
    cliente_db = cliente_service.buscar_cliente_por_tipo_y_num_identificacion(cliente_dto.tipo_identificacion,
                                                                              cliente_dto.num_identificacion)

    # Crear una nueva instancia de "Transacciones"
    transaccion_db = Transacciones(
        clientes_id=cliente_db.id,
        tipo_transaccion_id=tipo.id,
        fecha=func.now(),
    )

    # Crear cada detalle de transacción y agregarlo a la lista de detalles de la nueva transacción
    detalles = []
    for detalle in trasaccion_dto.detalles:
        producto = producto_service.buscar_producto_por_sku(detalle.producto_sku)
        subtotal = producto.precio * detalle.cantidad
        nuevo_detalle = DetalleTransacciones(
            cantidad=detalle.cantidad,
            subtotal=subtotal,
            producto=producto,
        )
        detalles.append(nuevo_detalle)

    transaccion_db.detalle_transacciones = detalles

    # Calcular el total de la transacción y guardarlo en la base de datos
    total = sum(detalle.subtotal for detalle in detalles)
    transaccion_db.total = total

    # Agregar la transacción al kardex
    kardex_service.agregar_transacciones(transaccion_db)

    # Guardar la transacción en la base de datos
    session.add(transaccion_db)
    session.commit()
    session.refresh(transaccion_db)

    return transaccion_db
