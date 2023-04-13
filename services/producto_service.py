from fastapi import HTTPException

from config.database import session
from dto.producto_dto import ProductoDTO, ProductoCreateDTO
from models.models import Productos


def crear_producto(producto_dto: ProductoCreateDTO):
    db_producto = Productos(**producto_dto.dict())
    db_producto.costo = 0
    db_producto.precio = 0
    session.add(db_producto)
    session.commit()
    session.refresh(db_producto)
    return db_producto


def buscar_producto_por_sku(producto_sku: str):
    db_producto = session.query(Productos).filter(Productos.sku == producto_sku).first()
    if db_producto is None:
        raise Exception("Producto no encontrado")
    return db_producto


def actualizar_producto(producto_sku: str, producto: ProductoDTO):
    db_producto = session.query(Productos).filter(Productos.sku == producto_sku).first()
    if db_producto is None:
        raise Exception("Producto no encontrado")
    update_data = producto.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_producto, key, value)
    session.commit()
    session.refresh(db_producto)
    return db_producto


def eliminar_producto_por_sku(producto_sku: str):
    db_producto = session.query(Productos).filter(Productos.id == producto_sku).first()
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    session.delete(db_producto)
    session.commit()
    return {"message": "Producto eliminado correctamente"}


def buscar_productos(skip: int = 0, limit: int = 100):
    productos = session.query(Productos).offset(skip).limit(limit).all()
    return [ProductoDTO.from_orm(producto) for producto in productos]
