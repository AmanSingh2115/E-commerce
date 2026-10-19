from langchain_core.language_models.fake import FakeListLLM
from typing import Any, List, Optional

class MockLLM(FakeListLLM):
    """
    A zero-network, deterministic mock LLM for local CrewAI testing.
    Inherits from FakeListLLM to pass strict Pydantic v2 validations.
    """
    # This dummy list satisfies the strict Pydantic checks
    responses: List[str] = ["dummy"] 
    
    def _call(self, prompt: str, stop: Optional[List[str]] = None, **kwargs: Any) -> str:
        prompt_lower = prompt.lower()
        
        # Deterministic routing based on keywords in the prompt
        if "escalation" in prompt_lower or "score" in prompt_lower:
            return "Mock Decision: The escalation score is high. Transferring to human support team."
        elif "ord-" in prompt_lower or "status" in prompt_lower:
            return "Mock Decision: I have checked the database. Here is your order status."
        elif "policy" in prompt_lower or "return" in prompt_lower:
            return "Mock Decision: According to Nykaa policy, returns are accepted within the specified window."
            
        return "Mock Decision: I am a local zero-network AI agent processing your request."

if __name__ == "__main__":
    # Test the mock LLM
    llm = MockLLM()
    print("Testing Mock LLM offline:")
    print(llm.invoke("What is the status of ORD-100001?"))
    