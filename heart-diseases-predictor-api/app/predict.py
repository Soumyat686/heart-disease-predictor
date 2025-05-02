import numpy as np
import joblib
from app.config import get_settings

# Load the model on module import
settings = get_settings()
model = joblib.load(settings.model_path)

def predict_death_event(age, anaemia, high_blood_pressure, creatinine_phosphokinase, 
                       diabetes, ejection_fraction, platelets, sex, 
                       serum_creatinine, serum_sodium, smoking, time):
    """
    Predict whether a patient will survive based on their medical data.
    
    Args:
        age (int): Age of the patient
        anaemia (int): Whether the patient has anaemia (0: No, 1: Yes)
        high_blood_pressure (int): Whether the patient has hypertension (0: No, 1: Yes)
        creatinine_phosphokinase (int): Level of CPK enzyme in the blood (mcg/L)
        diabetes (int): Whether the patient has diabetes (0: No, 1: Yes)
        ejection_fraction (int): Percentage of blood leaving the heart at each contraction
        platelets (float): Platelets in the blood (kiloplatelets/mL)
        sex (int): Woman or man (0: Woman, 1: Man)
        serum_creatinine (float): Level of serum creatinine in the blood (mg/dL)
        serum_sodium (int): Level of serum sodium in the blood (mEq/L)
        smoking (int): Whether the patient smokes (0: No, 1: Yes)
        time (int): Follow-up period (days)
        
    Returns:
        str: Prediction result ("Patient will survive" or "Patient will not survive")
    """
    # Create input array
    input_data = np.array([age, anaemia, high_blood_pressure, creatinine_phosphokinase, 
                          diabetes, ejection_fraction, platelets, sex, 
                          serum_creatinine, serum_sodium, smoking, time]).reshape(1, -1)

    # Make prediction
    prediction = model.predict(input_data)[0]

    # Return prediction
    return "Patient will survive" if prediction == 0 else "Patient will not survive"