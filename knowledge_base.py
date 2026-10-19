# knowledge_base.py

documents = [
    {
        "id": "doc1",
        "topic": "Returns",
        "content": "Nykaa accepts returns within 15 days of delivery for most products. Beauty and personal care items must be unused, sealed, and in original packaging to be eligible for a return."
    },
    {
        "id": "doc2",
        "topic": "Refunds",
        "content": "Refunds are processed to the original payment method within 5-7 business days after the returned item is received and inspected at our fulfillment center."
    },
    {
        "id": "doc3",
        "topic": "Shipping",
        "content": "Standard shipping takes 3-5 business days. Express shipping takes 1-2 business days. Orders with a total value above ₹500 qualify for free standard shipping."
    },
    {
        "id": "doc4",
        "topic": "Escalation",
        "content": "Issues regarding missing items in a delivery, severely damaged products, or shipment delays exceeding 7 days must be immediately escalated to the human support team."
    },
    {
        "id": "doc5",
        "topic": "Order Cancellation",
        "content": "Orders can only be cancelled before they are marked as 'Shipped'. Once an order is dispatched, the customer must refuse delivery or initiate a return after receiving it."
    }
]

def get_knowledge_base():
    """Returns the list of policy documents for the RAG pipeline."""
    return documents

if __name__ == "__main__":
    print(f"Knowledge base loaded with {len(documents)} policy documents.")
    