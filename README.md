# 📊 Vendor Sales Analysis

> A comprehensive analysis of inventory, sales, and vendor performance to optimize profitability in the retail and wholesale industry.

---

##  Table of Contents

- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [How to Run](#how-to-run)
- [Business Problem](#business-problem)
- [Exploratory Data Analysis](#exploratory-data-analysis)
  - [Summary Statistics](#summary-statistics)
  - [Negative & Zero Values](#negative--zero-values)
  - [Outliers & High Standard Deviations](#outliers-indicated-by-high-standard-deviations)
  - [Data Filtering](#data-filtering)
  - [Correlation Insights](#correlation-insights)
- [Research Questions & Key Findings](#research-questions--key-findings)
  - [1. Brands Needing Promotional Adjustment](#1-brands-needing-promotional-or-pricing-adjustment)
  - [2. Top Vendors & Brands by Sales](#2-top-vendors--brands-by-sales-performance)
  - [3. Vendor Contribution to Purchase Dollars](#3-vendor-contribution-to-total-purchase-dollars)
  - [4. Procurement Dependency on Top Vendors](#4-procurement-dependency-on-top-vendors)
  - [5. Bulk Purchasing & Unit Price Impact](#5-bulk-purchasing--unit-price-impact)
- [Recommendations](#recommendations)

---

## Project Structure

```
 vendor-performance-analysis/
├──  data/
│   └── inventory.db                        # SQLite database (tables: purchases, sales, purchase_prices, vendor_invoice, vendor_sales_summary)
├──  exploratory_data_analysis.ipynb      # EDA notebook — data exploration & correlation analysis
├──  vendor_performance_analysis.ipynb    # Main analysis notebook — research questions & visualizations
├──  README.md                            # Project documentation
```

---

## Requirements

Make sure you have **Python 3.8+** installed. Then install the required libraries:

```bash
pip install pandas numpy matplotlib seaborn scipy jupyter
```

Or if you use a `requirements.txt`:

```bash
pip install -r requirements.txt
```

**Full list of dependencies:**

| Library | Purpose |
|---|---|
| `pandas` | Data loading & manipulation |
| `numpy` | Numerical computations |
| `matplotlib` | Plotting & visualizations |
| `seaborn` | Statistical visualizations |
| `scipy` | Statistical tests (t-test, etc.) |
| `sqlite3` | Database connection (built-in) |
| `jupyter` | Running `.ipynb` notebooks |

---

## How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/vendor-performance-analysis.git
cd vendor-performance-analysis
```

### 2. Add the Database

Place your `inventory.db` SQLite file inside the project root (same directory as the notebooks). The database should contain the following tables:

- `purchases`
- `sales`
- `purchase_prices`
- `vendor_invoice`
- `vendor_sales_summary`

### 3. Launch Jupyter Notebook

```bash
jupyter notebook
```

### 4. Run the Notebooks (in order)

| Step | Notebook | Description |
|---|---|---|
| 1️⃣ | `exploratory_data_analysis.ipynb` | Connect to DB, explore raw tables, check data quality |
| 2️⃣ | `vendor_performance_analysis.ipynb` | Filter data, run analysis, generate all charts & findings |

Open each notebook and run all cells using:
- **Menu:** `Kernel → Restart & Run All`
- **Shortcut:** `Shift + Enter` to run cell by cell

>  **Note:** Both notebooks connect to `inventory.db` via `sqlite3.connect('inventory.db')`. Make sure the database file is in the **same directory** as the notebooks before running.

---

## Business Problem

Effective inventory and sales management are critical for optimizing profitability in the retail and wholesale industry. Companies need to ensure they are not incurring losses due to inefficient pricing, poor inventory turnover, or vendor dependency.

**The goals of this analysis are to:**

-  Identify underperforming brands that require promotional or pricing adjustments.
-  Determine top vendors contributing to sales and gross profit.
-  Understand the impact of bulk purchasing on unit costs.

---

## Exploratory Data Analysis

### Summary Statistics

The dataset contains **10,692 records** across key metrics including vendor numbers, brands, purchase/actual prices, volume, sales quantities, freight costs, gross profit, and profit margins.

**Key observations from the summary:**

| Metric | Notable Insight |
|---|---|
| `gross_profit` | Min value is negative — losses exist |
| `profit_margin` | Min of `-inf` — some transactions have zero revenue |
| `total_sales_quantity` | Min of `0` — some inventory was never sold |
| `stock_turnover` | Ranges from `0` to `274.5` — extreme variation in sell-through |
| `freight_cost` | Very high std deviation — logistics inefficiencies suspected |

---

### Negative & Zero Values

- **Gross Profit:** Minimum value below zero indicates some products are being sold at a loss — either due to high costs or discounts below purchase price.
- **Profit Margin:** A minimum of negative infinity suggests cases where revenue is zero or lower than total costs.
- **Total Sales Quantity & Sales Dollars:** Minimum values of `0` confirm that certain products were purchased but **never sold**, pointing to slow-moving or obsolete stock.

---

### Outliers Indicated by High Standard Deviations

- **Purchase & Actual Prices:** Max values far exceed the mean, indicating the presence of **premium products** in the catalog.
- **Freight Cost:** Large variance suggests either **logistics inefficiencies** or the impact of bulk shipment size differences.
- **Stock Turnover:** A range of `0` to `274.5` implies some products sell extremely fast while others remain in stock indefinitely. Values above `1` indicate that sold quantities exceed purchased quantities — likely fulfilled from older stock.

---

### Data Filtering

To improve the reliability of insights, the following records were removed:

| Filter Condition | Reason |
|---|---|
| `gross_profit <= 0` | Exclude loss-making transactions |
| `profit_margin <= 0` | Focus on profitable transactions only |
| `total_sales_quantity = 0` | Remove inventory that was never sold |

---

### Correlation Insights

Key findings from the correlation heatmap:

- **Purchase price vs. sales/profit:** Weak correlation (`-0.01` and `-0.02`) — price variations alone do **not** significantly drive revenue or profit.
- **Purchase quantity vs. sales quantity:** Strong positive correlation — confirms **efficient inventory turnover** across the dataset.
- **Profit margin vs. sales price:** Negative correlation — as sales price increases, margins tend to decrease, likely due to **competitive pricing pressures**.
- **Stock turnover vs. profitability:** Weak negative correlation — faster inventory movement does **not** guarantee higher margins.

---

## Research Questions & Key Findings

### 1. Brands Needing Promotional or Pricing Adjustment

> **Question:** Which brands exhibit lower sales performance but higher profit margins?

**198 brands** were identified with low total sales but above-average profit margins. These represent strong opportunities for targeted marketing, promotions, or pricing optimization to boost volume without sacrificing profitability.

**Sample of flagged brands:**

| Brand | Total Sales ($) | Profit Margin (%) |
|---|---|---|
| Santa Rita Organic Svgn Bl | 9.99 | 66.47 |
| Debauchery Pnt Nr | 11.58 | 65.98 |
| Concannon Glen Ellen Wh Zin | 15.95 | 83.45 |
| Crown Royal Apple | 27.86 | 89.81 |
| Sauza Sprklg Wild Berry Marg | 27.96 | 82.15 |
| Dad's Hat Rye Whiskey | 538.89 | 81.85 |
| A Bichot Clos Marechaudes | 539.94 | 67.74 |

>  These brands sit above the **High Margin Threshold** but below the **Low Sales Threshold** — prime candidates for promotional campaigns.

---

### 2. Top Vendors & Brands by Sales Performance

> **Question:** Which vendors and brands demonstrate the highest sales performance?

**Top 10 Vendors by Sales:**

| Vendor | Total Sales |
|---|---|
| Diageo North America Inc. | $67.99M |
| Martignetti Companies | $39.33M |
| Pernod Ricard USA | $32.06M |
| JIM Beam Brands Company | $31.42M |
| Bacardi USA Inc. | $24.85M |

**Top 10 Brands by Sales:**

| Brand | Total Sales |
|---|---|
| Jack Daniels No. 7 Black | $7.96M |
| Tito's Handmade Vodka | $7.40M |
| Grey Goose Vodka | $7.21M |
| Capt Morgan Spiced Rum | $6.36M |
| Absolut 80 Proof | $6.24M |

> A small number of vendors and brands drive the **majority of revenue**, underscoring their strategic importance to overall business growth.

---

### 3. Vendor Contribution to Total Purchase Dollars

> **Question:** Which vendors contribute the most to total purchase dollars?

| Vendor | Purchase Contribution (%) |
|---|---|
| Diageo North America Inc. | 16.3% |
| Martignetti Companies | 8.3% |
| Pernod Ricard USA | 7.76% |
| JIM Beam Brands Company | 7.64% |
| Bacardi USA Inc. | 5.67% |

> The Pareto chart confirms that a **small group of top vendors** accounts for a disproportionately large share of total procurement spend.

---

### 4. Procurement Dependency on Top Vendors

> **Question:** How dependent is total procurement on the top vendors?

| Group | Share of Total Purchases |
|---|---|
|  Top 10 Vendors | **65.69%** |
|  All Other Vendors | 34.31% |

>  **Risk Alert:** This high concentration creates significant **supply chain vulnerability**. A disruption from any top vendor could have outsized impact on operations — signaling a clear need for **vendor diversification**.

---

### 5. Bulk Purchasing & Unit Price Impact

> **Question:** Does bulk purchasing reduce unit costs, and what is the optimal order size?

| Order Size | Avg. Unit Purchase Price |
|---|---|
| Small | ~$3,500 (high variance) |
| Medium | Moderate reduction |
| Large | Significantly lowest |

**Key findings:**

- Bulk buyers (large order size) consistently achieve the **lowest unit prices**, enabling higher margins when inventory is managed efficiently.
- The price difference between small and large orders represents approximately a **~72% reduction in unit cost**.
- Bulk pricing strategies effectively encourage large-volume purchasing, driving higher overall sales even with lower per-unit revenue.

---

## Recommendations

Based on the analysis, the following strategic actions are recommended:

###  Diversify Vendor Partnerships
Reduce over-reliance on the top 10 vendors (currently at 65.69% of total procurement). Onboarding alternative suppliers will mitigate supply chain risks and improve negotiating leverage.

###  Leverage Bulk Purchasing
Take advantage of the ~72% cost reduction available through large-order purchasing. Pair this with strong inventory management practices to avoid overstock and obsolescence.

###  Targeted Marketing for High-Margin, Low-Sales Brands
The 198 identified brands with strong margins but weak sales volumes are ideal candidates for promotional campaigns, distribution expansion, or price restructuring to unlock revenue without sacrificing profitability.

###  Operational Efficiency
Implementing these recommendations collectively can help the company achieve **sustainable profitability**, reduce operational risk, and improve **overall supply chain efficiency**.

---

*Report generated from vendor performance dataset | Analysis covers 10,692 records across multiple product categories.*

## Author
Jeba Perveen

