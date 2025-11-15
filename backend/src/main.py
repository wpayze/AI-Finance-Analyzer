import logging
import time
from typing import Dict
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from src.api.endpoints import router as api_router # Import the router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Finance Analyzer",
    description="An API for uploading financial transaction files and retrieving AI-powered analysis.",
    version="1.0.0"
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Middleware to log details of incoming HTTP requests and their responses.
    """
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"Request: {request.method} {request.url.path} - Status: {response.status_code} - Time: {process_time:.4f}s")
    return response

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Global exception handler to catch all unhandled exceptions and return a structured JSON response.
    """
    logger.error(f"Unhandled exception for request: {request.method} {request.url.path}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred.", "error": str(exc)},
    )

app.include_router(api_router) # Include the router

@app.get("/")
def read_root() -> Dict[str, str]:
    """
    Root endpoint for the API.
    """
    return {"message": "Welcome to the AI Finance Analyzer API"}

# Later, we will include routers from the api sub-package here.
