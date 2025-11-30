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
from modules.report_archive_engine import archive_report
from modules.executive_presentation import generate_executive_presentation


# =========================================================
# 🧭 Fox Valley Tactical Command Deck — v7.7R with Presentation Mode
# =========================================================

st.set_page_config(page_title="Fox Valley Tactical Command Deck", layout="wide")

st.title("🧭 Fox Valley Tactical Command Deck — v7.7R Unified Presentation Core")
st.caption("Portfolio ║ Risk ║ Tactical Alerts ║ Intel Brief ║ Exec Report ║ Archive ║ Presentation")


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


# =========================================================
# 📊 Portfolio Processing
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
    st.dataframe(ts_df, use_container_width=True)
else:
    st.info("Upload a Portfolio CSV to begin.")
    st.stop()


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

st.subheader("🧠 Tactical Scoring Engine")
scored_df = calculate_tactical_scores(ts_df)
st.dataframe(scored_df, use_container_width=True)


# =========================================================
# 🛡 Risk Heatmap
# =========================================================

st.subheader("🛡 Risk Heatmap")
risk_df = generate_risk_heatmap(ts_df)
st.dataframe(risk_df, use_container_width=True)


# =========================================================
# 🚨 Tactical Alerts
# =========================================================

st.subheader("🚨 Tactical Alerts Dashboard")
alerts_list = generate_tactical_alerts(
    portfolio_df=ts_df,
    scored_df=scored_df,
    zacks_df=zacks_df if 'zacks_df' in locals() else None,
)
alert_df = alerts_to_dataframe(alerts_list)
st.dataframe(alert_df, use_container_width=True)


# =========================================================
# 📘 Tactical Intelligence Brief
# =========================================================

st.subheader("📘 Tactical Intelligence Brief")
brief_text = generate_intelligence_brief(
    portfolio_df=portfolio_df,
    zacks_df=zacks_df if 'zacks_df' in locals() else None,
    cash_value=cash_value,
    scored_df=scored_df
)
st.text_area("🛰 Strategic Narrative", brief_text, height=350)


# =========================================================
# 📑 Report Export & Archive
# =========================================================

st.subheader("📑 Report Export & Archive")
report_text = build_command_report(
    portfolio_df=portfolio_df,
    risk_df=risk_df,
    alerts_list=alerts_list,
    tactical_scores_df=scored_df,
    intelligence_brief_text=brief_text
)

st.text_area("📋 Full Report Preview", report_text, height=450)

colA, colB, colC = st.columns(3)

with colA:
    if st.button("📄 Export Tactical Report (PDF)"):
        pdf_file = export_report_to_pdf(report_text)
        with open(pdf_file, "rb") as f:
            st.download_button(
                label="⬇ Download Tactical Report (PDF)",
                data=f,
                file_name=pdf_file,
                mime="application/pdf",
            )

with colB:
    if st.button("🏛 Export Executive Briefing (PDF)"):
        exec_file = export_report_to_pdf(
            report_text,
            filename="Fox_Valley_Executive_Tactical_Briefing.pdf"
        )
        with open(exec_file, "rb") as f:
            st.download_button(
                label="🏛 Download Executive Briefing (PDF)",
                data=f,
                file_name=exec_file,
                mime="application/pdf",
            )

with colC:
    if st.button("🗄 Archive Report"):
        archived_file = export_report_to_pdf(report_text)
        archived_file = archive_report(archived_file)
        st.success(f"🗄 Archived to: {archived_file}")


# =========================================================
# 🏛 Executive Presentation Mode — Slide Viewer
# =========================================================

st.markdown("---")
st.subheader("🏛 Executive Presentation Mode — Slide Viewer")

slides = generate_executive_presentation(
    portfolio_summary=summary,
    risk_df=risk_df,
    tactical_scores_df=scored_df,
    alerts_list=alerts_list,
    intel_brief_text=brief_text
)

if "slide_index" not in st.session_state:
    st.session_state.slide_index = 0

col_prev, col_next = st.columns([1, 1])

with col_prev:
    if st.button("⬅ Previous Slide") and st.session_state.slide_index > 0:
        st.session_state.slide_index -= 1

with col_next:
    if st.button("Next Slide ➡") and st.session_state.slide_index < len(slides) - 1:
        st.session_state.slide_index += 1

current_slide = slides[st.session_state.slide_index]
st.markdown(f"### 📑 Slide {st.session_state.slide_index + 1} — {current_slide['title']}")
st.text_area("", current_slide["content"], height=350)


# =========================================================
# 🛠 Tactical Order Simulation
# =========================================================

st.subheader("🛠 Tactical Order Simulation")
col1, col2, col3, col4 = st.columns([1, 1, 1, 2])

with col1:
    action_type = st.selectbox("Action", ["BUY", "SELL", "TRIM", "HOLD"])
with col2:
    ticker = st.text_input("Ticker", "NVDA")
with col3:
    shares = st.number_input("Shares", min_value=0, step=1)
with col4:
    if st.button("📡 Execute Tactical Order"):
        st.success(process_tactical_action(action_type, ticker, shares))


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")
st.caption("🧭 Fox Valley Intelligence Engine — v7.7R Presentation Core")
