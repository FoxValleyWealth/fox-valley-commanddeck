import os
import pandas as pd

DATA_DIR = "data"


def _find_latest_portfolio_file() -> str | None:
    """
    Find the latest Fidelity portfolio CSV in the data/ folder.
    The files are expected to start with 'Portfolio_Positions'.
    """
    try:
        files = [
            f
            for f in os.listdir(DATA_DIR)
            if f.startswith("Portfolio_Positions") and f.endswith(".csv")
        ]
    except FileNotFoundError:
        print("⚠ 'data' directory not found.")
        return None

    if not files:
        print("⚠ No portfolio CSV files found in 'data'.")
        return None

    files.sort()
    latest = files[-1]
    path = os.path.join(DATA_DIR, latest)
    print(f"🗂 Using portfolio file: {latest}")
    return path


def load_portfolio():
    """
    Load the latest Fidelity portfolio export and normalize to standard columns.

    Returns
    -------
    pandas.DataFrame or None
        DataFrame with at least:
        - Ticker
        - Quantity
        - Current Value
        - Total Gain/Loss Dollar
        - Total Gain/Loss Percent

        Returns None if no usable data is found.
    """
    path = _find_latest_portfolio_file()
    if path is None:
        return None

    try:
        df_raw = pd.read_csv(path)

        # Normalize column names (case-insensitive, trimmed)
        col_map = {c.strip().lower(): c for c in df_raw.columns}

        def pick(*candidates):
            """Return the real column name matching any of the candidate keys."""
            for key in candidates:
                key = key.strip().lower()
                if key in col_map:
                    return col_map[key]
            return None

        # Fidelity export uses headers like: Symbol, Quantity, Current Value, Total Gain/Loss Dollar, Total Gain/Loss Percent
        symbol_col = pick("symbol", "ticker")
        qty_col = pick("quantity", "qty")
        value_col = pick("current value", "market value", "current value dollar")
        gain_d_col = pick(
            "total gain/loss dollar",
            "total gain/loss $",
            "total gain/loss",
        )
        gain_p_col = pick(
            "total gain/loss percent",
            "total gain/loss %",
            "total gain/loss percent ",
        )

        required = [symbol_col, qty_col, value_col]
        if any(c is None for c in required):
            print("⚠ Required columns not found in portfolio CSV. Columns detected:")
            print(list(df_raw.columns))
            return None

        df = pd.DataFrame()
        df["Ticker"] = df_raw[symbol_col].astype(str).str.upper()
        df["Quantity"] = pd.to_numeric(df_raw[qty_col], errors="coerce").fillna(0)

        # Clean currency-like field for current value
        current_val_series = (
            df_raw[value_col]
            .astype(str)
            .str.replace(r"[\$,]", "", regex=True)
        )
        df["Current Value"] = pd.to_numeric(current_val_series, errors="coerce").fillna(0.0)

        if gain_d_col is not None:
            v = df_raw[gain_d_col].astype(str).str.replace(r"[\$,]", "", regex=True)
            df["Total Gain/Loss Dollar"] = pd.to_numeric(v, errors="coerce").fillna(0.0)
        else:
            df["Total Gain/Loss Dollar"] = 0.0

        if gain_p_col is not None:
            v = df_raw[gain_p_col].astype(str).str.replace("%", "", regex=True)
            df["Total Gain/Loss Percent"] = pd.to_numeric(v, errors="coerce").fillna(0.0)
        else:
            df["Total Gain/Loss Percent"] = 0.0

        # Filter out positions with zero quantity (e.g., pure cash line)
        df = df[df["Quantity"] > 0].reset_index(drop=True)

        if df.empty:
            print("⚠ Portfolio file loaded but contains no positions with positive quantity.")
            return None

        print(f"✅ Loaded {len(df)} positions from portfolio.")
        return df

    except Exception as e:
        print(f"❌ Error loading portfolio: {e}")
        return None


if __name__ == "__main__":
    # Simple CLI check if you ever need it
    portfolio = load_portfolio()
    if portfolio is None:
        print("No portfolio data available.")
    else:
        print(portfolio.head())
