import streamlit as st
import pandas as pd
from fox_valley_intelligence_engine import (
    load_portfolio,
    load_zacks_files,
    crossmatch_with_zacks,
    run_profit_risk_analyzer
)

# =======================
# PAGE CONFIGURATION
# =======================
st.set_page_config(page_title="Fox Valley Tactical Command Deck", layout="wide")

st.title("🧭 Fox Valley Tactical Command Deck — v7.6R")
st.markdown("🚀 Live Tactical Intelligence | Zacks Synergy | Profit + Risk Analyzer")

# =======================
# LOAD DATA
# =======================
portfolio_df = load_portfolio()
zacks_files = load_zacks_files()

# =======================
# PORTFOLIO DISPLAY
# =======================
if portfolio_df is not None:
    st.subheader("📊 Portfolio Overview")
    st.dataframe(portfolio_df, use_container_width=True)

# =======================
# ZACKS FILE LOADING STATUS
# =======================
if zacks_files:
    st.subheader("📥 Zacks Screening Files Loaded")
    st.success(f"📂 {len(zacks_files)} Screening Files Detected")

    # Display each Zacks file separately with highlighting
    for category, df in zacks_files.items():
        st.markdown(f"### 📄 {category} Screen")
        if "Zacks Rank" in df.columns:
            df["🚨 Rank"] = df["Zacks Rank"].apply(lambda x: "⭐" if int(x) == 1 else "")
            st.dataframe(df[["Ticker", "Company Name", "Zacks Rank", "🚨 Rank"]].head(20), use_container_width=True)
        else:
            st.warning(f"⚠ 'Zacks Rank' column missing in {category}")

# =======================
# EXECUTE CROSSMATCH
# =======================
if st.button("🔍 Execute Tactical Crossmatch — Actionable Orders"):
    result = crossmatch_with_zacks(portfolio_df, zacks_files)
    if result is not None:
        st.subheader("🛡 Tactical Intelligence Output — Live Orders")
        st.dataframe(result, use_container_width=True)

# =======================
# PROFIT + RISK ANALYZER
# =======================
if st.button("💹 Run Profit & Risk Analyzer"):
    run_profit_risk_analyzer()
    st.success("📁 Profit & Risk Report Generated — Check Root Folder")

# =======================
# FOOTER
# =======================
st.markdown("---")
st.caption("Fox Valley Intelligence Engine — Built for Precision Tactical Execution")
