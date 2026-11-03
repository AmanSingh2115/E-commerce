import re

def mask_pii(text: str) -> str:
    """
    Input-side guardrail: Masks 10-digit Indian phone numbers and 
    the last 4 digits of payment cards before they reach the LLM.
    """
    # 1. Mask standard 10-digit phone numbers (with or without +91)
    text = re.sub(r'(?:\+91[\-\s]?)?\b\d{10}\b', '[PHONE_REDACTED]', text)
    
    # 2. Mask credit/debit card last 4 digits (e.g., "card ending in 1234")
    # Matches variations of "ending in ", "card ", or "ending with " followed by 4 digits.
    text = re.sub(r'(ending in |card |ending with )\d{4}\b', r'\g<1>[CARD_REDACTED]', text, flags=re.IGNORECASE)
    
    return text

def check_prompt_injection(text: str) -> bool:
    """
    Input-side guardrail: Detects basic prompt injection attempts.
    """
    injection_keywords = [
        "ignore previous instructions",
        "system prompt",
        "bypass",
        "you are now",
        "print your instructions"
    ]
    text_lower = text.lower()
    for keyword in injection_keywords:
        if keyword in text_lower:
            return True
    return False

def enforce_token_budget(query: str, max_budget: int = 50):
    """
    Enforces a strict runtime token budget cap.
    Using a word-split proxy to simulate token cost for local execution.
    """
    estimated_tokens = len(query.split())
    
    if estimated_tokens > max_budget:
        raise ValueError(f"Runtime Governance Alert: Request size ({estimated_tokens} tokens) exceeds the maximum allowed budget of {max_budget} tokens. Request rejected to prevent budget overrun.")
    
    return query

# Quick test to ensure it works
if __name__ == "__main__":
    test_input = "My order is delayed. Call me at 9876543210. Refund to card ending in 4321."
    print("Original:", test_input)
    print("Masked:", mask_pii(test_input))