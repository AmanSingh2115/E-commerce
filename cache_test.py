import time

# 1. Initialize the in-memory cache dictionary
rag_cache = {}

def normalize_query(query: str) -> str:
    """Normalizes text by lowercasing and stripping extra spaces to ensure identical queries match."""
    return " ".join(query.lower().split())

def simulated_llm_call(query: str) -> str:
    """Simulates the 2-second delay of an actual LLM generating a grounded response."""
    time.sleep(2)
    return "Apparel can be returned within 14 days of delivery. Tags must be intact."

def cached_generation(query: str) -> str:
    """Checks the cache before allowing an expensive RAG/LLM call."""
    normalized = normalize_query(query)
    
    # Task 16: Check for a cache hit
    if normalized in rag_cache:
        print("  -> [CACHE HIT] Avoiding redundant LLM call.")
        return rag_cache[normalized]
        
    # Task 16: Cache miss, run the pipeline and save the result
    print("  -> [CACHE MISS] Executing full LLM RAG generation...")
    response = simulated_llm_call(query)
    rag_cache[normalized] = response
    return response

if __name__ == "__main__":
    test_query = " What is the  return policy for apparel? "
    
    print("\n--- First Request: Database & LLM ---")
    start_time = time.time()
    cached_generation(test_query)
    print(f"Execution Time: {time.time() - start_time:.4f} seconds\n")
    
    print("--- Second Request: Identical Query ---")
    start_time = time.time()
    cached_generation(test_query)
    print(f"Execution Time: {time.time() - start_time:.4f} seconds\n")