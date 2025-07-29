import logging
import os
from contextlib import asynccontextmanager

import mlflow
from dotenv import load_dotenv
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):

    load_dotenv()
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    app.state.logger = logger
    logger.info("Application startup...")

    # Set MLflow tracking URI
    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))
    logger.info(f"MLflow tracking URI set to: {mlflow.get_tracking_uri()}")

    # Import services and routers here to ensure config is loaded first
    from src.py.routes.health.router import health_router
    from src.py.routes.model.router import model_router
    from src.py.services.ml_service import MLService
    from src.py.services.db_service import DatabaseService

    ml_service = MLService(logger)

    # Load a default model on startup
    default_model_uri = os.getenv("DEFAULT_MODEL_URI")
    if default_model_uri:
        try:
            ml_service.load_model(default_model_uri)
            logger.info(f"Successfully loaded default model from: {default_model_uri}")
        except Exception as e:
            logger.error(f"Failed to load default model: {e}")
    else:
        logger.warning("No default model URI provided. App will start without a loaded model.")

    app.state.ml_service = ml_service
    app.state.db_service = DatabaseService(logger, db_path=os.getenv("DB_PATH"))


    # Include routers
    app.include_router(model_router, prefix="/model", tags=["Model"])
    app.include_router(health_router, prefix="/health", tags=["Health"])

    yield

    # Code to run on shutdown can go here
    logger.info("Application shutdown.")


app = FastAPI(
    title="ML Engineering",
    description="Titanic Predictions.",
    version="0.0.1",
    lifespan=lifespan
)

@app.get("/", tags=["Root"])
async def root():
    """A simple root endpoint to confirm the API is running."""
    return {"message": "ML Engineer App"}
