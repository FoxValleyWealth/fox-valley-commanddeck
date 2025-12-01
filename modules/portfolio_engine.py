# === Fox Valley Intelligence Engine – Portfolio Engine v7.7R ===

import pandas as pd

# ------------------------------
# Load Portfolio CSV
# ------------------------------
def load_portfolio_data(file):
    try:
        df = pd.read_csv(file)

        # Normalize column names
        df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

        # Required columns check
        required = ["ticker", "shares", "cost_basis", "current_price"]
        for r in required:
            if r not in df.columns:
                raise ValueError(f"Missing required column: {r}")

        # Clean numeric columns
        numeric_cols = ["shares", "cost_basis", "current_price"]
        for col in numeric_cols:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(r"[\$,]", "", regex=True)
                .astype(float)
            )

        # Compute tactical fields
        df["position_value"] = df["shares"] * df["current_price"]
        df["total_cost"] = df["shares"] * df["cost_basis"]
        df["gain_loss"] = df["position_value"] - df["total_cost"]
        df["gain_loss_pct"] = (df["gain_loss"] / df["total_cost"]) * 100

        return df

    except Exception as e:
        print(f"Portfolio Load Error: {e}")
        return None


# ------------------------------
# Optional Manual Cash Override
# ------------------------------
def load_cash_position(manual_cash: float):
    try:
        return float(manual_cash)
    except:
        return 0.0


# ------------------------------
# Portfolio Summary Statistics
# ------------------------------
def calculate_portfolio_summary(df):
    if df is None or df.empty:
        return {
            "total_value": 0,
            "total_gain": 0,
            "avg_gain_pct": 0,
        }

    total_value = df["position_value"].sum()
    total_gain = df["gain_loss"].sum()
    avg_gain_pct = df["gain_loss_pct"].mean()

    return {
        "total_value": float(total_value),
        "total_gain": float(total_gain),
        "avg_gain_pct": float(avg_gain_pct),
    }
