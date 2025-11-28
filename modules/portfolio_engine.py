import os
import pandas as pd

DATA_FOLDER = "data"

def load_portfolio():
    """
    Load the latest Portfolio_Positions_*.csv file from /data.
    Returns a cleaned DataFrame or None if not found.
    """
    try:
        files = [
            f for f in os.listdir(DATA_FOLDER)
            if f.startswith("Portfolio_Positions_") and f.endswith(".csv")
        ]
        if not files:
            return None

        latest_file = sorted(files)[-1]  # Pick the most recent
        full_path = os.path.join(DATA_FOLDER, latest_file)

        df = pd.read_csv(full_path)

        required_columns = {"Ticker", "Quantity", "Current Value", "Cost Basis"}
        if not required_columns.issubset(df.columns):
            print(f"❌ Missing required columns in {latest_file}")
            return None

        df["Ticker"] = df["Ticker"].astype(str).str.upper()
        df.fillna(0, inplace=True)

        return df

    except Exception as e:
        print(f"⚠ Portfolio load failed: {e}")
        return None
