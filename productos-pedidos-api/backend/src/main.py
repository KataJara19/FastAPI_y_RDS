from contextlib import asynccontextmanager
from fastapi import FastAPI

from database.database import create_database
from routers.producto_router import router as producto_router
from routers.pedido_router import router as pedido_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_database()
    yield

app = FastAPI(
    title="API Productos y Pedidos",
    description="API REST des gestión de productos y pedidos",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(producto_router)
app.include_router(pedido_router)

@app.get("/", tags=["General"])
def root():
    return {"message": "API de Productos y Pedidos funcionando"}

@app.get("/health", tags=["General"])
def health():
    return {"status": "ok"}