from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

def register_not_found_handler(app: FastAPI):
    """
    Registers a catch-all path handler to return a structured JSON response
    when an unregistered route is requested.
    """
    @app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
    async def catch_all(request: Request, path_name: str):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "error": {
                    "message": f"Endpoint '{request.url.path}' not found on this server.",
                    "type": "NotFoundError"
                }
            }
        )
