import pandas as pd

# === Portfolio Engine — Full Tactical Version (v7.7R) ===
# Powers: Portfolio Overview | Risk Heatmap | Tactical Scoring | Intelligence Brief | PDF Reports

def load_portfolio_data(uploaded_file):
    """
    Fully tactical portfolio loader & calculator.
    """
    if uploaded_file is None:
        return None

    try:
        # Read uploaded CSV
        df = pd.read_csv(uploaded_file)

        # Standardize expected columns
        rename_map = {
            'Symbol': 'Ticker',
            'Quantity': 'Shares',
            'Last Price': 'Current Price',
            'Cost Basis Total': 'Cost Basis Total',
            'Cost Basis': 'Cost Basis',  # Already processed version
        }
        df.rename(columns=rename_map, inplace=True)

        # Clean numbers: remove $/commas and convert to numeric
        currency_columns = ['Current Price', 'Cost Basis Total', 'Cost Basis']
        for col in currency_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col].astype(str).str.replace('[\$,]', '', regex=True), errors='coerce')

        # === Compute Cost Basis per share if only total is provided ===
        if 'Cost Basis' not in df.columns and 'Cost Basis Total' in df.columns and 'Shares' in df.columns:
            df['Cost Basis'] = df['Cost Basis Total'] / df['Shares']

        # === Compute Market Value ===
        df['Market Value'] = df['Shares'] * df['Current Price']

        # === Compute Gain/Loss Dollar ===
        df['Gain/Loss $'] = (df['Current Price'] - df['Cost Basis']) * df['Shares']

        # === Compute Gain/Loss Percent ===
        df['Gain/Loss %'] = ((df['Current Price'] - df['Cost Basis']) / df['Cost Basis']) * 100

        # === Trailing Stop Price (Default 15% unless overridden in Dashboard) ===
        DEFAULT_STOP_PERCENT = 15
        df['Trailing Stop Price'] = df['Current Price'] * (1 - DEFAULT_STOP_PERCENT / 100)

        # === Basic Risk Level (for Heatmap) ===
        def risk_level(row):
            if row['Gain/Loss %'] < -10:
                return "High Risk"
            elif row['Gain/Loss %'] < 0:
                return "Moderate Risk"
            else:
                return "Stable"

        df['Risk Level'] = df.apply(risk_level, axis=1)

        # === Tactical Score Placeholder (integrates w/ Tactical Scoring Engine) ===
        df['Tactical Score'] = None  # Will be filled by scoring engine

        # === Final Clean Columns ===
        required_cols = [
            'Ticker', 'Shares', 'Cost Basis', 'Current Price',
            'Market Value', 'Gain/Loss $', 'Gain/Loss %',
            'Trailing Stop Price', 'Risk Level', 'Tactical Score'
        ]
        for col in required_cols:
            if col not in df.columns:
                df[col] = None

        return df

    except Exception as e:
        print(f"ERROR — Portfolio Engine Load Failure: {e}")
        return None


def calculate_portfolio_summary(df):
    """
    Tactical summary for Dashboard + Executive Reports.
    Returns total value, total gain, avg gain%, and risk distribution.
    """
    if df is None or df.empty:
        return None

    total_value = df['Market Value'].sum()
    total_gain = df['Gain/Loss $'].sum()
    avg_gain_pct = df['Gain/Loss %'].mean()

    risk_counts = df['Risk Level'].value_counts().to_dict()

    return {
        "total_value": total_value,
        "total_gain": total_gain,
        "avg_gain_pct": avg_gain_pct,
        "risk_distribution": risk_counts
    }
