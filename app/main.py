from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.dashboard import router as dashboard_router
from app.api.machines import router as machines_router
from app.api.orders import router as orders_router
from app.api.production import router as production_router
from app.api.products import router as products_router
from app.api.reports import router as reports_router
from app.api.stock import router as stock_router


app = FastAPI(
    title="SmartFactory API",
    description="Production and Inventory Management API",
    version="1.0.0",
)


app.include_router(auth_router)
app.include_router(products_router)
app.include_router(production_router)
app.include_router(machines_router)
app.include_router(reports_router)
app.include_router(stock_router)
app.include_router(orders_router)
app.include_router(dashboard_router)


@app.get("/")
def root():
    return {
        "application": "SmartFactory API",
        "version": "1.0.0",
        "status": "running",
    }
