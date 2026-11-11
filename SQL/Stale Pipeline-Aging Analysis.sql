USE SalesPerformancePortfolio;
GO

SELECT
    CASE
        WHEN DATEDIFF(DAY, created_date, '2026-12-31') <= 30
            THEN '0-30 Days'

        WHEN DATEDIFF(DAY, created_date, '2026-12-31') <= 60
            THEN '31-60 Days'

        WHEN DATEDIFF(DAY, created_date, '2026-12-31') <= 90
            THEN '61-90 Days'

        WHEN DATEDIFF(DAY, created_date, '2026-12-31') <= 180
            THEN '91-180 Days'

        ELSE '180+ Days'
    END AS age_bucket,

    COUNT(*) AS open_opportunities,

    SUM(opportunity_value) AS pipeline_value,

    ROUND(
        SUM(opportunity_value * probability),
        2
    ) AS weighted_pipeline

FROM dbo.opportunities

WHERE close_status = 'Open'

GROUP BY
    CASE
        WHEN DATEDIFF(DAY, created_date, '2026-12-31') <= 30
            THEN '0-30 Days'

        WHEN DATEDIFF(DAY, created_date, '2026-12-31') <= 60
            THEN '31-60 Days'

        WHEN DATEDIFF(DAY, created_date, '2026-12-31') <= 90
            THEN '61-90 Days'

        WHEN DATEDIFF(DAY, created_date, '2026-12-31') <= 180
            THEN '91-180 Days'

        ELSE '180+ Days'
    END

ORDER BY
    MIN(DATEDIFF(DAY, created_date, '2026-12-31'));