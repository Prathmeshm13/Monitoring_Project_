import pytest
import pandas as pd
import numpy as np
import joblib
from werkzeug.security import generate_password_hash, check_password_hash

# Load ML models
regressor = joblib.load("C:/Users/1041210/OneDrive - Blue Yonder/Desktop/FINAL_PYTHON_PROJECT/Backend/Data_generator/models/xgb_regressor.pkl")
classifier = joblib.load("C:/Users/1041210/OneDrive - Blue Yonder/Desktop/FINAL_PYTHON_PROJECT/Backend/Data_generator/models/trained_classifier (1).pkl")

def test_password_hashing():
    password = "testpassword"
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    assert check_password_hash(hashed_password, password) == True

def test_data_processing():
    joint_1_torque = 10.0
    load_variation = 5.0
    joint_1_temp = 50.0
    ambient_temp = 25.0
    joint_1_vibration = 0.5
    joint_1_velocity = 1.5
    voltage_fluctuation = 220.0
    
    σ_eff = joint_1_torque / (load_variation + 1)
    CDI = σ_eff
    TDF = np.exp((joint_1_temp - ambient_temp) / 20)
    VFI = joint_1_vibration * joint_1_velocity
    Voltage_Impact = voltage_fluctuation / 250

    data_df = pd.DataFrame([[σ_eff, CDI, TDF, VFI, Voltage_Impact]],
                           columns=["σ_eff", "CDI", "TDF", "VFI", "Voltage_Impact"])
    
    assert data_df.shape == (1, 5)

def test_model_prediction():
    sample_data = pd.DataFrame([[0.5, 0.5, 1.2, 0.75, 0.88]],
                                columns=["σ_eff", "CDI", "TDF", "VFI", "Voltage_Impact"])
    
    failure_risk_score = regressor.predict(sample_data)[0]
    failure_label = classifier.predict(sample_data)[0]
    
    assert isinstance(failure_risk_score, float)
    assert failure_label in [0, 1]  # Assuming binary classification
