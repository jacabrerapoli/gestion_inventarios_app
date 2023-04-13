from config.database import session
from models.models import TipoTransacciones


def buscar_tipo_transaccion_por_tipo(tipo: str) -> TipoTransacciones:
    return session.query(TipoTransacciones).filter(TipoTransacciones.tipo == tipo).first()
