from langchain_core.prompts import (
    ChatPromptTemplate
)

from langchain_core.output_parsers import (
    StrOutputParser
)

from app.core.llm import (
    get_llm
)


llm = get_llm()


class MemorySummarizer:

    def summarize(
        self,
        history
    ):

        prompt = (
            ChatPromptTemplate.from_template(
                """
                Summarize the following
                conversation.

                Conversation:
                {history}
                """
            )
        )

        chain = (

            prompt

            | llm

            | StrOutputParser()
        )

        return chain.invoke({

            "history": history
        })