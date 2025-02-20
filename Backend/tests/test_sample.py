import pytest
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
import numpy as np

def test_password_hashing():
    password = "testpassword"
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    assert check_password_hash(hashed_password, password)

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
    assert all(data_df.columns == ["σ_eff", "CDI", "TDF", "VFI", "Voltage_Impact"])
