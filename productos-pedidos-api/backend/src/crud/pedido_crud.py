from sqlmodel import Session, select
from models.pedido_model import Pedido
from schemas.pedido_schema import PedidoCreate, PedidoUpdate

def create_pedido(session: Session, data: PedidoCreate):
    pedido = Pedido.model_validate(data)
    session.add(pedido)
    session.commit()
    session.refresh(pedido)
    return pedido

def get_pedidos(session: Session):
    return session.exec(select(Pedido)).all()

def get_pedido(session: Session, pedido_id: int):
    return session.get(Pedido, pedido_id)

def update_pedido(session: Session, pedido: Pedido, data: PedidoUpdate):
    pedido.sqlmodel_update(data.model_dump(exclude_unset=True))
    session.add(pedido)
    session.commit()
    session.refresh(pedido)
    return pedido

def delete_pedido(session: Session, pedido: Pedido):
    session.delete(pedido)
    session.commit()