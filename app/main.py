from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Any, Dict
from .models.simple_valuation_model import SimpleValuationModel
from .models.base_valuation_model import BaseValuationModel
import logging
from .schemas import ValyzeInputSchema

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Valyze API - MVP",
    description="API for AI-powered data valuation (MVP) in the Minkalla Valyze module. "
                "Utilizes a pluggable ML model interface.",
    version="1.0.0",
)

model_config = {
    "name": "MVP_SimpleValuer",
    "version": "0.1.0",
    "base_value": 100,
    "multiplier_factor": {"high_value": 2.0, "medium_value": 1.0, "low_value": 0.5}
}
valuation_model: BaseValuationModel = SimpleValuationModel(model_config)

class ValuationRequest(BaseModel):
    input_data: ValyzeInputSchema

class ValuationResponse(BaseModel):
    valuation_score: float
    confidence_score: float
    valuation_timestamp: str
    model_used: str
    model_version: str
    message: str = "Data valuation completed successfully."

@app.get("/health", summary="Health check endpoint")
async def health_check():
    logger.info("Health check endpoint accessed.")
    return {"status": "ok", "service": "Valyze MVP"}

@app.post(
    "/valyze/data",
    response_model=ValuationResponse,
    summary="Submit data for valuation",
    status_code=status.HTTP_200_OK,
)
async def submit_data_for_valuation(request: ValuationRequest):
    try:
        valuation_result = valuation_model.predict(request.input_data.model_dump())
        
        logger.info(f"Data valued by {valuation_model.name} v{valuation_model.version}: "
                    f"Score={valuation_result.get('valuation_score')} for data_id={request.input_data.data_id}")
        
        print(f"[VERIFIABLE LOG]: Data valued by {valuation_model.name} v{valuation_model.version}: "
              f"Score={valuation_result.get('valuation_score')}")

    except Exception as e:
        logger.error(f"Error during valuation for data_id={request.input_data.data_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during valuation: {e}",
        )

    return ValuationResponse(
        valuation_score=valuation_result.get("valuation_score"),
        confidence_score=valuation_result.get("confidence_score", 0.0),
        valuation_timestamp=valuation_result.get("valuation_timestamp"),
        model_used=valuation_result.get("model_used"),
        model_version=valuation_result.get("model_version"),
    )
