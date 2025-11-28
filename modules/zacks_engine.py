"""
Zacks Screening Engine — v7.7R-Patch2
Handles loading and parsing of Zacks Growth / Defensive screens.
"""

import os
import pandas as pd

DATA_PATH = "data"

def load_zacks_screens():
    """Load all Zacks screen files (Growth1, Growth2, Defensive)."""
    screens = {}
    try:
        for file in os.listdir(DATA_PATH):
            if "Growth 1" in file:
                screens["Growth 1"] = pd.read_csv(os.path.join(DATA_PATH, file))
            elif "Growth 2" in file:
                screens["Growth 2"] = pd.read_csv(os.path.join(DATA_PATH, file))
            elif "Defensive" in file:
                screens["Defensive Dividends"] = pd.read_csv(os.path.join(DATA_PATH, file))
    except Exception:
        return {}

    return screens


def get_zacks_summary(screens: dict):
    """Return summary info for tactical_dashboard (counts, filenames)."""
    return {
        "total_files": len(screens),
        "file_list": list(screens.keys())
    }


def merge_with_portfolio(portfolio_df, screens: dict):
    """
    Merge screening results with portfolio data.
    Key: Ticker symbol.
    """
    if not screens:
        return portfolio_df  # No data to merge

    for name, df in screens.items():
        if "Ticker" in df.columns:
            df["Ticker"] = df["Ticker"].str.upper()
            portfolio_df = portfolio_df.merge(
                df[["Ticker", "Zacks Rank"]],
                on="Ticker",
                how="left",
                suffixes=("", f"_{name.replace(' ', '_')}")
            )

    return portfolio_df
