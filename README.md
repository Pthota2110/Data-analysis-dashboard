<div align="center">

# Sales Performance Intelligence Dashboard

### End-to-end Business Intelligence solution — from raw data to executive-ready insights

[![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/)
[![Excel](https://img.shields.io/badge/Excel-217346?style=for-the-badge&logo=microsoft-excel&logoColor=white)](https://www.microsoft.com/excel)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![DAX](https://img.shields.io/badge/DAX-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)](https://learn.microsoft.com/dax/)
[![CI](https://img.shields.io/badge/CI-GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)](/.github/workflows/validate.yml)

</div>

---

## Business Problem

A multi-national sales organization needed a single source of truth to track revenue, profitability, customer behaviour, and product performance across **6 countries**. Executives were relying on disconnected Excel sheets with no trend visibility or growth projections.

**This project delivers** a fully interactive Power BI dashboard that replaces manual reporting with live KPIs, drill-through analysis, and a modelled **+10% growth projection** — enabling data-driven decisions at every level of the business.

---

## Key Results

<div align="center">

| Metric | Value | Insight |
|:---:|:---:|:---|
| **Total Revenue** | $9.2M | Exceeded forecast in 3 of 4 quarters |
| **Net Profit** | $3.9M | 42% profit margin |
| **Total Orders** | 11,800 | Accessories drove the highest volume |
| **Unique Customers** | 17,400 | Avg. $1,431 revenue per customer |
| **Return Rate** | 2.1% | Helmets flagged as highest-return category |
| **Peak Month** | May 2022 | $1.83M — identified seasonal trend |
| **Growth Projection** | +10% | DAX-modelled incremental revenue target |

</div>

---

## Dashboard Pages

> Open `Sales-Dashbaords.pbix` in Power BI Desktop to explore the full interactive report.
> A PDF snapshot is available in `Sales Repots.pdf`.

### Page 1 — Executive Overview
Revenue vs. target trendline, profit/loss breakdown, and 10% growth projection across all regions. KPI cards give at-a-glance performance status for executives.

### Page 2 — Product & Category Analysis
Top 10 products ranked by revenue with return rate overlay. Category split (Accessories / Bikes / Clothing) with weekly order volume and MoM comparisons.

### Page 3 — Geographic Intelligence
Country-level performance across US, UK, Germany, France, Australia, and Canada. Drill-through to region-specific profit/loss and customer distribution.

### Page 4 — Customer Analytics
17.4K customer segmentation by income level and occupation (Professional, Skilled Manual, Management). Top 100 customers ranked by revenue with full order history.

---

## Data Pipeline

```
Raw Excel Files
      │
      ▼
┌─────────────────────────────┐
│   Excel — Data Cleaning     │  Nulls removed, dates standardised,
│                             │  lookup tables merged, types fixed
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│  Power BI — Data Model      │  Star schema: fact_Sales linked to
│  (Star Schema)              │  dim_Customer, dim_Product,
│                             │  dim_Territory, dim_Calendar
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│  DAX — Measures & KPIs      │  Revenue, Profit, Return Rate,
│                             │  Net Worth, Growth %, Rolling Avg
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│  Power BI — Interactive     │  4 report pages, slicers,
│  Dashboard (4 pages)        │  drill-through, bookmarks, tooltips
└─────────────────────────────┘
```

---

## Data Model — Star Schema

```
                    ┌──────────────────┐
                    │   dim_Calendar   │
                    │  date, year,     │
                    │  month, quarter  │
                    └────────┬─────────┘
                             │
┌──────────────┐    ┌────────▼─────────┐    ┌──────────────────┐
│ dim_Customer │    │   fact_Sales     │    │   dim_Product    │
│ customer_id  │◄───│  order_id        │───►│  product_id      │
│ name         │    │  customer_id     │    │  name            │
│ income_level │    │  product_id      │    │  category        │
│ occupation   │    │  territory_id    │    │  sub_category    │
│ country      │    │  order_date      │    │  cost            │
└──────────────┘    │  revenue         │    │  price           │
                    │  cost            │    └──────────────────┘
┌──────────────┐    │  profit          │
│dim_Territory │◄───│  quantity        │
│ territory_id │    │  return_flag     │
│ country      │    └──────────────────┘
│ region       │
└──────────────┘
```

---

## DAX Measures

| Measure | Formula | Purpose |
|---|---|---|
| `Total Revenue` | `SUMX(fact_Sales, [Qty] * [Unit Price])` | Gross revenue |
| `Total Profit` | `[Total Revenue] - [Total Cost]` | Net profit |
| `Profit Margin %` | `DIVIDE([Total Profit], [Total Revenue])` | Margin KPI |
| `Return Rate %` | `DIVIDE([Returns], [Total Orders])` | Quality signal |
| `Revenue per Customer` | `DIVIDE([Revenue], DISTINCTCOUNT([CustomerKey]))` | Customer value |
| `10% Growth Target` | `[Total Revenue] * 1.10` | Projection |
| `Rolling 3M Revenue` | `CALCULATE([Revenue], DATESINPERIOD(...,-3,MONTH))` | Trend window |
| `MoM Growth %` | `DIVIDE([Revenue] - [Revenue PM], [Revenue PM])` | Month-on-month |

Full DAX reference with syntax → [dax/measures.md](dax/measures.md)

---

## Project Structure

```
Data-analysis-dashboard/
├── Sales-Dashbaords.pbix          # Power BI report (open in PBI Desktop)
├── Sales Repots.pdf               # Exported PDF snapshot
├── scripts/
│   ├── sales_analysis.py          # Python EDA — replicates KPIs & charts
│   └── generate_insights.py       # Auto-generates executive insight bullets
├── dax/
│   └── measures.md                # All DAX measures with full syntax
├── docs/
│   └── data_dictionary.md         # Field definitions and business rules
├── requirements.txt               # Python dependencies
└── .github/workflows/
    └── validate.yml               # CI: validates Python scripts on push
```

---

## Python Analytics Scripts

The `scripts/` folder contains Python equivalents of the Power BI KPIs — useful for pipeline automation, scheduling, or deeper statistical analysis beyond what Power BI supports natively.

```bash
pip install -r requirements.txt
python scripts/sales_analysis.py      # KPI summary + matplotlib charts
python scripts/generate_insights.py   # Prints executive insight bullets
```

**Output includes:**
- Revenue & profit trend charts
- Customer segmentation breakdown
- Product return rate ranking
- Country-level performance comparison table

---

## Skills Demonstrated

| Skill Area | Tools & Techniques |
|---|---|
| **Data Cleaning** | Excel (VLOOKUP, IFERROR, Text-to-Columns, deduplication, pivot tables) |
| **Data Modelling** | Star schema design, relationship management, calculated columns in Power Query |
| **DAX** | Time intelligence, CALCULATE, DIVIDE, SUMX, rolling windows, MoM comparisons |
| **Visualisation** | KPI cards, line/bar charts, maps, matrix, drill-through, bookmarks, tooltips |
| **Python** | Pandas, Matplotlib, NumPy — EDA and automated executive reporting |
| **Business Storytelling** | Executive layout, colour-coded indicators, logical 4-page report flow |

---

## How to Run

### Power BI Dashboard
1. Download [Power BI Desktop](https://powerbi.microsoft.com/desktop/) (free)
2. Clone this repo:
   ```bash
   git clone https://github.com/Pthota2110/Data-analysis-dashboard.git
   ```
3. Open `Sales-Dashbaords.pbix`
4. Use slicers to filter by **Country**, **Year**, **Category**, or **Customer segment**

### Python Scripts
```bash
cd Data-analysis-dashboard
pip install -r requirements.txt
python scripts/sales_analysis.py
```

---

## Future Roadmap

- [ ] Connect to live Azure SQL / Redshift for auto-refresh via Power BI Service
- [ ] Add Python visual with Prophet/ARIMA for statistical sales forecasting
- [ ] Row-level security (RLS) for country-specific manager access
- [ ] Drill-through reports per regional manager
- [ ] Integrate with [Financial Data Platform](https://github.com/Pthota2110/Example-repository) pipeline for unified reporting

---

<div align="center">

**Pavan Thota** &nbsp;|&nbsp; [GitHub](https://github.com/Pthota2110) &nbsp;|&nbsp; [LinkedIn](https://linkedin.com/in/pavan-thota)

*Open to Data Engineer · BI Developer · Data Analyst roles*

</div>
