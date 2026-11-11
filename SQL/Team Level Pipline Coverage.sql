USE SalesPerformancePortfolio;
GO
-- ============================
-- TEAM PIPELINE COVERAGE
-- ============================

WITH team_open_pipeline AS (
    SELECT
        r.team,
        SUM(o.opportunity_value) AS open_pipeline_value,
        SUM(o.opportunity_value * o.probability) AS weighted_pipeline_value
    FROM dbo.opportunities o
    JOIN dbo.sales_reps r
        ON o.rep_id = r.rep_id
    WHERE o.close_status = 'Open'
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
)

SELECT
    tq.team,

    tq.total_quota,

    COALESCE(tp.open_pipeline_value, 0) AS open_pipeline_value,

    COALESCE(tp.weighted_pipeline_value, 0) AS weighted_pipeline_value,

    ROUND(
        COALESCE(tp.open_pipeline_value, 0) * 1.0
        / NULLIF(tq.total_quota, 0),
        2
    ) AS pipeline_coverage_ratio,

    ROUND(
        COALESCE(tp.weighted_pipeline_value, 0) * 1.0
        / NULLIF(tq.total_quota, 0),
        2
    ) AS weighted_pipeline_coverage_ratio

FROM team_quota tq

LEFT JOIN team_open_pipeline tp
    ON tq.team = tp.team

ORDER BY pipeline_coverage_ratio DESC;