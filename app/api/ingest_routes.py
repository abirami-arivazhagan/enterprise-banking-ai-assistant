from fastapi import APIRouter
from rag.ingestion.ingestion_pipeline import (
    IngestionPipeline
)

router = APIRouter()
pipeline = IngestionPipeline()

@router.post("/ingest")
def ingest_documents():

    pipeline.run()

    return {
        "status":
            "Documents ingested"
    }