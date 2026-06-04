# DAX Measures Reference

Full syntax for every measure used in the Sales Performance Dashboard.

---

## Revenue Measures

```dax
-- Gross revenue across all orders
Total Revenue =
SUMX(
    fact_Sales,
    fact_Sales[Quantity] * RELATED(dim_Product[Unit Price])
)

-- Previous month revenue (for MoM comparison)
Revenue PM =
CALCULATE(
    [Total Revenue],
    DATEADD(dim_Calendar[Date], -1, MONTH)
)

-- Month-over-month growth percentage
MoM Revenue Growth % =
DIVIDE(
    [Total Revenue] - [Revenue PM],
    [Revenue PM],
    0
)

-- 3-month rolling average revenue
Rolling 3M Revenue =
CALCULATE(
    [Total Revenue],
    DATESINPERIOD(
        dim_Calendar[Date],
        LASTDATE(dim_Calendar[Date]),
        -3,
        MONTH
    )
)

-- Year-to-date revenue
YTD Revenue =
TOTALYTD([Total Revenue], dim_Calendar[Date])
```

---

## Profit Measures

```dax
-- Total cost across all orders
Total Cost =
SUMX(
    fact_Sales,
    fact_Sales[Quantity] * RELATED(dim_Product[Standard Cost])
)

-- Net profit
Total Profit =
[Total Revenue] - [Total Cost]

-- Profit margin percentage
Profit Margin % =
DIVIDE([Total Profit], [Total Revenue], 0)

-- Previous period profit (for trend)
Profit PM =
CALCULATE(
    [Total Profit],
    DATEADD(dim_Calendar[Date], -1, MONTH)
)
```

---

## Order & Return Measures

```dax
-- Count of all orders
Total Orders =
DISTINCTCOUNT(fact_Sales[OrderNumber])

-- Count of returned orders
Total Returns =
CALCULATE(
    COUNTROWS(fact_Returns),
    fact_Returns[ReturnQuantity] > 0
)

-- Return rate percentage
Return Rate % =
DIVIDE(
    [Total Returns],
    [Total Orders],
    0
)
```

---

## Customer Measures

```dax
-- Unique customer count
Total Customers =
DISTINCTCOUNT(fact_Sales[CustomerKey])

-- Average revenue per customer
Revenue per Customer =
DIVIDE([Total Revenue], [Total Customers], 0)

-- Top customer revenue (for leaderboard)
Top Customer Revenue =
MAXX(
    SUMMARIZE(
        fact_Sales,
        dim_Customer[CustomerKey],
        "CustomerRevenue", [Total Revenue]
    ),
    [CustomerRevenue]
)
```

---

## Growth & Projection Measures

```dax
-- 10% incremental growth target
10% Growth Target =
[Total Revenue] * 1.10

-- Gap to target
Gap to Target =
[10% Growth Target] - [Total Revenue]

-- Percentage of target achieved
Target Achievement % =
DIVIDE([Total Revenue], [10% Growth Target], 0)
```

---

## KPI Status Measures (used in KPI card colour coding)

```dax
-- Revenue status vs target (for conditional formatting)
Revenue Status =
IF([MoM Revenue Growth %] >= 0, "Positive", "Negative")

-- Return rate alert flag
Return Rate Alert =
IF([Return Rate %] > 0.025, "HIGH", "NORMAL")

-- Profit margin health
Margin Health =
SWITCH(
    TRUE(),
    [Profit Margin %] >= 0.45, "Excellent",
    [Profit Margin %] >= 0.35, "Good",
    [Profit Margin %] >= 0.20, "Warning",
    "Critical"
)
```
