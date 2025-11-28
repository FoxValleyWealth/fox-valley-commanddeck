import streamlit as st
import pandas as pd
import os
from modules.zacks_engine import load_zacks_screens
from modules.profit_risk_analyzer import calculate_profit_and_risk, apply_tactical_flags
from modules.portfolio_engine import load_portfolio

st.set_page_config(page_title="Fox Valley Tactical Command Deck", layout="wide")

# === HEADER ===
st.title("🧭 Fox Valley Tactical Command Deck — v7.7R")
st.caption("🚀 Live Tactical Intelligence | Zacks Synergy | Profit + Risk Analyzer")

# === LOAD PORTFOLIO SAFELY ===
portfolio = load_portfolio()

if portfolio is None or portfolio.empty:
    st.warning("⚠ No valid portfolio file detected in /data.")
else:
    # AUTO-DETECT TICKER COLUMN
    ticker_col = None
    for col in portfolio.columns:
        if col.strip().lower() in ["ticker", "symbol", "ticker symbol", "tickersymbol"]:
            ticker_col = col
            break

    if ticker_col is None:
        st.error("❌ Portfolio missing Ticker/Symbol column. Cannot continue.")
    else:
        portfolio["Ticker"] = portfolio[ticker_col].astype(str).str.upper().str.strip()

        # === PORTFOLIO OVERVIEW ===
        st.subheader("📊 Portfolio Overview")
        st.write(f"🗂 Total Holdings: {len(portfolio)}")

        # === PROFIT & RISK ANALYSIS ===
        portfolio = calculate_profit_and_risk(portfolio)
        portfolio = apply_tactical_flags(portfolio)

        # === ZACKS SCREEN LOADING ===
        st.subheader("📥 Zacks Screening Files Loaded")
        zacks_screens = load_zacks_screens()
        
        if zacks_screens:
            st.write(f"📂 {len(zacks_screens)} Screening Files Detected")
            for name in zacks_screens.keys():
                st.write(f"📄 {name}")
        else:
            st.warning("⚠ No Zacks screening files found in /data.")

        # === TACTICAL ACTION GRID (Phase 2) ===
        st.subheader("🎯 Tactical Action Grid — Phase 2 Deployment")

        action_grid = portfolio[[
            "Ticker",
            "Profit %",
            "Risk Category",
            "Tactical Action"
        ]]

        def highlight_action(val):
            if val == "Trim / Lock Profits":
                return "background-color: #FFD700;"
            elif val == "Buy / Accumulate":
                return "background-color: #90EE90;"
            elif val == "Hold / Monitor":
                return "background-color: #ADD8E6;"
            return ""

        st.dataframe(
            action_grid.style.applymap(highlight_action, subset=["Tactical Action"]),
            use_container_width=True
        )

        st.success("🧮 Tactical Action Grid Rendered Successfully — Command Ready")

# === FOOTER ===
st.markdown("---")
st.caption("Fox Valley Intelligence Engine — Built for Precision Tactical Execution")
