from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from dto.cliente_dto import ClienteDTO, ClienteTransaccionDTO
from dto.detalle_transaccion_dto import DetalleTransaccionDTO, DetalleTransaccionResponseDTO
from dto.proveedor_dto import ProveedorTransaccionDTO


class TransaccionDTO(BaseModel):
    tipo_transaccion: str
    cliente: ClienteDTO = None
    total: float
    fecha: Optional[str]

    class Config:
        orm_mode = True


class TransaccionVentaDTO(BaseModel):
    cliente: Optional[ClienteTransaccionDTO]
    detalle_transacciones: Optional[List[DetalleTransaccionDTO]]

    class Config:
        orm_mode = True


class TransaccionCompraDTO(BaseModel):
    proveedor: Optional[ProveedorTransaccionDTO]
    detalle_transacciones: Optional[List[DetalleTransaccionDTO]]

    class Config:
        orm_mode = True


class TransaccionResponseVentaDTO(BaseModel):
    uuid: str
    cliente: Optional[ClienteTransaccionDTO]
    detalle_transacciones: Optional[List[DetalleTransaccionResponseDTO]]
    total: float
    fecha: datetime

    class Config:
        orm_mode = True


class TransaccionResponseCompraDTO(BaseModel):
    uuid: str
    proveedor: Optional[ProveedorTransaccionDTO]
    detalle_transacciones: Optional[List[DetalleTransaccionResponseDTO]]
    total: float
    fecha: datetime

    class Config:
        orm_mode = True
