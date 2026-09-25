from sqlmodel import Field, SQLModel

class Pedido(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    producto_id: int = Field(foreign_key="producto.id")
    cantidad: int
    direccion_envio: str
    estado: str = Field(default="Pendiente")