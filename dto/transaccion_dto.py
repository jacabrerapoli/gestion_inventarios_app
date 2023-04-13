from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from dto.cliente_dto import ClienteDTO, ClienteTransaccionDTO
from dto.detalle_transaccion_dto import DetalleTransaccionDTO, DetalleTransaccionResponseDTO


class TransaccionDTO(BaseModel):
    tipo_transaccion: str
    cliente: ClienteDTO = None
    total: float
    fecha: Optional[str]

    class Config:
        orm_mode = True


class TransaccionVentaDTO(BaseModel):
    cliente: Optional[ClienteTransaccionDTO]
    detalles: Optional[List[DetalleTransaccionDTO]]

    class Config:
        orm_mode = True


class TransaccionResponseDTO(BaseModel):
    uuid: str
    cliente: Optional[ClienteTransaccionDTO]
    detalle_transacciones: Optional[List[DetalleTransaccionResponseDTO]]
    total: float
    fecha: datetime

    class Config:
        orm_mode = True
