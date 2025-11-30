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
from modules.tactical_scoring_engine import calculate_tactical_scores
from modules.intelligence_brief import generate_intelligence_brief

# =========================================================
# 🧭 Fox Valley Tactical Command Deck — v7.7R Final Integrated Build
# =========================================================

st.set_page_config(
    page_title="Fox Valley Tactical Command Deck",
    layout="wide",
)

st.title("🧭 Fox Valley Tactical Command Deck — v7.7R Stable Core")
st.caption("Fox Valley Intelligence Engine — Portfolio | Zacks | Scoring | Stops | Tactical Narrative")

# =========================================================
# SIDEBAR — FILE INPUTS & SETTINGS
# =========================================================
st.sidebar.header("📂 Data Inputs")

portfolio_file = st.sidebar.file_uploader("Portfolio CSV", type=["csv"])

st.sidebar.subheader("📥 Zacks Screen Files")
growth1_file = st.sidebar.file_uploader("Growth 1 CSV", type=["csv"])
growth2_file = st.sidebar.file_uploader("Growth 2 CSV", type=["csv"])
dividend_file = st.sidebar.file_uploader("Defensive Dividends CSV", type=["csv"])

manual_cash = st.sidebar.number_input(
    "Manual Cash Override ($)",
    min_value=0.0,
    step=100.0,
    format="%.2f",
)

default_trailing_stop_pct = st.sidebar.slider(
    "Default Trailing Stop (%)",
    min_value=1,
    max_value=25,
    value=5,
)

st.sidebar.caption("Ensure headers match: Ticker, Shares, Cost Basis, Current Price.")

# =========================================================
# MAIN CONTENT
# =========================================================
col1, col2 = st.columns(2)

# =============== PORTFOLIO SIDE ===============
with col1:
    st.subheader("📊 Portfolio Overview")
    
    if portfolio_file:
        portfolio_df = load_portfolio_data(portfolio_file)
        cash_value = load_cash_position(manual_cash)

        summary = calculate_summary(portfolio_df, cash_value)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Value", f"${summary['total_value']:,}")
        c2.metric("Cash", f"${summary['cash']:,}")
        c3.metric("Gain/Loss", f"${summary['gain_loss_total']:,}")
        c4.metric("Avg Gain/Loss %", f"{summary['avg_gain_loss_pct']:.2f}%")

        st.markdown("#### Current Holdings")
        st.dataframe(portfolio_df, use_container_width=True)

        st.markdown("#### Trailing Stop Protection")
        ts_df = apply_trailing_stop(portfolio_df.copy(), default_trailing_stop_pct)
        st.dataframe(ts_df, use_container_width=True)

    else:
        st.info("Upload Portfolio CSV to enable holdings view.")

# =============== ZACKS SIDE ===============
with col2:
    st.subheader("🎯 Zacks Tactical Opportunities")

    if growth1_file or growth2_file or dividend_file:
        files_dict = {
            "Growth1": growth1_file,
            "Growth2": growth2_file,
            "Dividend": dividend_file,
        }
        zacks_df = merge_zacks_screens(files_dict)

        if not zacks_df.empty:
            st.markdown("#### Unified Zacks Screen")
            st.dataframe(prepare_zacks_export(zacks_df), use_container_width=True)

            st.markdown("#### 🔥 Rank 1 Priority Stocks")
            rank1_df = extract_rank1_candidates(zacks_df)
            st.dataframe(rank1_df, use_container_width=True)
        else:
            st.warning("No valid Zacks results.")
    else:
        st.info("Upload Zacks files to analyze tactical candidates.")

# =========================================================
# 🧠 Tactical Scoring (Full Table)
# =========================================================
if portfolio_file:
    st.markdown("### 🧠 Tactical Position Scoring")
    scored_df = calculate_tactical_scores(ts_df)
    st.dataframe(scored_df, use_container_width=True)

# =========================================================
# 📘 Tactical Intelligence Brief (Narrative Output)
# =========================================================
st.markdown("---")
st.subheader("📘 Tactical Intelligence Brief")

if portfolio_file:
    brief_text = generate_intelligence_brief(
        portfolio_df=portfolio_df,
        zacks_df=zacks_df if (growth1_file or growth2_file or dividend_file) else None,
        cash_value=cash_value,
        scored_df=scored_df
    )
    st.text_area("🛰 Automated Tactical Narrative", brief_text, height=350)
else:
    st.info("Upload portfolio and optional Zacks files to generate Intelligence Brief.")

# =========================================================
# 🚀 Tactical Action Controls (Simulation Only)
# =========================================================
st.markdown("---")
st.subheader("🛠 Tactical Action Controls (Simulation)")

c1, c2, c3, c4 = st.columns([1, 1, 1, 2])

with c1:
    action_type = st.selectbox("Action", ["BUY", "SELL", "TRIM", "HOLD"])

with c2:
    ticker = st.text_input("Ticker", placeholder="NVDA")

with c3:
    shares = st.number_input("Shares", min_value=0, step=1, value=0)

with c4:
    st.write("")
    execute_action = st.button("Execute Tactical Order")

if execute_action:
    result = process_tactical_action(action_type, ticker, shares)
    st.success(result)

# =========================================================
# FOOTER
# =========================================================
st.markdown("---")
st.caption("🧭 Fox Valley Intelligence Engine — v7.7R | Command Deck Stable Core")
