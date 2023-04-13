from typing import List

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

import services.producto_service as producto_service
from dto.cliente_dto import ClienteDTO
from dto.producto_dto import ProductoDTO, ProductoCreateDTO
from dto.transaccion_dto import TransaccionVentaDTO, TransaccionResponseDTO
from services import transaccion_service, tipo_transaccion_service
from services.cliente_service import obtener_clientes, buscar_cliente_por_tipo_y_num_identificacion, crear_cliente

app = FastAPI(title="GestionInventarios")


@app.get("/")
async def root():
    return {"status": "OK"}


@app.get(
    path="/clientes",
    response_model=List[ClienteDTO],
    tags=["Clientes"],
    description="Este servicio permite buscar clientes por tipo y numero de documento")
async def obtener_cliente_por_tipo_y_num_identificacion():
    return obtener_clientes()


@app.get("/clientes/identificacion", response_model=ClienteDTO, tags=["Clientes"])
async def obtener_cliente_por_tipo_y_num_identificacion(
        tipo_identificacion: str,
        num_identificacion: str
):
    result = buscar_cliente_por_tipo_y_num_identificacion(tipo_identificacion, num_identificacion)
    return jsonable_encoder(result)


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


@app.post("/transacciones/venta", response_model=TransaccionResponseDTO, tags=["Transacciones"])
async def guardar_transaccion(transaccion_dto: TransaccionVentaDTO):
    return transaccion_service.crear_transaccion_venta(transaccion_dto)


@app.get("/tipos_de_transaccion", response_model=List[TransaccionVentaDTO], tags=["Tipos de Transaccion"])
async def buscar_tipo_de_transaccion_por_tipo(tipo: str):
    return tipo_transaccion_service.buscar_tipo_transaccion_por_tipo(tipo)
