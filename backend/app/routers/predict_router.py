from fastapi import APIRouter, Request, Response

from backend.app.auth.dependencies import CurrentUser
from backend.app.core.limiter import limiter
from backend.app.core.ml import ModelPackage
from backend.app.schemas.predict_schema import PredictInput, PredictOutput
from backend.app.services.ecogrow_service import run_prediction

router = APIRouter(prefix="/predict", tags=["Predicciones"])


@router.post("/", response_model=PredictOutput, status_code=200, summary="Predecir estado del cultivo")
@limiter.limit("30/minute")
def predict(
    request: Request,
    response: Response,
    data: PredictInput,
    _: CurrentUser,
    model_package: ModelPackage,
) -> PredictOutput:
    return run_prediction(data, model_package)
