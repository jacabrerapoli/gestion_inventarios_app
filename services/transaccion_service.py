import uuid

from sqlalchemy import func

from config.database import session
from dto.transaccion_dto import TransaccionVentaDTO, TransaccionResponseVentaDTO, TransaccionCompraDTO, \
    TransaccionResponseCompraDTO
from enums.tipo_transaccion_enum import TipoTransaccionEnum
from models.models import Transacciones, DetalleTransacciones, Proveedores
from services import tipo_transaccion_service, cliente_service, producto_service, kardex_service, proveedor_service


def crear_transaccion_venta(transaccion_dto: TransaccionVentaDTO):
    # Buscar tipo de transacción
    tipo = tipo_transaccion_service.buscar_tipo_transaccion_por_tipo(TipoTransaccionEnum.VENTA.value)

    # Buscar cliente por tipo y número de identificación
    cliente_dto = transaccion_dto.cliente
    cliente_db = cliente_service.buscar_cliente_por_tipo_y_num_identificacion(cliente_dto.tipo_identificacion,
                                                                              cliente_dto.num_identificacion)

    # Crear una nueva instancia de "Transacciones"
    transaccion_db = Transacciones(
        clientes_id=cliente_db.id,
        tipo_transaccion_id=tipo.id,
        fecha=func.now(),
        uuid=uuid.uuid4()
    )

    crear_detalles(transaccion_db, transaccion_dto)

    return TransaccionResponseVentaDTO.from_orm(transaccion_db)


def crear_transaccion_compra(trasaccion_dto: TransaccionCompraDTO):
    # Buscar tipo de transacción
    tipo = tipo_transaccion_service.buscar_tipo_transaccion_por_tipo(TipoTransaccionEnum.COMPRA.value)

    # Buscar cliente por tipo y número de identificación
    proveedor_dto = trasaccion_dto.proveedor

    proveedor_db: Proveedores = proveedor_service.buscar_proveedor_por_tipo_y_num_identificacion(
        proveedor_dto.tipo_identificacion,
        proveedor_dto.numero_identificacion
    )

    # Crear una nueva instancia de "Transacciones"
    transaccion_db = Transacciones(
        proveedor_id=proveedor_db.id,
        tipo_transaccion_id=tipo.id,
        fecha=func.now(),
        uuid=uuid.uuid4()
    )

    # Crear cada detalle de transacción y agregarlo a la lista de detalle_transacciones de la nueva transacción
    crear_detalles(transaccion_db, trasaccion_dto)

    return TransaccionResponseCompraDTO.from_orm(transaccion_db)


def crear_detalles(transaccion_db, transaccion_dto):
    detalles = []
    for detalle in transaccion_dto.detalle_transacciones:
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
    # Guardar la transacción en la base de datos
    session.add(transaccion_db)
    session.commit()
    session.refresh(transaccion_db)
    # Agregar la transacción al kardex
    kardex_service.agregar_transacciones(transaccion_db)
