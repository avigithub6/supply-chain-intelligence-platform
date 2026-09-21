from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.inventory import router as inventory_router
from app.api.orders import router as orders_router
from app.api.shipments import router as shipments_router
from app.api.suppliers import router as suppliers_router
from app.core.config import settings
from app.core.logging import configure_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "Agentic AI platform for supply chain intelligence, "
        "retrieval, recommendations, and operational workflows."
    ),
    lifespan=lifespan,
)


app.include_router(health_router)
app.include_router(orders_router)
app.include_router(inventory_router)
app.include_router(suppliers_router)
app.include_router(shipments_router)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": "Welcome to SupplyChain AI Copilot",
        "status": "running",
    }