import streamlit as st
import pandas as pd

from modules.portfolio_engine import load_portfolio_data, load_cash_position, calculate_summary
from modules.zacks_unified_analyzer import merge_zacks_screens, extract_rank1_candidates, prepare_zacks_export
from modules.trailing_stop_manager import apply_trailing_stop
from modules.tactical_controls import process_tactical_action
from modules.tactical_scoring_engine import calculate_tactical_scores
from modules.intelligence_brief import generate_intelligence_brief
from modules.risk_heatmap_engine import generate_risk_heatmap
from modules.tactical_alerts import generate_tactical_alerts, alerts_to_dataframe
from modules.command_report_builder import build_command_report
from modules.pdf_export_engine import export_report_to_pdf


# =========================================================
# 🧭 Fox Valley Tactical Command Deck — v7.7R Dashboard
# Portfolio | Risk | Scoring | Alerts | Intel Brief | PDF Export
# =========================================================

st.set_page_config(page_title="Fox Valley Tactical Command Deck", layout="wide")

st.title("🧭 Fox Valley Tactical Command Deck — v7.7R")
st.caption("Portfolio ║ Risk ║ Tactical Alerts ║ Intelligence Brief ║ PDF Export System")


# =========================================================
# 📂 Sidebar Inputs
# =========================================================

st.sidebar.header("📂 Data Inputs")

portfolio_file = st.sidebar.file_uploader("Portfolio CSV", type=["csv"])

st.sidebar.subheader("📥 Zacks Screen Files")
growth1_file = st.sidebar.file_uploader("Growth 1 CSV", type=["csv"])
growth2_file = st.sidebar.file_uploader("Growth 2 CSV", type=["csv"])
dividend_file = st.sidebar.file_uploader("Defensive Dividends CSV", type=["csv"])

manual_cash = st.sidebar.number_input("Manual Cash Override ($)", min_value=0.0, step=100.0, format="%.2f")

default_trailing_stop_pct = st.sidebar.slider("Default Trailing Stop (%)", 1, 25, 5)

st.sidebar.caption("Required CSV headers: Ticker, Shares, Cost Basis, Current Price.")


# =========================================================
# 📊 Portfolio Overview
# =========================================================

if portfolio_file:
    portfolio_df = load_portfolio_data(portfolio_file)
    cash_value = load_cash_position(manual_cash)
    summary = calculate_summary(portfolio_df, cash_value)

    st.subheader("📊 Portfolio Overview")

    a, b, c, d = st.columns(4)
    a.metric("Total Value", f"${summary['total_value']:,}")
    b.metric("Cash", f"${summary['cash']:,}")
    c.metric("Gain/Loss", f"${summary['gain_loss_total']:,}")
    d.metric("Avg Gain/Loss %", f"{summary['avg_gain_loss_pct']:.2f}%")

    ts_df = apply_trailing_stop(portfolio_df.copy(), default_trailing_stop_pct)
    st.markdown("#### Holdings with Trailing Stops")
    st.dataframe(ts_df, use_container_width=True)
else:
    st.info("Upload a portfolio file.")


# =========================================================
# 🎯 Zacks Tactical Candidates
# =========================================================

if any([growth1_file, growth2_file, dividend_file]):
    st.subheader("🎯 Zacks Tactical Candidates")
    zacks_df = merge_zacks_screens({
        "Growth1": growth1_file,
        "Growth2": growth2_file,
        "Dividend": dividend_file,
    })

    if not zacks_df.empty:
        st.markdown("#### Unified Zacks Data")
        st.dataframe(prepare_zacks_export(zacks_df), use_container_width=True)

        st.markdown("#### 🔥 Rank 1 Tactical Opportunities")
        st.dataframe(extract_rank1_candidates(zacks_df), use_container_width=True)


# =========================================================
# 🧠 Tactical Scoring Engine
# =========================================================

if portfolio_file:
    st.subheader("🧠 Tactical Scoring Engine")
    scored_df = calculate_tactical_scores(ts_df)
    st.dataframe(scored_df, use_container_width=True)


# =========================================================
# 🛡 Risk Heatmap
# =========================================================

if portfolio_file:
    st.subheader("🛡 Risk Heatmap")
    risk_df = generate_risk_heatmap(ts_df)
    st.dataframe(risk_df, use_container_width=True)


# =========================================================
# 🚨 Tactical Alerts
# =========================================================

if portfolio_file:
    st.subheader("🚨 Tactical Alerts Dashboard")
    alerts_list = generate_tactical_alerts(
        portfolio_df=ts_df,
        scored_df=scored_df if 'scored_df' in locals() else None,
        zacks_df=zacks_df if 'zacks_df' in locals() else None,
    )
    alert_df = alerts_to_dataframe(alerts_list)
    st.dataframe(alert_df, use_container_width=True)


# =========================================================
# 📘 Intelligence Brief (Narrative)
# =========================================================

if portfolio_file:
    st.subheader("📘 Intelligence Brief")
    brief_text = generate_intelligence_brief(
        portfolio_df=portfolio_df,
        zacks_df=zacks_df if 'zacks_df' in locals() else None,
        cash_value=cash_value,
        scored_df=scored_df if 'scored_df' in locals() else None
    )
    st.text_area("🛰 Strategic Narrative", brief_text, height=350)


# =========================================================
# 📑 Command Report + PDF Export Button
# =========================================================

if portfolio_file:
    st.subheader("📑 Generate Official Command Report")

    report_text = build_command_report(
        portfolio_df=portfolio_df,
        risk_df=risk_df if 'risk_df' in locals() else None,
        alerts_list=alerts_list if 'alerts_list' in locals() else None,
        tactical_scores_df=scored_df if 'scored_df' in locals() else None,
        intelligence_brief_text=brief_text if 'brief_text' in locals() else None,
    )

    st.text_area("📋 Command Tactical Report (Preview)", report_text, height=450)

    if st.button("📄 Export to PDF"):
        pdf_file = export_report_to_pdf(report_text)
        with open(pdf_file, "rb") as f:
            st.download_button(
                label="⬇ Download Tactical Command Report (PDF)",
                data=f,
                file_name=pdf_file,
                mime="application/pdf",
            )
        st.success("Tactical Command Report PDF generated successfully.")


# =========================================================
# 🛠 Tactical Order Control Panel
# =========================================================

st.subheader("🛠 Tactical Order Simulation")

c1, c2, c3, c4 = st.columns([1, 1, 1, 2])
with c1:
    action_type = st.selectbox("Action", ["BUY", "SELL", "TRIM", "HOLD"])
with c2:
    ticker = st.text_input("Ticker", "NVDA")
with c3:
    shares = st.number_input("Shares", min_value=0, step=1, value=0)
with c4:
    execute_action = st.button("Execute Tactical Order")

if execute_action:
    st.success(process_tactical_action(action_type, ticker, shares))


# =========================================================
# FOOTER
# =========================================================
st.markdown("---")
st.caption("🧭 Fox Valley Intelligence Engine — v7.7R Tactical Core")
