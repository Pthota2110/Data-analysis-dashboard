# Data Dictionary

Field definitions, business rules, and data types for the Sales Performance Dashboard.

---

## fact_Sales

The central fact table. One row = one line item on a sales order.

| Column | Type | Description | Example |
|---|---|---|---|
| `OrderNumber` | VARCHAR | Unique order identifier | SO-12345 |
| `OrderLineItem` | INT | Line number within an order (1-based) | 1 |
| `OrderDate` | DATE | Date the order was placed | 2022-05-15 |
| `StockDate` | DATE | Date inventory was allocated | 2022-05-14 |
| `CustomerKey` | INT | FK → dim_Customer | 29506 |
| `TerritoryKey` | INT | FK → dim_Territory | 5 |
| `ProductKey` | INT | FK → dim_Product | 214 |
| `Quantity` | INT | Units ordered | 2 |
| `ReturnFlag` | BOOLEAN | True if order was returned | FALSE |

---

## dim_Customer

| Column | Type | Description | Example |
|---|---|---|---|
| `CustomerKey` | INT | Surrogate PK | 29506 |
| `FirstName` | VARCHAR | Customer first name | Ruben |
| `LastName` | VARCHAR | Customer last name | Suarez |
| `EmailAddress` | VARCHAR | Contact email | rsuarez@email.com |
| `AnnualIncome` | INT | Household annual income (USD) | 80000 |
| `IncomeLevel` | VARCHAR | Banded income level | Average |
| `Occupation` | VARCHAR | Employment type | Skilled Manual |
| `HomeOwner` | BOOLEAN | Owns home | TRUE |
| `TotalChildren` | INT | Number of children | 2 |

**Income Level bands:**

| Band | Annual Income |
|---|---|
| Low | < $30,000 |
| Average | $30,000 – $70,000 |
| High | > $70,000 |

---

## dim_Product

| Column | Type | Description | Example |
|---|---|---|---|
| `ProductKey` | INT | Surrogate PK | 214 |
| `ProductSKU` | VARCHAR | Product code | BK-R50B-44 |
| `ProductName` | VARCHAR | Full product name | Sport-100 Helmet (Black) |
| `ModelName` | VARCHAR | Model family | Sport-100 |
| `ProductDescription` | VARCHAR | Marketing description | — |
| `ProductColor` | VARCHAR | Colour variant | Black |
| `ProductSize` | VARCHAR | Size (if applicable) | 44 |
| `ProductWeight` | DECIMAL | Weight in lbs | 1.77 |
| `ProductCost` | DECIMAL | Standard cost (USD) | 13.49 |
| `ProductPrice` | DECIMAL | List price (USD) | 34.99 |
| `CategoryName` | VARCHAR | Top-level category | Accessories |
| `SubcategoryName` | VARCHAR | Sub-category | Helmets |

---

## dim_Territory

| Column | Type | Description | Example |
|---|---|---|---|
| `TerritoryKey` | INT | Surrogate PK | 5 |
| `Region` | VARCHAR | Sales region name | Southwest |
| `Country` | VARCHAR | Country name | United States |
| `Continent` | VARCHAR | Continent | North America |

**Countries in scope:** United States, United Kingdom, Germany, France, Australia, Canada

---

## dim_Calendar

Generated date dimension covering 2020-01-01 → 2022-12-31.

| Column | Type | Description |
|---|---|---|
| `Date` | DATE | Calendar date (PK) |
| `DayOfWeek` | INT | 1 = Sunday … 7 = Saturday |
| `DayName` | VARCHAR | Monday, Tuesday … |
| `DayOfMonth` | INT | 1 – 31 |
| `DayOfYear` | INT | 1 – 366 |
| `WeekOfYear` | INT | ISO week number |
| `MonthName` | VARCHAR | January … December |
| `MonthNumber` | INT | 1 – 12 |
| `Quarter` | INT | 1 – 4 |
| `Year` | INT | 2020, 2021, 2022 |
| `IsWeekend` | BOOLEAN | Saturday or Sunday |

---

## dim_Returns

| Column | Type | Description |
|---|---|---|
| `ReturnDate` | DATE | Date return was processed |
| `TerritoryKey` | INT | FK → dim_Territory |
| `ProductKey` | INT | FK → dim_Product |
| `ReturnQuantity` | INT | Number of units returned |

---

## Business Rules

1. **Revenue** = `Quantity × Unit Price` (list price, not discounted)
2. **Profit** = `Revenue − Cost` (standard cost, not actual fulfilment cost)
3. **Return Rate** = `Returned Orders ÷ Total Orders` (order-level, not unit-level)
4. **Revenue per Customer** = `Total Revenue ÷ DISTINCTCOUNT(CustomerKey)` — includes customers with zero returns
5. **Growth Projection** = `Total Revenue × 1.10` — a flat 10% uplift applied at report level via DAX
6. Orders with `ReturnFlag = TRUE` are **included** in revenue totals (net-of-returns view uses the Returns table separately)
