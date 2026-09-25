from sqlmodel import Field, SQLModel

class Producto(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    descripcion: str | None = None
    precio: float
    stock: int