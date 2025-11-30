import pandas as pd

# =========================================================
# 🧠 Tactical Scoring Engine — v7.7R Stable Build
# Generates:
# - Position Strength Score (0–100)
# - Tactical Priority Label
# - Risk Exposure Indicator
# =========================================================

def calculate_tactical_scores(portfolio_df):
    """
    Adds tactical scoring components based on:
    - Gain/Loss %
    - Zacks Rank (if available)
    - Trailing Stop Risk Level
    - Momentum Factor (basic price change logic)
    """

    if portfolio_df.empty:
        return portfolio_df

    df = portfolio_df.copy()

    # Ensure numeric
    for col in ["Gain/Loss %", "Current Price", "Stop Price"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # ===== 1) Score based on Gain/Loss % =====
    df["GainScore"] = df["Gain/Loss %"].apply(lambda x: 40 if x > 25 else
                                                     30 if x > 10 else
                                                     20 if x > 0 else
                                                     10)

    # ===== 2) Zacks Tactical Score (if integrated) =====
    if "Zacks Rank" in df.columns:
        df["ZacksScore"] = df["Zacks Rank"].apply(lambda x: 35 if x == 1 else
                                                            25 if x == 2 else
                                                            15 if x == 3 else
                                                             0)
    else:
        df["ZacksScore"] = 0

    # ===== 3) Trailing Stop Risk =====
    if "Stop Price" in df.columns:
        df["RiskGap %"] = round(((df["Current Price"] - df["Stop Price"]) / df["Current Price"]) * 100, 2)

        df["RiskScore"] = df["RiskGap %"].apply(lambda x: 25 if x >= 10 else
                                                         15 if x >= 6 else
                                                          5 if x > 0 else
                                                          0)
    else:
        df["RiskScore"] = 5

    # ===== 4) Momentum Score Placeholder =====
    df["MomentumScore"] = 10  # Can be replaced later with real indicator

    # ===== Final Weighted Calculation =====
    df["TacticalScore"] = round(
        df["GainScore"] + df["ZacksScore"] + df["RiskScore"] + df["MomentumScore"], 0
    )

    # ===== Tactical Priority Label =====
    def map_priority(score):
        if score >= 80:
            return "STRONG BUY"
        elif score >= 60:
            return "ACCUMULATE/HOLD"
        elif score >= 40:
            return "CAUTION / HOLD"
        else:
            return "AT RISK / TRIM"

    df["Tactical Priority"] = df["TacticalScore"].apply(map_priority)

    return df[[
        "Ticker",
        "Current Price",
        "Gain/Loss %",
        "Stop Price",
        "RiskScore",
        "ZacksScore",
        "GainScore",
        "MomentumScore",
        "TacticalScore",
        "Tactical Priority",
    ]]
