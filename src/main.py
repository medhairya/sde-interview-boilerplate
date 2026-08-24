import os
import uvicorn
from dotenv import load_dotenv
from src.config.db import engine, Base

# Ensure environment variables are loaded
load_dotenv()

# Create all database tables on server start (simplifies SQL schema setup during interviews)
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8000"))
    env = os.getenv("ENV", "development")

    # Enable reload only in development mode
    reload = (env == "development")

    print(f"\n=======================================================")
    print(f"[*] Starting Uvicorn API server in [{env}] mode")
    print(f"[*] Local Base URL:   http://{host}:{port}")
    print(f"[*] Swagger Docs:     http://{host}:{port}/docs")
    print(f"[*] ReDoc:            http://{host}:{port}/redoc")
    print(f"=======================================================\n")

    uvicorn.run(
        "src.app:app",
        host=host,
        port=port,
        reload=reload
    )
