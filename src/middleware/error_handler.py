import os
import traceback
import logging
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, HTTPException

logger = logging.getLogger("app")

def register_error_handlers(app):
    """
    Registers global exception handlers on the FastAPI app instance.
    """
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """
        Handles Pydantic request body/query validation errors.
        """
        errors = []
        for error in exc.errors():
            errors.append({
                "field": " -> ".join([str(loc) for loc in error["loc"]]),
                "message": error["msg"],
                "type": error["type"]
            })
        
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "success": False,
                "error": {
                    "message": "Validation failed for request inputs.",
                    "type": "ValidationError",
                    "details": errors
                }
            }
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """
        Handles explicit HTTPExceptions raised within path handlers.
        """
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "message": exc.detail,
                    "type": "HTTPException"
                }
            }
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        """
        Catch-all exception handler for uncaught server-side exceptions.
        """
        logger.error(f"Uncaught exception: {exc}\n{traceback.format_exc()}")
        
        env = os.getenv("ENV", "development")
        error_content = {
            "success": False,
            "error": {
                "message": "An unexpected error occurred on the server.",
                "type": "InternalServerError"
            }
        }
        
        # Include trace in response during development
        if env == "development":
            error_content["error"]["details"] = str(exc)
            error_content["error"]["stack"] = traceback.format_exc().split("\n")
            
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=error_content
        )
