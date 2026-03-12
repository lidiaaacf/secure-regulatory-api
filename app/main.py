from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging
from app.api.routes import router
from app.core.middleware import (
    SecurityMiddleware,
    RateLimitMiddleware,
    InternalAPIMiddleware,
)
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
    app.state.ALLOWED_API_KEYS = ["test-key-1", "test-key-2"]
    yield


app = FastAPI(
    title="Compliance & Security Validation API",
    version="1.1.0",
    lifespan=lifespan,
)

app.add_middleware(SecurityMiddleware)
app.add_middleware(RateLimitMiddleware, max_requests=100, window_seconds=60)
app.add_middleware(InternalAPIMiddleware)

register_exception_handlers(app)
app.include_router(router)
