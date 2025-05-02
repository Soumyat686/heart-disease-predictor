# api.py
import os
import sys
import uvicorn
from fastapi import FastAPI, HTTPException, Query, APIRouter, Request
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Literal
import pandas as pd
import sys
import os

# Get the project root directory (3 levels up from api.py)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

# Add the project root to the path so we can import project modules
#sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from income_predictor.predict import predict, load_model
from income_predictor.processing.validation import validate_input_data
api_router = APIRouter()


# Initialize FastAPI app
app = FastAPI(
    title="Census Income Prediction API",
    description="API for predicting whether income exceeds $50K based on census data",
    version="0.1.0"
)
app.include_router(api_router)
# Load model at startup
@app.on_event("startup")
async def startup_event():
    try:
        global model
        model = load_model()
    except Exception as e:
        print(f"Error loading model: {e}")

# Define input data model
class CensusInput(BaseModel):
    age: int = Field(..., ge=18, le=90, description="Age of the individual (18-90)")
    education: Literal["Bachelors", "HS-grad", "Masters", "Doctorate", "Some-college", "Assoc", "Elementary"] = Field(
        ..., description="Education level"
    )
    occupation: Literal["Professional", "White-collar", "Sales", "Blue-collar", "Service", "Other"] = Field(
        ..., description="Occupation category"
    )
    hours_per_week: int = Field(..., ge=1, le=168, description="Working hours per week")
    marital_status: Literal["Married", "Never-married", "Divorced", "Separated", "Widowed"] = Field(
        ..., description="Marital status"
    )
    gender: Literal["Male", "Female"] = Field(..., description="Gender")
    capital_gain: float = Field(..., ge=0, description="Capital gain")
    capital_loss: float = Field(..., ge=0, description="Capital loss")
    
    class Config:
        schema_extra = {
            "example": {
                "age": 35,
                "education": "Bachelors",
                "occupation": "Professional",
                "hours_per_week": 40,
                "marital_status": "Married",
                "gender": "Female",
                "capital_gain": 0,
                "capital_loss": 0
            }
        }

# Define prediction output model
class PredictionOutput(BaseModel):
    prediction: Literal[0, 1] = Field(..., description="Prediction result (0: <=50K, 1: >50K)")
    prediction_label: str = Field(..., description="Human-readable prediction")
    probability: Optional[float] = Field(None, description="Probability of the prediction")

# Define batch input model
class BatchPredictionInput(BaseModel):
    inputs: List[CensusInput] = Field(..., description="List of census data inputs")

# Define batch prediction output
class BatchPredictionOutput(BaseModel):
    predictions: List[PredictionOutput] = Field(..., description="List of prediction results")
    
@api_router.get("/")
def root():
    return {"message": "Welcome to the Census Income Prediction API. Visit /docs for the API documentation."}

@api_router.get("/health")
def health_check():
    """API health check endpoint"""
    return {
        "status": "ok",
        "message": "API is running"
    }

@api_router.post("/predict", response_model=PredictionOutput)
def make_prediction(input_data: CensusInput):
    """
    Make income prediction based on census data
    
    Returns:
        prediction: 0 (<=50K) or 1 (>50K)
        prediction_label: String representation
        probability: Probability of the prediction
    """
    try:
        # Convert pydantic model to dict
        input_dict = input_data.dict()
        
        # Make prediction
        prediction_result = predict(input_dict)
        
        # Get probability if available (requires classifier with predict_proba method)
        probability = None
        try:
            # If model has predict_proba method, use it
            if hasattr(model, 'predict_proba'):
                probabilities = model.predict_proba(pd.DataFrame([input_dict]))
                probability = float(probabilities[0][1])  # Probability of class 1
        except Exception:
            # If error occurs, just skip probability
            pass
            
        # Create response
        prediction_label = ">50K" if prediction_result[0] == 1 else "<=50K"
        return {
            "prediction": int(prediction_result[0]),
            "prediction_label": prediction_label,
            "probability": probability
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/predict/batch", response_model=BatchPredictionOutput)
def make_batch_prediction(batch_input: BatchPredictionInput):
    """
    Make batch predictions for multiple inputs
    
    Returns:
        predictions: List of prediction results
    """
    try:
        # Convert inputs to DataFrame
        input_dicts = [item.dict() for item in batch_input.inputs]
        input_df = pd.DataFrame(input_dicts)
        
        # Make predictions
        predictions = predict(input_df)
        
        # Get probabilities if available
        probabilities = None
        try:
            if hasattr(model, 'predict_proba'):
                probabilities = model.predict_proba(input_df)
        except Exception:
            pass
            
        # Create response
        results = []
        for i, pred in enumerate(predictions):
            pred_int = int(pred)
            prediction_label = ">50K" if pred_int == 1 else "<=50K"
            
            result = {
                "prediction": pred_int,
                "prediction_label": prediction_label,
                "probability": float(probabilities[i][1]) if probabilities is not None else None
            }
            results.append(result)
            
        return {"predictions": results}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
