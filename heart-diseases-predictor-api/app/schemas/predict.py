from pydantic import BaseModel, Field

class PredictionInput(BaseModel):
    """
    Input model for heart failure prediction.
    
    This model contains all required parameters for the prediction.
    """
    age: int = Field(..., description="Age of the patient", gt=0, example=65)
    anaemia: int = Field(..., description="Decrease of red blood cells (0: No, 1: Yes)", ge=0, le=1, example=0)
    high_blood_pressure: int = Field(..., description="If the patient has hypertension (0: No, 1: Yes)", ge=0, le=1, example=1)
    creatinine_phosphokinase: int = Field(..., description="Level of CPK enzyme in the blood (mcg/L)", ge=0, example=582)
    diabetes: int = Field(..., description="If the patient has diabetes (0: No, 1: Yes)", ge=0, le=1, example=0)
    ejection_fraction: int = Field(..., description="Percentage of blood leaving the heart at each contraction", ge=0, le=100, example=30)
    platelets: float = Field(..., description="Platelets in the blood (kiloplatelets/mL)", ge=0, example=265000)
    sex: int = Field(..., description="Woman or man (0: Woman, 1: Man)", ge=0, le=1, example=1)
    serum_creatinine: float = Field(..., description="Level of serum creatinine in the blood (mg/dL)", ge=0, example=1.9)
    serum_sodium: int = Field(..., description="Level of serum sodium in the blood (mEq/L)", ge=0, example=130)
    smoking: int = Field(..., description="If the patient smokes (0: No, 1: Yes)", ge=0, le=1, example=0)
    time: int = Field(..., description="Follow-up period (days)", ge=0, example=4)
    
    class Config:
        schema_extra = {
            "example": {
                "age": 65,
                "anaemia": 0,
                "high_blood_pressure": 1,
                "creatinine_phosphokinase": 582,
                "diabetes": 0,
                "ejection_fraction": 30,
                "platelets": 265000,
                "sex": 1,
                "serum_creatinine": 1.9,
                "serum_sodium": 130,
                "smoking": 0,
                "time": 4
            }
        }

class PredictionResponse(BaseModel):
    """Response model for heart failure prediction."""
    result: str = Field(..., description="Prediction result")