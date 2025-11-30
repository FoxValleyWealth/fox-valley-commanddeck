import pandas as pd

# =========================================================
# Trailing Stop Manager — v7.7R Final Stable Build
# Supports fixed and custom trailing stops
# =========================================================


def apply_trailing_stop(df, trailing_stop_pct=5):
    """
    Applies a universal trailing stop (percentage-based)
    Example:
        If Current Price = $100 and Stop = 5%
        Stop Price = $95
    """
    if df.empty or "Current Price" not in df.columns:
        return df

    df["Stop Price"] = (df["Current Price"] * (1 - trailing_stop_pct / 100)).round(2)
    df["Protection Gap %"] = (
        (df["Current Price"] - df["Stop Price"]) / df["Current Price"] * 100
    ).round(2)

    return df


def apply_custom_trailing_stops(df, stop_dict):
    """
    Apply custom trailing stops based on specific stock risk.
    stop_dict format example:
        {
            'NVDA': 7.5,
            'CNQ': 4,
            'XPER': 6,
        }
    Stocks not listed in stop_dict use 5% default.
    """
    if df.empty:
        return df

    df["Stop Price"] = None
    df["Protection Gap %"] = None

    for idx, row in df.iterrows():
        ticker = row.get("Ticker", None)
        price = row.get("Current Price", None)

        if pd.isna(ticker) or pd.isna(price):
            continue

        pct = stop_dict.get(ticker, 5)
        stop_price = round(price * (1 - pct / 100), 2)
        gap_pct = round(((price - stop_price) / price) * 100, 2)

        df.loc[df["Ticker"] == ticker, "Stop Price"] = stop_price
        df.loc[df["Ticker"] == ticker, "Protection Gap %"] = gap_pct

    return df
