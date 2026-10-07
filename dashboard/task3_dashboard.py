import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# ==========================================
# 1. LOAD YOUR REAL DATA
# ==========================================

file_path = "data/superstore_cleaned.csv"

df = pd.read_csv(file_path)

df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")

print("Dataset loaded successfully!")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])


# ==========================================
# 2. CALCULATE KPIs
# ==========================================

total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_orders = df["Order ID"].nunique()
total_customers = df["Customer ID"].nunique()


# ==========================================
# 3. PREPARE DATA FOR CHARTS
# ==========================================

monthly_sales = (
    df.dropna(subset=["Order Date"])
      .groupby(df["Order Date"].dt.to_period("M"))["Sales"]
      .sum()
      .reset_index()
)

monthly_sales["Order Date"] = monthly_sales["Order Date"].astype(str)


category_sales = (
    df.groupby("Category")["Sales"]
      .sum()
      .reset_index()
)


category_profit = (
    df.groupby("Category")["Profit"]
      .sum()
      .reset_index()
)


region_sales = (
    df.groupby("Region")["Sales"]
      .sum()
      .reset_index()
)


top_products = (
    df.groupby("Product Name")["Sales"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
      .sort_values()
      .reset_index()
)


segment_sales = (
    df.groupby("Segment")["Sales"]
      .sum()
      .reset_index()
)


# ==========================================
# 4. CREATE DASHBOARD
# ==========================================

fig = make_subplots(
    rows=4,
    cols=2,

    subplot_titles=(
        "Monthly Sales Trend",
        "Sales by Category",
        "Sales by Region",
        "Top 10 Products by Sales",
        "Profit by Category",
        "Sales by Customer Segment",
        "Sales by Ship Mode",
        "Profit Trend"
    ),

    specs=[
        [{"type": "xy"}, {"type": "xy"}],
        [{"type": "domain"}, {"type": "xy"}],
        [{"type": "xy"}, {"type": "xy"}],
        [{"type": "xy"}, {"type": "xy"}]
    ]
)


# ==========================================
# 5. MONTHLY SALES
# ==========================================

fig.add_trace(
    go.Scatter(
        x=monthly_sales["Order Date"],
        y=monthly_sales["Sales"],
        mode="lines+markers",
        name="Monthly Sales"
    ),
    row=1,
    col=1
)


# ==========================================
# 6. SALES BY CATEGORY
# ==========================================

fig.add_trace(
    go.Bar(
        x=category_sales["Category"],
        y=category_sales["Sales"],
        name="Category Sales"
    ),
    row=1,
    col=2
)


# ==========================================
# 7. SALES BY REGION
# ==========================================

fig.add_trace(
    go.Pie(
        labels=region_sales["Region"],
        values=region_sales["Sales"],
        name="Region Sales"
    ),
    row=2,
    col=1
)


# ==========================================
# 8. TOP 10 PRODUCTS
# ==========================================

fig.add_trace(
    go.Bar(
        x=top_products["Sales"],
        y=top_products["Product Name"],
        orientation="h",
        name="Top Products"
    ),
    row=2,
    col=2
)


# ==========================================
# 9. PROFIT BY CATEGORY
# ==========================================

fig.add_trace(
    go.Bar(
        x=category_profit["Category"],
        y=category_profit["Profit"],
        name="Category Profit"
    ),
    row=3,
    col=1
)


# ==========================================
# 10. SALES BY SEGMENT
# ==========================================

fig.add_trace(
    go.Bar(
        x=segment_sales["Segment"],
        y=segment_sales["Sales"],
        name="Segment Sales"
    ),
    row=3,
    col=2
)


# ==========================================
# 11. SALES BY SHIP MODE
# ==========================================

ship_mode_sales = (
    df.groupby("Ship Mode")["Sales"]
      .sum()
      .reset_index()
)

fig.add_trace(
    go.Bar(
        x=ship_mode_sales["Ship Mode"],
        y=ship_mode_sales["Sales"],
        name="Ship Mode Sales"
    ),
    row=4,
    col=1
)


# ==========================================
# 12. PROFIT TREND
# ==========================================

monthly_profit = (
    df.dropna(subset=["Order Date"])
      .groupby(df["Order Date"].dt.to_period("M"))["Profit"]
      .sum()
      .reset_index()
)

monthly_profit["Order Date"] = monthly_profit["Order Date"].astype(str)

fig.add_trace(
    go.Scatter(
        x=monthly_profit["Order Date"],
        y=monthly_profit["Profit"],
        mode="lines+markers",
        name="Monthly Profit"
    ),
    row=4,
    col=2
)


# ==========================================
# 13. DASHBOARD STYLE
# ==========================================

fig.update_layout(
    title={
        "text": "Superstore Sales & Profit Dashboard",
        "x": 0.5
    },

    height=1500,

    template="plotly_white",

    showlegend=False
)


# ==========================================
# 14. SAVE DASHBOARD
# ==========================================

output_folder = "."

os.makedirs(output_folder, exist_ok=True)

output_file = os.path.join(
    output_folder,
    "sales_profit_dashboard.html"
)

fig.write_html(
    output_file,
    include_plotlyjs=True
)

print()
print("======================================")
print("TASK 3 DASHBOARD CREATED SUCCESSFULLY")
print("======================================")
print("Total Sales:", round(total_sales, 2))
print("Total Profit:", round(total_profit, 2))
print("Total Orders:", total_orders)
print("Total Customers:", total_customers)
print()
print("Dashboard saved to:")
print(output_file)