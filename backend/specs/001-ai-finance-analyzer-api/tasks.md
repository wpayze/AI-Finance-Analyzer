# Tasks: AI-Powered Financial Analysis Backend

**Feature**: AI-Powered Financial Analysis Backend
**Generated**: 2025-11-15

This document breaks down the implementation of the feature into actionable, dependency-ordered tasks.

---

## Phase 1: Project Setup

**Goal**: Initialize the project structure and dependencies.

- [X] T001 Create the main application directory `src/`
- [X] T002 Create the tests directory `tests/`
- [X] T003 Create sub-packages for the layered architecture: `src/api/`, `src/services/`, `src/models/`, `src/core/`
- [X] T004 Create an empty `requirements.txt` file
- [X] T005 Create a `.env` file from `.env.example` (or create a new one) to hold environment variables like `GROQ_API_KEY`
- [X] T006 Add initial dependencies to `requirements.txt`: `fastapi`, `uvicorn[standard]`, `pydantic`, `python-dotenv`, `groq`, `python-multipart`, `openpyxl`

---

## Phase 2: Foundational Components

**Goal**: Implement core, non-feature-specific components that are prerequisites for all user stories.

- [X] T007 [P] Implement a configuration loader in `src/core/config.py` to load the `GROQ_API_KEY` from the `.env` file
- [X] T008 [P] Define the core Pydantic models in `src/models/schemas.py` based on `data-model.md`: `AnalysisJob`, `Transaction`, `Insight`, `Prediction`
- [X] T009 Initialize the FastAPI application in `src/main.py`
- [X] T010 Implement a global exception handler in `src/main.py` to catch errors and return structured JSON responses

---

## Phase 3: User Story 1 - File Upload and Initial Processing

**Goal**: A developer can upload a financial transaction file (CSV/Excel) and have the system accept and parse it, returning a job ID.
**Independent Test**: Can be tested by calling the `/upload` endpoint with a valid file and verifying a `202` response with a job ID.

- [X] T011 [US1] Create an in-memory data store for analysis jobs in `src/core/storage.py` (a simple dictionary to hold job status and results)
- [ ] T012 [US1] Implement the file parsing logic in `src/services/parser.py` to handle CSV and Excel files, returning a list of `Transaction` objects
- [X] T013 [US1] Implement the ingestion service in `src/services/ingestion.py` that uses the parser, creates an `AnalysisJob`, stores it, and returns the job details
- [X] T014 [US1] Create the `/upload` endpoint in `src/api/endpoints.py` that uses the ingestion service and returns a `202 Accepted` response

---

## Phase 4: User Story 2 - Trigger and Retrieve AI Analysis

**Goal**: A developer can retrieve the results of the AI-powered analysis, including categorized transactions, spending patterns, and generated insights.
**Independent Test**: Poll the `/analysis/{job_id}/status` endpoint. Once complete, call `/analysis/{job_id}/transactions` and verify the returned data is structured and complete.

- [X] T015 [US2] Implement the Groq API client in `src/services/groq_client.py`. It should have a method to send transaction descriptions for categorization using the Llama 3 8B model.
- [X] T016 [US2] Implement the core analysis logic in `src/services/analysis.py`. This service will orchestrate the process: take parsed transactions, use the `groq_client` to categorize them, and generate insights/predictions.
- [X] T017 [US2] Modify the ingestion service in `src/services/ingestion.py` to trigger the analysis service asynchronously (e.g., using FastAPI's `BackgroundTasks`).
- [X] T018 [P] [US2] Implement the `/analysis/{job_id}/status` endpoint in `src/api/endpoints.py` to retrieve job status from the in-memory store.
- [X] T019 [P] [US2] Implement the `/analysis/{job_id}/transactions` endpoint in `src/api/endpoints.py`.
- [X] T020 [P] [US2] Implement the `/analysis/{job_id}/insights` endpoint in `src/api/endpoints.py`.
- [X] T021 [P] [US2] Implement the `/analysis/{job_id}/predictions` endpoint in `src/api/endpoints.py`.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Goal**: Add final touches, logging, and documentation.

- [X] T022 [P] Implement structured logging middleware in `src/main.py` to log request/response details.
- [X] T023 [P] Add detailed docstrings and type hints to all functions and methods.
- [X] T024 Create a `README.md` at the project root with updated setup and usage instructions based on the final implementation.

---

## Dependencies & Execution Strategy

-   **User Story Dependencies**: US2 is dependent on US1. The file upload mechanism must be in place before analysis can be performed.
-   **Implementation Strategy**: The feature should be implemented in phases.
    1.  First, implement **Phase 1, 2, and 3** to deliver the MVP: the ability to upload a file and get a job ID. This is a testable, valuable increment.
    2.  Next, implement **Phase 4** to add the core AI analysis functionality.
    3.  Finally, complete **Phase 5** to ensure the service is robust and maintainable.
-   **Parallel Execution**:
    -   Within Phase 2, `config.py` and `models/schemas.py` can be developed in parallel.
    -   Within Phase 4, after the core analysis service is complete, all the retrieval endpoints (T018-T021) can be implemented in parallel as they are independent reads from the data store.
