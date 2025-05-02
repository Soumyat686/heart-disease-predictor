from pydantic import BaseModel, Field

class HealthResponse(BaseModel):
    """Response model for health check endpoint."""
    status: str = Field(..., description="API status")