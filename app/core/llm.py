from langchain_openai import (
    ChatOpenAI
)

from langchain_anthropic import (
    ChatAnthropic
)

from app.core.config import (

    OPENAI_API_KEY,

    ANTHROPIC_API_KEY,

    OPENAI_MODEL,

    CLAUDE_MODEL
)

# =========================================================
# LLM SERVICE
# =========================================================

class LLMService:

    def __init__(self):

        self.primary_llm = None

        self.fallback_llm = None

        # =================================================
        # OPENAI
        # =================================================

        if OPENAI_API_KEY:

            self.primary_llm = ChatOpenAI(

                model=OPENAI_MODEL,

                temperature=0.3,

                api_key=OPENAI_API_KEY
            )

        # =================================================
        # CLAUDE
        # =================================================

        if ANTHROPIC_API_KEY:

            self.fallback_llm = ChatAnthropic(

                model=CLAUDE_MODEL,

                temperature=0.3,

                api_key=ANTHROPIC_API_KEY
            )

    # =====================================================
    # INVOKE
    # =====================================================

    def invoke(
        self,
        messages
    ):

        # =================================================
        # PRIMARY
        # =================================================

        if self.primary_llm:

            try:

                return self.primary_llm.invoke(
                    messages
                )

            except Exception as e:

                print(
                    f"[LLM] OpenAI failed: {e}"
                )

        # =================================================
        # FALLBACK
        # =================================================

        if self.fallback_llm:

            try:

                return self.fallback_llm.invoke(
                    messages
                )

            except Exception as e:

                print(
                    f"[LLM] Claude failed: {e}"
                )

        raise RuntimeError(
            "No working LLM available."
        )