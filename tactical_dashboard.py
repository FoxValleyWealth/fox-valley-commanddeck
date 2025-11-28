import streamlit as st
import pandas as pd

# Correct imports — only from real, existing functions
from modules.portfolio_engine import load_portfolio
from modules.zacks_engine import load_zacks_screens
from modules.profit_risk_analyzer import (
    calculate_profit_and_risk,
    apply_tactical_flags
)

# === PAGE CONFIG ===
st.set_page_config(page_title="Fox Valley Tactical Command Deck", page_icon="🧭", layout="wide")

st.title("🧭 Fox Valley Tactical Command Deck — v7.7R")
st.caption("🚀 Live Tactical Intelligence | Zacks Synergy | Profit + Risk Analyzer")


# === LOAD PORTFOLIO ===
portfolio = load_portfolio()

if isinstance(portfolio, pd.DataFrame) and not portfolio.empty:
    portfolio["Ticker"] = portfolio["Ticker"].astype(str).str.upper()
    st.subheader("📊 Portfolio Overview")
    st.dataframe(portfolio)
else:
    st.warning("⚠ No valid portfolio data found. Upload or verify your Portfolio file.")


# === LOAD ZACKS FILES ===
zacks_files = load_zacks_screens()
st.subheader("📥 Zacks Screening Files Loaded")
st.write(f"📂 {len(zacks_files)} Screening Files Detected")

for name in zacks_files:
    st.write(f"📄 {name}")


# === PROFIT & RISK ANALYSIS ===
if isinstance(portfolio, pd.DataFrame) and not portfolio.empty:

    # Apply profit & risk logic safely
    st.subheader("💹 Tactical Profit & Risk Analysis")

    df = calculate_profit_and_risk(portfolio)
    df = apply_tactical_flags(df)

    st.dataframe(
        df[["Ticker", "Profit %", "Risk Category", "Tactical Action"]]
    )

    st.subheader("🎯 Tactical Action Grid")
    st.dataframe(
        df[["Ticker", "Quantity", "Profit %", "Risk Category", "Tactical Action"]]
    )

else:
    st.info("💡 Portfolio required to activate Tactical Action Grid.")


# === FOOTER ===
st.write("---")
st.caption("Fox Valley Intelligence Engine — Built for Precision Tactical Execution")
