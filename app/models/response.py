from pydantic import BaseModel

class ForecastResponse(BaseModel):
    predicted_demand: int
    confidence: float
    message: str = "Success"
