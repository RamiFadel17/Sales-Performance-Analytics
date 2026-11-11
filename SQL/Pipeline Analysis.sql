USE SalesPerformancePortfolio;
GO

SELECT
    forecast_category,

    COUNT(*) AS open_opportunities,

    SUM(opportunity_value) AS pipeline_value,

    ROUND(
        SUM(opportunity_value * probability),
        2
    ) AS weighted_pipeline,

    ROUND(
        AVG(opportunity_value * 1.0),
        2
    ) AS avg_deal_size,

    ROUND(
        AVG(DATEDIFF(
            DAY,
            created_date,
            '2026-12-31'
        ) * 1.0),
        1
    ) AS avg_opportunity_age_days

FROM dbo.opportunities

WHERE close_status = 'Open'

GROUP BY forecast_category

ORDER BY
    CASE forecast_category
        WHEN 'Commit' THEN 1
        WHEN 'Best Case' THEN 2
        WHEN 'Pipeline' THEN 3
        ELSE 4
    END;