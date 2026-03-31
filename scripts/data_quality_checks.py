import pandas as pd
import sys

def check_sales_data(filepath: str):
    """
    Validates the transformed sales data to ensure business rules are met.
    Throws Exception if quality checks fail, triggering an Airflow task failure.
    """
    print(f"🔍 [DQ] Validating Sales File: {filepath}")
    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        raise FileNotFoundError(f"Missing file for DQ check: {filepath}")

    # Check 1: No negative amounts
    if (df['amount'] < 0).any():
        raise ValueError("❌ Data Quality Check Failed: Found negative amounts in sales data.")

    # Check 2: Essential columns exist
    required_cols = ['order_id', 'customer_id', 'amount', 'status', 'order_date']
    if not all(col in df.columns for col in required_cols):
        raise ValueError(f"❌ Data Quality Check Failed: Missing required columns. Found: {df.columns.tolist()}")

    # Check 3: Status is valid
    valid_statuses = {"COMPLETED", "PENDING", "REFUNDED", "CANCELED"}
    if not set(df['status'].unique()).issubset(valid_statuses):
        raise ValueError("❌ Data Quality Check Failed: Found unfamiliar status codes.")
        
    print(f"✅ Sales Data Quality passed for {len(df)} records.")
    return True

def check_inventory_data(filepath: str):
    """
    Validates inventory aggregated data.
    """
    print(f"🔍 [DQ] Validating Inventory File: {filepath}")
    df = pd.read_csv(filepath)
    
    # Check 1: No negative stock
    if (df['stock_level'] < 0).any():
        raise ValueError("❌ Data Quality Check Failed: Inventory cannot be negative.")
        
    print(f"✅ Inventory Data Quality passed.")
    return True

if __name__ == "__main__":
    # Can be run manually for debugging
    if len(sys.argv) < 3:
        print("Usage: python data_quality_checks.py [sales|inventory] [path]")
        sys.exit(1)
        
    check_type, path = sys.argv[1], sys.argv[2]
    if check_type == "sales":
        check_sales_data(path)
    elif check_type == "inventory":
        check_inventory_data(path)
