from fastapi import APIRouter, Request
from typing import Dict, Any
from app.schemas.report import ReportSchema, SummarySchema
from app.rules.engine import RulesEngine
from app.services.report_builder import ReportBuilder

router = APIRouter()
engine = RulesEngine()

@router.post("/validate", response_model=ReportSchema)
async def validate_endpoint(payload: Dict[str, Any], request: Request):

    rule_results = engine.run(payload)

    return ReportBuilder.build_report(
        rule_results=rule_results,
        request_id=getattr(request.state, "correlation_id", "")
    )