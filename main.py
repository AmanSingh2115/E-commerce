from fastapi import FastAPI
from pydantic import BaseModel
from crew_agents import ecommerce_crew
from guardrails import mask_pii

# 1. Initialize the FastAPI server
app = FastAPI(title="Nykaa Capstone Backend")

# 2. Define the expected JSON format for incoming requests
class CustomerQuery(BaseModel):
    text: str

# 3. Create the HTTP POST endpoint
@app.post("/api/support")
def run_support_crew(query: CustomerQuery):
    print(f"\n--- Incoming Request: {query.text} ---")
    
    # Apply your security guardrails first
    safe_input = mask_pii(query.text)
    
    # Trigger your local Llama 3.2 multi-agent system
    result = ecommerce_crew.kickoff(inputs={'customer_query': safe_input})
    
    # Return the final agent decision as a clean JSON response
    return {
        "status": "success",
        "agent_response": str(result)
    }