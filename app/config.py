import os

class Settings:
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017/inventory")
    PORT: int = int(os.getenv("PORT", "5001"))

settings = Settings()
