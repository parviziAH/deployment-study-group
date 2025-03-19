import json
from utils import load_json, save_json


def calculate_restock_needs():
    """
    Calculates which inventory items need restocking based on current stock and sales data.
    Restock rule: if stock < sales * 2, item needs restocking
    """
    # Load inventory data
    data = load_json("input_data.json")

    # Process each item to determine restock needs
    results = []
    for item in data:
        needs_restock = item["stock"] < item["sales"] * 2
        results.append({
            "item": item["item"],
            "current_stock": item["stock"],
            "recent_sales": item["sales"],
            "restock": needs_restock,
            "recommended_order": (item["sales"] * 2 - item["stock"]) if needs_restock else 0
        })

    # Save results to output file
    save_json("output_data.json", results)
    print(f"Processed {len(data)} inventory items. Results saved to output_data.json")


if __name__ == "__main__":
    calculate_restock_needs()