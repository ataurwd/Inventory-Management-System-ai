from pydantic import BaseModel

class ForecastRequest(BaseModel):
    product_id: str
    days_history: int = 90
