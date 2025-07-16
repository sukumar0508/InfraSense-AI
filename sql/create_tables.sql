-- Use your database
CREATE DATABASE IF NOT EXISTS infrasense_ai;
USE infrasense_ai;

-- 1. server_logs
CREATE TABLE IF NOT EXISTS server_logs (
  server_id VARCHAR(20),
  timestamp DATETIME,
  cpu_usage FLOAT,
  ram_usage FLOAT,
  disk_io FLOAT,
  net_usage FLOAT
);



CREATE TABLE IF NOT EXISTS helpdesk_tickets (
  ticket_id INT PRIMARY KEY,
  timestamp DATETIME,
  issue VARCHAR(255),
  department VARCHAR(100),
  priority VARCHAR(50),
  resolved VARCHAR(10)
);


-- 3. cost_report
CREATE TABLE IF NOT EXISTS cost_report (
  month VARCHAR(10),
  server_id VARCHAR(20),
  service VARCHAR(100),
  cost FLOAT
);

SHOW TABLES;

