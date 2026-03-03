# Secure Regulatory API

## Project Details
The Secure Regulatory API (Validation API) is a robust and highly secure REST API built with FastAPI and Python 3.12. It is designed to handle regulatory data validation with strict enforcement of Pydantic schemas. The project prioritizes structured logging, centralized exception handling, and robust middleware architectures to ensure auditability and data integrity.

## Requirements
- **Python:** 3.12.x
- **Core Framework:** FastAPI
- **Validation:** Pydantic
- **App Server:** Uvicorn
- **Containerization:** Docker (distroless final image)
- **Dependencies:** Refer to `requirements.txt` for the full list (includes FastAPI, Pydantic, Uvicorn, AnyIO, Starlette, email-validator, python-json-logger, prometheus-fastapi-instrumentator, and more)

## Policy and Security Rules
Security is a primary focus for this project. The API implements several security controls:
- **Strict Data Validation:** Utilizes Pydantic schemas with mass assignment protection (`extra="forbid"`) to reject unknown fields and prevent injection attacks.
- **Authentication:** Enforced via API keys using constant-time comparison.
- **Data Protection:** No sensitive payloads or API keys are ever logged. TLS is strictly required for production usage.
- **Auditing:** Implements structured logging and Correlation IDs in middleware for request traceability.
- **CI/CD Security:** Automated pipeline includes dependency vulnerability scanning, Static Application Security Testing (SAST), linting, type checking, and container image scanning.
- **No Dynamic Execution:** Execution of `eval()` or `exec()` is prohibited.
- **Vulnerability Reporting:** Responsibly disclose vulnerabilities directly to lidiafcarvalho@outlook.com. Do NOT open a public issue. Thorough security policies are outlined in `SECURITY.md`.

## Execution Details

### Running Locally (Development)
You can run the API directly using Python and Uvicorn:

```bash
# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On macOS/Linux

# Install requirements
pip install -r requirements.txt

# Run the FastAPI application
uvicorn app.main:app --reload
```

### Running via Docker
The project includes a multi-stage `Dockerfile` that produces a secure, lightweight distroless image:

```bash
# Build the Docker image
docker build -t secure-regulatory-api .

# Run the container
docker run -p 8000:8000 secure-regulatory-api uvicorn app.main:app --host 0.0.0.0 --port 8000
```