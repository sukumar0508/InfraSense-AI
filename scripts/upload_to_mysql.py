import pandas as pd
import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Suku@#0508',
    database='infrasense_ai'
)

cursor = conn.cursor()

# Load CSV files
server_logs = pd.read_csv('C:/Users/shash/Desktop/InfraSense-AI/data/server_logs.csv')
helpdesk = pd.read_csv('C:/Users/shash/Desktop/InfraSense-AI/data/helpdesk_tickets.csv')
cost_report = pd.read_csv('C:/Users/shash/Desktop/InfraSense-AI/data/cost_report.csv')

# Insert into server_logs
for _, row in server_logs.iterrows():
    cursor.execute("""
        INSERT INTO server_logs (server_id, timestamp, cpu_usage, ram_usage, disk_io, net_usage)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, tuple(row))

# Insert into helpdesk_tickets
for _, row in helpdesk.iterrows():
    cursor.execute("""
        INSERT INTO helpdesk_tickets (ticket_id, timestamp, issue, department, priority, resolved)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, tuple(row))

# Insert into cost_report
for _, row in cost_report.iterrows():
    cursor.execute("""
        INSERT INTO cost_report (month, server_id, service, cost)
        VALUES (%s, %s, %s, %s)
    """, tuple(row))

# Commit and close
conn.commit()
conn.close()

print("✅ All data uploaded successfully to MySQL!")
