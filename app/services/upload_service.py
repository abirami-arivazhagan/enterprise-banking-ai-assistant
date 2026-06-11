import os
import shutil

from rag.ingestion.ingestion_pipeline import (
    IngestionPipeline
)

from memory.upload_context import (
    upload_context_store
)

class UploadService:
    def __init__(self):
        self.pipeline = (
            IngestionPipeline()
        )
    async def upload_document(
        self,
        file,
        session_id="default"
    ):
        upload_dir = "uploads"
        os.makedirs(
            upload_dir,
            exist_ok=True
        )
        file_path = os.path.join(
            upload_dir,
            file.filename
        )
        with open(file_path, "wb") as f:

            shutil.copyfileobj(
                file.file,
                f
            )
        ingestion_result = (
            self.pipeline.ingest(
                file_path
            )
        )

        upload_context_store.set_latest(
            session_id,
            {
                "filename": file.filename,
                "path": file_path,
                "preview": ingestion_result.get(
                    "preview",
                    ""
                )
            }
        )

        return {
            "status": "success",
            "filename": file.filename,
            "ingestion": ingestion_result
        }
