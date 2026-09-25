from sqlmodel import SQLModel

class PedidoCreate(SQLModel):
    producto_id: int
    cantidad: int
    direccion_envio: str

class PedidoUpdate(SQLModel):
    cantidad: int | None = None
    direccion_envio: str | None = None
    estado: str | None = None