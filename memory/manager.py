from memory.conversational_memory import (
    ConversationalMemory
)

class MemoryManager:

    def __init__(self):

        self.sessions = {}
    def get_memory(
        self,
        session_id
    ):
        if session_id not in self.sessions:
            self.sessions[session_id] = ConversationalMemory()
        return self.sessions[
            session_id
        ]
