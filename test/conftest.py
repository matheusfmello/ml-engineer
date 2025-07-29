import pytest
from unittest.mock import MagicMock
from fastapi import Request


@pytest.fixture
def mock_logger():
    logger = MagicMock()
    return logger


@pytest.fixture
def mock_request(mock_logger):
    request = MagicMock(spec=Request)
    request.app.state.logger = mock_logger
    return request


@pytest.fixture
def mock_ml_service():
    ml_service = MagicMock()
    ml_service.model_id = "test-model-id"
    return ml_service


@pytest.fixture
def mock_db_service():
    db_service = MagicMock()
    return db_service
