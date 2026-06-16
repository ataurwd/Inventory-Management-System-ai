import pandas as pd
from prophet import Prophet
import logging

def forecast_product(transactions: list, forecast_days: int = 30):
    if not transactions or len(transactions) < 2:
        return { "predicted_demand": 0, "confidence": 0.0 }
        
    try:
        df = pd.DataFrame(transactions, columns=['ds', 'y'])  # ds=date, y=qty_sold
        
        # Prophet handles time series forecasting
        model = Prophet(yearly_seasonality=True, weekly_seasonality=True)
        # Suppress prophet logs
        logging.getLogger("prophet").setLevel(logging.WARNING)
        
        model.fit(df)
        
        future = model.make_future_dataframe(periods=forecast_days)
        forecast = model.predict(future)
        
        # Sum the predicted demand for the forecast period
        predicted_demand = forecast.tail(forecast_days)['yhat'].sum()
        
        # Calculate a basic confidence metric
        confidence = 1 - (forecast['yhat_upper'] - forecast['yhat_lower']).mean() / forecast['yhat'].mean()
        
        # Ensure non-negative
        predicted_demand = max(0, predicted_demand)
        confidence = max(0.0, min(1.0, confidence))
        
        return { 
            "predicted_demand": round(predicted_demand), 
            "confidence": round(confidence, 2) 
        }
    except Exception as e:
        print(f"Prophet forecast error: {e}")
        return { "predicted_demand": 0, "confidence": 0.0 }
