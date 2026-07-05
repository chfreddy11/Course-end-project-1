import csv
import os
import random

# ==========================================
# 1. SETUP & PATH CONFIGURATION
# ==========================================
folder_path = r"C:\Users\Chris\OneDrive\Desktop\VT AGI\Python refresher\Assessments\Course end project 1"
csv_file_name = "customer_purchases.csv"
report_file_name = "Analytics_Summary_Report.txt"

csv_full_path = os.path.join(folder_path, csv_file_name)
report_full_path = os.path.join(folder_path, report_file_name)

# Ensure the destination directory exists
os.makedirs(folder_path, exist_ok=True)


# ==========================================
# 2. DATA GENERATION STAGE
# ==========================================
# Product options per category
products_pool = {
    "Electronics": ["Smartphone", "Laptop", "Headphones", "Smartwatch", "Tablet"],
    "Home Goods": ["Blender", "Coffee Maker", "Desk Lamp", "Air Purifier", "Vacuum"],
    "Clothing": ["Jacket", "Sneakers", "Jeans", "Sweater", "T-Shirt"],
}

generated_rows = []

# Generate 10 unique customer IDs
for i in range(1, 11):
    customer_id = f"CUST{1000 + i}"

    # Flatten categories and items into a single list of tuples to sample from
    all_available_products = []
    for category, products in products_pool.items():
        for product in products:
            all_available_products.append((category, product))

    # Pick 4 random unique product-category pairs for this customer
    customer_purchases = random.sample(all_available_products, 4)

    for category, product in customer_purchases:
        # Lowered minimum to $5 to ensure some total orders land in the Low/Moderate tiers
        cost = round(random.uniform(5, 1500), 2)

        # Generate a random profit margin percentage (between 10% and 40%)
        margin_percentage = round(random.uniform(0.10, 0.40), 2)
        profit = round(cost * margin_percentage, 2)

        generated_rows.append(
            [
                customer_id,
                category,
                product,
                f"${cost:.2f}",
                f"{int(margin_percentage * 100)}%",
                f"${profit:.2f}",
            ]
        )

# Write generated data out to the CSV file
headers = ["Customer ID", "Category", "Product", "Cost", "Profit Margin", "Profit"]
with open(csv_full_path, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    writer.writerows(generated_rows)

print(f"--> Success: New data generated and written to {csv_file_name}\n")


# ==========================================
# 3. DATA READING & INGESTION STAGE
# ==========================================
customer_names = set()
order_tuples = []
customer_orders_dict = {}

with open(csv_full_path, mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        cust_id = row["Customer ID"]
        category = row["Category"]
        product = row["Product"]
        # Scrub formatting out of currency strings to perform math
        price = float(row["Cost"].replace("$", "").replace(",", ""))

        customer_names.add(cust_id)
        order_tuples.append((cust_id, product, price, category))

        if cust_id not in customer_orders_dict:
            customer_orders_dict[cust_id] = []
        customer_orders_dict[cust_id].append(product)

customer_names_list = sorted(list(customer_names))


# ==========================================
# 4. DATA PROCESSING & ANALYSIS STAGE
# ==========================================
# A. Product Catalog Map & Set
product_to_category = {prod: cat for _, prod, _, cat in order_tuples}
unique_categories = sorted(list({cat for _, _, _, cat in order_tuples}))

# B. Calculate Total Spending per Customer
customer_spending = {}
for cust_id, _, price, _ in order_tuples:
    customer_spending[cust_id] = customer_spending.get(cust_id, 0.0) + price

# C. Segment Customers (Using your original $50 and $100 limits)
customer_classification = {}
for cust_id, total_spent in customer_spending.items():
    if total_spent > 100:
        customer_classification[cust_id] = "High-Value Buyer"
    elif 50 <= total_spent <= 100:
        customer_classification[cust_id] = "Moderate Buyer"
    else:
        customer_classification[cust_id] = "Low-Value Buyer"

# D. Generate Revenue per Category
category_revenue = {}
for _, _, price, category in order_tuples:
    category_revenue[category] = category_revenue.get(category, 0.0) + price

# E. Complete Unique Product Set and Filter Electronics via List Comprehension
unique_products_ordered = sorted(list({prod for _, prod, _, _ in order_tuples}))
electronics_buyers = sorted(
    list({cust for cust, _, _, cat in order_tuples if cat == "Electronics"})
)

# F. Top 3 Highest Spending Customers via sorting
top_three = sorted(customer_spending.items(), key=lambda x: x[1], reverse=True)[:3]

# G. Set Operations for Multi-Category Buyers & Cross-Over Categories
customer_category_sets = {}
for cust_id, _, _, category in order_tuples:
    if cust_id not in customer_category_sets:
        customer_category_sets[cust_id] = set()
    customer_category_sets[cust_id].add(category)

multi_category_buyers = sorted(
    [c for c, cats in customer_category_sets.items() if len(cats) > 1]
)
clothing_buyers = {cust for cust, _, _, cat in order_tuples if cat == "Clothing"}
elec_buyers_set = set(electronics_buyers)
both_elec_and_cloth = sorted(list(elec_buyers_set.intersection(clothing_buyers)))


# ==========================================
# 5. OUTPUT REPORT GENERATION STAGE
# ==========================================
with open(report_full_path, mode="w", encoding="utf-8") as out:
    out.write("=========================================================\n")
    out.write("             BUSINESS SUMMARY ANALYTICS REPORT           \n")
    out.write("=========================================================\n\n")

    out.write("1. PRODUCT CHANNEL CLASSIFICATIONS\n")
    out.write(f" - Active Categories: {', '.join(unique_categories)}\n")
    out.write(f" - Evaluated Unique SKUs: {len(unique_products_ordered)} items\n\n")

    out.write("2. ACCOUNT CUSTOMER SEGMENTATION SUMMARY\n")
    for cust, spend in sorted(customer_spending.items()):
        out.write(
            f" - Account: {cust} | Revenue: ${spend:,.2f} | Tag: {customer_classification[cust]}\n"
        )

    out.write("\n3. SECTOR FINANCIAL REVENUE TRACKING\n")
    for cat, rev in category_revenue.items():
        out.write(f" - {cat} Total Pipeline Volume: ${rev:,.2f}\n")

    out.write("\n4. TOP PERFORMING CONSUMERS\n")
    for idx, (cust, spend) in enumerate(top_three, 1):
        out.write(f"   {idx}. Account ID: {cust} (Total Volume: ${spend:,.2f})\n")

    out.write("\n5. BEHAVIORAL INTERSECTION METRICS\n")
    out.write(
        f" - Diversified Category Shoppers (>1 Category): {', '.join(multi_category_buyers)}\n"
    )
    out.write(
        f" - Core Overlap Shoppers (Electronics AND Clothing): {', '.join(both_elec_and_cloth) if both_elec_and_cloth else 'None'}\n"
    )

print(f"--> Success: Report file created at {report_file_name}")
print("Process fully completed!")