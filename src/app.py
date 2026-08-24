from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes.index import router as api_router
from src.middleware.error_handler import register_error_handlers
from src.middleware.not_found import register_not_found_handler

def create_app() -> FastAPI:
    """
    App Factory function. Creates, configures and returns the FastAPI app instance.
    """
    app = FastAPI(
        title="RESTful API Boilerplate",
        description="A scalable, clean FastAPI backend boilerplate designed for technical coding interviews.",
        version="1.0.0",
        docs_url="/docs",      # Interactive Swagger UI API documentation path
        redoc_url="/redoc"    # Alternative API documentation path
    )

    # Configure CORS (Cross-Origin Resource Sharing)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Open to all origins by default in interview settings
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register API routers
    app.include_router(api_router)

    # Register global exception handlers (Validation, HTTP, Uncaught exceptions)
    register_error_handlers(app)

    # Register catch-all 404 handler (MUST be registered after all routers)
    register_not_found_handler(app)

    return app

app = create_app()
