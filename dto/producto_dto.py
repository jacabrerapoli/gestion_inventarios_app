from pydantic import BaseModel


class ProductoDTO(BaseModel):
    sku: str
    nombre: str
    marca: str
    linea: str
    descripcion: str
    precio: float
    costo: float

    class Config:
        orm_mode = True


class ProductoCreateDTO(BaseModel):
    sku: str
    nombre: str
    marca: str
    linea: str
    descripcion: str

    class Config:
        orm_mode = True


class ProductoResponseDTO(BaseModel):
    sku: str
    nombre: str
    marca: str
    linea: str
    precio: float

    class Config:
        orm_mode = True
