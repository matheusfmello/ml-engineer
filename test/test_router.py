import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from src.py.routes.model.router import post_predict, post_load, get_history


def test_post_predict_success(mock_request, mock_ml_service, mock_db_service):
    payload = MagicMock()
    payload.model_dump.return_value = {"feature": "value"}
    mock_ml_service.predict.return_value = {
        "prediction": 1,
        "probability": 0.95
    }

    result = post_predict(
        request=mock_request,
        payload=payload,
        ml_service=mock_ml_service,
        db_service=mock_db_service
    )

    assert result == {"prediction": 1, "probability": 0.95}
    mock_db_service.insert_prediction.assert_called_once_with(
        model_id="test-model-id",
        prediction=1,
        probability=0.95
    )


def test_post_predict_runtime_error(mock_request, mock_ml_service, mock_db_service):
    payload = MagicMock()
    payload.model_dump.return_value = {"feature": "value"}
    mock_ml_service.predict.side_effect = RuntimeError("Prediction failed")

    with pytest.raises(HTTPException) as excinfo:
        post_predict(
            request=mock_request,
            payload=payload,
            ml_service=mock_ml_service,
            db_service=mock_db_service
        )
    assert excinfo.value.status_code == 400
    assert "Prediction failed" in excinfo.value.detail


def test_post_predict_unexpected_error(mock_request, mock_ml_service, mock_db_service):
    payload = MagicMock()
    payload.model_dump.return_value = {"feature": "value"}
    mock_ml_service.predict.side_effect = Exception("Unexpected error")

    with pytest.raises(HTTPException) as excinfo:
        post_predict(
            request=mock_request,
            payload=payload,
            ml_service=mock_ml_service,
            db_service=mock_db_service
        )
    assert excinfo.value.status_code == 500
    assert "internal error" in excinfo.value.detail


def test_post_load_success(mock_request, mock_ml_service):
    payload = MagicMock()
    payload.model_uri = "some/path/model.pkl"
    mock_ml_service.load_model.return_value = {"status": "loaded"}

    result = post_load(
        request=mock_request,
        payload=payload,
        ml_service=mock_ml_service
    )

    assert result == {"status": "loaded"}
    mock_ml_service.load_model.assert_called_once_with("some/path/model.pkl")


def test_get_history_success(mock_request, mock_ml_service, mock_db_service):
    mock_ml_service.model_id = "test-model-id"
    mock_db_service.get_history.return_value = [{"prediction": 1, "probability": 0.95}]

    result = get_history(
        request=mock_request,
        ml_service=mock_ml_service,
        db_service=mock_db_service
    )

    assert result == {"history": [{"prediction": 1, "probability": 0.95}]}
    mock_db_service.get_history.assert_called_once_with(model_id="test-model-id")
