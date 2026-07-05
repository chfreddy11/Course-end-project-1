# To generate a beautiful PDF directly from Python, you can use ReportLab.
# ReportLab is the industry standard for creating standalone PDF documents without
# needing external web dependencies like Chrome or HTML engines.
#
# Install ReportLab using:
# pip install reportlab

import csv
import os
import random

# ReportLab libraries for PDF generation
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

# ==========================================
# 1. SETUP & PATH CONFIGURATION
# ==========================================
folder_path = r"C:\Users\Chris\OneDrive\Desktop\VT AGI\Python refresher\Assessments\Course end project 1"
csv_file_name = "customer_purchases.csv"
report_file_name = "Analytics_Summary_Report.txt"
pdf_file_name = "Analytics_Summary_Report.pdf"

csv_full_path = os.path.join(folder_path, csv_file_name)
report_full_path = os.path.join(folder_path, report_file_name)
pdf_full_path = os.path.join(folder_path, pdf_file_name)

# Ensure the destination directory exists
os.makedirs(folder_path, exist_ok=True)


# ==========================================
# 2. DATA GENERATION STAGE
# ==========================================
products_pool = {
    "Electronics": ["Smartphone", "Laptop", "Headphones", "Smartwatch", "Tablet"],
    "Home Goods": ["Blender", "Coffee Maker", "Desk Lamp", "Air Purifier", "Vacuum"],
    "Clothing": ["Jacket", "Sneakers", "Jeans", "Sweater", "T-Shirt"],
}

generated_rows = []

# Generate 10 unique customer IDs
for i in range(1, 11):
    customer_id = f"CUST{1000 + i}"

    # Gather all product pairs
    all_available_products = []
    for category, products in products_pool.items():
        for product in products:
            all_available_products.append((category, product))

    # Pick 4 random unique product-category pairs for this customer
    customer_purchases = random.sample(all_available_products, 4)

    for category, product in customer_purchases:
        # Lowered minimum to $5 to ensure some total orders land in the Low/Moderate tiers
        cost = round(random.uniform(5, 1500), 2)
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

# Write to CSV
headers = ["Customer ID", "Category", "Product", "Cost", "Profit Margin", "Profit"]
with open(csv_full_path, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    writer.writerows(generated_rows)

print(f"--> Success: New data generated and written to {csv_file_name}")


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
        price = float(row["Cost"].replace("$", "").replace(",", ""))

        customer_names.add(cust_id)
        order_tuples.append((cust_id, product, price, category))

        if cust_id not in customer_orders_dict:
            customer_orders_dict[cust_id] = []
        customer_orders_dict[cust_id].append(product)


# ==========================================
# 4. DATA PROCESSING & ANALYSIS STAGE
# ==========================================
unique_categories = sorted(list({cat for _, _, _, cat in order_tuples}))
unique_products_ordered = sorted(list({prod for _, prod, _, _ in order_tuples}))

# Calculate Total Spending per Customer
customer_spending = {}
for cust_id, _, price, _ in order_tuples:
    customer_spending[cust_id] = customer_spending.get(cust_id, 0.0) + price

# Segment Customers (Original $50 and $100 boundaries)
customer_classification = {}
for cust_id, total_spent in customer_spending.items():
    if total_spent > 100:
        customer_classification[cust_id] = "High-Value Buyer"
    elif 50 <= total_spent <= 100:
        customer_classification[cust_id] = "Moderate Buyer"
    else:
        customer_classification[cust_id] = "Low-Value Buyer"

# Generate Revenue per Category
category_revenue = {}
for _, _, price, category in order_tuples:
    category_revenue[category] = category_revenue.get(category, 0.0) + price

# Find Electronics buyers using list comprehension
electronics_buyers = sorted(
    list({cust for cust, _, _, cat in order_tuples if cat == "Electronics"})
)

# Top 3 Spend accounts
top_three = sorted(customer_spending.items(), key=lambda x: x[1], reverse=True)[:3]

# Set Operations
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
# 5. TXT REPORT GENERATION STAGE
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

print(f"--> Success: Text report created at {report_file_name}")


# ==========================================
# 6. PDF SUMMARY REPORT GENERATION STAGE
# ==========================================
doc = SimpleDocTemplate(pdf_full_path, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
styles = getSampleStyleSheet()

# Custom styles for a polished look
title_style = ParagraphStyle(
    'DocTitle', parent=styles['Heading1'], fontSize=22, textColor=colors.HexColor('#1A365D'), spaceAfter=6, alignment=1
)
subtitle_style = ParagraphStyle(
    'DocSubTitle', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Oblique', textColor=colors.HexColor('#4A5568'), spaceAfter=20, alignment=1
)
h2_style = ParagraphStyle(
    'SectionHeading', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor('#2B6CB0'), spaceBefore=14, spaceAfter=8
)
body_style = ParagraphStyle(
    'BodyText', parent=styles['Normal'], fontSize=10.5, leading=14, spaceAfter=8
)
bullet_style = ParagraphStyle(
    'BulletText', parent=styles['Normal'], fontSize=10.5, leading=14, leftIndent=15, spaceAfter=4
)

story = []

# Title & Subtitle
story.append(Paragraph("Course End Project 1: Business Analytics Report", title_style))
story.append(Paragraph("Automated Data Generation and Behavioral Execution Summary", subtitle_style))

# Section 1
story.append(Paragraph("1. Product Channel Classifications", h2_style))
story.append(Paragraph(f"<b>Active Categories Explored:</b> {', '.join(unique_categories)}", body_style))
story.append(Paragraph(f"<b>Total Evaluated Unique SKUs:</b> {len(unique_products_ordered)} unique items found across categories.", body_style))

# Section 2: Customer Segmentation Table
story.append(Paragraph("2. Customer Segmentation Summary", h2_style))
story.append(Paragraph("Customers have been dynamically segmented based on total expenditures (Low-Value: &lt;$50 | Moderate-Value: $50-$100 | High-Value: &gt;$100):", body_style))

# Build Table Data
table_data = [["Customer ID", "Total Spend", "Classification Segment"]]
for cust, spend in sorted(customer_spending.items()):
    table_data.append([cust, f"${spend:,.2f}", customer_classification[cust]])