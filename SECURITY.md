# Security Policy

## Supported Versions

Only the latest major release receives security updates.

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly.

Do NOT open a public issue.

Send details to:
lidiafcarvalho@outlook.com

Include:

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested mitigation (if available)

You will receive acknowledgment within 72 hours.

## Security Controls

This API implements:

- Strict Pydantic schema validation
- Rejection of unknown fields
- Structured logging
- Correlation IDs
- API key authentication
- Constant-time API key comparison
- Centralized exception handling
- No dynamic code execution
- No eval/exec usage

## CI/CD Security

The pipeline performs:

- Dependency vulnerability scanning
- Static Application Security Testing (SAST)
- Linting and type checking
- Container image scanning

## Data Handling

- No sensitive payload data is logged
- API keys are never logged
- TLS is required in production
- Logs are structured and auditable

## Threat Model

Primary protections include:

- Injection prevention via strict typing
- Mass assignment protection (`extra="forbid"`)
- Authentication enforcement
- Deterministic rule execution
- Error response sanitization