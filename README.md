# 🔍 Business Waste Detective

An AI-powered retail analytics dashboard that helps identify where a business is losing money and provides actionable recommendations using the Gemini API.

## 🎯 Business Problem

Retail businesses can generate high sales but still lose money because of excessive discounts, product returns, high shipping costs, unsold inventory, and low-profit products.

This project investigates five major areas of business waste:

- 💸 Discount Waste
- ↩️ Return Waste
- 🚚 Shipping Waste
- 📦 Inventory Waste
- 📉 Profit Leakage

Users can filter the analysis by **Category** and **Region**.

## 📊 Dashboard Features

- Interactive KPI cards
- Category and Region filters
- Discount Waste analysis
- Return Waste analysis
- Shipping Waste analysis
- Inventory Waste analysis
- Profit Leakage analysis
- Interactive charts using Plotly
- 🤖 AI Business Advisor powered by Gemini

## 🛠️ Technologies Used

- Python
- Pandas
- Plotly
- Streamlit
- Gemini API

## 📁 Dataset

The project uses five retail datasets:

- Customers
- Products
- Orders
- Returns
- Inventory

The raw datasets were cleaned and prepared using Pandas before being used in the dashboard.

## 📂 Project Structure

Business Waste Detective/
│
├── Data/
│   ├── customers_clean.csv
│   ├── products_clean.csv
│   ├── orders_clean.csv
│   ├── returns_clean.csv
│   └── inventory_clean.csv
│
├── app.py
├── data_cleaning.ipynb
├── requirements.txt
├── .gitignore
└── README.md

## 🤖 AI Business Advisor

The dashboard sends the calculated business findings to the Gemini API.

The AI provides:

1. Main finding
2. Why it matters
3. What the manager should investigate
4. One practical recommendation

The AI does not calculate the business metrics. The calculations are performed by the application and Gemini is used to explain the findings and provide recommendations.

## 🚀 Run the Project Locally

Install the required libraries:

```bash
pip install -r requirements.txt