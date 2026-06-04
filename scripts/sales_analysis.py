"""
Sales Performance Analysis — Python equivalent of the Power BI KPIs.

Generates synthetic data matching the dashboard's structure, computes all
KPI measures, and produces publication-quality charts saved to /output/.

Run:
    python scripts/sales_analysis.py
"""

import os
import random
from datetime import date, timedelta

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Colour palette (matches Power BI corporate theme) ────────────────────────
GOLD   = "#F2C811"
DARK   = "#1A1A2E"
BLUE   = "#16213E"
ACCENT = "#0F3460"
RED    = "#E94560"
GREEN  = "#00B894"
GREY   = "#636E72"
WHITE  = "#FFFFFF"

plt.rcParams.update({
    "figure.facecolor": DARK,
    "axes.facecolor":   BLUE,
    "axes.edgecolor":   GREY,
    "axes.labelcolor":  WHITE,
    "xtick.color":      WHITE,
    "ytick.color":      WHITE,
    "text.color":       WHITE,
    "grid.color":       ACCENT,
    "grid.linewidth":   0.5,
    "font.family":      "DejaVu Sans",
})

# ── Synthetic data matching the dashboard dataset ─────────────────────────────
CATEGORIES   = ["Accessories", "Bikes", "Clothing"]
CAT_WEIGHTS  = [0.55, 0.25, 0.20]
COUNTRIES    = ["United States", "United Kingdom", "Germany", "France", "Australia", "Canada"]
OCCUPATIONS  = ["Professional", "Skilled Manual", "Management", "Clerical", "Manual"]
PRODUCTS     = [
    "Water Bottle – 30oz", "Sport-100 Helmet (Red)", "Sport-100 Helmet (Black)",
    "Mountain Tire Tube", "Road Tire Tube", "Patch Kit", "Mountain Bottle Cage",
    "Road Bottle Cage", "HL Road Frame", "HL Mountain Frame",
]

random.seed(42)
np.random.seed(42)


def generate_orders(n: int = 11_800) -> pd.DataFrame:
    start = date(2020, 1, 1)
    end   = date(2022, 12, 31)
    days  = (end - start).days

    records = []
    customer_ids = [f"C{i:05d}" for i in range(1, 17_401)]

    for _ in range(n):
        order_date  = start + timedelta(days=random.randint(0, days))
        category    = random.choices(CATEGORIES, weights=CAT_WEIGHTS)[0]
        unit_price  = np.random.lognormal(5.5, 1.2) if category == "Bikes" else np.random.lognormal(3.5, 0.9)
        unit_cost   = unit_price * random.uniform(0.45, 0.65)
        quantity    = random.choices([1, 2, 3, 4], weights=[0.70, 0.18, 0.08, 0.04])[0]
        returned    = random.random() < 0.021

        records.append({
            "order_date":   order_date,
            "customer_id":  random.choice(customer_ids),
            "product":      random.choice(PRODUCTS),
            "category":     category,
            "country":      random.choices(COUNTRIES, weights=[0.35, 0.18, 0.15, 0.12, 0.12, 0.08])[0],
            "occupation":   random.choice(OCCUPATIONS),
            "unit_price":   round(unit_price, 2),
            "unit_cost":    round(unit_cost, 2),
            "quantity":     quantity,
            "revenue":      round(unit_price * quantity, 2),
            "cost":         round(unit_cost  * quantity, 2),
            "returned":     returned,
        })

    df = pd.DataFrame(records)
    df["profit"]      = df["revenue"] - df["cost"]
    df["order_month"] = pd.to_datetime(df["order_date"]).dt.to_period("M")
    df["year"]        = pd.to_datetime(df["order_date"]).dt.year
    return df


def print_kpi_summary(df: pd.DataFrame) -> None:
    total_revenue  = df["revenue"].sum()
    total_profit   = df["profit"].sum()
    profit_margin  = total_profit / total_revenue * 100
    total_orders   = len(df)
    unique_cust    = df["customer_id"].nunique()
    rev_per_cust   = total_revenue / unique_cust
    return_rate    = df["returned"].mean() * 100
    growth_target  = total_revenue * 1.10

    print("\n" + "═" * 55)
    print("  SALES PERFORMANCE — EXECUTIVE KPI SUMMARY")
    print("═" * 55)
    print(f"  Total Revenue       : ${total_revenue:>12,.0f}")
    print(f"  Total Profit        : ${total_profit:>12,.0f}")
    print(f"  Profit Margin       : {profit_margin:>11.1f}%")
    print(f"  Total Orders        : {total_orders:>12,}")
    print(f"  Unique Customers    : {unique_cust:>12,}")
    print(f"  Revenue / Customer  : ${rev_per_cust:>12,.0f}")
    print(f"  Return Rate         : {return_rate:>11.2f}%")
    print(f"  +10% Growth Target  : ${growth_target:>12,.0f}")
    print("═" * 55 + "\n")


# ── Chart 1: Monthly Revenue vs Target ───────────────────────────────────────
def plot_revenue_trend(df: pd.DataFrame) -> None:
    monthly = df.groupby("order_month")["revenue"].sum().reset_index()
    monthly["order_month"] = monthly["order_month"].astype(str)
    monthly["target"]      = monthly["revenue"].mean() * 1.05

    fig, ax = plt.subplots(figsize=(14, 5))
    ax.fill_between(monthly["order_month"], monthly["revenue"], alpha=0.15, color=GOLD)
    ax.plot(monthly["order_month"], monthly["revenue"], color=GOLD,   linewidth=2.5, label="Actual Revenue",  marker="o", markersize=4)
    ax.plot(monthly["order_month"], monthly["target"],  color=RED,    linewidth=1.5, label="Monthly Target",  linestyle="--")

    peak_idx = monthly["revenue"].idxmax()
    ax.annotate(
        f"Peak\n${monthly.loc[peak_idx,'revenue']:,.0f}",
        xy=(monthly.loc[peak_idx,"order_month"], monthly.loc[peak_idx,"revenue"]),
        xytext=(peak_idx - 3, monthly["revenue"].max() * 0.88),
        arrowprops=dict(arrowstyle="->", color=WHITE),
        color=WHITE, fontsize=9,
    )

    ax.set_title("Monthly Revenue vs Target", fontsize=14, fontweight="bold", pad=15, color=WHITE)
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue (USD)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M"))
    ax.legend(facecolor=BLUE, edgecolor=GREY, labelcolor=WHITE)
    plt.xticks(rotation=45, ha="right", fontsize=7)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/01_revenue_trend.png", dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {OUTPUT_DIR}/01_revenue_trend.png")


# ── Chart 2: Profit by Country ────────────────────────────────────────────────
def plot_country_performance(df: pd.DataFrame) -> None:
    country_df = df.groupby("country").agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
        orders=("revenue", "count"),
    ).sort_values("revenue", ascending=True)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    colors_rev = [GREEN if v > country_df["revenue"].median() else GOLD for v in country_df["revenue"]]
    axes[0].barh(country_df.index, country_df["revenue"], color=colors_rev, edgecolor=DARK, linewidth=0.5)
    axes[0].set_title("Revenue by Country", fontsize=12, fontweight="bold", color=WHITE)
    axes[0].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M"))

    colors_pro = [GREEN if v > 0 else RED for v in country_df["profit"]]
    axes[1].barh(country_df.index, country_df["profit"], color=colors_pro, edgecolor=DARK, linewidth=0.5)
    axes[1].set_title("Profit by Country", fontsize=12, fontweight="bold", color=WHITE)
    axes[1].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M"))

    for ax in axes:
        ax.grid(axis="x", alpha=0.3)
        ax.spines[["top", "right"]].set_visible(False)

    plt.suptitle("Geographic Performance", fontsize=14, fontweight="bold", color=WHITE, y=1.02)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/02_country_performance.png", dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {OUTPUT_DIR}/02_country_performance.png")


# ── Chart 3: Category & Product Analysis ─────────────────────────────────────
def plot_category_analysis(df: pd.DataFrame) -> None:
    cat_df = df.groupby("category").agg(
        revenue=("revenue", "sum"),
        orders=("revenue", "count"),
        return_rate=("returned", "mean"),
    ).sort_values("revenue", ascending=False)

    prod_df = df.groupby("product").agg(
        revenue=("revenue", "sum"),
        return_rate=("returned", "mean"),
    ).sort_values("revenue", ascending=True).tail(10)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    bars = axes[0].bar(cat_df.index, cat_df["revenue"], color=[GOLD, ACCENT, GREEN], edgecolor=DARK, linewidth=0.5, width=0.5)
    for bar, ret in zip(bars, cat_df["return_rate"]):
        axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20000,
                     f"{ret*100:.1f}% ret.", ha="center", va="bottom", fontsize=8, color=RED)
    axes[0].set_title("Revenue by Category\n(return rate labelled)", fontsize=11, fontweight="bold", color=WHITE)
    axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M"))

    colors_p = [RED if r > 0.025 else GOLD for r in prod_df["return_rate"]]
    axes[1].barh(prod_df.index, prod_df["revenue"], color=colors_p, edgecolor=DARK, linewidth=0.5)
    axes[1].set_title("Top 10 Products by Revenue\n(red = high return rate)", fontsize=11, fontweight="bold", color=WHITE)
    axes[1].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1e3:.0f}K"))

    for ax in axes:
        ax.grid(axis="y" if ax == axes[0] else "x", alpha=0.3)
        ax.spines[["top", "right"]].set_visible(False)

    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/03_category_products.png", dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {OUTPUT_DIR}/03_category_products.png")


# ── Chart 4: Customer Segmentation ───────────────────────────────────────────
def plot_customer_segmentation(df: pd.DataFrame) -> None:
    seg_df = df.groupby("occupation")["revenue"].sum().sort_values(ascending=False)

    top_cust = (
        df.groupby("customer_id")["revenue"].sum()
        .sort_values(ascending=False)
        .head(20)
        .reset_index()
    )
    top_cust["rank"] = range(1, 21)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    wedge_colors = [GOLD, GREEN, ACCENT, GREY, RED]
    wedges, texts, autotexts = axes[0].pie(
        seg_df.values,
        labels=seg_df.index,
        autopct="%1.1f%%",
        colors=wedge_colors[:len(seg_df)],
        startangle=140,
        wedgeprops={"edgecolor": DARK, "linewidth": 1.5},
        textprops={"color": WHITE},
    )
    for at in autotexts:
        at.set_fontsize(9)
    axes[0].set_title("Revenue by Occupation", fontsize=12, fontweight="bold", color=WHITE)

    axes[1].scatter(top_cust["rank"], top_cust["revenue"], color=GOLD, s=80, zorder=3, edgecolors=WHITE, linewidths=0.5)
    axes[1].fill_between(top_cust["rank"], top_cust["revenue"], alpha=0.1, color=GOLD)
    axes[1].set_title("Top 20 Customers by Revenue", fontsize=12, fontweight="bold", color=WHITE)
    axes[1].set_xlabel("Customer Rank")
    axes[1].set_ylabel("Revenue (USD)")
    axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    axes[1].grid(alpha=0.3)
    axes[1].spines[["top", "right"]].set_visible(False)

    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/04_customer_segmentation.png", dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {OUTPUT_DIR}/04_customer_segmentation.png")


def main():
    print("\nGenerating synthetic sales dataset...")
    df = generate_orders(11_800)
    print(f"  {len(df):,} orders | {df['customer_id'].nunique():,} customers | {df['order_date'].min()} → {df['order_date'].max()}")

    print_kpi_summary(df)

    print("Generating charts...")
    plot_revenue_trend(df)
    plot_country_performance(df)
    plot_category_analysis(df)
    plot_customer_segmentation(df)

    print(f"\nAll charts saved to ./{OUTPUT_DIR}/")
    print("Done.\n")


if __name__ == "__main__":
    main()
