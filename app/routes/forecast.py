from fastapi import APIRouter, HTTPException
from app.models.request import ForecastRequest
from app.models.response import ForecastResponse
from app.services.mongo_service import get_product_transactions
from app.services.prophet_service import forecast_product

router = APIRouter()

@router.post("/predict", response_model=ForecastResponse)
async def predict(request: ForecastRequest):
    try:
        # Fetch historical
        transactions = get_product_transactions(request.product_id, days=request.days_history)
        
        # We need at least 2 data points for Prophet
        if len(transactions) < 2:
            return ForecastResponse(
                predicted_demand=0,
                confidence=0.0,
                message="Insufficient historical data for forecasting"
            )
            
        # Run forecast
        result = forecast_product(transactions, forecast_days=30)
        
        return ForecastResponse(
            predicted_demand=result["predicted_demand"],
            confidence=result["confidence"],
            message="Forecast successful"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
