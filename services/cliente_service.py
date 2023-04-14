from sqlalchemy.exc import NoResultFound

from dto.cliente_dto import ClienteDTO
from config.database import *
from models.models import Clientes


def obtener_clientes():
    clientes = session.query(Clientes).all()
    return [ClienteDTO.from_orm(cliente) for cliente in clientes]


def buscar_cliente_por_tipo_y_num_identificacion(tipo_identificacion: str, num_identificacion: str):
    try:
        cliente = session.query(Clientes).filter(
            Clientes.tipo_identificacion == tipo_identificacion,
            Clientes.num_identificacion == num_identificacion
        ).one()
        return cliente
    except NoResultFound:
        raise Exception("No se encontró el cliente con los datos proporcionados.")
    except Exception as e:
        raise Exception("Ocurrió un error al buscar el cliente: " + str(e))


def crear_cliente(cliente_dto: ClienteDTO):
    cliente = Clientes(**cliente_dto.dict())
    session.add(cliente)
    session.commit()
    session.refresh(cliente)
