from pathlib import Path
from typing import Annotated, Any

import joblib
from fastapi import Depends, Request

_MODEL_PATH = Path(__file__).parent.parent.parent / "modelo_ecogrow.pkl"


def load_model() -> dict[str, Any]:
    return joblib.load(_MODEL_PATH)


def get_model_package(request: Request) -> dict[str, Any]:
    return request.app.state.model_package


ModelPackage = Annotated[dict[str, Any], Depends(get_model_package)]
