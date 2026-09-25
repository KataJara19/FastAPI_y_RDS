from sqlmodel import SQLModel

class ProductoCreate(SQLModel):
    nombre: str
    descripcion: str | None = None
    precio: float
    stock: int

class ProductoUpdate(SQLModel):
    nombre: str | None = None
    descripcion: str | None = None
    precio: float | None = None
    stock: int | None = None