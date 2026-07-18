import sys
from db_save import save_conversation
from dotenv import load_dotenv
from openai import OpenAI

from ingest import load_faq_data, build_index
from metrics import RAGWithMetrics


def create_assistant():
    load_dotenv()

    documents = load_faq_data()
    index = build_index(documents=documents)

    base_rag = RAGWithMetrics(index=index, llm_client=OpenAI())

    return base_rag


if __name__ == "__main__":
    assistant = create_assistant()

    query = "How do I join the course?"

    if len(sys.argv) > 2:
        query = sys.argv[1]

    answer = assistant.rag(query=query)
    print(answer)

    save_conversation(record=assistant.last_call, question=query, course="llm-zoomcamp")
