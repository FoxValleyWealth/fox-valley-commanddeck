import pandas as pd
import numpy as np

# =========================================================
# 🛡 Fox Valley Risk Heatmap Engine — v7.7R Final Stable Build
# Identifies position-level risk signals:
# • Stop-loss proximity
# • Capital concentration
# • Unrealized loss severity
# • Tactical risk priority levels (Low → Critical)
# =========================================================

def generate_risk_heatmap(portfolio_df):
    """
    Accepts portfolio_df and returns a structured DataFrame showing:
    - StopRisk %
    - Capital Weight %
    - Loss Severity %
    - Tactical Risk Level (LOW/MEDIUM/HIGH/CRITICAL)
    """
    if portfolio_df is None or portfolio_df.empty:
        return pd.DataFrame()

    df = portfolio_df.copy()

    # Ensure numeric precision
    numeric_cols = ["Current Value", "Gain/Loss $", "Gain/Loss %", "Current Price", "Stop Price"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # 1️⃣ Capital Weight (% of portfolio value)
    df["CapitalWeight %"] = round(
        (df["Current Value"] / df["Current Value"].sum()) * 100, 2
    )

    # 2️⃣ StopRisk — how close is price to stop (%)
    if "Stop Price" in df.columns:
        df["StopRisk %"] = round(
            ((df["Current Price"] - df["Stop Price"]) / df["Current Price"]) * 100, 2
        )
    else:
        df["StopRisk %"] = np.nan

    # 3️⃣ Loss Severity % — contribution to negative portfolio value
    df["LossSeverity %"] = np.where(
        df["Gain/Loss $"] < 0,
        round((abs(df["Gain/Loss $"]) / abs(df[df["Gain/Loss $"] < 0]["Gain/Loss $"]).sum()) * 100, 2),
        0
    )

    # 4️⃣ Tactical Risk Level — Unified Risk Assessment
    def tactical_risk_level(row):
        if row["CapitalWeight %"] > 25 or row["LossSeverity %"] > 30:
            return "CRITICAL"
        if row["StopRisk %"] <= 2 or row["Gain/Loss %"] < -10:
            return "HIGH"
        if row["StopRisk %"] <= 5 or row["Gain/Loss %"] < 0:
            return "MEDIUM"
        return "LOW"

    df["Risk Level"] = df.apply(tactical_risk_level, axis=1)

    # Output structure
    return df[[
        "Ticker",
        "CapitalWeight %",
        "Gain/Loss %",
        "StopRisk %",
        "LossSeverity %",
        "Risk Level",
    ]]
