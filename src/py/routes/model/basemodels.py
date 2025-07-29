from typing import List, Optional
from pydantic import BaseModel, Field


class PredictionInput(BaseModel):
    """Input features for a single Titanic prediction."""
    pclass: int = Field(..., description="Ticket class (1 = 1st, 2 = 2nd, 3 = 3rd)", example=3)
    sex: str = Field(..., description="Sex of the passenger", example="male")
    age: float = Field(..., description="Age in years", example=22.0)
    sibsp: int = Field(..., description="Number of siblings/spouses aboard", example=1)
    parch: int = Field(..., description="Number of parents/children aboard", example=0)
    fare: float = Field(..., description="Passenger fare", example=7.25)
    embarked: str = Field(..., description="Port of Embarkation (C=Cherbourg, Q=Queenstown, S=Southampton)", example="S")

class LoadRequest(BaseModel):
    """Request to load a new model from MLFlow."""
    model_uri: str = Field(..., description="MLflow model URI (e.g., 'models:/MyModel/production')", example="models:/TitanicSurvival/production")


class PredictionResponse(BaseModel):
    """Response containing the survival prediction."""
    prediction: int
    probability: Optional[float]

class LoadResponse(BaseModel):
    """Confirmation response for loading a model."""
    message: str = "Model loaded successfully"
    model_uri: str

class HistoryItem(BaseModel):
    """A single entry in the prediction history."""
    timestamp: str
    model_id: str
    prediction: int
    probability: float

class HistoryResponse(BaseModel):
    """Response containing the list of all predictions made."""
    history: List[HistoryItem]
