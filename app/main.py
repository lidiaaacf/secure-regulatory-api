from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging
from app.api.routes import router
from app.core.middleware import CorrelationIdMiddleware
from app.core.exceptions import register_exception_handlers
from app.core.engine_registry import create_engine
from app.config import settings

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(message)s",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.rules_engine = create_engine()
    yield


app = FastAPI(
    title="Compliance & Security Validation API",
    version="1.1.0",
    lifespan=lifespan,
)

app.add_middleware(CorrelationIdMiddleware)
register_exception_handlers(app)
app.include_router(router)
