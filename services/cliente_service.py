from dto.cliente_dto import ClienteDTO
from config.database import *
from models.models import Clientes


def obtener_clientes():
    clientes = session.query(Clientes).all()
    return [ClienteDTO.from_orm(cliente) for cliente in clientes]


def buscar_cliente_por_tipo_y_num_identificacion(tipo_identificacion: str, num_identificacion: str):
    cliente = session.query(Clientes).filter(
        Clientes.tipo_identificacion == tipo_identificacion,
        Clientes.num_identificacion == num_identificacion
    ).first()
    return cliente


def crear_cliente(cliente_dto: ClienteDTO):
    cliente = Clientes(**cliente_dto.dict())
    session.add(cliente)
    session.commit()
    session.refresh(cliente)
