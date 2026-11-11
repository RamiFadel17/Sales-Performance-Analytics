USE SalesPerformancePortfolio;
GO

SELECT
    stage,

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
        AVG(
            DATEDIFF(
                DAY,
                created_date,
                '2026-12-31'
            ) * 1.0
        ),
        1
    ) AS avg_opportunity_age_days

FROM dbo.opportunities

WHERE close_status = 'Open'

GROUP BY stage

ORDER BY
    CASE stage
        WHEN 'Prospecting' THEN 1
        WHEN 'Qualification' THEN 2
        WHEN 'Discovery' THEN 3
        WHEN 'Proposal' THEN 4
        WHEN 'Negotiation' THEN 5
        ELSE 6
    END;