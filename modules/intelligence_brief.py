import pandas as pd

# =========================================================
# 📘 Intelligence Brief Engine — v7.7R Final Stable Build
# Generates full tactical narrative summary for dashboard
# =========================================================

def generate_intelligence_brief(portfolio_df=None, zacks_df=None, cash_value=None, scored_df=None):
    brief = []
    brief.append("🧭 Fox Valley Tactical Intelligence Brief — v7.7R\n")

    # ===== 1️⃣ Cash Posture =====
    if cash_value is not None:
        if cash_value == 0:
            brief.append("💰 Cash fully depleted — No tactical flexibility available.")
        elif cash_value < 5000:
            brief.append(f"💰 Marginal cash position (${cash_value:,.2f}) — severely limited options.")
        elif cash_value < 20000:
            brief.append(f"💰 Moderate tactical liquidity (${cash_value:,.2f}) — controlled deployments possible.")
        else:
            brief.append(f"💰 Strong liquidity at **${cash_value:,.2f}** — deployment-ready.")
    else:
        brief.append("💰 Cash status unknown.")
    brief.append("---")

    # ===== 2️⃣ Portfolio Strength Summary =====
    if portfolio_df is not None and not portfolio_df.empty:
        total_positions = len(portfolio_df)
        winners = portfolio_df[portfolio_df["Gain/Loss $"] > 0]
        losers = portfolio_df[portfolio_df["Gain/Loss $"] < 0]

        brief.append(f"📊 Active holdings: **{total_positions} positions**")
        brief.append(f"✔ {len(winners)} profitable • ✘ {len(losers)} under cost basis")

        if not winners.empty:
            top_gain = winners.sort_values("Gain/Loss $", ascending=False).iloc[0]
            brief.append(f"🔥 Top performer: **{top_gain['Ticker']}** — Gain ${top_gain['Gain/Loss $']:,.2f}")

        if not losers.empty:
            top_loss = losers.sort_values("Gain/Loss $", ascending=True).iloc[0]
            brief.append(f"⚠ Highest risk exposure: **{top_loss['Ticker']}** — Loss ${abs(top_loss['Gain/Loss $']):,.2f}")
    else:
        brief.append("📊 No portfolio data available.")
    brief.append("---")

    # ===== 3️⃣ Zacks Rank Tactical Highlights =====
    if zacks_df is not None and not zacks_df.empty:
        rank1 = zacks_df[zacks_df["zacks_rank"] == 1]
        if not rank1.empty:
            tickers = ", ".join(rank1["ticker"].head(6).tolist())
            brief.append(f"🎯 High-priority Rank 1 candidates: **{tickers}**")

            top_cap = rank1.sort_values("market_cap", ascending=False).iloc[0]
            brief.append(f"🏆 Largest candidate: **{top_cap['ticker']}** — Market Cap ${top_cap['market_cap']:,.0f}M")
        else:
            brief.append("🎯 No current Rank 1 Zacks candidates.")
    else:
        brief.append("🗂 Zacks scan data unavailable.")
    brief.append("---")

    # ===== 4️⃣ Tactical Scoring Intelligence =====
    if scored_df is not None and not scored_df.empty:
        top_score = scored_df.sort_values("TacticalScore", ascending=False).iloc[0]
        brief.append(
            f"🧠 Tactical Strength Leader: **{top_score['Ticker']}** — "
            f"Score {int(top_score['TacticalScore'])} ({top_score['Tactical Priority']})."
        )
    brief.append("---")

    # ===== 5️⃣ Final Tactical Outlook =====
    brief.append(
        "🔎 Tactical Outlook:\n"
        "• Review trailing-stop proximity and risk clusters\n"
        "• Prioritize Rank 1 + high TacticalScore candidates\n"
        "• Monitor capital concentration in weak positions\n"
        "• Assess feasibility of strategic deployment based on liquidity\n"
    )
    brief.append("🧭 End of Tactical Intelligence Brief.")
    return "\n".join(brief)
