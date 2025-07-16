USE infrasense_ai;

-- Top 5 helpdesk issues
SELECT issue, COUNT(*) AS frequency
FROM helpdesk_tickets
GROUP BY issue
ORDER BY frequency DESC
LIMIT 5;

-- Average CPU per server
SELECT server_id, AVG(cpu_usage) AS avg_cpu
FROM server_logs
GROUP BY server_id;

-- Total cost by month
SELECT month, server_id, SUM(cost) AS total_cost
FROM cost_report
GROUP BY month, server_id;
