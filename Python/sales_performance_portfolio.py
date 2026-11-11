import pandas as pd
import numpy as np
import random

from datetime import datetime, timedelta

# Reproducibility
SEED = 42

np.random.seed(SEED)
random.seed(SEED)

START_DATE = pd.Timestamp("2025-01-01")
END_DATE = pd.Timestamp("2026-12-31")

N_REPS = 36
N_ACCOUNTS = 750
N_OPPORTUNITIES = 3000
# -----------------------------
# SALES REPS TABLE
# -----------------------------

teams = ["SMB", "Mid-Market", "Enterprise"]
regions = ["Canada East", "Canada West", "US East", "US West"]

managers = [
    "Emma Collins",
    "Daniel Brooks",
    "Sophia Martinez",
    "Liam Carter",
    "Olivia Bennett",
    "Noah Thompson"
]

first_names = [
    "Alex", "Jordan", "Taylor", "Morgan", "Casey", "Jamie",
    "Avery", "Riley", "Cameron", "Drew", "Parker", "Reese"
]

last_names = [
    "Smith", "Johnson", "Brown", "Wilson", "Taylor", "Anderson",
    "Thomas", "Moore", "Martin", "Jackson", "White", "Harris"
]

rep_names = [
    f"{random.choice(first_names)} {random.choice(last_names)}"
    for _ in range(N_REPS)
]

sales_reps = pd.DataFrame({
    "rep_id": range(1, N_REPS + 1),
    "rep_name": rep_names,
    "team": np.random.choice(
        teams,
        size=N_REPS,
        p=[0.40, 0.35, 0.25]
    ),
    "region": np.random.choice(
        regions,
        size=N_REPS
    ),
    "manager": np.random.choice(
        managers,
        size=N_REPS
    )
})

print(sales_reps.head())
# Generate realistic hire dates between 2021 and 2026
hire_start = pd.Timestamp("2021-01-01")
hire_end = pd.Timestamp("2026-10-01")

sales_reps["hire_date"] = pd.to_datetime(
    np.random.choice(
        pd.date_range(hire_start, hire_end),
        size=N_REPS
    )
)

# Employment status
sales_reps["employment_status"] = np.random.choice(
    ["Active", "Inactive"],
    size=N_REPS,
    p=[0.90, 0.10]
)

# Annual quota based on team
quota_map = {
    "SMB": 600000,
    "Mid-Market": 1000000,
    "Enterprise": 1600000
}

sales_reps["annual_quota"] = sales_reps["team"].map(quota_map)

# Calculate tenure in months as of the end of the dataset
sales_reps["tenure_months"] = (
    (END_DATE.year - sales_reps["hire_date"].dt.year) * 12
    + (END_DATE.month - sales_reps["hire_date"].dt.month)
)

# Ramping status
sales_reps["is_ramping"] = sales_reps["tenure_months"] < 6

# Capacity factor based on tenure
def assign_capacity(tenure_months):
    if tenure_months < 3:
        return 0.50
    elif tenure_months < 6:
        return 0.75
    else:
        return 1.00

sales_reps["capacity_factor"] = sales_reps["tenure_months"].apply(assign_capacity)

print(sales_reps.head())
# -----------------------------
# ACCOUNTS TABLE
# -----------------------------

industries = [
    "Technology",
    "Financial Services",
    "Retail",
    "Healthcare",
    "Manufacturing",
    "Professional Services"
]

lead_sources = [
    "Inbound",
    "Outbound",
    "Partner",
    "Event",
    "Referral"
]

segments = ["SMB", "Mid-Market", "Enterprise"]

company_prefixes = [
    "Northstar", "BluePeak", "Summit", "Vertex", "Nova",
    "Crescent", "Evergreen", "Pioneer", "Apex", "Horizon",
    "Brightline", "Stonebridge", "Redwood", "Clearview", "Silverline"
]

company_suffixes = [
    "Technologies", "Solutions", "Systems", "Group", "Industries",
    "Partners", "Labs", "Holdings", "Services", "Networks"
]

account_names = [
    f"{random.choice(company_prefixes)} {random.choice(company_suffixes)}"
    for _ in range(N_ACCOUNTS)
]

accounts = pd.DataFrame({
    "account_id": range(1, N_ACCOUNTS + 1),
    "account_name": account_names,

    "segment": np.random.choice(
        segments,
        size=N_ACCOUNTS,
        p=[0.50, 0.30, 0.20]
    ),

    "industry": np.random.choice(
        industries,
        size=N_ACCOUNTS
    ),

    "region": np.random.choice(
        regions,
        size=N_ACCOUNTS
    ),

    "lead_source": np.random.choice(
        lead_sources,
        size=N_ACCOUNTS,
        p=[0.30, 0.30, 0.15, 0.10, 0.15]
    )
})

print(accounts.head())
# Employee count based on segment
def assign_employee_count(segment):
    if segment == "SMB":
        return np.random.randint(20, 250)
    elif segment == "Mid-Market":
        return np.random.randint(250, 2000)
    else:
        return np.random.randint(2000, 20000)

accounts["employee_count"] = accounts["segment"].apply(assign_employee_count)



# Annual revenue based on segment
def assign_annual_revenue(segment):
    if segment == "SMB":
        return random.randint(2_000_000, 50_000_000)
    elif segment == "Mid-Market":
        return random.randint(50_000_000, 500_000_000)
    else:
        return random.randint(500_000_000, 5_000_000_000)

accounts["annual_revenue"] = accounts["segment"].apply(assign_annual_revenue)


# Customer status
accounts["customer_status"] = np.random.choice(
    ["Prospect", "Customer"],
    size=N_ACCOUNTS,
    p=[0.65, 0.35]
)


# Account creation date
account_start = pd.Timestamp("2020-01-01")
account_end = END_DATE

accounts["created_date"] = pd.to_datetime(
    np.random.choice(
        pd.date_range(account_start, account_end),
        size=N_ACCOUNTS
    )
)

print(accounts.head())
# -----------------------------
# OPPORTUNITIES TABLE
# -----------------------------

stages = [
    "Prospecting",
    "Qualification",
    "Discovery",
    "Proposal",
    "Negotiation",
    "Closed Won",
    "Closed Lost"
]

stage_probabilities = {
    "Prospecting": 0.10,
    "Qualification": 0.25,
    "Discovery": 0.40,
    "Proposal": 0.60,
    "Negotiation": 0.80,
    "Closed Won": 1.00,
    "Closed Lost": 0.00
}

products = [
    "Core Platform",
    "Analytics Add-on",
    "Automation Suite",
    "Enterprise Package"
]

deal_types = [
    "New Business",
    "Expansion",
    "Renewal"
]

forecast_categories = [
    "Pipeline",
    "Best Case",
    "Commit",
    "Closed"
]

lost_reasons = [
    "Price",
    "Competitor",
    "No Decision",
    "Budget",
    "Timing",
    "Product Fit"
]


# Randomly assign accounts and reps
opportunities = pd.DataFrame({
    "opportunity_id": range(1, N_OPPORTUNITIES + 1),

    "account_id": np.random.choice(
        accounts["account_id"],
        size=N_OPPORTUNITIES
    ),

    "rep_id": np.random.choice(
        sales_reps["rep_id"],
        size=N_OPPORTUNITIES
    ),

    "created_date": pd.to_datetime(
        np.random.choice(
            pd.date_range(START_DATE, END_DATE),
            size=N_OPPORTUNITIES
        )
    ),

    "stage": np.random.choice(
        stages,
        size=N_OPPORTUNITIES,
        p=[0.12, 0.16, 0.16, 0.14, 0.10, 0.18, 0.14]
    ),

    "product": np.random.choice(
        products,
        size=N_OPPORTUNITIES
    ),

    "deal_type": np.random.choice(
        deal_types,
        size=N_OPPORTUNITIES,
        p=[0.55, 0.25, 0.20]
    )
})

# Make opportunity creation dates valid
rep_hire_lookup = sales_reps.set_index("rep_id")["hire_date"].to_dict()
account_created_lookup = accounts.set_index("account_id")["created_date"].to_dict()

def assign_valid_created_date(row):
    earliest_date = max(
        START_DATE,
        rep_hire_lookup[row["rep_id"]],
        account_created_lookup[row["account_id"]]
    )

    days_available = (END_DATE - earliest_date).days

    return earliest_date + pd.Timedelta(
        days=random.randint(0, days_available)
    )

opportunities["created_date"] = opportunities.apply(
    assign_valid_created_date,
    axis=1
)
# Check opportunities table
print("\nOPPORTUNITIES TABLE")
print(opportunities.head())

print("\nOPPORTUNITIES COLUMNS")
print(opportunities.columns.tolist())

print("\nSTAGE COUNTS")
print(opportunities["stage"].value_counts())
# Probability based on stage
opportunities["probability"] = opportunities["stage"].map(stage_probabilities)

# Bring account segment and lead source into opportunities
opportunities = opportunities.merge(
    accounts[["account_id", "segment", "lead_source"]],
    on="account_id",
    how="left"
)

# Opportunity value based on segment
def assign_opportunity_value(segment):
    if segment == "SMB":
        return random.randint(5_000, 50_000)
    elif segment == "Mid-Market":
        return random.randint(40_000, 250_000)
    else:
        return random.randint(200_000, 1_500_000)

opportunities["opportunity_value"] = opportunities["segment"].apply(
    assign_opportunity_value
)

# Expected close date
opportunities["expected_close_date"] = (
    opportunities["created_date"]
    + pd.to_timedelta(
        np.random.randint(30, 241, size=N_OPPORTUNITIES),
        unit="D"
    )
)

# Actual close date only for closed opportunities
closed_mask = opportunities["stage"].isin(
    ["Closed Won", "Closed Lost"]
)

opportunities["actual_close_date"] = pd.NaT

def assign_actual_close_date(row):
    if row["stage"] not in ["Closed Won", "Closed Lost"]:
        return pd.NaT

    max_days = (END_DATE - row["created_date"]).days

    if max_days <= 0:
        return row["created_date"]

    cycle_days = random.randint(
        1,
        min(220, max_days)
    )

    return row["created_date"] + pd.Timedelta(
        days=cycle_days
    )

opportunities["actual_close_date"] = opportunities.apply(
    assign_actual_close_date,
    axis=1
)

# Close status
def assign_close_status(stage):
    if stage == "Closed Won":
        return "Won"
    elif stage == "Closed Lost":
        return "Lost"
    else:
        return "Open"

opportunities["close_status"] = opportunities["stage"].apply(
    assign_close_status
)

# Lost reason
opportunities["lost_reason"] = None

lost_mask = opportunities["stage"] == "Closed Lost"

opportunities.loc[lost_mask, "lost_reason"] = np.random.choice(
    lost_reasons,
    size=lost_mask.sum()
)

# Sales cycle
opportunities["sales_cycle_days"] = (
    opportunities["actual_close_date"]
    - opportunities["created_date"]
).dt.days

# Forecast category
def assign_forecast_category(stage):
    if stage in ["Prospecting", "Qualification", "Discovery"]:
        return "Pipeline"
    elif stage == "Proposal":
        return "Best Case"
    elif stage == "Negotiation":
        return "Commit"
    else:
        return "Closed"

opportunities["forecast_category"] = opportunities["stage"].apply(
    assign_forecast_category
)

# Final validation
print("\nOPPORTUNITIES TABLE")
print(opportunities.head())

print("\nOPPORTUNITIES COLUMNS")
print(opportunities.columns.tolist())
# -----------------------------
# QUOTAS TABLE
# -----------------------------

quota_rows = []

for _, rep in sales_reps.iterrows():
    for month_start in pd.date_range(
        START_DATE,
        END_DATE,
        freq="MS"
    ):

        if month_start < rep["hire_date"].replace(day=1):
            continue

        monthly_quota = rep["annual_quota"] / 12

        # Reduce quota for ramping reps
        adjusted_quota = monthly_quota * rep["capacity_factor"]

        quota_rows.append({
            "quota_id": len(quota_rows) + 1,
            "rep_id": rep["rep_id"],
            "year": month_start.year,
            "month": month_start.month,
            "quarter": f"Q{((month_start.month - 1) // 3) + 1}",
            "monthly_quota": round(adjusted_quota)
        })

quotas = pd.DataFrame(quota_rows)

quotas["quarterly_quota"] = quotas["monthly_quota"] * 3

print("\nQUOTAS TABLE")
print(quotas.head())

print("\nQUOTAS SHAPE")
print(quotas.shape)

# -----------------------------
# SALES TRANSACTIONS TABLE
# -----------------------------

won_opportunities = opportunities[
    opportunities["stage"] == "Closed Won"
].copy()

transactions = won_opportunities[
    [
        "opportunity_id",
        "account_id",
        "rep_id",
        "actual_close_date",
        "product",
        "opportunity_value"
    ]
].copy()

transactions = transactions.rename(
    columns={"actual_close_date": "transaction_date"}
)

# Create transaction ID
transactions.insert(
    0,
    "transaction_id",
    range(1, len(transactions) + 1)
)

# Generate discount percentage
transactions["discount_pct"] = np.random.choice(
    [0.00, 0.05, 0.10, 0.15, 0.20],
    size=len(transactions),
    p=[0.20, 0.25, 0.30, 0.15, 0.10]
)

# Booking amount before discount
transactions["booking_amount"] = transactions["opportunity_value"]

# Net revenue after discount
transactions["net_revenue"] = (
    transactions["booking_amount"]
    * (1 - transactions["discount_pct"])
).round(2)

# Remove opportunity_value because booking_amount replaces it
transactions = transactions.drop(
    columns=["opportunity_value"]
)

print("\nSALES TRANSACTIONS TABLE")
print(transactions.head())

print("\nSALES TRANSACTIONS SHAPE")
print(transactions.shape)

# -----------------------------
# CALIBRATE REP PERFORMANCE
# -----------------------------

# Total quota by rep
quota_totals = (
    quotas.groupby("rep_id")["monthly_quota"]
    .sum()
    .reset_index(name="total_quota")
)

# Assign realistic target attainment by rep
quota_totals["target_attainment"] = np.random.choice(
    [0.65, 0.75, 0.85, 0.95, 1.00, 1.05, 1.10, 1.20, 1.30, 1.40, 1.50],
    size=len(quota_totals),
    p=[0.05, 0.08, 0.10, 0.12, 0.15, 0.15, 0.12, 0.08, 0.06, 0.05, 0.04]
)

quota_totals["target_revenue"] = (
    quota_totals["total_quota"]
    * quota_totals["target_attainment"]
)

# Current revenue by rep
current_revenue = (
    transactions.groupby("rep_id")["net_revenue"]
    .sum()
    .reset_index(name="current_revenue")
)

# Calculate scaling factor
performance_scale = quota_totals.merge(
    current_revenue,
    on="rep_id",
    how="left"
)

performance_scale["current_revenue"] = (
    performance_scale["current_revenue"].fillna(0)
)

performance_scale["scale_factor"] = np.where(
    performance_scale["current_revenue"] > 0,
    performance_scale["target_revenue"]
    / performance_scale["current_revenue"],
    1
)

scale_lookup = performance_scale.set_index("rep_id")[
    "scale_factor"
].to_dict()

# Scale transaction values
transactions["booking_amount"] = (
    transactions.apply(
        lambda row: row["booking_amount"]
        * scale_lookup[row["rep_id"]],
        axis=1
    )
).round(2)

transactions["net_revenue"] = (
    transactions["booking_amount"]
    * (1 - transactions["discount_pct"])
).round(2)

# Validate resulting attainment
check_revenue = (
    transactions.groupby("rep_id")["net_revenue"]
    .sum()
    .reset_index(name="total_revenue")
)

check_attainment = quota_totals.merge(
    check_revenue,
    on="rep_id",
    how="left"
)

check_attainment["attainment_pct"] = (
    check_attainment["total_revenue"]
    / check_attainment["total_quota"]
    * 100
).round(2)

print("\nREP QUOTA ATTAINMENT CHECK")
print(
    check_attainment[
        ["rep_id", "total_quota", "total_revenue", "attainment_pct"]
    ].sort_values("attainment_pct", ascending=False)
)

# Validate resulting attainment
check_revenue = (
    transactions.groupby("rep_id")["net_revenue"]
    .sum()
    .reset_index(name="total_revenue")
)

check_attainment = quota_totals.merge(
    check_revenue,
    on="rep_id",
    how="left"
)

check_attainment["attainment_pct"] = (
    check_attainment["total_revenue"]
    / check_attainment["total_quota"]
    * 100
).round(2)

print("\nREP QUOTA ATTAINMENT CHECK")
print(
    check_attainment[
        ["rep_id", "total_quota", "total_revenue", "attainment_pct"]
    ].sort_values("attainment_pct", ascending=False)
)
# -----------------------------
# SALES ACTIVITIES TABLE
# -----------------------------

activity_rows = []

week_starts = pd.date_range(
    START_DATE,
    END_DATE,
    freq="W-MON"
)

for _, rep in sales_reps.iterrows():
    for week_start in week_starts:
        if week_start < rep["hire_date"]:
            continue

        # Activity levels vary slightly by team
        if rep["team"] == "SMB":
            calls = np.random.randint(35, 80)
            emails = np.random.randint(80, 160)
            meetings = np.random.randint(5, 15)
            demos = np.random.randint(2, 8)

        elif rep["team"] == "Mid-Market":
            calls = np.random.randint(25, 60)
            emails = np.random.randint(60, 130)
            meetings = np.random.randint(6, 16)
            demos = np.random.randint(3, 9)

        else:
            calls = np.random.randint(15, 45)
            emails = np.random.randint(40, 100)
            meetings = np.random.randint(5, 14)
            demos = np.random.randint(3, 10)

        opportunities_created = np.random.randint(0, 6)

        active_opportunities = np.random.randint(8, 35)

        hours_available = 40 * rep["capacity_factor"]

        activity_rows.append({
            "activity_id": len(activity_rows) + 1,
            "rep_id": rep["rep_id"],
            "week_start": week_start,
            "calls": calls,
            "emails": emails,
            "meetings": meetings,
            "demos": demos,
            "opportunities_created": opportunities_created,
            "active_opportunities": active_opportunities,
            "hours_available": round(hours_available, 1)
        })

sales_activities = pd.DataFrame(activity_rows)

print("\nSALES ACTIVITIES TABLE")
print(sales_activities.head())

print("\nSALES ACTIVITIES SHAPE")
print(sales_activities.shape)
# -----------------------------
# FINAL DATA VALIDATION
# -----------------------------

print("\n--- TABLE SHAPES ---")
print("sales_reps:", sales_reps.shape)
print("accounts:", accounts.shape)
print("opportunities:", opportunities.shape)
print("quotas:", quotas.shape)
print("transactions:", transactions.shape)
print("sales_activities:", sales_activities.shape)

print("\n--- NULL CHECKS ---")
print("sales_reps\n", sales_reps.isnull().sum())
print("\naccounts\n", accounts.isnull().sum())
print("\nopportunities\n", opportunities.isnull().sum())
print("\nquotas\n", quotas.isnull().sum())
print("\ntransactions\n", transactions.isnull().sum())
print("\nsales_activities\n", sales_activities.isnull().sum())

print("\n--- KEY CHECKS ---")
print("Unique rep IDs:", sales_reps["rep_id"].nunique())
print("Unique account IDs:", accounts["account_id"].nunique())
print("Unique opportunity IDs:", opportunities["opportunity_id"].nunique())

print(
    "Closed Won opportunities:",
    (opportunities["stage"] == "Closed Won").sum()
)

print(
    "Sales transactions:",
    len(transactions)
)

print("\n--- DUPLICATE KEY CHECKS ---")
print("sales_reps duplicate rep_id:",
      sales_reps["rep_id"].duplicated().sum())

print("accounts duplicate account_id:",
      accounts["account_id"].duplicated().sum())

print("opportunities duplicate opportunity_id:",
      opportunities["opportunity_id"].duplicated().sum())

print("transactions duplicate transaction_id:",
      transactions["transaction_id"].duplicated().sum())
# -----------------------------
# BUSINESS LOGIC VALIDATION
# -----------------------------

print("\n--- BUSINESS LOGIC CHECKS ---")

# Close dates outside dataset
print(
    "Actual close dates after dataset end:",
    (opportunities["actual_close_date"] > END_DATE).sum()
)

print(
    "Expected close dates after dataset end:",
    (opportunities["expected_close_date"] > END_DATE).sum()
)

# Opportunity before rep hire date
opp_rep_check = opportunities.merge(
    sales_reps[["rep_id", "hire_date"]],
    on="rep_id",
    how="left"
)

print(
    "Opportunities before rep hire date:",
    (opp_rep_check["created_date"] < opp_rep_check["hire_date"]).sum()
)

# Opportunity before account creation
opp_account_check = opportunities.merge(
    accounts[["account_id", "created_date"]],
    on="account_id",
    how="left",
    suffixes=("_opportunity", "_account")
)

print(
    "Opportunities before account creation:",
    (
        opp_account_check["created_date_opportunity"]
        < opp_account_check["created_date_account"]
    ).sum()
)
# -----------------------------
# EXPORT CSV FILES
# -----------------------------

sales_reps.to_csv("sales_reps.csv", index=False)
accounts.to_csv("accounts.csv", index=False)
opportunities.to_csv("opportunities.csv", index=False)
quotas.to_csv("quotas.csv", index=False)
transactions.to_csv("sales_transactions.csv", index=False)
sales_activities.to_csv("sales_activities.csv", index=False)

print("\nCSV files exported successfully.")