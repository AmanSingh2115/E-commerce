import chromadb
from knowledge_base import get_knowledge_base

def setup_rag_collection():
    """
    Initializes the ChromaDB local vector database and loads Nykaa policy documents.
    """
    # Create a local persistent database in the 'chroma_db' folder
    client = chromadb.PersistentClient(path="./chroma_db")
    
    # Create or get the collection
    collection = client.get_or_create_collection(name="nykaa_policies")
    
    # Load documents from our knowledge base
    docs = get_knowledge_base()
    
    # Check if collection is empty before adding to avoid duplicates
    if collection.count() == 0:
        documents = [doc["content"] for doc in docs]
        metadatas = [{"topic": doc["topic"]} for doc in docs]
        ids = [doc["id"] for doc in docs]
        
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print("Documents successfully embedded and added to ChromaDB.")
    else:
        print(f"ChromaDB already contains {collection.count()} documents.")
        
    return collection

def retrieve_policy(query_text: str, n_results: int = 1) -> str:
    """
    Queries the local vector database for the most relevant policy.
    """
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_collection(name="nykaa_policies")
    
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )
    
    if results['documents'] and results['documents'][0]:
        return results['documents'][0][0]
    return "No relevant policy found."

if __name__ == "__main__":
    print("Setting up Local RAG Pipeline...")
    setup_rag_collection()
    print("\nTesting the RAG retrieval:")
    test_query = "How many days do I have to return an item?"
    print(f"Query: '{test_query}'")
    print(f"Retrieved Policy: {retrieve_policy(test_query)}")
    