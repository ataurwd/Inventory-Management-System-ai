from pymongo import MongoClient
from app.config import settings
from datetime import datetime, timedelta

# Create a global MongoClient instance to reuse connections
client = MongoClient(settings.MONGO_URI)

def get_db():
    try:
        return client.get_default_database()
    except Exception:
        # Fallback to parsing from URI or using "test"
        from urllib.parse import urlparse
        try:
            parsed = urlparse(settings.MONGO_URI)
            db_name = parsed.path.strip("/")
            if "?" in db_name:
                db_name = db_name.split("?")[0]
            if not db_name:
                db_name = "test"
            return client[db_name]
        except Exception:
            return client["test"]

db = get_db()

def get_product_transactions(product_id: str, days: int = 90) -> list:
    """
    Fetch transactions for a product over the last N days.
    Returns a list of dicts with 'ds' (date string) and 'y' (quantity sold/out).
    """
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    from bson.objectid import ObjectId
    try:
        product_query = ObjectId(product_id)
    except Exception:
        product_query = product_id

    # We only care about stock OUT (sales/usage) to forecast demand
    pipeline = [
        {
            "$match": {
                "product": product_query,
                "type": "OUT",
                "createdAt": { "$gte": cutoff_date }
            }
        },
        {
            "$project": {
                "date": { "$dateToString": { "format": "%Y-%m-%d", "date": "$createdAt" } },
                "quantity": 1
            }
        },
        {
            "$group": {
                "_id": "$date",
                "total_qty": { "$sum": "$quantity" }
            }
        },
        {
            "$sort": { "_id": 1 }
        }
    ]
    
    results = list(db.transactions.aggregate(pipeline))
    
    # Format for Prophet
    formatted = [{"ds": r["_id"], "y": r["total_qty"]} for r in results]
    return formatted
