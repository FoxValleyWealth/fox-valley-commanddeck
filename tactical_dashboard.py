import streamlit as st
import pandas as pd
from modules.portfolio_engine import load_portfolio_data
from modules.zacks_engine import load_zacks_screens

st.set_page_config(page_title="Fox Valley Tactical Command Deck", layout="wide")

# === HEADER ===
st.title("🧭 Fox Valley Tactical Command Deck — v7.7R")
st.subheader("🚀 Live Tactical Intelligence | Zacks Synergy | Portfolio Insights")

# === LOAD DATA ===
portfolio = load_portfolio_data()
zacks_files = load_zacks_screens()

# === ZACKS FILE DISPLAY ===
st.markdown("### 📥 Zacks Screening Files Loaded")
if zacks_files:
    st.success(f"📂 {len(zacks_files)} Screening Files Detected")
    for file_name in zacks_files:
        st.markdown(f"📄 {file_name}")
else:
    st.warning("⚠ No valid Zacks screening files detected in /data")

# === PORTFOLIO SECTION ===
st.markdown("---")
st.markdown("### 📊 Portfolio Overview")

if portfolio is None or portfolio.empty:
    st.error("⚠ No valid portfolio data found. Please verify your Portfolio file in /data.")
else:
    st.success("📂 Portfolio Loaded Successfully")

    # Display clean portfolio summary
    columns_to_show = ["Ticker", "Quantity", "Current Value", "Cost Basis Per Share", 
                       "Last Price", "Total Gain/Loss Dollar", "Total Gain/Loss Percent"]

    available_columns = [col for col in columns_to_show if col in portfolio.columns]
    st.dataframe(portfolio[available_columns], use_container_width=True)

    total_value = portfolio["Current Value"].replace('[\$,]', '', regex=True).astype(float).sum()
    st.metric("💰 Total Portfolio Value", f"${total_value:,.2f}")

    st.markdown("---")
    st.markdown("### 💹 Tactical Action Grid (Preview Mode)")
    st.info("Tactical Action Grid will activate once full Profit & Risk Engine is stable.")

# === FOOTER ===
st.markdown("---")
st.caption("Fox Valley Intelligence Engine — Built for Precision Tactical Execution")
