import gradio as gr
import joblib
import numpy as np

# Load the trained model
model = joblib.load("xgboost-model.pkl")

def predict_death_event(age, anaemia, high_blood_pressure, creatinine_phosphokinase, 
                       diabetes, ejection_fraction, platelets, sex, 
                       serum_creatinine, serum_sodium, smoking, time):
    # Create input array
    input_data = np.array([age, anaemia, high_blood_pressure, creatinine_phosphokinase, 
                          diabetes, ejection_fraction, platelets, sex, 
                          serum_creatinine, serum_sodium, smoking, time]).reshape(1, -1)

    # Make prediction
    prediction = model.predict(input_data)[0]

    # Return prediction
    return "Patient will survive" if prediction == 0 else "Patient will not survive"

# Define input components
age = gr.Slider(minimum=40, maximum=95, value=65, label="Age")
anaemia = gr.Radio(choices=[0, 1], label="Anaemia (0=No, 1=Yes)")
high_blood_pressure = gr.Radio(choices=[0, 1], label="High Blood Pressure (0=No, 1=Yes)")
creatinine_phosphokinase = gr.Slider(minimum=23, maximum=7861, value=582, label="Creatinine Phosphokinase (CPK)")
diabetes = gr.Radio(choices=[0, 1], label="Diabetes (0=No, 1=Yes)")
ejection_fraction = gr.Slider(minimum=14, maximum=80, value=38, label="Ejection Fraction")
platelets = gr.Slider(minimum=25100, maximum=850000, value=265000, label="Platelets")
sex = gr.Radio(choices=[0, 1], label="Sex (0=Female, 1=Male)")
serum_creatinine = gr.Slider(minimum=0.5, maximum=9.4, value=1.1, label="Serum Creatinine")
serum_sodium = gr.Slider(minimum=113, maximum=148, value=136, label="Serum Sodium")
smoking = gr.Radio(choices=[0, 1], label="Smoking (0=No, 1=Yes)")
time = gr.Slider(minimum=4, maximum=285, value=100, label="Time")

# Gradio interface
title = "Patient Survival Prediction"
description = "Predict survival of patient with heart failure, given their clinical record"

iface = gr.Interface(
    fn=predict_death_event,
    inputs=[age, anaemia, high_blood_pressure, creatinine_phosphokinase, 
            diabetes, ejection_fraction, platelets, sex, 
            serum_creatinine, serum_sodium, smoking, time],
    outputs="text",
    title=title,
    description=description,
    allow_flagging='never'
)

if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=7860)