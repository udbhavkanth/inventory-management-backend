from pydantic import BaseModel, Field


class RootResponse(BaseModel):
    """Response schema for the root endpoint."""

    message: str = Field(..., examples=["Inventory Management API Running"])


class HealthResponse(BaseModel):
    """Response schema for the health check endpoint."""

    status: str = Field(..., examples=["healthy"])
