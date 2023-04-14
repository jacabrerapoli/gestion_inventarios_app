from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

import services.producto_service as producto_service
from dto.cliente_dto import ClienteDTO
from dto.producto_dto import ProductoDTO, ProductoCreateDTO
from dto.proveedor_dto import ProveedorRequestDTO
from dto.transaccion_dto import TransaccionVentaDTO, TransaccionResponseVentaDTO, TransaccionCompraDTO, \
    TransaccionResponseCompraDTO
from services import transaccion_service, tipo_transaccion_service, proveedor_service, kardex_service
from services.cliente_service import obtener_clientes, buscar_cliente_por_tipo_y_num_identificacion, crear_cliente

app = FastAPI(title="GestionInventarios")


@app.get("/")
async def root():
    return {"status": "OK"}


@app.get(
    path="/clientes",
    response_model=List[ClienteDTO],
    tags=["Clientes"],
    description="Este servicio permite buscar todos los clientes")
async def buscar_todos_los_clientes():
    return obtener_clientes()


@app.get("/clientes/identificacion", response_model=ClienteDTO, tags=["Clientes"])
async def obtener_cliente_por_tipo_y_num_identificacion(
        tipo_identificacion: str,
        num_identificacion: str
):
    try:
        result = buscar_cliente_por_tipo_y_num_identificacion(tipo_identificacion, num_identificacion)
        return jsonable_encoder(result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/clientes", response_model=ClienteDTO, tags=["Clientes"])
async def guardar_cliente(cliente: ClienteDTO):
    try:
        crear_cliente(cliente)
    except Exception as e:
        error_message = e.args[0]
        error_status_code = 500  # default status code for internal server errors
        if isinstance(e, Exception):
            error_status_code = 400  # specific status code for bad requests
        error_response = {"error": error_message}
        return JSONResponse(content=error_response, status_code=error_status_code)

    success_response = {"message": "Cliente guardado exitosamente"}
    return JSONResponse(content=success_response, status_code=200)


@app.get("/productos", response_model=List[ProductoDTO], tags=["Productos"])
async def buscar_productos():
    return producto_service.buscar_productos()


@app.post("/productos", response_model=ProductoDTO, tags=["Productos"])
async def guardar_productos(producto_dto: ProductoCreateDTO):
    return producto_service.crear_producto(producto_dto)


@app.post("/transacciones/ventas", response_model=TransaccionResponseVentaDTO, tags=["Transacciones"])
async def guardar_transaccion_ventas(transaccion_dto: TransaccionVentaDTO):
    return transaccion_service.crear_transaccion_venta(transaccion_dto)


@app.post("/transacciones/compras", response_model=TransaccionResponseCompraDTO, tags=["Transacciones"])
async def guardar_transaccion_compras(transaccion_dto: TransaccionCompraDTO):
    try:
        return transaccion_service.crear_transaccion_compra(transaccion_dto)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/tipos_de_transaccion", response_model=List[TransaccionVentaDTO], tags=["Tipos de Transaccion"])
async def buscar_tipo_de_transaccion_por_tipo(tipo: str):
    return tipo_transaccion_service.buscar_tipo_transaccion_por_tipo(tipo)


@app.get("/proveedores", response_model=List[ProveedorRequestDTO], tags=["Proveedores"])
async def buscar_proveedores():
    return proveedor_service.buscar_proveedores()


@app.post("/proveedores", response_model=ProveedorRequestDTO, tags=["Proveedores"])
async def crear_proveedor(proveedor_dto: ProveedorRequestDTO):
    return proveedor_service.crear_proveedor(proveedor_dto)


@app.get("/kardex", tags=["Kardex"])
async def listar_kardex_por_producto_sku(sku: str):
    return kardex_service.listar_kardex_por_producto_sku(sku)
