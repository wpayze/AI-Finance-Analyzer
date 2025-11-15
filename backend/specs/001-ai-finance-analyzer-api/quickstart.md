# Quickstart: AI Finance Analyzer Backend

**Generated**: 2025-11-15

This guide provides instructions to set up and run the backend service locally.

## Prerequisites

-   Python 3.10+
-   `pip` and `venv`

## Setup

1.  **Clone the repository** (if you haven't already).

2.  **Create and activate a virtual environment**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
    ```

3.  **Install dependencies**:
    The project follows a minimal dependency philosophy. The `requirements.txt` file will be created during implementation. For now, the planned dependencies are:
    ```bash
    pip install fastapi "uvicorn[standard]" pydantic python-multipart openpyxl groq
    ```

4.  **Set up environment variables**:
    Create a `.env` file in the root of the `backend` directory and add your Groq API key:
    ```
    GROQ_API_KEY="your_api_key_here"
    ```

## Running the Service

1.  **Start the FastAPI server**:
    ```bash
    uvicorn main:app --reload
    ```
    *(This assumes the main FastAPI app instance is in a file named `main.py`)*

2.  **Access the API documentation**:
    Once the server is running, navigate to `http://127.0.0.1:8000/docs` in your browser to view the interactive Swagger UI documentation generated from the OpenAPI schema.

## Basic Workflow

1.  Use the `/docs` interface or a tool like `curl` to **POST** a transaction file (CSV or Excel) to the `/upload` endpoint.
2.  Copy the `job_id` from the response.
3.  **GET** the `/analysis/{job_id}/status` endpoint to check the job's progress.
4.  Once the status is `COMPLETED`, you can **GET** the other endpoints (`/transactions`, `/insights`, `/predictions`) to retrieve the analysis results.
