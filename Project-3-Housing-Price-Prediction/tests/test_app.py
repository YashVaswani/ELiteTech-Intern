import sys
import os
import pytest

# Add the project root to the python path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from app.app import app

@pytest.fixture
def client():
    """A test client for the app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test that the home page loads successfully."""
    response = client.get("/")
    assert response.status_code == 200
    
    # Simple check to see if the page contains the word 'Predict' or 'Housing'
    html = response.get_data(as_text=True)
    assert "Housing" in html or "Predict" in html

def test_about_page(client):
    """Test that the about page loads successfully."""
    response = client.get("/about")
    assert response.status_code == 200

def test_prediction_invalid_input(client):
    """Test the prediction endpoint with missing or invalid data."""
    response = client.post("/predict", data={
        "area": "",
        "bedrooms": "3",
        "bathrooms": "2"
    })
    
    # Even on error, it renders the template (200 status code) but shows an error message
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Error" in html or "required" in html.lower()
