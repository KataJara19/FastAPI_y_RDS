from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from crud.producto_crud import (
    create_producto,
    delete_producto,
    get_producto,
    get_productos,
    update_producto,
)
from database.database import get_session
from models.producto_model import Producto
from schemas.producto_schema import ProductoCreate, ProductoUpdate

router = APIRouter(
    prefix="/productos",
    tags=["Productos"],
)

@router.post("/", response_model=Producto, status_code=201)
def create(data: ProductoCreate, session: Session = Depends(get_session)):
    return create_producto(session, data)

@router.get("/", response_model=list[Producto])
def get_all(session: Session = Depends(get_session)):
    return get_productos(session)

@router.get("/{producto_id}", response_model=Producto)
def get_by_id(producto_id: int, session: Session = Depends(get_session)):
    producto = get_producto(session, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@router.put("/{producto_id}", response_model=Producto)
def update(
    producto_id: int,
    data: ProductoUpdate,
    session: Session = Depends(get_session),
):
    producto = get_producto(session, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return update_producto(session, producto, data)

@router.delete("/{producto_id}")
def delete(producto_id: int, session: Session = Depends(get_session)):
    producto = get_producto(session, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    delete_producto(session, producto)
    return {"message": "Producto eliminado correctamente"}