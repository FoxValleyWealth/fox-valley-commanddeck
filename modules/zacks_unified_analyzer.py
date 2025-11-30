import pandas as pd

# =========================================================
# 📁 Zacks Unified Analyzer — v7.7R Final Stable Build
# Merges Growth1, Growth2, Dividend screens into one dataset
# Extracts high-priority Rank 1 candidates
# Provides clean export for dashboard and risk/reporting engines
# =========================================================

def load_zacks_file(file_path, screen_source):
    """
    Loads and standardizes a Zacks screen file.
    Expected columns may vary, so we normalize to:
    Ticker, Zacks Rank, Name, Industry, Market Cap, PE, PEG, Price
    """
    try:
        df = pd.read_csv(file_path)
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
        df["screen_source"] = screen_source

        required = [
            "ticker", "zacks_rank", "name", "industry",
            "market_cap", "pe", "peg", "price"
        ]
        for col in required:
            if col not in df.columns:
                df[col] = None

        return df[required + ["screen_source"]]

    except Exception as e:
        print(f"Error loading Zacks file ({screen_source}): {e}")
        return pd.DataFrame()


def merge_zacks_screens(files_dict):
    """
    Accepts dict of uploaded files:
    {
        'Growth1': file1,
        'Growth2': file2,
        'Dividend': file3
    }
    Returns unified DataFrame.
    """
    merged_frames = []

    for screen_name, file_path in files_dict.items():
        if file_path:
            df = load_zacks_file(file_path, screen_name)
            if not df.empty:
                merged_frames.append(df)

    if not merged_frames:
        print("No Zacks files loaded.")
        return pd.DataFrame()

    unified = pd.concat(merged_frames, ignore_index=True)
    unified["zacks_rank"] = pd.to_numeric(unified["zacks_rank"], errors="coerce")
    unified["market_cap"] = pd.to_numeric(unified["market_cap"], errors="coerce")

    unified.sort_values(by="zacks_rank", inplace=True)
    unified.drop_duplicates(subset=["ticker"], keep="first", inplace=True)

    return unified.reset_index(drop=True)


def extract_rank1_candidates(df):
    """
    Returns only Zacks Rank = 1 stocks,
    sorted by descending Market Cap (highest first).
    """
    if df.empty:
        return pd.DataFrame()

    rank1 = df[df["zacks_rank"] == 1].copy()
    rank1["market_cap"] = pd.to_numeric(rank1["market_cap"], errors="coerce")
    rank1.sort_values(by="market_cap", ascending=False, inplace=True)

    return rank1.reset_index(drop=True)


def prepare_zacks_export(df):
    """
    Standard export format for dashboards and scoring modules.
    """
    if df.empty:
        return df

    export_cols = [
        "ticker", "name", "zacks_rank", "industry",
        "market_cap", "pe", "peg", "price", "screen_source"
    ]
    return df[export_cols].copy()
