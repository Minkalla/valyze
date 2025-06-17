from fastapi.testclient import TestClient
from ..main import app
from ..schemas import ValyzeInputSchema

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "Valyze MVP"}

def test_submit_data_for_valuation_success():
    test_data = ValyzeInputSchema(
        data_id="test_data_123",
        category="customer_profile",
        value_points={"age": 30, "location": "NYC", "purchases_count": 5},
        is_sensitive=True,
        source="CRM"
    )
    
    response = client.post(
        "/valyze/data",
        json={"input_data": test_data.dict()}
    )
    
    assert response.status_code == 200
    assert response.json()["message"] == "Data valuation completed successfully."
    assert "valuation_score" in response.json()
    assert isinstance(response.json()["valuation_score"], (int, float))
    assert response.json()["model_used"] == "MVP_SimpleValuer"
    assert response.json()["model_version"] == "0.1.0"

def test_submit_data_for_valuation_invalid_input():
    response = client.post(
        "/valyze/data",
        json={"input_data": {"category": "test"}}
    )
    assert response.status_code == 422
    assert "detail" in response.json()
    assert any("data_id" in error["loc"] for error in response.json()["detail"])

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
        json={"input_data": test_data.dict(by_alias=True)}
    )
    
    assert response.status_code == 200
    assert response.json()["model_used"] == "MVP_SimpleValuer"
    assert response.json()["valuation_score"] == 100.0
