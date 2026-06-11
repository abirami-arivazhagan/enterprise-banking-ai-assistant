class UploadContextStore:

    def __init__(self):

        self.sessions = {}

    def set_latest(
        self,
        session_id,
        upload
    ):

        self.sessions[session_id] = upload

    def get_latest(
        self,
        session_id
    ):

        return self.sessions.get(
            session_id
        )

    def clear(
        self,
        session_id
    ):

        self.sessions.pop(
            session_id,
            None
        )


upload_context_store = UploadContextStore()
