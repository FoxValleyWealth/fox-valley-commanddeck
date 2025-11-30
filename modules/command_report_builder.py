import pandas as pd

# =========================================================
# 📑 Fox Valley Command Report Builder — v7.7R Final Build
# Generates full tactical command narrative for reporting.
# Combines:
# • Portfolio summary
# • Tactical Alerts
# • Risk Heatmap (if available)
# • Tactical Scores
# • Intelligence Brief
# Returns a formatted narrative report string
# =========================================================

def build_command_report(
    portfolio_df=None,
    risk_df=None,
    alerts_list=None,
    tactical_scores_df=None,
    intelligence_brief_text=None
):
    sections = []
    sections.append("🧭 FOX VALLEY TACTICAL COMMAND REPORT — v7.7R\n")

    # ===== 1️⃣ Portfolio Overview =====
    sections.append("📊 PORTFOLIO OVERVIEW")
    if portfolio_df is not None and not portfolio_df.empty:
        total_value = portfolio_df["Current Value"].sum()
        sections.append(f"• Total Portfolio Value: ${total_value:,.2f}")
        sections.append(f"• Number of Active Positions: {len(portfolio_df)}")

        top_holding = portfolio_df.sort_values("Current Value", ascending=False).iloc[0]
        sections.append(
            f"• Largest Position: {top_holding['Ticker']} — "
            f"${top_holding['Current Value']:,.2f}\n"
        )
    else:
        sections.append("⚠ No portfolio data available.\n")

    # ===== 2️⃣ Tactical Risk Heatmap (if available) =====
    sections.append("🛡 RISK HEATMAP ANALYSIS")
    if risk_df is not None and not risk_df.empty:
        high_risk = risk_df[risk_df["Risk Level"].isin(["HIGH", "CRITICAL"])]
        if not high_risk.empty:
            sections.append("⚠ High Exposure Positions:")
            for _, row in high_risk.iterrows():
                sections.append(
                    f"   • {row['Ticker']} — {row['Risk Level']} Risk "
                    f"(StopRisk {row['StopRisk %']}%, Weight {row['CapitalWeight %']}%)"
                )
        else:
            sections.append("• No HIGH or CRITICAL risk positions at this time.\n")
    else:
        sections.append("⚠ No risk heatmap data available.\n")

    # ===== 3️⃣ Tactical Alerts =====
    sections.append("\n🚨 TACTICAL ALERTS")
    if alerts_list:
        for alert in alerts_list:
            sections.append(f"• {alert}")
    else:
        sections.append("📈 No tactical alerts triggered.\n")

    # ===== 4️⃣ Tactical Scoring Highlights =====
    sections.append("\n🧠 TACTICAL SCORING LEADERS")
    if tactical_scores_df is not None and not tactical_scores_df.empty:
        top_scores = tactical_scores_df.sort_values("TacticalScore", ascending=False).head(3)
        for _, row in top_scores.iterrows():
            sections.append(
                f"   • {row['Ticker']} — Score {int(row['TacticalScore'])} "
                f"({row['Tactical Priority']})"
            )
    else:
        sections.append("⚠ Tactical scoring not available.\n")

    # ===== 5️⃣ Intelligence Brief (Narrative) =====
    sections.append("\n📘 TACTICAL INTELLIGENCE BRIEF")
    if intelligence_brief_text:
        sections.append(intelligence_brief_text)
    else:
        sections.append("⚠ Intelligence Brief not available.\n")

    # ===== End =====
    sections.append("\n🧭 END OF COMMAND REPORT")
    return "\n".join(sections)


# ============================ EXPORT HELPERS ============================

def command_report_to_textfile(report_text, filename="command_report.txt"):
    """Exports tactical report to a plain text file."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(report_text)
    return filename
