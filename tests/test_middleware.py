from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.core.middleware import SecurityMiddleware, RateLimitMiddleware


def create_app_with_middleware(security_middleware=True, rate_limit_middleware=True):
    app = FastAPI()

    @app.get("/test")
    async def test_endpoint():
        return {"ok": True}

    if security_middleware:
        app.add_middleware(SecurityMiddleware)
    if rate_limit_middleware:
        app.add_middleware(RateLimitMiddleware, max_requests=2, window_seconds=1)

    return app


def test_security_headers_and_correlation_id():
    app = create_app_with_middleware(
        security_middleware=True, rate_limit_middleware=False
    )
    client = TestClient(app)

    response = client.get("/test")

    assert response.headers["Strict-Transport-Security"]
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["Referrer-Policy"] == "no-referrer"
    assert response.headers["X-XSS-Protection"] == "1; mode=block"
    assert "X-Correlation-ID" in response.headers
    assert len(response.headers["X-Correlation-ID"]) > 0


def test_rate_limit_allows_under_limit():
    app = create_app_with_middleware(
        security_middleware=False, rate_limit_middleware=True
    )
    client = TestClient(app)

    r1 = client.get("/test")
    assert r1.status_code == 200

    r2 = client.get("/test")
    assert r2.status_code == 200


def test_rate_limit_blocks_over_limit():
    app = create_app_with_middleware(
        security_middleware=False, rate_limit_middleware=True
    )
    client = TestClient(app)

    client.get("/test")
    client.get("/test")
    r3 = client.get("/test")
    assert r3.status_code == 429
    assert r3.text == "Rate limit exceeded"


def test_rate_limit_resets_after_window():
    import time

    app = create_app_with_middleware(
        security_middleware=False, rate_limit_middleware=True
    )
    client = TestClient(app)

    client.get("/test")
    client.get("/test")
    time.sleep(1.1)
    r3 = client.get("/test")
    assert r3.status_code == 200


def test_combined_middleware():
    app = create_app_with_middleware(
        security_middleware=True, rate_limit_middleware=True
    )
    client = TestClient(app)

    r = client.get("/test")
    assert r.status_code == 200
    assert r.headers["X-Content-Type-Options"] == "nosniff"
    assert "X-Correlation-ID" in r.headers

    client.get("/test")
    client.get("/test")
    r2 = client.get("/test")
    assert r2.status_code == 429
