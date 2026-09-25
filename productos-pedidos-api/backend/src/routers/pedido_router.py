from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from crud.pedido_crud import (
    create_pedido,
    delete_pedido,
    get_pedido,
    get_pedidos,
    update_pedido,
)
from database.database import get_session
from models.pedido_model import Pedido
from schemas.pedido_schema import PedidoCreate, PedidoUpdate

router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"],
)

@router.post("/", response_model=Pedido, status_code=201)
def create(data: PedidoCreate, session: Session = Depends(get_session)):
    return create_pedido(session, data)

@router.get("/", response_model=list[Pedido])
def get_all(session: Session = Depends(get_session)):
    return get_pedidos(session)

@router.get("/{pedido_id}", response_model=Pedido)
def get_by_id(pedido_id: int, session: Session = Depends(get_session)):
    pedido = get_pedido(session, pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido

@router.put("/{pedido_id}", response_model=Pedido)
def update(
    pedido_id: int,
    data: PedidoUpdate,
    session: Session = Depends(get_session),
):
    pedido = get_pedido(session, pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return update_pedido(session, pedido, data)

@router.delete("/{pedido_id}")
def delete(pedido_id: int, session: Session = Depends(get_session)):
    pedido = get_pedido(session, pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    delete_pedido(session, pedido)
    return {"message": "Pedido eliminado correctamente"}