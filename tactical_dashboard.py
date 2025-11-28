import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Fox Valley Tactical Command Deck", layout="wide")

# === HEADER ===
st.title("🧭 Fox Valley Tactical Command Deck — v7.7R")
st.subheader("🚀 Live Tactical Intelligence | Zacks Synergy | Portfolio Insights")

# === DIRECT PORTFOLIO LOADER (No module import) ===
def load_portfolio_direct():
    try:
        files = [f for f in os.listdir("data") if f.startswith("Portfolio_Positions") and f.endswith(".csv")]
        if not files:
            return None
        latest_file = sorted(files)[-1]
        df = pd.read_csv(os.path.join("data", latest_file))
        return df
    except Exception:
        return None

# === SIMPLE ZACKS SCREEN DETECTOR (No module import) ===
def load_zacks_screens_simple():
    try:
        files = [f for f in os.listdir("data") if f.startswith("zacks") or "Growth" in f or "Defensive" in f]
        return files
    except Exception:
        return []

# === FETCH DATA ===
portfolio = load_portfolio_direct()
zacks_files = load_zacks_screens_simple()

# === ZACKS FILE DISPLAY ===
st.markdown("### 📥 Zacks Screening Files Loaded")
if zacks_files:
    st.success(f"📂 {len(zacks_files)} Screening Files Detected")
    for file_name in zacks_files:
        st.markdown(f"📄 {file_name}")
else:
    st.warning("⚠ No valid Zacks screening files detected in /data")

st.markdown("---")

# === PORTFOLIO SECTION ===
st.markdown("### 📊 Portfolio Overview")

if portfolio is None or portfolio.empty:
    st.error("⚠ No valid portfolio data found. Check /data folder.")
else:
    st.success("📂 Portfolio Loaded Successfully")

    display_columns = ["Symbol", "Quantity", "Current Value", "Last Price", "Total Gain/Loss Dollar", "Total Gain/Loss Percent"]
    available_cols = [c for c in display_columns if c in portfolio.columns]

    st.dataframe(portfolio[available_cols], use_container_width=True)

    total_value = pd.to_numeric(portfolio["Current Value"].replace('[\$,]', '', regex=True), errors='coerce').sum()
    st.metric("💰 Total Portfolio Value", f"${total_value:,.2f}")

st.markdown("---")
st.caption("Fox Valley Intelligence Engine — Stabilized Tactical Core v7.7R")
