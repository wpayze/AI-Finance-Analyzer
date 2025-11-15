from typing import Dict, Any
from uuid import UUID
from src.models.schemas import AnalysisJob, Transaction, Insight, Prediction

# This is a simple in-memory "database" for demonstration purposes.
# In a production environment, you would use a real database like PostgreSQL,
# a key-value store like Redis, or a dedicated job queue system.
db: Dict[UUID, AnalysisJob] = {}
"""In-memory storage for AnalysisJob objects, keyed by job_id."""

# We will also store results here, keyed by job_id
results_db: Dict[UUID, Dict[str, Any]] = {}
"""In-memory storage for analysis results (transactions, insights, predictions), keyed by job_id."""
