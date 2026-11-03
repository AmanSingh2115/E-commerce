from guardrails import enforce_token_budget

# 1. Standard request (Under budget)
standard_query = "What is the status of ORD-100001?"
print("Testing normal query...")
enforce_token_budget(standard_query)
print("Normal query passed successfully!\n")

# 2. Oversized request (Over budget)
oversized_query = "Where is my order? " * 30  # Generates a 90+ token request
print("Testing oversized query...")
try:
    enforce_token_budget(oversized_query)
except ValueError as e:
    print(f"BLOCKED: {e}")