import random

def generate_dataset(seed=42, num_records=45):
    """
    Generates a mock dataset of Nykaa e-commerce orders.
    Meets capstone requirements: seed=42, >=40 records, and ~20% delay rate.
    """
    random.seed(seed)
    categories = ['Apparel', 'Electronics', 'Home', 'Footwear', 'Beauty']
    statuses = ['Placed', 'Shipped', 'Delivered', 'Returned', 'Refunded']
    
    dataset = []
    for i in range(1, num_records + 1):
        # Generate a realistic order ID like ORD-100001
        record_id = f"ORD-{100000 + i}"
        
        dataset.append({
            "record_id": record_id,
            "category": random.choice(categories),
            "status": random.choice(statuses),
            "order_value_inr": random.randint(500, 15000),
            "days_since_created": random.randint(0, 30),
            "delayed_shipment": random.random() < 0.20 # ~20% probability of being delayed
        })
        
    return dataset

if __name__ == "__main__":
    # Test the dataset generation
    data = generate_dataset()
    print(f"Successfully generated {len(data)} mock orders.")
    print("Sample Order:", data[0])