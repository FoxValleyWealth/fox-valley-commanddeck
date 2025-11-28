import pandas as pd
import os

def load_portfolio_data():
    try:
        # Detect Fidelity-style portfolio file
        portfolio_files = [f for f in os.listdir("data") if f.startswith("Portfolio_Positions")]
        if not portfolio_files:
            return None

        # Always use the latest portfolio export
        latest_file = sorted(portfolio_files)[-1]
        df = pd.read_csv(f"data/{latest_file}")

        # Normalize column names for mapping
        df.columns = df.columns.str.strip().str.replace(" ", "").str.replace("/", "").str.upper()

        # Map Fidelity export to Command Deck schema
        df = df.rename(columns={
            "SYMBOL": "Ticker",
            "DESCRIPTION": "Description",
            "QUANTITY": "Quantity",
            "LASTPRICE": "LastPrice",
            "CURRENTVALUE": "CurrentValue"
        })

        # Ensure minimal required columns
        required_columns = ["Ticker", "Description", "Quantity", "LastPrice", "CurrentValue"]
        for col in required_columns:``
            if col not in df.columns:
                df[col] = None  # Placeholder for missing data

        # Uppercase tickers
        df["Ticker"] = df["Ticker"].astype(str).str.upper()

        # Trim to required dashboard schema
        return df[required_columns]

    except Exception as e:
        print(f"Portfolio Load Error: {e}")
        return None
