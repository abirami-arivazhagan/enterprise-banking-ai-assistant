import uuid
import json
import os
from datetime import datetime

COMPLAINT_STORE = "complaints.json"

def load_complaints():

    if not os.path.exists(COMPLAINT_STORE):

        return []

    with open(
        COMPLAINT_STORE,
        "r"
    ) as file:

        return json.load(file)

def save_complaints(complaints):

    with open(
        COMPLAINT_STORE,
        "w"
    ) as file:

        json.dump(
            complaints,
            file,
            indent=2
        )

class ComplaintTools:
    @staticmethod
    def create_complaint(
        issue_type,
        description,
        session_id="default"
    ):
        ticket_id = str(
            uuid.uuid4()
        )[:8]
        complaint = {
            "status": "success",
            "ticket_id": ticket_id,
            "issue_type": issue_type,
            "description": description,
            "session_id": session_id,
            "created_at": datetime.utcnow().isoformat(),
            "message":
            "Complaint registered successfully."
        }
        complaints = load_complaints()
        complaints.append(
            complaint
        )
        save_complaints(
            complaints
        )
        return complaint
    @staticmethod
    def list_complaints(
        session_id="default"
    ):
        complaints = [
            complaint
            for complaint in load_complaints()
            if complaint["session_id"] == session_id
        ]
        return {
            "status":
            "success",
            "complaints":
            complaints
        }
