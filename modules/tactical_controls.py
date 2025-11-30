# =========================================================
# 🎯 Tactical Controls — v7.7R Final Stable Build
# Simulated Trade Control System for Command Deck
# Supports: BUY | SELL | TRIM | HOLD
# No real brokerage integration — safe execution
# =========================================================

def process_tactical_action(action_type, ticker, shares):
    """
    Handles tactical action requests for Buy, Sell, Trim, Hold.
    
    Parameters:
        action_type (str): BUY, SELL, TRIM, HOLD
        ticker (str): Stock symbol (e.g., NVDA)
        shares (int/float): Number of shares
    
    Returns:
        str: Confirmation message for dashboard display.
    """

    if not ticker:
        return "⚠ Invalid action — Ticker is required."

    if action_type.upper() in ["BUY", "SELL", "TRIM"] and (not shares or shares <= 0):
        return f"⚠ Invalid share quantity for {action_type}."

    action_type = action_type.upper()

    if action_type == "BUY":
        return f"🟢 Tactical BUY order queued — {shares} shares of {ticker}."

    elif action_type == "SELL":
        return f"🔴 Tactical SELL order queued — {shares} shares of {ticker}."

    elif action_type == "TRIM":
        return f"🟠 Tactical TRIM order queued — reduce {ticker} by {shares} shares."

    elif action_type == "HOLD":
        return f"🟡 HOLD — No action taken for {ticker}."

    else:
        return f"⚠ Unknown action type: {action_type}. Must be BUY, SELL, TRIM, or HOLD."
