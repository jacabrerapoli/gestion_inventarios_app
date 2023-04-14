from typing import List

from sqlalchemy.exc import NoResultFound

from config.database import session
from dto.proveedor_dto import ProveedorRequestDTO
from models.models import Proveedores


def buscar_proveedores():
    proveedores: List[Proveedores] = session.query(Proveedores).all()
    return [ProveedorRequestDTO.from_orm(proveedor) for proveedor in proveedores]


def crear_proveedor(proveedor_dto=ProveedorRequestDTO):
    proveedor: Proveedores = Proveedores(**proveedor_dto.__dict__)
    session.add(proveedor)
    session.commit()
    session.refresh(proveedor)
    return proveedor_dto.from_orm(proveedor)


def buscar_proveedor_por_tipo_y_num_identificacion(tipo_identificacion: str, num_identificacion: str) -> Proveedores:
    try:
        proveedor_db: Proveedores = session.query(Proveedores).filter(
            Proveedores.tipo_identificacion == tipo_identificacion,
            Proveedores.numero_identificacion == num_identificacion
        ).one()
        return proveedor_db
    except NoResultFound:
        raise Exception("No se encontró el proveedor con los datos proporcionados.")
    except Exception as e:
        raise Exception("Ocurrió un error al buscar el proveedor: " + str(e))
