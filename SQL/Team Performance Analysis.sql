USE SalesPerformancePortfolio;
GO

WITH team_revenue AS (
    SELECT
        r.team,
        SUM(t.net_revenue) AS total_revenue
    FROM dbo.sales_transactions t
    JOIN dbo.sales_reps r
        ON t.rep_id = r.rep_id
    GROUP BY r.team
),

team_quota AS (
    SELECT
        r.team,
        SUM(q.monthly_quota) AS total_quota
    FROM dbo.quotas q
    JOIN dbo.sales_reps r
        ON q.rep_id = r.rep_id
    GROUP BY r.team
),

team_opportunities AS (
    SELECT
        r.team,
        COUNT(*) AS total_opportunities,
        SUM(CASE WHEN o.close_status = 'Won' THEN 1 ELSE 0 END) AS won_opportunities,
        AVG(
            CASE
                WHEN o.close_status IN ('Won', 'Lost')
                THEN o.sales_cycle_days
            END
        ) AS avg_sales_cycle_days
    FROM dbo.opportunities o
    JOIN dbo.sales_reps r
        ON o.rep_id = r.rep_id
    GROUP BY r.team
)

SELECT
    r.team,
    COUNT(DISTINCT r.rep_id) AS rep_count,

    COALESCE(tr.total_revenue, 0) AS total_revenue,
    COALESCE(tq.total_quota, 0) AS total_quota,

    ROUND(
        COALESCE(tr.total_revenue, 0) * 100.0
        / NULLIF(tq.total_quota, 0),
        2
    ) AS quota_attainment_pct,

    COALESCE(topp.total_opportunities, 0) AS total_opportunities,
    COALESCE(topp.won_opportunities, 0) AS won_opportunities,

    ROUND(
        COALESCE(topp.won_opportunities, 0) * 100.0
        / NULLIF(topp.total_opportunities, 0),
        2
    ) AS win_rate_pct,

    ROUND(topp.avg_sales_cycle_days, 1) AS avg_sales_cycle_days

FROM dbo.sales_reps r

LEFT JOIN team_revenue tr
    ON r.team = tr.team

LEFT JOIN team_quota tq
    ON r.team = tq.team

LEFT JOIN team_opportunities topp
    ON r.team = topp.team

GROUP BY
    r.team,
    tr.total_revenue,
    tq.total_quota,
    topp.total_opportunities,
    topp.won_opportunities,
    topp.avg_sales_cycle_days

ORDER BY quota_attainment_pct DESC;