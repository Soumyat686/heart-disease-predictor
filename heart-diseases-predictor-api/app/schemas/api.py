from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
import time

from app.schemas.health import HealthResponse
from app.schemas.predict import PredictionInput, PredictionResponse
from app.config import get_settings
from app import predict
from app.schemas.metrics import track_prediction, track_age

router = APIRouter()

@router.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint to verify the API is running."""
    return HealthResponse(status="ok")

@router.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict_endpoint(input_data: PredictionInput):
    """
    Predict heart failure death event based on patient data.
    
    This endpoint takes patient medical information and returns a prediction
    about their survival chances.
    """
    try:
        # Track age metric
        track_age(input_data.age)
        
        # Start timing the prediction
        prediction_start = time.time()
        
        prediction = predict.predict_death_event(
            age=input_data.age,
            anaemia=input_data.anaemia,
            high_blood_pressure=input_data.high_blood_pressure,
            creatinine_phosphokinase=input_data.creatinine_phosphokinase,
            diabetes=input_data.diabetes,
            ejection_fraction=input_data.ejection_fraction,
            platelets=input_data.platelets,
            sex=input_data.sex,
            serum_creatinine=input_data.serum_creatinine,
            serum_sodium=input_data.serum_sodium,
            smoking=input_data.smoking,
            time=input_data.time
        )
        
        # Track prediction metrics
        track_prediction(prediction, prediction_start)
        
        return PredictionResponse(result=prediction)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")