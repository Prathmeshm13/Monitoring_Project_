import pytest
import json
from Backend import app, mysql
from flask import session

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['MYSQL_DB'] = 'test_failure_monitoring'  # Use a test database
    client = app.test_client()
    yield client

def test_signup(client):
    response = client.post('/signup', json={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpassword'
    })
    assert response.status_code in [201, 400]  # 400 if email already exists
    

def test_login(client):
    response = client.post('/login', json={
        'email': 'testuser@example.com',
        'password': 'testpassword'
    })
    assert response.status_code in [200, 401]  # 401 if invalid credentials

def test_protected_route(client):
    client.post('/login', json={
        'email': 'testuser@example.com',
        'password': 'testpassword'
    })
    response = client.get('/')
    assert response.status_code == 200

def test_logout(client):
    client.get('/logout')
    with client.session_transaction() as sess:
        assert 'loggedin' not in sess

def test_stream_data(client):
    response = client.get('/stream-data')
    assert response.status_code == 200
    assert response.mimetype == 'text/event-stream'

def test_plot_data(client):
    response = client.get('/plot-data')
    assert response.status_code == 200
    assert response.mimetype == 'application/json'

def test_model_predictions():
    from app import regressor, classifier
    import pandas as pd
    import numpy as np
    
    sample_input = pd.DataFrame([[1.0, 1.0, 1.0, 1.0, 1.0]], 
                                 columns=["σ_eff", "CDI", "TDF", "VFI", "Voltage_Impact"])
    
    risk_score = regressor.predict(sample_input)
    label = classifier.predict(sample_input)
    
    assert isinstance(risk_score[0], (float, np.float32, np.float64))
    assert isinstance(label[0], (int, np.int32, np.int64))
