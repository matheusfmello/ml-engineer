import logging
from typing import Dict, Any

import mlflow
import pandas as pd

class MLService:
    """
    A service to manage the ML model lifecycle, including loading, prediction,
    and history tracking.
    """
    def __init__(self, logger: logging.Logger):
        self.model: Any = None
        self.model_id: str = None
        self.logger: logging.Logger = logger

    def load_model(self, model_uri: str):
        """
        Loads a model from the specified MLflow URI.
        
        Args:
            model_uri (str): The URI of the model to load (e.g., 'models:/MyModel/1').
        
        Raises:
            Exception: If the model loading fails.
        """
        try:
            self.logger.info(f"Loading model from URI: {model_uri}")
            self.model = mlflow.sklearn.load_model(model_uri)
            self.logger.info("Model loaded successfully.")
            self.model_id = model_uri
        except Exception as e:
            self.logger.error(f"Failed to load model from {model_uri}: {e}")
            raise

    def predict(self, input_data: dict) -> Dict[str, Any]:
        """
        Makes a prediction using the loaded model.

        Args:
            input_data (dict): The input data for prediction.

        Returns:
            A dict containing the probability and prediction.

        Raises:
            ValueError: If no model is loaded.
        """
        if not self.model:
            self.logger.error("Prediction attempt failed: No model is loaded.")
            raise ValueError("No model loaded. Please load a model using the /load endpoint.")

        self.logger.info(f"Making prediction on input: {input_data}")

        # Convert input_data to DataFrame
        df = pd.DataFrame([input_data])

        # Model prediction
        prediction = self.model.predict(df)

        probability = self.model.predict_proba(df)[0][1]  # return survival probability

        result = {
            "probability": probability,
            "prediction": int(prediction[0])
        }

        # Store the request and prediction in history
        self.logger.info(f"Prediction successful: {result}")

        return result
