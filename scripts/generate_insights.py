"""
Auto-generate executive insight bullets from the sales dataset.

Mirrors the Key Insights section of the Power BI dashboard in plain text.
Useful for scheduled email reports or Slack notifications.

Run:
    python scripts/generate_insights.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from sales_analysis import generate_orders
import pandas as pd
import numpy as np


def compute_insights(df: pd.DataFrame) -> list[str]:
    insights = []

    # Revenue peak
    monthly = df.groupby("order_month")["revenue"].sum()
    peak_month = monthly.idxmax()
    peak_val   = monthly.max()
    insights.append(f"Revenue peaked at ${peak_val:,.0f} in {peak_month} — highest single month on record.")

    # MoM growth
    monthly_sorted = monthly.sort_index()
    mom_pct = monthly_sorted.pct_change().dropna() * 100
    avg_mom = mom_pct.mean()
    insights.append(f"Average month-over-month revenue growth: {avg_mom:+.1f}%.")

    # Top product
    top_product = df.groupby("product")["revenue"].sum().idxmax()
    top_rev     = df.groupby("product")["revenue"].sum().max()
    insights.append(f"Top-selling product: '{top_product}' — ${top_rev:,.0f} in total revenue.")

    # Highest return category
    cat_ret = df.groupby("category")["returned"].mean() * 100
    worst_cat = cat_ret.idxmax()
    insights.append(f"'{worst_cat}' has the highest return rate at {cat_ret.max():.2f}% — review product quality or descriptions.")

    # Top country
    top_country = df.groupby("country")["revenue"].sum().idxmax()
    top_c_rev   = df.groupby("country")["revenue"].sum().max()
    insights.append(f"{top_country} leads geographically with ${top_c_rev:,.0f} revenue ({top_c_rev/df['revenue'].sum()*100:.1f}% of total).")

    # Top occupation
    top_occ     = df.groupby("occupation")["revenue"].sum().idxmax()
    top_occ_rev = df.groupby("occupation")["revenue"].sum().max()
    insights.append(f"'{top_occ}' customers drive the most revenue: ${top_occ_rev:,.0f}.")

    # Top customer
    top_cust    = df.groupby("customer_id")["revenue"].sum().idxmax()
    top_cust_r  = df.groupby("customer_id")["revenue"].sum().max()
    insights.append(f"Highest-value customer ({top_cust}) generated ${top_cust_r:,.0f} in revenue.")

    # Growth projection
    total_rev   = df["revenue"].sum()
    target      = total_rev * 1.10
    delta       = target - total_rev
    insights.append(f"10% growth target: ${target:,.0f} — requires ${delta:,.0f} incremental revenue.")

    # Accessories dominance
    acc_share = df[df["category"] == "Accessories"]["revenue"].sum() / df["revenue"].sum() * 100
    insights.append(f"Accessories account for {acc_share:.1f}% of total orders — highest category share.")

    # Overall profit margin
    margin = df["profit"].sum() / df["revenue"].sum() * 100
    insights.append(f"Overall profit margin: {margin:.1f}% — target is >40% for healthy operations.")

    return insights


def main():
    print("\nGenerating dataset...")
    df = generate_orders(11_800)

    print("\n" + "═" * 60)
    print("  EXECUTIVE INSIGHTS — AUTO-GENERATED")
    print("═" * 60)
    insights = compute_insights(df)
    for i, insight in enumerate(insights, 1):
        print(f"\n  {i}. {insight}")
    print("\n" + "═" * 60 + "\n")


if __name__ == "__main__":
    main()
