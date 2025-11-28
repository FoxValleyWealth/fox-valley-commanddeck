import pandas as pd
import os
import glob

def load_portfolio_data():
    try:
        # Find the latest Fidelity portfolio file
        portfolio_files = glob.glob("data/Portfolio_Positions*.csv")
        if not portfolio_files:
            return None

        latest_file = max(portfolio_files, key=os.path.getmtime)

        # Load with safe settings for Fidelity CSV format
        df = pd.read_csv(
            latest_file,
            engine="python",
            on_bad_lines="skip"
        )

        # 🚨 Normalize column names
        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
            .str.replace(r"[^a-zA-Z0-9]", "", regex=True)
            .str.upper()
        )

        # 🚨 Required columns — minimal to activate dashboard
        required = ["SYMBOL", "QUANTITY", "CURRENTVALUE"]
        if not all(col in df.columns for col in required):
            return None

        # 🚨 Final cleaning
        df["SYMBOL"] = df["SYMBOL"].str.upper().str.strip()
        df = df[df["SYMBOL"].notna()]

        # Make it ready for Tactical Grid
        return df.reset_index(drop=True)

    except Exception as e:
        return None
