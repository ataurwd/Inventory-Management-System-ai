from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="SmartStock AI Service",
    description="Prophet-based demand forecasting microservice",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "prophet-ai", "version": "1.0.0"}


from app.routes import forecast
app.include_router(forecast.router, prefix="/api", tags=["forecast"])
