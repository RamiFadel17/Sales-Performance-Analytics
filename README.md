# Sales Performance Analytics

End-to-end sales operations analytics project using **SQL, Python, Power BI, and synthetic CRM data** to analyze revenue performance, pipeline health, forecasting, quota attainment, sales efficiency, and opportunity aging.

## Dashboard Preview

### Executive Overview

![Executive Overview](Screenshots/Executive%20Overview.png)

### Pipeline & Forecast

![Pipeline & Forecast](Screenshots/Pipeline%20%26%20Forecast.png)

## Project Objective

The goal of this project is to simulate a real Sales Operations / Revenue Operations analytics workflow and answer practical business questions such as:

- Are sales teams on track to hit quota?
- Which teams have the strongest and weakest pipeline coverage?
- How much open pipeline exists, and how much is realistically weighted to close?
- How healthy is the pipeline by stage and forecast category?
- Which teams have the strongest win rates?
- How long does it take to close opportunities?
- Is a significant portion of pipeline becoming stale?
- How does forecast composition differ across Enterprise, Mid-Market, and SMB teams?

## Tools Used

- **SQL Server / SSMS** — data exploration, joins, aggregations, KPI calculations, pipeline analysis
- **Python / Pandas** — data validation, transformation, exploratory analysis
- **Power BI** — data modeling, DAX measures, dashboard development and visualization
- **Excel / CSV** — source data structure and validation

## Dataset

The project uses synthetic CRM and sales operations data across six main datasets:

- Accounts
- Opportunities
- Sales Representatives
- Sales Activities
- Quotas
- Sales Transactions

The data models a B2B sales organization with three sales teams:

- Enterprise
- Mid-Market
- SMB

### Data Period and Generation

This project uses synthetic CRM and sales operations data created specifically for this independent portfolio analysis. The dataset simulates a B2B sales organization with Enterprise, Mid-Market, and SMB teams and includes opportunities, sales activity, quota, transaction, and account data across a simulated reporting period.

No real company, customer, or personally identifiable data is used.

## Data Model

The Power BI model connects the core sales tables using relationships such as:

- Sales Reps → Opportunities
- Sales Reps → Quotas
- Sales Reps → Sales Activities
- Sales Reps → Sales Transactions
- Accounts → Opportunities
- Accounts → Sales Transactions

A dedicated stage-order table is also used to preserve the logical sales funnel sequence:

**Prospecting → Qualification → Discovery → Proposal → Negotiation**

## Key KPIs

### Total Revenue
Total net revenue generated from completed sales transactions.

### Quota Attainment %
Measures actual revenue performance relative to assigned sales quota.

**Formula:**

`Revenue ÷ Quota`

### Open Pipeline Value
Total value of all currently open opportunities.

### Weighted Pipeline
Probability-adjusted value of open opportunities.

**Formula:**

`Opportunity Value × Probability`

### Pipeline Coverage
Measures how much open pipeline exists relative to quota.

**Formula:**

`Open Pipeline ÷ Quota`

### Weighted Pipeline Coverage
Measures probability-adjusted pipeline relative to quota.

**Formula:**

`Weighted Pipeline ÷ Quota`

### Win Rate
Measures the proportion of closed opportunities that were won.

**Formula:**

`Won Opportunities ÷ Closed Opportunities`

### Average Sales Cycle
Average number of days required to close an opportunity.

## Dashboard Pages

### 1. Executive Overview

Provides a high-level view of overall sales performance including:

- Total Revenue
- Quota Attainment
- Open Pipeline
- Weighted Pipeline
- Win Rate
- Average Sales Cycle
- Revenue vs Quota by Team
- Win Rate by Team
- Pipeline Coverage vs Weighted Coverage by Team

### 2. Pipeline & Forecast

Focuses on pipeline quality and forecasting, including:

- Open Pipeline by Sales Stage
- Open Pipeline by Forecast Category
- Pipeline Aging
- Forecast Mix by Team

Forecast categories include:

- Pipeline
- Best Case
- Commit

## Key Findings

A few of the key insights from the analysis include:

- SMB has the strongest pipeline coverage, with approximately 12.65x raw coverage and 5.14x weighted coverage.
- Mid-Market follows with approximately 7.38x raw coverage and 2.94x weighted coverage.
- Enterprise has the weakest pipeline cushion, at approximately 4.51x raw coverage and 1.73x weighted coverage.
- Overall win rate is approximately 56.98%.
- Average sales cycle is approximately 80.4 days.
- 60.1% of open pipeline ($274M of $456M) is aged 180+ days, indicating significant stale-pipeline risk.
- Forecast analysis shows that a significant share of open pipeline remains in the general Pipeline category rather than higher-confidence Best Case or Commit categories.

## Business Interpretation

The project demonstrates how Sales Operations can move beyond reporting raw sales numbers and instead evaluate:

- pipeline sufficiency
- forecast confidence
- deal progression
- sales efficiency
- quota performance
- stale opportunities
- team-level performance differences

The broader sales funnel can be summarized as:

**Sales Activity → Opportunity Creation → Pipeline → Stage Progression → Forecast → Win → Revenue**

## Repository Structure

```text
Sales-Performance-Analytics/
│
├── CSV Files/
├── SQL/
├── Python/
├── PowerBI/
├── Screenshots/
└── README.md
```

## About the Project

This is an independent portfolio project built using synthetic data to demonstrate practical skills in:

- Sales Operations Analytics
- Revenue Operations
- SQL
- Python
- Power BI
- Data Modeling
- DAX
- Pipeline Management
- Forecasting
- KPI Development
- Business Intelligence

## How to Run

1. Load the CSV files from the `CSV Files/` folder into SQL Server or your preferred analytics environment.
2. Run the SQL scripts in the `SQL/` folder to reproduce the pipeline, forecasting, aging, team-performance, and KPI analyses.
3. Open the Power BI file in the `PowerBI/` folder to explore the completed data model and dashboards.

The Python script in the Python/ folder is used for data validation, transformation, and exploratory analysis.
