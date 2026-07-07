import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------

st.set_page_config(
    page_title="InventoryAI Pro",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------
# LOAD CSS
# ------------------------------------------------

with open("assets/theme.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ------------------------------------------------
# HEADER
# ------------------------------------------------

st.title("📦 InventoryAI Pro")

st.caption(
    "AI-Powered Retail Analytics & Demand Forecasting Platform"
)


# ------------------------------------------------
# Helper Functions
# ------------------------------------------------
def format_currency(number,symbol="$"):

    if number>=1_000_000_000:
        return f"{symbol}{number/1e9:.1f}B"

    elif number>=1_000_000:
        return f"{symbol}{number/1e6:.1f}M"

    elif number>=1000:
        return f"{symbol}{number/1000:.1f}K"

    return f"{symbol}{number:.0f}"


def guess_column(columns,keywords):

    for c in columns:

        name=c.lower()

        for k in keywords:

            if k in name:
                return c

    return None

# ------------------------------------------------
# Upload Dataset
# ------------------------------------------------
st.markdown("---")

uploaded_file=st.file_uploader(
    "Upload Inventory Dataset",
    type=["csv"]
)

if uploaded_file is None:

    st.info("Upload a CSV dataset.")

    st.stop()

df=pd.read_csv(uploaded_file)

df.columns=df.columns.str.strip()


# ------------------------------------------------
# Dataset Preview
# ------------------------------------------------
st.subheader("Dataset Preview")

st.dataframe(df.head())


# ------------------------------------------------
# Dynamic Column Dectection
# ------------------------------------------------
product_guess=guess_column(df.columns,["product"])

category_guess=guess_column(df.columns,["category"])

region_guess=guess_column(df.columns,["region"])

inventory_guess=guess_column(df.columns,
["inventory"])

sales_guess=guess_column(df.columns,
["units sold","sales"])

forecast_guess=guess_column(df.columns,
["forecast","demand"])

price_guess=guess_column(df.columns,
["price"])

store_guess=guess_column(df.columns,
["store"])

date_guess=guess_column(df.columns,
["date"])


# ------------------------------------------------
# Column Mapping
# ------------------------------------------------

st.subheader("Column Mapping")

c1,c2,c3=st.columns(3)

with c1:

    product_col=st.selectbox(
        "Product",
        df.columns,
        index=df.columns.get_loc(product_guess)
        if product_guess else 0
    )

    category_col=st.selectbox(
        "Category",
        df.columns,
        index=df.columns.get_loc(category_guess)
        if category_guess else 0
    )

with c2:

    inventory_col=st.selectbox(
        "Inventory",
        df.columns,
        index=df.columns.get_loc(inventory_guess)
        if inventory_guess else 0
    )

    sales_col=st.selectbox(
        "Sales",
        df.columns,
        index=df.columns.get_loc(sales_guess)
        if sales_guess else 0
    )

with c3:

    forecast_col=st.selectbox(
        "Forecast",
        df.columns,
        index=df.columns.get_loc(forecast_guess)
        if forecast_guess else 0
    )

    price_col=st.selectbox(
        "Price",
        df.columns,
        index=df.columns.get_loc(price_guess)
        if price_guess else 0
    )