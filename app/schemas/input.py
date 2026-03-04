from pydantic import BaseModel, Field, field_validator
from typing import Dict, Any, Literal


class DynamicInputSchema(BaseModel):
    payload: Dict[str, Any] = Field(..., description="Arbitrary JSON payload")

    model_config = {"extra": "forbid", "strict": True}

    @field_validator("payload")
    def prevent_empty_payload(cls, v):
        if not v:
            raise ValueError("Payload cannot be empty")
        return v


class TransactionInput(BaseModel):
    transaction_id: str = Field(..., min_length=1)
    customer_id: str = Field(..., min_length=1)
    amount: float = Field(..., gt=0)
    currency: Literal["USD", "EUR", "BRL"]
    country: str = Field(..., min_length=2, max_length=2)
    device_trusted: bool = False

    model_config = {"extra": "forbid", "strict": True}

    @field_validator("country")
    def uppercase_country(cls, v):
        return v.upper()
