import csv
import os

# --- 1. SETUP & FILE PATHS ---
folder_path = r"C:\Users\Chris\OneDrive\Desktop\VT AGI\Python refresher\Assessments\Course end project 1"
file_name = "customer_purchases.csv"
full_path = os.path.join(folder_path, file_name)
output_summary_path = os.path.join(folder_path, "Analytics_Summary_Report.txt")

# Initialize containers
customer_names = set()
order_tuples = []
customer_orders_dict = {}

# Read input data
if not os.path.exists(full_path):
    raise FileNotFoundError(f"Source data file not found at: {full_path}")

with open(full_path, mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        cust_id = row["Customer ID"]
        category = row["Category"]
        product = row["Product"]
        price = float(row["Cost"].replace("$", "").replace(",", ""))

        customer_names.add(cust_id)
        order_tuples.append((cust_id, product, price, category))
        
        if cust_id not in customer_orders_dict:
            customer_orders_dict[cust_id] = []
        customer_orders_dict[cust_id].append(product)

customer_names_list = sorted(list(customer_names))

# --- 2. CATEGORY DATA MAPPING ---
product_to_category = {prod: cat for _, prod, _, cat in order_tuples}
unique_categories = sorted(list({cat for _, _, _, cat in order_tuples}))

# --- 3. SPENDING ANALYSIS & SEGMENTATION ---
customer_spending = {}
for cust_id, _, price, _ in order_tuples:
    customer_spending[cust_id] = customer_spending.get(cust_id, 0.0) + price

customer_classification = {}
for cust_id, total_spent in customer_spending.items():
    if total_spent > 3000:
        customer_classification[cust_id] = "High-Value Buyer"
    elif 1000 <= total_spent <= 3000:
        customer_classification[cust_id] = "Moderate Buyer"
    else:
        customer_classification[cust_id] = "Low-Value Buyer"

# --- 4. ADVANCED BUSINESS INSIGHTS ---
category_revenue = {}
for _, _, price, category in order_tuples:
    category_revenue[category] = category_revenue.get(category, 0.0) + price

unique_products_ordered = sorted(list({prod for _, prod, _, _ in order_tuples}))
electronics_buyers = sorted(list({cust for cust, _, _, cat in order_tuples if cat == "Electronics"}))
top_three = sorted(customer_spending.items(), key=lambda x: x[1], reverse=True)[:3]

# --- 5. ADVANCED SET OPERATIONS ---
customer_category_sets = {}
for cust_id, _, _, category in order_tuples:
    if cust_id not in customer_category_sets:
        customer_category_sets[cust_id] = set()
    customer_category_sets[cust_id].add(category)

multi_category_buyers = sorted([c for c, cats in customer_category_sets.items() if len(cats) > 1])
clothing_buyers = {cust for cust, _, _, cat in order_tuples if cat == "Clothing"}
elec_buyers_set = set(electronics_buyers)
both_elec_and_cloth = sorted(list(elec_buyers_set.intersection(clothing_buyers)))

# --- 6. WRITE REPORT OUT TO SUMMARY FILE ---
with open(output_summary_path, mode="w", encoding="utf-8") as out:
    out.write("=========================================================\n")
    out.write("             BUSINESS SUMMARY ANALYTICS REPORT           \n")
    out.write("=========================================================\n\n")
    
    out.write("1. PRODUCT CHANNEL CLASSIFICATIONS\n")
    out.write(f" - Active Categories: {', '.join(unique_categories)}\n")
    out.write(f" - Evaluated Unique SKUs: {len(unique_products_ordered)} items\n\n")
    
    out.write("2. ACCOUNT ACCOUNT SEGMENTATION SUMMARY\n")
    for cust, spend in sorted(customer_spending.items()):
        out.write(f" - Account: {cust} | Revenue: ${spend:,.2f} | Tag: {customer_classification[cust]}\n")
    
    out.write("\n3. SECTOR FINANCIAL REVENUE TRACKING\n")
    for cat, rev in category_revenue.items():
        out.write(f" - {cat} Total Pipeline Volume: ${rev:,.2f}\n")
        
    out.write("\n4. TOP PERFORMING CONSUMERS\n")
    for idx, (cust, spend) in enumerate(top_three, 1):
        out.write(f"   {idx}. Account ID: {cust} (Total Volume: ${spend:,.2f})\n")
        
    out.write("\n5. BEHAVIORAL INTERSECTION METRICS\n")
    out.write(f" - Diversified Category Shoppers (>1 Category): {', '.join(multi_category_buyers)}\n")
    out.write(f" - Core Overlap Shoppers (Electronics AND Clothing): {', '.join(both_elec_and_cloth) if both_elec_and_cloth else 'None'}\n")

print(f"Summary Report generated and saved successfully to:\n{output_summary_path}")