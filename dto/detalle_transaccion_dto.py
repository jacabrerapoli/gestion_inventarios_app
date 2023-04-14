from typing import Optional

from pydantic import BaseModel

from dto.producto_dto import ProductoResponseDTO


class DetalleTransaccionDTO(BaseModel):
    cantidad: int
    producto_sku: str

    class Config:
        orm_mode = True


class DetalleTransaccionResponseDTO(BaseModel):
    cantidad: int
    subtotal: float
    producto: Optional[ProductoResponseDTO]

    class Config:
        orm_mode = True
