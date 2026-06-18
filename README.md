# Vendor Performance Analysis

## Project Overview

This project analyzes vendor performance using sales, purchase, inventory, and pricing data to identify opportunities for improving profitability, inventory management, and procurement efficiency.

The analysis combines ETL processing, SQL-based data integration, exploratory data analysis (EDA), statistical testing, and interactive dashboard development to generate actionable business insights.

---

## Business Problem

Organizations often struggle to answer questions such as:

* Which vendors contribute the most to sales and profit?
* How much capital is tied up in unsold inventory?
* Which brands require promotional or pricing adjustments?
* Are high-performing vendors more profitable than low-performing vendors?
* Which vendors have slow-moving inventory?

This project addresses these questions through data-driven analysis.

---

## Dataset

The project uses six datasets:

| Dataset             | Records |
| ------------------- | ------: |
| Sales               |  12.8M+ |
| Purchases           |   2.3M+ |
| Beginning Inventory |   206K+ |
| Ending Inventory    |   224K+ |
| Purchase Prices     |    12K+ |
| Vendor Invoices     |     5K+ |

**Total Records Processed:** 15.6M+

---

## Tech Stack

* Python
* Pandas
* NumPy
* SQL
* SQLite
* Matplotlib
* Seaborn
* SciPy
* Power BI

---

## Project Workflow

### 1. ETL Pipeline

* Loaded multiple CSV datasets into SQLite.
* Processed large files using chunk-based ingestion.
* Implemented logging and error handling.
* Created a centralized database for analysis.

### 2. Data Preparation

* Cleaned missing and inconsistent records.
* Filtered invalid profit and sales observations.
* Created derived business metrics including:

  * Gross Profit
  * Profit Margin
  * Sales-to-Purchase Ratio
  * Stock Turnover
  * Unsold Inventory Value

### 3. Exploratory Data Analysis (EDA)

* Summary statistics
* Distribution analysis
* Correlation analysis
* Vendor and brand performance evaluation
* Inventory turnover analysis

### 4. Statistical Analysis

* 95% Confidence Interval Estimation
* Two-Sample T-Test
* Vendor profitability comparison

### 5. Dashboard Development

Created an interactive Power BI dashboard to monitor:

* Total Sales
* Gross Profit
* Profit Margin
* Unsold Capital
* Vendor Contribution
* Inventory Turnover
* Brand Performance
## Data Availability

Due to GitHub file size limitations, the original **sales.csv** and **purchases.csv** datasets are not included in this repository.

The analysis, ETL scripts, SQL queries, notebooks, and dashboard files are provided to demonstrate the complete workflow. Large source files can be obtained from the original dataset source.

---

## Key Findings

### Inventory Insights

* Identified **$2.71M** in capital tied up in unsold inventory.
* A small group of vendors accounted for the majority of locked inventory value.

### Vendor Performance

* Top 10 vendors contributed **65.69%** of total procurement.
* Large vendors generated the highest sales volumes and profits.

### Brand Performance

* Identified multiple brands with low sales but high profit margins.
* These products may benefit from targeted promotional strategies.

### Statistical Findings

* Low-sales vendors achieved significantly higher profit margins than high-sales vendors.
* Two-sample t-test confirmed the difference was statistically significant (**p < 0.05**).

---

## Dashboard

(Add dashboard screenshots here)

---

## Repository Structure

```text
project/
│
├── data/
├── notebooks/
├── scripts/
│   └── etl_data_loading.py
├── dashboard/
├── screenshots/
├── inventory.db
└── README.md
```

---

## Business Impact

The project demonstrates how analytics can support:

* Inventory optimization
* Vendor management
* Procurement planning
* Profitability analysis
* Data-driven decision making
