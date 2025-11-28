import streamlit as st
import pandas as pd
import glob

# === PAGE CONFIG ===
st.set_page_config(page_title="Fox Valley Tactical Command Deck", layout="wide")

st.title("🧭 Fox Valley Tactical Command Deck — v7.7R")
st.caption("🚀 Live Tactical Intelligence | Zacks Synergy | Profit + Risk Analyzer")

# === LOAD PORTFOLIO ===
portfolio_files = glob.glob("data/Portfolio_Positions_*.csv")
if portfolio_files:
    portfolio_file = sorted(portfolio_files)[-1]
    portfolio = pd.read_csv(portfolio_file)
    portfolio["Ticker"] = portfolio["Ticker"].str.upper()

    st.success(f"📊 Portfolio Loaded: {portfolio_file}")
else:
    st.error("⚠ No Portfolio File Available")
    st.stop()

# === LOAD ZACKS DATA ===
zacks_files = glob.glob("data/zacks_custom_screen_*.csv")
if zacks_files:
    zacks_all = pd.concat([pd.read_csv(f) for f in zacks_files], ignore_index=True)
    zacks_all["Ticker"] = zacks_all["Ticker"].astype(str).str.upper()

    st.success(f"📂 {len(zacks_files)} Zacks Screening Files Loaded")
else:
    st.error("⚠ No Zacks Files Found")
    st.stop()

# === MERGE LIVE CROSSMATCH ===
merged = pd.merge(portfolio, zacks_all, on="Ticker", how="inner")

display_cols = [
    "Ticker", "Quantity", "Last Price", "Current Value",
    "Zacks Rank", "Company Name",
    "Total Gain/Loss Percent", "Risk Category", "Tactical Action"
]

available_cols = [c for c in display_cols if c in merged.columns]

# === COLOR HIGHLIGHTING ===
def highlight_zacks(val):
    if val == 1:
        return "background-color: gold; font-weight: bold;"
    elif val == 2:
        return "background-color: lightgreen;"
    return ""

def highlight_action(val):
    if "Strong Buy" in val:
        return "background-color: lightgreen; font-weight: bold;"
    elif "Trim" in val:
        return "background-color: lightcoral; font-weight: bold;"
    elif "Hold" in val:
        return "background-color: lightblue;"
    return ""

# === DISPLAY CROSSMATCH GRID ===
if not merged.empty:
    st.subheader("🛡 Tactical Action Grid — Live Holdings Intelligence")
    st.caption("Real-Time Holdings | Zacks Rank | Profit Status | Tactical Actions")

    styled_df = merged[available_cols].style.applymap(highlight_zacks, subset=["Zacks Rank"]) \
                                           .applymap(highlight_action, subset=["Tactical Action"])

    st.dataframe(styled_df, use_container_width=True)

    # Downloadable CSV
    csv = merged[available_cols].to_csv(index=False)
    st.download_button(
        label="📥 Download Tactical Action Grid (CSV)",
        data=csv,
        file_name="tactical_action_grid.csv",
        mime="text/csv"
    )
else:
    st.warning("📭 No actionable crossmatch found between portfolio & Zacks data.")

st.markdown("---")
st.caption("🧭 Fox Valley Intelligence Engine — Built for Precision Tactical Execution")
