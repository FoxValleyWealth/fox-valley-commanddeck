# === Fox Valley Command Deck – Tactical Dashboard v7.7R ===
# Full System Integration Build – Portfolio | Zacks | Risk | Alerts | Reports

import streamlit as st
import pandas as pd
from modules.portfolio_engine import load_portfolio_data, calculate_portfolio_summary
from modules.zacks_unified_analyzer import load_zacks_files, merge_zacks_screens
from modules.trailing_stop_manager import apply_trailing_stops
from modules.tactical_scoring_engine import generate_tactical_scores
from modules.intelligence_brief import build_intelligence_brief
from modules.risk_heatmap_engine import generate_risk_heatmap
from modules.tactical_alerts_engine import generate_alerts
from modules.pdf_export_engine import export_report_to_pdf
from modules.report_archive_engine import archive_report
from modules.exec_report_engine import build_exec_report
from modules.presentation_mode_engine import build_presentation_slides
from modules.slide_export_engine import export_slides_to_pdf

# === Page Layout ===
st.set_page_config(page_title="Fox Valley Tactical Command Deck", layout="wide")

st.title("🧭 Fox Valley Tactical Command Deck — v7.7R Full Executive Authority")
st.caption("Portfolio ║ Risk ║ Tactical Alerts ║ Intel Brief ║ Exec Report ║ Archive ║ Presentation")

# === SIDEBAR INPUTS ===
st.sidebar.header("📂 Data Inputs")

portfolio_file = st.sidebar.file_uploader("Portfolio CSV", type=['csv'])
growth1_file = st.sidebar.file_uploader("Growth 1 CSV", type=['csv'])
growth2_file = st.sidebar.file_uploader("Growth 2 CSV", type=['csv'])
defdiv_file = st.sidebar.file_uploader("Defensive Dividends CSV", type=['csv'])

manual_cash = st.sidebar.number_input("Manual Cash Override ($)", min_value=0.0, value=0.0)
default_stop = st.sidebar.slider("Default Trailing Stop (%)", 1, 25, 15)

# === PROCESS PORTFOLIO CSV ===
portfolio_df = None
summary = None

if portfolio_file:
    portfolio_df = load_portfolio_data(portfolio_file)

    if portfolio_df is not None:
        # Apply trailing stops
        portfolio_df = apply_trailing_stops(portfolio_df, default_stop)

        # Tactical scoring
        portfolio_df = generate_tactical_scores(portfolio_df)

        # Build intelligence brief
        summary = calculate_portfolio_summary(portfolio_df)

# === DISPLAY PORTFOLIO ===
st.subheader("📊 Portfolio Overview")

if portfolio_df is None:
    st.info("Upload a Portfolio CSV to begin.")
else:
    st.dataframe(portfolio_df)

    st.metric("Estimated Total Value", f"${summary['total_value']:,.2f}")
    st.metric("Total Gain/Loss", f"${summary['total_gain']:,.2f}")
    st.metric("Avg Gain/Loss %", f"{summary['avg_gain_pct']:.2f}%")

# === LOAD ZACKS FILES ===
st.subheader("🎯 Zacks Unified Candidates")

zacks_df = None

if growth1_file or growth2_file or defdiv_file:
    zacks_df = load_zacks_files(growth1_file, growth2_file, defdiv_file)

    if zacks_df is not None:
        merged_df = merge_zacks_screens(portfolio_df, zacks_df)
        st.dataframe(merged_df)
    else:
        st.warning("Zacks screening data could not be processed.")
else:
    st.info("Upload at least one Zacks CSV to enable candidate analysis.")

# === RISK HEATMAP ===
st.subheader("🔥 Risk Heatmap")

if portfolio_df is not None:
    heatmap = generate_risk_heatmap(portfolio_df)
    st.pyplot(heatmap)
else:
    st.info("Upload a Portfolio CSV to generate Heatmap.")

# === TACTICAL ALERTS ===
st.subheader("⚠ Tactical Alerts")

if portfolio_df is not None:
    alerts = generate_alerts(portfolio_df)
    st.write(alerts)
else:
    st.info("Upload Portfolio CSV to enable alerts.")

# === INTELLIGENCE BRIEF ===
st.subheader("🧠 Intelligence Brief")

if portfolio_df is not None:
    brief = build_intelligence_brief(portfolio_df, summary)
    st.write(brief)
else:
    st.info("Portfolio required to generate Intelligence Brief.")

# === EXEC REPORT ===
st.subheader("📄 Executive Report")

if st.button("Generate PDF Report"):
    if portfolio_df is not None:
        pdf_bytes = build_exec_report(portfolio_df, summary)
        st.success("Executive Report generated successfully!")
        st.download_button("Download PDF", pdf_bytes, file_name="Executive_Report.pdf")
    else:
        st.error("Portfolio data is required.")

# === ARCHIVE SYSTEM ===
st.subheader("🗂 Report Archive")

if st.button("Archive Latest Report"):
    if portfolio_df is not None:
        archive_report(pdf_bytes)
        st.success("Report archived successfully!")
    else:
        st.error("Portfolio data required.")

# === PRESENTATION MODE ===
st.subheader("🎥 Presentation Mode")

if st.button("Generate Slide Deck"):
    if portfolio_df is not None:
        slides = build_presentation_slides(portfolio_df, summary)
        st.success("Slide deck created successfully!")
    else:
        st.error("Portfolio data required.")

if st.button("Export Slides to PDF"):
    if portfolio_df is not None:
        slide_pdf = export_slides_to_pdf(slides)
        st.download_button("Download Slide PDF", slide_pdf, file_name="Slides.pdf")
    else:
        st.error("Portfolio data required.")
