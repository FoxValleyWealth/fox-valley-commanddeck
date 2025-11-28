import streamlit as st
import pandas as pd
from fox_valley_intelligence_engine import (
    load_portfolio,
    load_zacks_screens,
    evaluate_profit_risk
)

# === PAGE CONFIG ===
st.set_page_config(
    page_title="Fox Valley Tactical Command Deck",
    page_icon="🧭",
    layout="wide"
)

st.title("🧭 Fox Valley Tactical Command Deck — v7.7R")
st.caption("🚀 Live Tactical Intelligence | Zacks Synergy | Profit + Risk Analyzer")


# === LOAD PORTFOLIO ===
portfolio = load_portfolio()  # <-- Correct function execution

# Validate portfolio safely
if portfolio is None or not isinstance(portfolio, pd.DataFrame) or portfolio.empty:
    st.warning("⚠ No valid portfolio data found. Upload or verify your portfolio file.")
else:
    portfolio["Ticker"] = portfolio["Ticker"].str.upper()
    st.subheader("📊 Portfolio Overview")
    st.dataframe(portfolio)


# === LOAD ZACKS FILES ===
zacks_files = load_zacks_screens()
st.subheader("📥 Zacks Screening Files Loaded")
st.write(f"📂 {len(zacks_files)} Screening Files Detected")

for file_name in zacks_files:
    st.write(f"📄 {file_name}")


# === PROFIT & RISK ANALYSIS ===
if portfolio is not None and isinstance(portfolio, pd.DataFrame) and not portfolio.empty:
    st.subheader("💹 Tactical Profit & Risk Analysis")

    profit_risk_df = evaluate_profit_risk(portfolio)

    # Display essential tactical data
    st.dataframe(
        profit_risk_df[
            ["Ticker", "Profit %", "Risk Category", "Tactical Action"]
        ]
    )

    # Tactical Action Grid (Phase 2 core)
    st.subheader("🎯 Tactical Action Grid")
    st.dataframe(
        profit_risk_df[
            ["Ticker", "Quantity", "Profit %", "Risk Category", "Tactical Action"]
        ]
    )

else:
    st.info("💡 Portfolio required to activate Tactical Action Grid.")


st.write("---")
st.caption("Fox Valley Intelligence Engine — Built for Precision Tactical Execution")
