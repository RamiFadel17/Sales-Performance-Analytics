USE SalesPerformancePortfolio;
GO

WITH team_activity AS (
    SELECT
        r.team,

        SUM(a.calls) AS total_calls,
        SUM(a.emails) AS total_emails,
        SUM(a.meetings) AS total_meetings,
        SUM(a.demos) AS total_demos,
        SUM(a.opportunities_created) AS opportunities_created,

        SUM(a.calls + a.emails + a.meetings + a.demos) AS total_activities

    FROM dbo.sales_activities a

    JOIN dbo.sales_reps r
        ON a.rep_id = r.rep_id

    GROUP BY r.team
),

team_wins AS (
    SELECT
        r.team,
        COUNT(*) AS won_opportunities
    FROM dbo.opportunities o

    JOIN dbo.sales_reps r
        ON o.rep_id = r.rep_id

    WHERE o.close_status = 'Won'

    GROUP BY r.team
)

SELECT
    ta.team,

    ta.total_calls,
    ta.total_emails,
    ta.total_meetings,
    ta.total_demos,
    ta.opportunities_created,
    ta.total_activities,

    COALESCE(tw.won_opportunities, 0) AS won_opportunities,

    ROUND(
        ta.opportunities_created * 100.0
        / NULLIF(ta.total_activities, 0),
        2
    ) AS activity_to_opportunity_pct,

    ROUND(
        COALESCE(tw.won_opportunities, 0) * 100.0
        / NULLIF(ta.opportunities_created, 0),
        2
    ) AS opportunity_to_win_pct

FROM team_activity ta

LEFT JOIN team_wins tw
    ON ta.team = tw.team

ORDER BY opportunity_to_win_pct DESC;