import streamlit as st
import pandas as pd
import glob
from fox_valley_intelligence_engine import (
    load_portfolio,
    load_zacks_files,
    crossmatch_with_zacks,
    run_profit_risk_analyzer
)

st.set_page_config(page_title="Tactical Command Deck", layout="wide")

st.title("🧭 Fox Valley Tactical Command Deck — v7.5R")
st.markdown("🚀 Live Tactical Intelligence | Zacks Synergy | Profit + Risk Analyzer")

portfolio_df = load_portfolio()
zacks_files = load_zacks_files()

if portfolio_df is not None:
    st.subheader("📊 Portfolio Overview")
    st.dataframe(portfolio_df.head(20))

if zacks_files:
    st.subheader("📥 Zacks Screening Files Loaded")
    st.success(f"{len(zacks_files)} Zacks Files Loaded")

if st.button("🔍 Execute Tactical Crossmatch"):
    result = crossmatch_with_zacks(portfolio_df, zacks_files)
    if result is not None:
        st.subheader("🛡 Tactical Intelligence Output")
        st.dataframe(result)

if st.button("💹 Run Profit & Risk Analyzer"):
    run_profit_risk_analyzer()
    st.success("📁 Reports Generated (CSV + PDF) — Check Repo Folder")
