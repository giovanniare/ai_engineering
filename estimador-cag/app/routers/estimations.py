from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.llm_service import generate_estimation

router = APIRouter(prefix="/estimate", tags=["estimations"])


class EstimationRequest(BaseModel):
    transcription: str = Field(..., min_length=1, description="Transcripcion de la reunion")


class EstimationResponse(BaseModel):
    estimation: str
    model: str
    provider: str


@router.post("", response_model=EstimationResponse)
def create_estimation(request: EstimationRequest) -> EstimationResponse:
    estimation, model, provider = generate_estimation(request.transcription)
    return EstimationResponse(estimation=estimation, model=model, provider=provider)
