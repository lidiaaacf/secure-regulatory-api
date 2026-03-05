from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi import Response
import uuid
import logging
from collections import defaultdict
import time

request_counts = defaultdict(list)


class RateLimitMiddleware(BaseHTTPMiddleware):

    def __init__(self, app, max_requests: int = 100, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.clients = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        now = time.time()
        timestamps = self.clients[client_ip]

        self.clients[client_ip] = [
            t for t in timestamps if now - t < self.window_seconds
        ]

        if len(self.clients[client_ip]) >= self.max_requests:
            return Response("Rate limit exceeded", status_code=429)

        self.clients[client_ip].append(now)

        return await call_next(request)


class SecurityMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
        request.state.correlation_id = correlation_id

        logging.info(
            f"[{correlation_id}] Incoming request: {request.method} {request.url}"
        )

        response: Response = await call_next(request)

        response.headers["X-Correlation-ID"] = correlation_id
        response.headers["Strict-Transport-Security"] = (
            "max-age=63072000; includeSubDomains; preload"
        )
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["X-XSS-Protection"] = "1; mode=block"

        return response
