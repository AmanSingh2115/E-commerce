from crewai.tools import tool
from dataset import generate_dataset

# Generate the mock database once and store it in memory
_mock_orders = generate_dataset(seed=42)
ORDERS_DB = {order["record_id"]: order for order in _mock_orders}

@tool("Order Status Tool")
def check_order_status(record_id: str) -> dict:
    """
    Checks the status of a Nykaa order and calculates an escalation score.
    Returns the status, order value, and escalation score. Input should be the exact order ID.
    """
    order = ORDERS_DB.get(record_id)
    if not order:
        return {"error": f"Order {record_id} not found."}
    
    # Calculate Escalation Score [0.0 to 1.0]
    # 1. Normalize the days_since_created (0 to 30 days) to a 0.0 - 0.5 scale.
    recency_weight = (order["days_since_created"] / 30.0) * 0.5
    
    # 2. Add a flat 0.5 penalty if the shipment is delayed.
    delayed_weight = 0.5 if order["delayed_shipment"] else 0.0
    
    escalation_score = recency_weight + delayed_weight
    
    # Threshold Justification: A score above 0.65 requires escalation. 
    # This means ANY delayed order older than 9 days (0.5 + (9/30)*0.5 = 0.65) triggers an escalation.
    
    return {
        "status": order["status"],
        "order_value_inr": order["order_value_inr"],
        "escalation_score": round(escalation_score, 2),
        "needs_escalation": escalation_score > 0.65
    }

# Quick test to ensure it works
if __name__ == "__main__":
    sample_id = list(ORDERS_DB.keys())[0]
    print(f"Testing tool with ID {sample_id}:")
    print(check_order_status.invoke({"record_id": sample_id}))
    