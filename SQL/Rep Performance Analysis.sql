USE SalesPerformancePortfolio;
GO

SELECT 'sales_reps' AS table_name, COUNT(*) AS row_count FROM dbo.sales_reps
UNION ALL
SELECT 'accounts', COUNT(*) FROM dbo.accounts
UNION ALL
SELECT 'opportunities', COUNT(*) FROM dbo.opportunities
UNION ALL
SELECT 'quotas', COUNT(*) FROM dbo.quotas
UNION ALL
SELECT 'sales_transactions', COUNT(*) FROM dbo.sales_transactions
UNION ALL
SELECT 'sales_activities', COUNT(*) FROM dbo.sales_activities;
SELECT TOP 5 * FROM dbo.sales_reps;
SELECT TOP 5 * FROM dbo.accounts;
SELECT TOP 5 * FROM dbo.opportunities;
SELECT TOP 5 * FROM dbo.quotas;
SELECT TOP 5 * FROM dbo.sales_transactions;
SELECT TOP 5 * FROM dbo.sales_activities;
ALTER TABLE dbo.quotas
ALTER COLUMN quarter VARCHAR(10);
UPDATE dbo.quotas
SET quarter =
    CASE
        WHEN month BETWEEN 1 AND 3 THEN 'Q1'
        WHEN month BETWEEN 4 AND 6 THEN 'Q2'
        WHEN month BETWEEN 7 AND 9 THEN 'Q3'
        WHEN month BETWEEN 10 AND 12 THEN 'Q4'
    END;
    WITH revenue_by_rep AS (
    SELECT
        rep_id,
        SUM(net_revenue) AS total_revenue
    FROM dbo.sales_transactions
    GROUP BY rep_id
),

quota_by_rep AS (
    SELECT
        rep_id,
        SUM(monthly_quota) AS total_quota
    FROM dbo.quotas
    GROUP BY rep_id
)

SELECT
    r.rep_id,
    r.rep_name,
    r.team,
    r.region,
    COALESCE(rv.total_revenue, 0) AS total_revenue,
    COALESCE(q.total_quota, 0) AS total_quota,
    ROUND(
        COALESCE(rv.total_revenue, 0) * 100.0
        / NULLIF(q.total_quota, 0),
        2
    ) AS quota_attainment_pct
FROM dbo.sales_reps r
LEFT JOIN revenue_by_rep rv
    ON r.rep_id = rv.rep_id
LEFT JOIN quota_by_rep q
    ON r.rep_id = q.rep_id
ORDER BY quota_attainment_pct DESC;
USE SalesPerformancePortfolio;
GO

WITH rep_revenue AS (
    SELECT
        rep_id,
        SUM(net_revenue) AS total_revenue
    FROM dbo.sales_transactions
    GROUP BY rep_id
),

rep_quota AS (
    SELECT
        rep_id,
        SUM(monthly_quota) AS total_quota
    FROM dbo.quotas
    GROUP BY rep_id
),

rep_opportunities AS (
    SELECT
        rep_id,
        COUNT(*) AS total_opportunities,
        SUM(CASE WHEN close_status = 'Won' THEN 1 ELSE 0 END) AS won_opportunities,
        AVG(CASE
            WHEN close_status IN ('Won', 'Lost')
            THEN sales_cycle_days
        END) AS avg_sales_cycle_days
    FROM dbo.opportunities
    GROUP BY rep_id
)

SELECT
    r.rep_id,
    r.rep_name,
    r.team,
    r.region,

    COALESCE(rv.total_revenue, 0) AS total_revenue,
    COALESCE(q.total_quota, 0) AS total_quota,

    ROUND(
        COALESCE(rv.total_revenue, 0) * 100.0
        / NULLIF(q.total_quota, 0),
        2
    ) AS quota_attainment_pct,

    COALESCE(o.total_opportunities, 0) AS total_opportunities,
    COALESCE(o.won_opportunities, 0) AS won_opportunities,

    ROUND(
        COALESCE(o.won_opportunities, 0) * 100.0
        / NULLIF(o.total_opportunities, 0),
        2
    ) AS win_rate_pct,

    ROUND(o.avg_sales_cycle_days, 1) AS avg_sales_cycle_days

FROM dbo.sales_reps r

LEFT JOIN rep_revenue rv
    ON r.rep_id = rv.rep_id

LEFT JOIN rep_quota q
    ON r.rep_id = q.rep_id

LEFT JOIN rep_opportunities o
    ON r.rep_id = o.rep_id

ORDER BY quota_attainment_pct DESC;