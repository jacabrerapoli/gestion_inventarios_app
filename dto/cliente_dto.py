from pydantic import BaseModel


class ClienteDTO(BaseModel):
    tipo_identificacion: str
    num_identificacion: str
    nombres: str
    apellidos: str
    correo: str
    direccion: str
    telefono: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "nombre": "John",
                "apellido": "Doe",
                "tipo_identificacion": "CC",
                "num_identificacion": "123456789",
                "direccion": "Calle Falsa 123",
                "telefono": "1234567890"
            }
        }


class ClienteTransaccionDTO(BaseModel):
    tipo_identificacion: str
    num_identificacion: str

    class Config:
        orm_mode = True
