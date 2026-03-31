import os
import json
import random
import uuid
import pandas as pd
from datetime import datetime
from faker import Faker

fake = Faker()

def generate_sales_data(target_date: str, output_path: str):
    """
    Simulates extracting daily sales data from an E-Commerce API.
    """
    print(f"[Sales API] Extracting Data for date: {target_date}")
    
    # Randomly fail 5% of the time to demonstrate Airflow Retries
    if random.random() < 0.05:
        raise ConnectionError("Simulated API Error 503 Service Unavailable")
        
    num_records = random.randint(50, 500)
    data = []
    
    for _ in range(num_records):
        data.append({
            "order_id": str(uuid.uuid4()),
            "customer_id": fake.random_int(min=1, max=10000),
            "amount": round(random.uniform(10.5, 999.9), 2),
            "status": random.choice(["COMPLETED", "PENDING", "REFUNDED", "COMPLETED"]),
            "order_date": target_date
        })
        
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False)
    print(f"✅ Successfully wrote {len(data)} sales records to {output_path}")

def generate_inventory_data(target_date: str, output_path: str):
    """
    Simulates extracting daily inventory data.
    """
    print(f"[Inventory API] Extracting Data for date: {target_date}")
    
    num_items = 200
    data = []
    for i in range(1, num_items + 1):
        data.append({
            "product_id": f"PRD_{i:04d}",
            "stock_level": random.randint(0, 500),
            "warehouse_id": random.choice(["WH_EAST", "WH_WEST", "WH_NORTH"]),
            "snapshot_date": target_date
        })
        
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False)
    print(f"✅ Successfully wrote {len(data)} inventory records to {output_path}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True, help="Execution date (YYYY-MM-DD)")
    parser.add_argument("--type", required=True, choices=["sales", "inventory"], help="Type of data to extract")
    parser.add_argument("--output", required=True, help="Output CSV path")
    args = parser.parse_args()
    
    if args.type == "sales":
        generate_sales_data(args.date, args.output)
    elif args.type == "inventory":
        generate_inventory_data(args.date, args.output)
