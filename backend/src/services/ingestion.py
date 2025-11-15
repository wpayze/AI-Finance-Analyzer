from typing import List
from fastapi import UploadFile
from src.models.schemas import AnalysisJob, JobStatus, Transaction
from src.core.storage import db, results_db
from src.services.parser import parse_csv, parse_excel, FileParsingError
from src.services.analysis import analysis_service
from datetime import datetime
from uuid import UUID # Added for type hinting

class IngestionService:
    """
    Service responsible for handling file uploads, parsing, and orchestrating analysis jobs.
    """
    def create_analysis_job(self) -> AnalysisJob:
        """
        Creates a new analysis job and stores it in the in-memory database.
        
        Returns:
            The newly created AnalysisJob object.
        """
        job = AnalysisJob()
        db[job.job_id] = job
        return job

    async def process_file(self, job_id: str, file: UploadFile) -> AnalysisJob:
        """
        Processes an uploaded file, parses its content, triggers analysis,
        and updates the job status.
        
        Args:
            job_id: The ID of the analysis job.
            file: The uploaded file (CSV or Excel).
            
        Returns:
            The updated AnalysisJob object.
            
        Raises:
            ValueError: If the job_id is not found.
            FileParsingError: If the file type is unsupported or parsing fails.
            Exception: For any other unexpected errors during processing.
        """
        job = db.get(UUID(job_id)) # Convert job_id to UUID
        if not job:
            raise ValueError(f"Job with ID {job_id} not found.")

        job.status = JobStatus.IN_PROGRESS
        db[job.job_id] = job # Update job status in DB

        try:
            file_content = await file.read()
            transactions: List[Transaction] = []

            if file.filename.endswith('.csv'):
                transactions = parse_csv(file_content.decode('utf-8'))
            elif file.filename.endswith('.xls') or file.filename.endswith('.xlsx'):
                transactions = parse_excel(file_content)
            else:
                raise FileParsingError("Unsupported file type. Only CSV and Excel are supported.")
            
            # Trigger analysis service
            analysis_results = await analysis_service.analyze_transactions(transactions) # Pass Transaction objects
            
            # Store parsed transactions and analysis results
            results_db[job.job_id] = analysis_results

            job.status = JobStatus.COMPLETED
            db[job.job_id] = job # Update job status in DB
            return job

        except FileParsingError as e:
            job.status = JobStatus.FAILED
            job.error_message = str(e)
            db[job.job_id] = job
            raise
        except Exception as e:
            job.status = JobStatus.FAILED
            job.error_message = f"An unexpected error occurred during file processing: {e}"
            db[job.job_id] = job
            raise

ingestion_service = IngestionService()
