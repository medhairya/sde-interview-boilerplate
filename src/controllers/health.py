import os
from sqlalchemy.orm import Session
from sqlalchemy import text

def check_health(db: Session):
    """
    Controller function that verifies database connection and returns
    overall system status.
    """
    try:
        # Execute a simple query to verify database accessibility
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"unreachable: {str(e)}"

    is_healthy = db_status == "connected"

    return {
        "status": "healthy" if is_healthy else "degraded",
        "services": {
            "database": db_status,
            "api": "online"
        },
        "environment": os.getenv("ENV", "development")
    }
