from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.config.db import get_db
from src.controllers import health

# Main API router
router = APIRouter(prefix="/api/v1")

@router.get("/health", tags=["Health"])
def get_health(db: Session = Depends(get_db)):
    """
    Check the health of the API application and its database dependencies.
    """
    return health.check_health(db)

# -------------------------------------------------------------------
# Example of how candidates can register resource routers:
#
# from src.routes.users import router as users_router
# router.include_router(users_router, prefix="/users", tags=["Users"])
# -------------------------------------------------------------------
