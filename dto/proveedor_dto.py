from pydantic import BaseModel


class ProveedorRequestDTO(BaseModel):
    tipo_identificacion: str
    numero_identificacion: str
    nombre_empresa: str
    nombre_representante: str
    apellido_representante: str
    correo: str
    direccion: str
    telefono: str

    class Config:
        orm_mode = True


class ProveedorTransaccionDTO(BaseModel):
    tipo_identificacion: str
    numero_identificacion: str

    class Config:
        orm_mode = True
