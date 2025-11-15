from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException, status
from src.services.ingestion import ingestion_service, FileParsingError
from src.models.schemas import AnalysisJob, JobStatus, Transaction, Insight, Prediction
from src.core.storage import db, results_db
from uuid import UUID
from typing import List

router = APIRouter()

@router.post("/upload", response_model=AnalysisJob, status_code=status.HTTP_202_ACCEPTED)
async def upload_file(file: UploadFile = File(..., description="The transaction file (CSV or Excel) to upload."), 
                      background_tasks: BackgroundTasks = None) -> AnalysisJob:
    """
    Uploads a transaction file (CSV or Excel) for AI-powered financial analysis.
    The file is processed asynchronously.
    
    Args:
        file: The uploaded file.
        background_tasks: FastAPI's dependency for running background tasks.
        
    Returns:
        An AnalysisJob object with the initial status.
        
    Raises:
        HTTPException: If the file type is unsupported.
    """
    if not file.filename.endswith(('.csv', '.xls', '.xlsx')):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported file type. Only CSV and Excel are supported."
        )

    job = ingestion_service.create_analysis_job()
    
    # Process the file in a background task
    # This allows the API to respond immediately while processing happens
    background_tasks.add_task(ingestion_service.process_file, str(job.job_id), file)
    
    return job

@router.get("/analysis/{job_id}/status", response_model=AnalysisJob)
async def get_analysis_status(job_id: UUID) -> AnalysisJob:
    """
    Retrieves the current status of an analysis job.
    
    Args:
        job_id: The unique identifier of the analysis job.
        
    Returns:
        An AnalysisJob object with its current status.
        
    Raises:
        HTTPException: If the job is not found.
    """
    job = db.get(job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found.")
    return job

@router.get("/analysis/{job_id}/transactions", response_model=List[Transaction])
async def get_categorized_transactions(job_id: UUID) -> List[Transaction]:
    """
    Retrieves the categorized transactions for a completed analysis job.
    
    Args:
        job_id: The unique identifier of the analysis job.
        
    Returns:
        A list of Transaction objects with assigned categories.
        
    Raises:
        HTTPException: If the job is not found, not completed, or transactions are unavailable.
    """
    job = db.get(job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found.")
    if job.status != JobStatus.COMPLETED:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Analysis not yet completed for this job.")
    
    results = results_db.get(job_id)
    if not results or "categorized_transactions" not in results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categorized transactions not found for this job.")
    
    return results["categorized_transactions"]

@router.get("/analysis/{job_id}/insights", response_model=List[Insight])
async def get_financial_insights(job_id: UUID) -> List[Insight]:
    """
    Retrieves AI-generated insights (spending patterns, anomalies) for a completed analysis job.
    
    Args:
        job_id: The unique identifier of the analysis job.
        
    Returns:
        A list of Insight objects.
        
    Raises:
        HTTPException: If the job is not found, not completed, or insights are unavailable.
    """
    job = db.get(job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found.")
    if job.status != JobStatus.COMPLETED:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Analysis not yet completed for this job.")
    
    results = results_db.get(job_id)
    if not results or "insights" not in results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Insights not found for this job.")
    
    return results["insights"]

@router.get("/analysis/{job_id}/predictions", response_model=List[Prediction])
async def get_spending_predictions(job_id: UUID) -> List[Prediction]:
    """
    Retrieves future spending predictions for a completed analysis job.
    
    Args:
        job_id: The unique identifier of the analysis job.
        
    Returns:
        A list of Prediction objects.
        
    Raises:
        HTTPException: If the job is not found, not completed, or predictions are unavailable.
    """
    job = db.get(job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found.")
    if job.status != JobStatus.COMPLETED:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Analysis not yet completed for this job.")
    
    results = results_db.get(job_id)
    if not results or "predictions" not in results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Predictions not found for this job.")
    
    return results["predictions"]
