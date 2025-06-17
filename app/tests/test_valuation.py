# app/tests/test_valuation.py

from fastapi.testclient import TestClient
from app.main import app
from app.schemas import ValyzeInputSchema

# Create a test client for your FastAPI application
client = TestClient(app)

# Test the /health endpoint
def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "Valyze MVP"}

# Test the /valyze/data endpoint with valid input
def test_submit_data_for_valuation_success():
    # Example data conforming to ValyzeInputSchema
    test_data = ValyzeInputSchema(
        data_id="test_data_123",
        category="customer_profile",
        value_points={"age": 30, "location": "NYC", "purchases_count": 5},
        is_sensitive=True,
        source="CRM"
    )

    response = client.post(
        "/valyze/data",
        json={"input_data": test_data.dict()} # Wrap in input_data as per main.py's ValuationRequest
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Data valuation completed successfully."
    assert "valuation_score" in response.json()
    assert isinstance(response.json()["valuation_score"], (int, float))
    assert response.json()["model_used"] == "MVP_SimpleValuer"
    assert response.json()["model_version"] == "0.1.0"

# Test the /valyze/data endpoint with invalid input (missing required field)
def test_submit_data_for_valuation_invalid_input():
    response = client.post(
        "/valyze/data",
        json={"input_data": {"category": "test"}} # Missing data_id
    )
    assert response.status_code == 422 # FastAPI's validation error code
    assert "detail" in response.json()
    assert any("data_id" in error["loc"] for error in response.json()["detail"])

# Test the /valyze/data endpoint with a different priority to check model logic
def test_submit_data_for_valuation_different_priority():
    test_data = ValyzeInputSchema(
        data_id="test_data_456",
        category="marketing_data",
        value_points={"campaign_id": "xyz", "clicks": 100},
        is_sensitive=False,
        source="AdPlatform"
    )

    response = client.post(
        "/valyze/data",
        json={"input_data": test_data.dict(by_alias=True)} # Ensure dict conversion is compatible
    )

    assert response.status_code == 200
    assert response.json()["model_used"] == "MVP_SimpleValuer"
    # Verify the score changes based on the model's multiplier factor (default is 1.0 if priority not specified)
    assert response.json()["valuation_score"] == 100.0 # From SimpleValuationModel base_value = 100, default multiplier 1.0