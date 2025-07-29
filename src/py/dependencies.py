import logging

from fastapi import Request

from src.py.services.db_service import DatabaseService
from src.py.services.ml_service import MLService


def get_logger(request: Request) -> logging.Logger:
    return request.app.state.logger


def get_ml_service(request: Request) -> MLService:
    return request.app.state.ml_service


def get_db_service(request: Request) -> DatabaseService:
    return request.app.state.db_service
