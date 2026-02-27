from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging

class ValidationError(Exception):
    """Raised when data validation fails."""
    def __init__(self, message: str, field: str | None = None):
        self.message = message
        self.field = field
        super().__init__(message)


class UnauthorizedError(Exception):
    """Raised when authentication/authorization fails."""
    def __init__(self, message: str = "Unauthorized"):
        self.message = message
        super().__init__(message)


def register_exception_handlers(app: FastAPI):
    """Register all custom exception handlers."""

    @app.exception_handler(ValidationError)
    async def validation_exception_handler(request: Request, exc: ValidationError):
        correlation_id = getattr(request.state, "correlation_id", None)
        logging.error(
            f"[{correlation_id}] Validation failed: {exc.message} (field={exc.field})"
        )
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "error": exc.message,
                "field": exc.field,
                "correlation_id": correlation_id,
            },
        )

    @app.exception_handler(UnauthorizedError)
    async def unauthorized_exception_handler(request: Request, exc: UnauthorizedError):
        correlation_id = getattr(request.state, "correlation_id", None)
        logging.warning(f"[{correlation_id}] Unauthorized access: {exc.message}")
        return JSONResponse(
            status_code=401,
            content={
                "success": False,
                "error": exc.message,
                "correlation_id": correlation_id,
            },
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        correlation_id = getattr(request.state, "correlation_id", None)
        logging.exception(f"[{correlation_id}] Unhandled exception: {exc}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "Internal server error",
                "correlation_id": correlation_id,
            },
        )