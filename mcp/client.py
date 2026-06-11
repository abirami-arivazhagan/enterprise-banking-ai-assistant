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

from rag.retrievers.hybrid import (
    build_hybrid_retriever
)

from rag.query_transform import (
    hyde_transform
)

from rag.rerankers.cross_encoder_reranker import (
    rerank_documents
)

from prompt_manager.loader import (
    load_prompt
)


class RAGChain:

    def __init__(self):

        self.llm = get_llm()

        self.retriever = (
            build_hybrid_retriever()
        )

    def retrieve_documents(
        self,
        query
    ):

        transformed_query = (
            hyde_transform(query)
        )

        retrieved_docs = (
            self.retriever.invoke(
                transformed_query
            )
        )

        reranked_docs = (
            rerank_documents(
                query,
                retrieved_docs
            )
        )

        return reranked_docs

    def build_chain(self):

        prompt_template = load_prompt(
            "rag_qa"
        )

        prompt = ChatPromptTemplate.from_template(
            prompt_template
        )

        chain = (

            RunnablePassthrough.assign(

                docs=lambda x:
                    self.retrieve_documents(
                        x["query"]
                    ),

                context=lambda x:
                    "\n\n".join([

                        doc.page_content

                        for doc in x["docs"]

                    ])

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

        docs = self.retrieve_documents(
            inputs["query"]
        )

        return {

            "response": response,

            "retrieved_docs": docs,

            "citations": [

                {
                    "source":
                    doc.metadata.get(
                        "source",
                        "Unknown"
                    )
                }

                for doc in docs

            ]
        }