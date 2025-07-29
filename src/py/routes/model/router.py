from fastapi.routing import APIRouter
from fastapi import Depends, Request, HTTPException, status

from src.py.dependencies import get_ml_service, get_db_service
from src.py.services.db_service import DatabaseService
from src.py.services.ml_service import MLService
from .basemodels import (
    PredictionInput,
    PredictionResponse,
    LoadRequest,
    LoadResponse,
    HistoryResponse
)

model_router = APIRouter()


@model_router.post('/predict', response_model=PredictionResponse, summary="Make a prediction")
def post_predict(
    request: Request,
    payload: PredictionInput,
    ml_service: MLService = Depends(get_ml_service),
    db_service: DatabaseService = Depends(get_db_service),
):
    """Receives passenger data and returns a survival prediction."""
    logger = request.app.state.logger
    logger.info("Endpoint '/model/predict' called.")

    try:
        prediction_result = ml_service.predict(payload.model_dump())
    except RuntimeError as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"An unexpected error occurred during prediction: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An internal error occurred."
        )

    db_service.insert_prediction(
        model_id=ml_service.model_id,
        prediction=prediction_result['prediction'],
        probability=prediction_result['probability']
    )

    return prediction_result


@model_router.post('/load', response_model=LoadResponse, summary="Load a new ML model")
def post_load(
    request: Request,
    payload: LoadRequest,
    ml_service: MLService = Depends(get_ml_service)
):
    """Loads a new model from the specified file path."""
    logger = request.app.state.logger
    logger.info(f"Endpoint '/model/load' called with path: {payload.model_uri}")

    result = ml_service.load_model(payload.model_uri)

    logger.info(f"Successfully loaded model from {payload.model_uri}")
    return result


@model_router.get('/history', response_model=HistoryResponse, summary="Get prediction history")
def get_history(
    request: Request,
    ml_service: MLService = Depends(get_ml_service),
    db_service: DatabaseService = Depends(get_db_service),
):
    """Returns the history of all prediction calls made."""
    logger = request.app.state.logger
    logger.info("Endpoint '/model/history' called.")

    history = db_service.get_history(model_id=ml_service.model_id)
    return {"history": history}
