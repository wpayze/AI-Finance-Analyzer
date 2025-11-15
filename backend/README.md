# AI Finance Analyzer Backend

This is a backend-only system that helps users analyze their personal finances using AI. It accepts user-uploaded bank transaction files (CSV or Excel), parses and validates the data, extracts relevant transaction fields, and prepares it for AI-powered analysis. The system classifies expenses, detects spending patterns, identifies anomalous transactions, generates monthly spending predictions, and produces structured financial insights.

## Features

-   **File Upload**: Accepts CSV and Excel transaction files.
-   **AI-Powered Categorization**: Classifies expenses into meaningful categories using Groq's Llama 3 8B model.
-   **Financial Insights**: Detects spending patterns and identifies anomalous transactions.
-   **Spending Predictions**: Generates monthly spending predictions.
-   **RESTful API**: Exposes endpoints for file upload, analysis status, categorized transactions, insights, and predictions.

## Technology Stack

-   **Language**: Python 3.10+
-   **Web Framework**: FastAPI
-   **Data Validation**: Pydantic
-   **File Parsing**: `csv` (built-in), `openpyxl`
-   **AI Inference**: Groq API (Llama 3 8B model)

## Setup

### Prerequisites

-   Python 3.10+
-   `pip` and `venv`

### Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd backend
    ```

2.  **Create and activate a virtual environment**:
    ```bash
    python -m venv .venv
    # On Windows:
    .venv\Scripts\activate
    # On macOS/Linux:
    source .venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables**:
    Create a `.env` file in the root of the `backend` directory and add your Groq API key:
    ```
    GROQ_API_KEY="your_groq_api_key_here"
    ```
    You can obtain a Groq API key from [Groq Cloud](https://console.groq.com/keys).

## Running the Service

1.  **Start the FastAPI server**:
    ```bash
    uvicorn src.main:app --reload
    ```
    The server will typically run on `http://127.0.0.1:8000`.

2.  **Access the API documentation**:
    Once the server is running, navigate to `http://127.0.0.1:8000/docs` in your browser to view the interactive Swagger UI documentation generated from the OpenAPI schema.

## API Usage

The API provides the following main endpoints:

-   `POST /upload`: Upload a CSV or Excel transaction file. Returns an `AnalysisJob` ID.
-   `GET /analysis/{job_id}/status`: Check the status of an analysis job.
-   `GET /analysis/{job_id}/transactions`: Retrieve categorized transactions for a completed job.
-   `GET /analysis/{job_id}/insights`: Retrieve AI-generated insights (patterns, anomalies).
-   `GET /analysis/{job_id}/predictions`: Retrieve spending predictions.

### Example Workflow

1.  **Upload a file**:
    Use the `/docs` interface or a tool like `curl` to `POST` your transaction file to `http://127.0.0.1:8000/upload`.
    Example `curl` command (replace `your_file.csv` with your file path):
    ```bash
    curl -X 'POST' \
      'http://127.0.0.1:8000/upload' \
      -H 'accept: application/json' \
      -H 'Content-Type: multipart/form-data' \
      -F 'file=@your_file.csv;type=text/csv'
    ```
    Note the `job_id` from the response.

2.  **Check status**:
    ```bash
    curl -X 'GET' \
      'http://127.0.0.1:8000/analysis/{job_id}/status' \
      -H 'accept: application/json'
    ```
    Wait until the `status` field is `COMPLETED`.

3.  **Retrieve results**:
    ```bash
    # Get categorized transactions
    curl -X 'GET' \
      'http://172.0.0.1:8000/analysis/{job_id}/transactions' \
      -H 'accept: application/json'

    # Get insights
    curl -X 'GET' \
      'http://127.0.0.1:8000/analysis/{job_id}/insights' \
      -H 'accept: application/json'

    # Get predictions
    curl -X 'GET' \
      'http://127.0.0.1:8000/analysis/{job_id}/predictions' \
      -H 'accept: application/json'
    ```

## Contributing

Please refer to the project's `CONTRIBUTING.md` (if available) for guidelines on how to contribute.

## License

This project is licensed under the MIT License.
