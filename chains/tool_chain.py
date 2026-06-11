from langchain_core.runnables import (
    RunnablePassthrough
)

from langchain_core.output_parsers import (
    StrOutputParser
)

from langchain_core.prompts import (
    ChatPromptTemplate
)

from app.core.llm import get_llm
from rag.retrievers.retriever_basic import get_retriever
from prompt_manager.loader import load_prompt


class RAGChain:
    def __init__(self):
        self.llm = get_llm()
        self.retriever = get_retriever()

    def retrieve_context(self, query):

        docs = self.retriever.invoke(query)

        return {
            "docs": docs,
            "context": "\n\n".join([
                doc.page_content
                for doc in docs
            ])
        }

    def build_chain(self):
        prompt_template = load_prompt(
            "rag_qa"
        )

        prompt = ChatPromptTemplate.from_template(
            prompt_template
        )

        chain = (

            RunnablePassthrough.assign(

                retrieved=lambda x:
                    self.retrieve_context(
                        x["query"]
                    ),

                context=lambda x:
                    x["retrieved"]["context"]

            )

            | prompt

            | self.llm

            | StrOutputParser()

        )

        return chain.with_retry()

    def invoke(self, inputs):
        chain = self.build_chain()
        response = chain.invoke({
            "query": inputs["query"],
            "role": inputs.get(
                "role",
                "customer"
            )
        })
        retrieved = self.retrieve_context(
            inputs["query"]
        )
        return {
            "response": response,
            "retrieved_docs":
                retrieved["docs"],
            "citations": [
                {
                    "source":
                    doc.metadata.get(
                        "source",
                        "Unknown"
                    )
                }
                for doc in retrieved["docs"]

            ]
        }