import pandas as pd

# =========================================================
# 🚨 Tactical Alerts Engine — v7.7R Final Stable Build
# Generates real-time tactical alerts based on:
# • Stop breaches
# • Unrealized loss analysis
# • Capital concentration risk
# • Tactical Score + Zacks Opportunity Flags
# =========================================================

def generate_tactical_alerts(portfolio_df=None, scored_df=None, zacks_df=None):
    if portfolio_df is None or portfolio_df.empty:
        return ["📭 No portfolio data available for alerts."]

    alerts = []
    df = portfolio_df.copy()
    df["Current Value"] = pd.to_numeric(df["Current Value"], errors="coerce")
    df["Gain/Loss %"] = pd.to_numeric(df["Gain/Loss %"], errors="coerce")
    df["Current Price"] = pd.to_numeric(df["Current Price"], errors="coerce")
    df["Stop Price"] = pd.to_numeric(df.get("Stop Price", None), errors="coerce")

    # ===== 🚨 1. Stop Breach Detection =====
    if "Stop Price" in df.columns:
        breached = df[df["Current Price"] <= df["Stop Price"]]
        for _, row in breached.iterrows():
            alerts.append(
                f"🚨 STOP BREACH: {row['Ticker']} is below stop "
                f"({row['Current Price']:.2f} ≤ {row['Stop Price']:.2f}). Immediate review required."
            )

    # ===== ⚠ 2. Unrealized Loss Warning =====
    severe_loss = df[df["Gain/Loss %"] <= -10]
    for _, row in severe_loss.iterrows():
        alerts.append(
            f"⚠ HEAVY LOSS: {row['Ticker']} is down {row['Gain/Loss %']:.2f}%, "
            f"review risk mitigation or exit strategy."
        )

    # ===== 🛑 3. Capital Concentration Risk (>20%) =====
    df["CapitalWeight %"] = round((df["Current Value"] / df["Current Value"].sum()) * 100, 2)
    concentration = df[df["CapitalWeight %"] > 20]
    for _, row in concentration.iterrows():
        alerts.append(
            f"🛑 CAPITAL CLUSTER: {row['Ticker']} accounts for {row['CapitalWeight %']:.2f}% "
            f"of total portfolio value. Diversification recommended."
        )

    # ===== ⏳ 4. 3% Stop Proximity Warning =====
    if "Stop Price" in df.columns:
        df["StopRisk %"] = round(((df["Current Price"] - df["Stop Price"]) / df["Current Price"]) * 100, 2)
        near_stop = df[df["StopRisk %"] <= 3]
        for _, row in near_stop.iterrows():
            alerts.append(
                f"⏳ NEAR STOP: {row['Ticker']} is within {row['StopRisk %']:.2f}% of trailing stop."
            )

    # ===== 🎯 5. Tactical Opportunity — Rank1 + Strong Tactical Score =====
    if scored_df is not None and not scored_df.empty and zacks_df is not None and not zacks_df.empty:
        merged = pd.merge(scored_df, zacks_df, left_on="Ticker", right_on="ticker", how="inner")
        tactical_buys = merged[
            (merged["zacks_rank"] == 1) & 
            (merged["TacticalScore"] >= 80)
        ]
        for _, row in tactical_buys.iterrows():
            alerts.append(
                f"🎯 HIGH-PROBABILITY BUY SIGNAL: {row['Ticker']} — "
                f"Rank 1 with TacticalScore {row['TacticalScore']}."
            )

    # ===== No alerts? =====
    if not alerts:
        alerts.append("📈 No critical tactical alerts. Portfolio remains stable.")

    return alerts


# =========================================================
# 🗂 Export-Friendly Helper Format
# =========================================================
def alerts_to_dataframe(alerts_list):
    """Converts alert messages to a DataFrame for dashboard export."""
    return pd.DataFrame({"Tactical Alerts": alerts_list}) if alerts_list else pd.DataFrame()
