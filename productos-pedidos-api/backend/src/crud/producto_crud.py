from sqlmodel import Session, select
from models.producto_model import Producto
from schemas.producto_schema import ProductoCreate, ProductoUpdate

def create_producto(session: Session, data: ProductoCreate):
    producto = Producto.model_validate(data)
    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto

def get_productos(session: Session):
    return session.exec(select(Producto)).all()

def get_producto(session: Session, producto_id: int):
    return session.get(Producto, producto_id)

def update_producto(session: Session, producto: Producto, data: ProductoUpdate):
    producto.sqlmodel_update(data.model_dump(exclude_unset=True))
    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto

def delete_producto(session: Session, producto: Producto):
    session.delete(producto)
    session.commit()