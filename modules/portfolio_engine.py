import pandas as pd

# =========================================================
# 📁 Portfolio Engine — v7.7R Final Stable Build
# Loads, validates, calculates, and exports portfolio data
# =========================================================

def load_portfolio_data(file_path):
    """
    Load portfolio CSV.
    Required columns:
        - Ticker
        - Shares
        - Cost Basis
        - Current Price
    Adds:
        - Current Value
        - Gain/Loss $
        - Gain/Loss %
    """
    try:
        df = pd.read_csv(file_path)
        df.columns = df.columns.str.strip()

        required = ["Ticker", "Shares", "Cost Basis", "Current Price"]
        if not all(col in df.columns for col in required):
            raise ValueError(f"CSV missing required columns: {required}")

        df["Shares"] = pd.to_numeric(df["Shares"], errors="coerce").fillna(0)
        df["Cost Basis"] = pd.to_numeric(df["Cost Basis"], errors="coerce").fillna(0)
        df["Current Price"] = pd.to_numeric(df["Current Price"], errors="coerce").fillna(0)

        df["Current Value"] = round(df["Shares"] * df["Current Price"], 2)
        df["Gain/Loss $"] = round(df["Current Value"] - (df["Shares"] * df["Cost Basis"]), 2)
        df["Gain/Loss %"] = round(
            (df["Gain/Loss $"] / (df["Shares"] * df["Cost Basis"]).replace(0, pd.NA)) * 100, 2
        )

        return df

    except Exception as e:
        print(f"Error loading portfolio data: {e}")
        return pd.DataFrame()


def load_cash_position(manual_cash=None, file_value=None):
    """
    Determines cash value available for trading.
    Manual override takes priority.
    """
    if manual_cash is not None:
        return round(float(manual_cash), 2)
    if file_value is not None:
        return round(float(file_value), 2)
    return 0.00


def calculate_summary(df, cash_value):
    """
    Generates summary stats for dashboard top metrics.
    """
    if df.empty:
        return {
            "total_value": cash_value,
            "cash": cash_value,
            "invested_value": 0,
            "gain_loss_total": 0,
            "avg_gain_loss_pct": 0,
        }

    invested_value = df["Current Value"].sum()
    gain_loss_total = df["Gain/Loss $"].sum()
    avg_gain_loss_pct = df["Gain/Loss %"].mean()

    total_value = invested_value + cash_value

    return {
        "total_value": round(total_value, 2),
        "cash": round(cash_value, 2),
        "invested_value": round(invested_value, 2),
        "gain_loss_total": round(gain_loss_total, 2),
        "avg_gain_loss_pct": round(avg_gain_loss_pct, 2),
    }


def prepare_portfolio_export(df):
    """
    Standard portfolio export for scoring, stops, and tactical briefing.
    """
    if df.empty:
        return df

    export_cols = [
        "Ticker", "Shares", "Cost Basis", "Current Price",
        "Current Value", "Gain/Loss $", "Gain/Loss %"
    ]
    return df[export_cols].copy()
