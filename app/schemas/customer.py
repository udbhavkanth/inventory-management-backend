from datetime import datetime
from uuid import UUID

from email_validator import EmailNotValidError, validate_email
from pydantic import BaseModel, ConfigDict, Field, field_validator


class CustomerCreate(BaseModel):
    """Payload for creating a customer."""

    full_name: str = Field(..., min_length=1, max_length=255)
    email: str = Field(..., min_length=1, max_length=255)
    phone: str = Field(..., min_length=1, max_length=50)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        try:
            validated = validate_email(value.strip(), check_deliverability=False)
            return validated.normalized.lower()
        except EmailNotValidError:
            raise ValueError("Please use a valid email address") from None


class CustomerResponse(BaseModel):
    """Customer response schema."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    full_name: str
    email: str
    phone: str | None
    created_at: datetime
