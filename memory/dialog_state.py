class DialogStateStore:
    def __init__(self):
        self.sessions = {}
    def get(
        self,
        session_id
    ):
        return self.sessions.get(
            session_id,
            {}
        )
    def set(
        self,
        session_id,
        value
    ):
        self.sessions[session_id] = value
    def clear(
        self,
        session_id
    ):
        self.sessions.pop(
            session_id,
            None
        )
dialog_state_store = DialogStateStore()
