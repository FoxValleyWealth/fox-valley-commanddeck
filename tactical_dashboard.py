import streamlit as st
import pandas as pd

from modules.portfolio_engine import (
    load_portfolio_data,
    load_cash_position,
    calculate_summary,
)

from modules.zacks_unified_analyzer import (
    merge_zacks_screens,
    extract_rank1_candidates,
    prepare_zacks_export,
)

from modules.trailing_stop_manager import (
    apply_trailing_stop,
)

from modules.tactical_controls import process_tactical_action
from modules.tactical_scoring_engine import calculate_tactical_scores
from modules.intelligence_brief import generate_intelligence_brief
from modules.risk_heatmap_engine import generate_risk_heatmap
from modules.tactical_alerts import generate_tactical_alerts
from modules.command_report_builder import build_command_report

# =========================================================
# 🧭 Fox Valley Tactical Command Deck — v7.7R
# Full-System Dashboard — Risk Heatmap Fully Integrated
# =========================================================

st.set_page_config(page_title="Fox Valley Tactical Command Deck", layout="wide")

st.title("🧭 Fox Valley Tactical Command Deck — v7.7R Stable Core")
st.caption("Portfolio | Zacks | Trailing Stops | Tactical Scoring | Risk Heatmap | Intelligence Brief | Alerts")


# =========================================================
# 📂 SIDEBAR — Data Inputs
# =========================================================
st.sidebar.header("📂 Data Inputs")

portfolio_file = st.sidebar.file_uploader("Portfolio CSV", type=["csv"])

st.sidebar.subheader("📥 Zacks Screen Files")
growth1_file = st.sidebar.file_uploader("Growth 1 CSV", type=["csv"])
growth2_file = st.sidebar.file_uploader("Growth 2 CSV", type=["csv"])
dividend_file = st.sidebar.file_uploader("Defensive Dividends CSV", type=["csv"])

manual_cash = st.sidebar.number_input("Manual Cash Override ($)", min_value=0.0, step=100.0, format="%.2f")
default_trailing_stop_pct = st.sidebar.slider("Default Trailing Stop (%)", 1, 25, 5)

st.sidebar.caption("CSV must include: Ticker, Shares, Cost Basis, Current Price.")


# =========================================================
# 📊 MAIN CONTENT — Two Column Layout
# =========================================================
col1, col2 = st.columns(2)

# ---------------- Portfolio Overview ----------------
with col1:
    st.subheader("📊 Portfolio Overview")

    if portfolio_file:
        portfolio_df = load_portfolio_data(portfolio_file)
        cash_value = load_cash_position(manual_cash)
        summary = calculate_summary(portfolio_df, cash_value)

        a, b, c, d = st.columns(4)
        a.metric("Total Value", f"${summary['total_value']:,}")
        b.metric("Cash", f"${summary['cash']:,}")
        c.metric("Gain/Loss", f"${summary['gain_loss_total']:,}")
        d.metric("Avg Gain/Loss %", f"{summary['avg_gain_loss_pct']:.2f}%")

        st.markdown("#### Holdings with Trailing Stops")
        ts_df = apply_trailing_stop(portfolio_df.copy(), default_trailing_stop_pct)
        st.dataframe(ts_df, use_container_width=True)
    else:
        st.info("Upload a portfolio CSV to enable analysis.")

# ---------------- Zacks Screening ----------------
with col2:
    st.subheader("🎯 Zacks Tactical Candidates")
    if any([growth1_file, growth2_file, dividend_file]):
        files_dict = {"Growth1": growth1_file, "Growth2": growth2_file, "Dividend": dividend_file}
        zacks_df = merge_zacks_screens(files_dict)

        if not zacks_df.empty:
            st.markdown("#### Unified Zacks Screen Data")
            st.dataframe(prepare_zacks_export(zacks_df), use_container_width=True)

            st.markdown("#### 🔥 Rank 1 Opportunities")
            rank1_df = extract_rank1_candidates(zacks_df)
            st.dataframe(rank1_df, use_container_width=True)
        else:
            st.warning("No valid Zacks candidates found.")
    else:
        st.info("Upload Zacks screen files to enable this section.")


# =========================================================
# 🧠 Tactical Scoring Table
# =========================================================
if portfolio_file:
    st.markdown("### 🧠 Tactical Scoring (Position Strength)")
    scored_df = calculate_tactical_scores(ts_df)
    st.dataframe(scored_df, use_container_width=True)


# =========================================================
# 🛡 RISK HEATMAP — NEW FULLY INTEGRATED
# =========================================================
st.markdown("---")
st.subheader("🛡 Tactical Risk Heatmap")

if portfolio_file:
    risk_df = generate_risk_heatmap(ts_df)
    st.dataframe(risk_df, use_container_width=True)
else:
    st.info("Upload portfolio data to view tactical risk heatmap.")


# =========================================================
# 🚨 Tactical Alerts
# =========================================================
st.markdown("---")
st.subheader("🚨 Tactical Alerts")

if portfolio_file:
    alerts_list = generate_tactical_alerts(
        portfolio_df=ts_df,
        scored_df=scored_df if 'scored_df' in locals() else None,
        zacks_df=zacks_df if 'zacks_df' in locals() else None,
    )
    for alert in alerts_list:
        st.write(alert)
else:
    st.info("Alerts will generate when portfolio data is loaded.")


# =========================================================
# 📘 Tactical Intelligence Brief
# =========================================================
st.markdown("---")
st.subheader("📘 Tactical Intelligence Brief")

if portfolio_file:
    brief_text = generate_intelligence_brief(
        portfolio_df=portfolio_df,
        zacks_df=zacks_df if 'zacks_df' in locals() else None,
        cash_value=cash_value,
        scored_df=scored_df if 'scored_df' in locals() else None
    )
    st.text_area("🛰 Strategic Narrative Report", brief_text, height=350)
else:
    st.info("Upload portfolio and Zacks files to produce full Intelligence Brief.")


# =========================================================
# 📑 Command Report Export (Preview Only — PDF Later)
# =========================================================
st.markdown("---")
st.subheader("📑 Command Report — Export Preview")

if portfolio_file:
    report_preview = build_command_report(
        portfolio_df=portfolio_df,
        risk_df=risk_df if 'risk_df' in locals() else None,
        alerts_list=alerts_list if 'alerts_list' in locals() else None,
        tactical_scores_df=scored_df if 'scored_df' in locals() else None,
        intelligence_brief_text=brief_text if 'brief_text' in locals() else None,
    )
    st.text_area("📝 Command Report Preview", report_preview, height=450)
else:
    st.info("Generate report after loading portfolio and analysis modules.")


# =========================================================
# 🛠 Tactical Action Controls (Simulation Only)
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
    execute_action = st.button("Execute Order")

if execute_action:
    result = process_tactical_action(action_type, ticker, shares)
    st.success(result)


# =========================================================
# FOOTER
# =========================================================
st.markdown("---")
st.caption("🧭 Fox Valley Intelligence Engine — v7.7R Tactical Core")
