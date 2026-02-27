from fastapi import FastAPI
from app.api.routes import router
from app.logging_config import setup_logging
from app.config import settings
from app.core.middleware import CorrelationIdMiddleware
from app.core.exceptions import register_exception_handlers

setup_logging(settings.LOG_LEVEL)

app = FastAPI(title="Validation API", version="1.0.0")

app.add_middleware(CorrelationIdMiddleware)
app.include_router(router)

register_exception_handlers(app)