from rag.embedding.embedding_utils import load_embedding_model, embed_documents
from rag.retriever.retriever_utils import load_vector_index, search_index

def get_relevant_documents(query, top_k=5):
    model = load_embedding_model()
    index, metadata = load_vector_index()

    query_vector = embed_documents([query], model)[0]
    results = search_index(query_vector, index, metadata, top_k=top_k)

    return results

if __name__ == "__main__":
    query = input("Enter your query: ")
    results = get_relevant_documents(query)
    print("\nTop Relevant Chunks:")
    for r in results:
        print(f"- Title: {r['metadata'].get('title', 'N/A')} (Score: {r['score']:.2f})")
