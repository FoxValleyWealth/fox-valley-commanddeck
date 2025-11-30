import streamlit as st
import pandas as pd

from modules.portfolio_engine import (
    load_portfolio_data,
    load_cash_position,
    calculate_summary,
    prepare_portfolio_export,
)
from modules.zacks_unified_analyzer import (
    merge_zacks_screens,
    extract_rank1_candidates,
    prepare_zacks_export,
)
from modules.trailing_stop_manager import (
    apply_trailing_stop,
    apply_custom_trailing_stops,
)
from modules.tactical_controls import process_tactical_action

# =========================================================
# 🧭 Fox Valley Tactical Command Deck — v7.7R
# Single-page stable dashboard using v7.7R modules
# =========================================================

st.set_page_config(
    page_title="Fox Valley Tactical Command Deck",
    layout="wide",
)

st.title("🧭 Fox Valley Tactical Command Deck — v7.7R Stable Core")

st.caption("Fox Valley Intelligence Engine — Portfolio | Zacks | Trailing Stops | Tactical Controls")

# =========================================================
# SIDEBAR — FILE INPUTS & CASH OVERRIDE
# =========================================================
st.sidebar.header("📂 Data Inputs")

portfolio_file = st.sidebar.file_uploader("Portfolio CSV", type=["csv"])

st.sidebar.markdown("---")
st.sidebar.subheader("📥 Zacks Screen Files")
growth1_file = st.sidebar.file_uploader("Growth 1 CSV", type=["csv"])
growth2_file = st.sidebar.file_uploader("Growth 2 CSV", type=["csv"])
dividend_file = st.sidebar.file_uploader("Defensive Dividends CSV", type=["csv"])

st.sidebar.markdown("---")
manual_cash = st.sidebar.number_input(
    "Manual Cash Override ($)",
    min_value=0.0,
    step=100.0,
    format="%.2f",
    help="Enter your actual cash available to trade from Fidelity. Overrides any file value.",
)

default_trailing_stop_pct = st.sidebar.slider(
    "Default Trailing Stop (%)",
    min_value=1,
    max_value=25,
    value=5,
    step=1,
)

st.sidebar.markdown("---")
st.sidebar.caption("Ensure CSV headers match: Ticker, Shares, Cost Basis, Current Price.")

# =========================================================
# MAIN LAYOUT
# =========================================================
col_portfolio, col_zacks = st.columns(2)

# ---------------------------------------------------------
# PORTFOLIO SECTION
# ---------------------------------------------------------
with col_portfolio:
    st.subheader("📊 Portfolio Overview")

    if portfolio_file:
        # Load portfolio
        portfolio_df = load_portfolio_data(portfolio_file)
        cash_value = load_cash_position(manual_cash)

        summary = calculate_summary(portfolio_df, cash_value)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Portfolio Value", f"${summary['total_value']:,}")
        c2.metric("Cash Available", f"${summary['cash']:,}")
        c3.metric("Total Gain/Loss", f"${summary['gain_loss_total']:,}")
        c4.metric("Avg Gain/Loss %", f"{summary['avg_gain_loss_pct']:.2f}%")

        st.markdown("#### Current Holdings")
        st.dataframe(portfolio_df, use_container_width=True)

        # Trailing stops
        st.markdown("#### Trailing Stop Protection (Default %)")
        ts_df = apply_trailing_stop(portfolio_df.copy(), trailing_stop_pct=default_trailing_stop_pct)
        st.dataframe(ts_df, use_container_width=True)

    else:
        st.info("Upload a **Portfolio CSV** in the sidebar to view holdings and trailing stops.")

# ---------------------------------------------------------
# ZACKS SECTION
# ---------------------------------------------------------
with col_zacks:
    st.subheader("🎯 Zacks Unified Candidates")

    if growth1_file or growth2_file or dividend_file:
        files_dict = {
            "Growth1": growth1_file,
            "Growth2": growth2_file,
            "Dividend": dividend_file,
        }
        zacks_df = merge_zacks_screens(files_dict)

        if not zacks_df.empty:
            st.markdown("#### Unified Zacks Screen Universe")
            st.dataframe(prepare_zacks_export(zacks_df), use_container_width=True)

            st.markdown("#### 🔥 Zacks Rank 1 Candidates (Highest Priority)")
            rank1_df = extract_rank1_candidates(zacks_df)
            if not rank1_df.empty:
                st.dataframe(prepare_zacks_export(rank1_df), use_container_width=True)
            else:
                st.info("No Zacks Rank 1 candidates found in uploaded screens.")
        else:
            st.warning("No valid Zacks data loaded. Check file formats and try again.")
    else:
        st.info("Upload at least one **Zacks CSV** (Growth1, Growth2, or Defensive Dividends) in the sidebar.")

# =========================================================
# TACTICAL CONTROLS
# =========================================================
st.markdown("---")
st.subheader("🛠 Tactical Action Controls (Simulation Only)")

c1, c2, c3, c4 = st.columns([1, 1, 1, 2])

with c1:
    action_type = st.selectbox("Action", ["BUY", "SELL", "TRIM", "HOLD"])

with c2:
    ticker = st.text_input("Ticker", placeholder="NVDA")

with c3:
    shares = st.number_input("Shares", min_value=0, step=1, value=0)

with c4:
    st.write("")
    st.write("")
    execute = st.button("Execute Tactical Action")

if execute:
    result = process_tactical_action(action_type, ticker, shares)
    st.success(result)

# =========================================================
# FOOTER
# =========================================================
st.markdown("---")
st.caption("🧭 Fox Valley Intelligence Engine — v7.7R | Command Deck Stable Core")
