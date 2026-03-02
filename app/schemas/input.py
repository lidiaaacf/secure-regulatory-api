from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator
from uuid import UUID
from decimal import Decimal
from typing import Dict, Any

class DynamicInputSchema(BaseModel):
    payload: Dict[str, Any] = Field(..., description="Arbitrary JSON payload")

    model_config = {
        "extra": "forbid",
        "strict": True
    }