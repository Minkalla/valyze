from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Any, Dict
from .models.simple_valuation_model import SimpleValuationModel
from .models.base_valuation_model import BaseValuationModel
import logging # Import the logging module for provenance logging

# Configure logging for the application.
# Messages with INFO level or higher will be processed.
# The format includes timestamp, log level, and the message itself.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__) # Get a logger instance for this module

# Initialize FastAPI application
app = FastAPI(
    title="Valyze API - MVP",
    description="API for AI-powered data valuation (MVP) in the Minkalla Valyze module. "
                "Utilizes a pluggable ML model interface.",
    version="1.0.0",
)

# --- ML Model Loading (Task 3.2.3) ---
# For MVP, we load a single instance of SimpleValuationModel.
# In a Version 1.0 product, this would be replaced by a dynamic model registry and loader
# capable of managing multiple ML models and their versions.
model_config = {
    "name": "MVP_SimpleValuer",
    "version": "0.1.0",
    "base_value": 100,
    "multiplier_factor": {"high_value": 2.0, "medium_value": 1.0, "low_value": 0.5}
}
# Instantiate the selected valuation model
valuation_model: BaseValuationModel = SimpleValuationModel(model_config)

# --- Request and Response Models ---
# Define the data structure for incoming valuation requests
class ValuationRequest(BaseModel):
    """
    Schema for data valuation requests.
    This model defines the expected structure of input data for valuation.
    In a V1.0 product, this input will typically be validated against a dynamically registered schema (Task 3.4).
    """
    data: Dict[str, Any] # Arbitrary data payload for valuation; structure flexible for MVP

# Define the data structure for outgoing valuation responses
class ValuationResponse(BaseModel):
    """
    Schema for data valuation responses.
    This model defines the expected structure of the output after a data valuation is performed.
    """
    valuation_score: float
    confidence_score: float
    valuation_timestamp: str
    model_used: str
    model_version: str
    message: str = "Data valuation completed successfully."

# --- API Endpoints ---

@app.get("/health", summary="Health check endpoint")
async def health_check():
    """
    Returns the operational status of the Valyze service.
    This endpoint is used to verify that the service is running and responsive.
    """
    logger.info("Health check endpoint accessed.") # Log health check access
    return {"status": "ok", "service": "Valyze MVP"}

@app.post(
    "/valyze/data",
    response_model=ValuationResponse,
    summary="Submit data for valuation",
    status_code=status.HTTP_200_OK,
)
async def submit_data_for_valuation(request: ValuationRequest):
    """
    Submits an arbitrary data payload for valuation by the configured ML model.
    For the MVP, this uses the SimpleValuationModel to return a rule-based valuation.
    """
    # --- Placeholder for Schema Registration (Task 3.4) ---
    # In a Version 1.0 product, the incoming 'request.data' would be validated
    # against a dynamically registered schema here to ensure data quality and format.
    # For MVP, we simply pass the data directly to the model.

    try:
        # Perform the valuation prediction using the loaded model
        valuation_result = valuation_model.predict(request.data)
        
        # --- Minimal Valuation Provenance Logging (Task 3.3) ---
        # For MVP, we log the valuation event to the application's console/log stream.
        # In a Version 1.0 product, this result, along with input hash, model version,
        # and other metadata, would be logged immutably to a dedicated provenance ledger (e.g., blockchain).
        logger.info(f"Data valued by {valuation_model.name} v{valuation_model.version}: "
                    f"Score={valuation_result.get('valuation_score')} for data_id={request.data.get('data_id', 'N/A')}")
        
        # This print statement provides a direct "Verifiable Log" to the console for MVP demonstration.
        print(f"[VERIFIABLE LOG]: Data valued by {valuation_model.name} v{valuation_model.version}: "
              f"Score={valuation_result.get('valuation_score')}")

    except Exception as e:
        # Basic error handling for model prediction failures.
        # Errors are logged at ERROR level, including traceback for debugging.
        logger.error(f"Error during valuation for data_id={request.data.get('data_id', 'N/A')}: {e}", exc_info=True)
        # Re-raise HTTPException for client consumption
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during valuation: {e}",
        )

    # Return the structured valuation response
    return ValuationResponse(
        valuation_score=valuation_result.get("valuation_score"),
        confidence_score=valuation_result.get("confidence_score", 0.0),
        valuation_timestamp=valuation_result.get("valuation_timestamp"),
        model_used=valuation_result.get("model_used"),
        model_version=valuation_result.get("model_version"),
    )
