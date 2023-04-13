from pydantic import BaseModel


class DetalleTransaccionDTO(BaseModel):
    cantidad: int
    producto_sku: str

    class Config:
        orm_mode = True
