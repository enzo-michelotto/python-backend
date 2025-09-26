import logging
from fastapi import FastAPI
from app.config import settings
from app.database import init_db
from app.routers import customer_router

logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

app = FastAPI(title="Client_Ms", version="1.0.0")


@app.on_event("startup")
async def on_startup():
    await init_db()
    logger.info("Database initialized")


app.include_router(customer_router.router)
