import pandas as pd

def calculate_profit_and_risk(df):
    """
    Takes a cleaned portfolio DataFrame and calculates:
    - Cost Basis Total (Quantity * Purchase Price)
    - Unrealized Gain/Loss Dollar
    - Unrealized Gain/Loss Percent
    """

    # Ensure required fields exist
    required = ["Ticker", "Quantity", "Current Value", "Purchase Price"]
    for col in required:
        if col not in df.columns:
            print(f"⚠ Missing required column: {col}")
            return df

    # Calculate cost basis total (per position)
    df["Cost Basis Total"] = df["Quantity"] * df["Purchase Price"]

    # Calculate Unrealized Profit/Loss Dollar
    df["Unrealized Gain/Loss Dollar"] = df["Current Value"] - df["Cost Basis Total"]

    # Percent Gain/Loss
    df["Unrealized Gain/Loss Percent"] = (
        df["Unrealized Gain/Loss Dollar"] / df["Cost Basis Total"] * 100
    ).replace([float("inf"), -float("inf")], 0).fillna(0)

    # Round values
    df["Cost Basis Total"] = df["Cost Basis Total"].round(2)
    df["Unrealized Gain/Loss Dollar"] = df["Unrealized Gain/Loss Dollar"].round(2)
    df["Unrealized Gain/Loss Percent"] = df["Unrealized Gain/Loss Percent"].round(2)

    print("📊 Profit & Risk calculations applied.")
    return df
