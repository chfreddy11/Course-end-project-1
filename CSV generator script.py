import csv
import os
import random

# 1. Define the exact file path
# Using a raw string (r"...") prevents Windows backslashes from causing errors
folder_path = r"C:\Users\Chris\OneDrive\Desktop\VT AGI\Python refresher\Assessments\Course end project 1"
file_name = "customer_purchases.csv"
full_path = os.path.join(folder_path, file_name)

# 2. Define the product pool per category
products_pool = {
    "Electronics": ["Smartphone", "Laptop", "Headphones", "Smartwatch", "Tablet"],
    "Home Goods": ["Blender", "Coffee Maker", "Desk Lamp", "Air Purifier", "Vacuum"],
    "Clothing": ["Jacket", "Sneakers", "Jeans", "Sweater", "T-Shirt"],
}

# 3. Generate the data
data = []

# Generate 10 unique customer IDs (e.g., CUST1001 to CUST1010)
for i in range(1, 11):
    customer_id = f"CUST{1000 + i}"

    # Each customer purchases 4 random products total
    # We sample from all available products across the 3 categories
    all_available_products = []
    for category, products in products_pool.items():
        for product in products:
            all_available_products.append((category, product))

    # Pick 4 random unique product-category pairs for this customer
    customer_purchases = random.sample(all_available_products, 4)

    for category, product in customer_purchases:
        # Generate random cost between $25 and $1500
        cost = round(random.uniform(25, 1500), 2)

        # Generate a random profit margin percentage (e.g., between 10% and 40%)
        # and calculate the actual profit dollars
        margin_percentage = round(random.uniform(0.10, 0.40), 2)
        profit = round(cost * margin_percentage, 2)

        data.append(
            [
                customer_id,
                category,
                product,
                f"${cost:.2f}",
                f"{int(margin_percentage * 100)}%",
                f"${profit:.2f}",
            ]
        )

# 4. Ensure the directory exists and write to CSV
try:
    os.makedirs(folder_path, exist_ok=True)

    headers = [
        "Customer ID",
        "Category",
        "Product",
        "Cost",
        "Profit Margin",
        "Profit",
    ]

    with open(full_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(data)

    print(f"Success! CSV file generated and saved to:\n{full_path}")

except Exception as e:
    print(f"An error occurred while saving the file: {e}")