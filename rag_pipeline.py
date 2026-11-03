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

def retrieve_policy(query_text: str, n_results: int = 1, threshold: float = 1.2) -> str:
    """
    Queries the local vector database for the most relevant policy.
    Enforces a strict distance threshold to prevent hallucinations.
    """
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_collection(name="nykaa_policies")
    
    # 1. Ask ChromaDB to include 'distances' in the results
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results,
        include=["documents", "distances"] 
    )
    
    if results['documents'] and results['documents'][0]:
        best_doc = results['documents'][0][0]
        distance = results['distances'][0][0]
        
        # Print the distance so you can calibrate your threshold for Task 4
        print(f"\n[DEBUG RAG] Query: '{query_text}' | Distance Score: {distance:.4f}")
        
        # 2. Reject the query if the distance is too high (poor match)
        # You must tune this threshold number based on your printed debug scores!
        if distance > threshold:
            return "I don't know. I cannot find this information in the knowledge base."
            
        return best_doc
        
    return "I don't know. I cannot find this information in the knowledge base."