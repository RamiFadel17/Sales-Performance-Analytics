USE SalesPerformancePortfolio;
GO

SELECT
    r.team,
    o.forecast_category,

    COUNT(*) AS opportunities,

    SUM(o.opportunity_value) AS pipeline_value,

    ROUND(
        SUM(o.opportunity_value * o.probability),
        2
    ) AS weighted_pipeline,

    ROUND(
        AVG(o.opportunity_value * 1.0),
        2
    ) AS avg_deal_size

FROM dbo.opportunities o

JOIN dbo.sales_reps r
    ON o.rep_id = r.rep_id

WHERE o.close_status = 'Open'

GROUP BY
    r.team,
    o.forecast_category

ORDER BY
    r.team,

    CASE o.forecast_category
        WHEN 'Commit' THEN 1
        WHEN 'Best Case' THEN 2
        WHEN 'Pipeline' THEN 3
        ELSE 4
    END;