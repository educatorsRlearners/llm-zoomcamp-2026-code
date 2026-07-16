import sys

from dotenv import load_dotenv
from rag_helper import RAGBase

from ingest import load_faq_data, build_index
from openai import OpenAI


def create_assistant():
    load_dotenv()

    documents = load_faq_data()
    index = build_index(documents=documents)

    base_rag = RAGBase(index=index, llm_client=OpenAI())

    return base_rag


if __name__ == "__main__":
    assistant = create_assistant()

    query = "How do I join the course?"

    if len(sys.argv) > 2:
        query = sys.argv[1]

    answer = assistant.rag(query=query)
    print(answer)
