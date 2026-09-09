import streamlit as st
import pandas as pd
import plotly.express as px
import os
from dotenv import load_dotenv
from google import genai

# -----------------------------
# Load API key from .env
# -----------------------------

from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


# -----------------------------
# Page setup
# -----------------------------

st.set_page_config(
    page_title="Business Waste Detective",
    page_icon="🔎",
    layout="wide"
)


# -----------------------------
# Load cleaned data
# -----------------------------

@st.cache_data
def load_data():

    customers = pd.read_csv("customers_clean.csv")
    products = pd.read_csv("products_clean.csv")
    orders = pd.read_csv("orders_clean.csv")
    returns = pd.read_csv("returns_clean.csv")
    inventory = pd.read_csv("inventory_clean.csv")

    return customers, products, orders, returns, inventory


customers, products, orders, returns, inventory = load_data()


# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.title("🔎 Business Waste Detective")

investigation = st.sidebar.selectbox(
    "Select Investigation",
    [
        "Discount Waste",
        "Return Waste",
        "Shipping Waste",
        "Inventory Waste",
        "Profit Leakage"
    ]
)

category = st.sidebar.selectbox(
    "Category",
    ["All"] + sorted(products["Category"].dropna().unique())
)

region = st.sidebar.selectbox(
    "Region",
    ["All"] + sorted(customers["Region"].dropna().unique())
)


# -----------------------------
# Filter orders
# -----------------------------

filtered_orders = orders.copy()

if category != "All":
    filtered_orders = filtered_orders[
        filtered_orders["Category"] == category
    ]

if region != "All":
    filtered_orders = filtered_orders[
        filtered_orders["Region"] == region
    ]


# -----------------------------
# Title
# -----------------------------

st.title("🔎 Business Waste Detective")

st.write(
    "Identify where the business is losing money and understand why."
)

st.divider()


# -----------------------------
# KPIs
# -----------------------------

revenue = filtered_orders["Revenue"].sum()
profit = filtered_orders["Profit"].sum()
orders_count = filtered_orders["OrderID"].nunique()
shipping = filtered_orders["ShippingCost"].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Revenue", f"₹{revenue:,.0f}")
col2.metric("Profit", f"₹{profit:,.0f}")
col3.metric("Orders", f"{orders_count:,}")
col4.metric("Shipping Cost", f"₹{shipping:,.0f}")


st.divider()


# =====================================================
# DISCOUNT WASTE
# =====================================================

if investigation == "Discount Waste":

    st.header("🏷️ Discount Waste")

    discount_amount = (
        filtered_orders["Revenue"] *
        filtered_orders["Discount"]
    ).sum()

    st.metric(
        "Estimated Discount Amount",
        f"₹{discount_amount:,.0f}"
    )

    product_discount = (
        filtered_orders
        .groupby("ProductID")["Discount"]
        .mean()
        .reset_index()
        .sort_values("Discount", ascending=False)
        .head(10)
    )

    fig = px.bar(
        product_discount,
        x="ProductID",
        y="Discount",
        title="Top Products by Average Discount"
    )

    st.plotly_chart(fig, use_container_width=True)


# =====================================================
# RETURN WASTE
# =====================================================

elif investigation == "Return Waste":

    st.header("↩️ Return Waste")

    refund_amount = returns["RefundAmount"].sum()
    return_count = len(returns)

    col1, col2 = st.columns(2)

    col1.metric("Total Returns", f"{return_count:,}")
    col2.metric("Total Refunds", f"₹{refund_amount:,.0f}")

    reason_data = (
        returns["ReturnReason"]
        .value_counts()
        .reset_index()
    )

    reason_data.columns = ["Return Reason", "Returns"]

    fig = px.bar(
        reason_data,
        x="Return Reason",
        y="Returns",
        title="Returns by Reason"
    )

    st.plotly_chart(fig, use_container_width=True)


# =====================================================
# SHIPPING WASTE
# =====================================================

elif investigation == "Shipping Waste":

    st.header("🚚 Shipping Waste")

    region_shipping = (
        filtered_orders
        .groupby("Region")["ShippingCost"]
        .sum()
        .reset_index()
        .sort_values("ShippingCost", ascending=False)
    )

    fig = px.bar(
        region_shipping,
        x="Region",
        y="ShippingCost",
        title="Shipping Cost by Region"
    )

    st.plotly_chart(fig, use_container_width=True)


# =====================================================
# INVENTORY WASTE
# =====================================================

elif investigation == "Inventory Waste":

    st.header("📦 Inventory Waste")

    inventory_summary = (
        inventory
        .groupby("ProductID")
        .agg(
            StockReceived=("StockReceived", "sum"),
            StockSold=("StockSold", "sum"),
            ClosingStock=("ClosingStock", "last")
        )
        .reset_index()
    )

    inventory_summary["SellThroughRate"] = (
        inventory_summary["StockSold"] /
        inventory_summary["StockReceived"].replace(0, 1)
    )

    slow_products = (
        inventory_summary
        .sort_values("SellThroughRate")
        .head(10)
    )

    fig = px.bar(
        slow_products,
        x="ProductID",
        y="ClosingStock",
        title="Products with Low Sell-Through"
    )

    st.plotly_chart(fig, use_container_width=True)


# =====================================================
# PROFIT LEAKAGE
# =====================================================

elif investigation == "Profit Leakage":

    st.header("📉 Profit Leakage")

    category_profit = (
        filtered_orders
        .groupby("Category")
        .agg(
            Revenue=("Revenue", "sum"),
            Profit=("Profit", "sum")
        )
        .reset_index()
    )

    category_profit["ProfitMargin"] = (
        category_profit["Profit"] /
        category_profit["Revenue"] * 100
    )

    fig = px.bar(
        category_profit,
        x="Category",
        y="Profit",
        title="Profit by Category"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        category_profit.sort_values("ProfitMargin"),
        use_container_width=True
    )


# =====================================================
# AI BUSINESS ADVISOR
# =====================================================

st.divider()

st.header("🤖 AI Business Advisor")

st.write(
    "Get an AI-generated explanation and recommended action "
    "based on the business findings above."
)

if st.button("✨ Generate Recommendation"):

    if not api_key:

        st.error("OPENAI_API_KEY was not found in your .env file.")

    else:

        findings = f""" 
Investigation: {investigation} 
 
Category filter: {category} 
 
Region filter: {region} 
 
Revenue: ₹{revenue:,.0f} 
 
Profit: ₹{profit:,.0f} 
 
Orders: {orders_count:,} 
 
Shipping Cost: ₹{shipping:,.0f} 
""" 
 
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=f"""
You are a business analyst helping a retail manager.

Look at the business findings provided.

Give:
1. Main finding
2. Why it matters
3. What the manager should investigate
4. One practical recommendation

Do not invent numbers.
Keep the answer short and easy to understand.

Business findings:
{findings}
"""
        )

        st.success("AI Recommendation")

        st.write(response.text)
