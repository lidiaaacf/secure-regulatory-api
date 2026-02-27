from fastapi import APIRouter, Request
from app.schemas.input import InputSchema
from app.schemas.report import ReportSchema
from app.services.validation import validate_data
from app.services.report_builder import ReportBuilder
from app.core.security import validate_api_key

router = APIRouter()

ALLOWED_API_KEYS = ["my-secret-key"]

@router.post("/validate", response_model=ReportSchema)
async def validate_endpoint(payload: InputSchema, request: Request):
    validate_api_key(request, allowed_keys=ALLOWED_API_KEYS)

    rule_results = validate_data(payload.model_dump())

    report = ReportBuilder.build_report(
        rule_results,
        request_id=getattr(request.state, "correlation_id", "")
    )

    return report