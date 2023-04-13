from typing import Optional, List

from pydantic import BaseModel

from dto.cliente_dto import ClienteDTO, ClienteTransaccionDTO
from dto.detalle_transaccion_dto import DetalleTransaccionDTO


class TransaccionDTO(BaseModel):
    tipo_transaccion: str
    cliente: ClienteDTO = None
    total: float
    fecha: Optional[str]

    class Config:
        orm_mode = True


class TransaccionVentaDTO(BaseModel):
    cliente: ClienteTransaccionDTO
    detalles: List[DetalleTransaccionDTO]

    class Config:
        orm_mode = True
