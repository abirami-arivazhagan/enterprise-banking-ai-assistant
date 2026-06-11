from collections import deque
from app.core.config import (
    MEMORY_WINDOW_SIZE
)

class ConversationalMemory:
    def __init__(
        self,
        window_size=MEMORY_WINDOW_SIZE
    ):
        self.messages = deque(
            maxlen=window_size * 2
        )
    def save_context(
        self,
        question,
        answer
    ):
        self.messages.append(
            {
                "role": "user",
                "content": question
            }
        )
        self.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

    def load_context(self):
        return list(
            self.messages
        )
