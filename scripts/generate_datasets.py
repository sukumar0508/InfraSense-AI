import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# Folder path
folder_path = 'data'

# Ensure the path exists
os.makedirs(folder_path, exist_ok=True)

# 1️⃣ server_logs.csv
timestamps = pd.date_range(start="2024-06-01", periods=100, freq="H")
servers = ['srv_001', 'srv_002', 'srv_003', 'srv_004']
server_logs = []

for server in servers:
    for ts in timestamps:
        server_logs.append({
            'server_id': server,
            'timestamp': ts,
            'cpu_usage': round(np.random.uniform(10, 90), 2),
            'ram_usage': round(np.random.uniform(30, 95), 2),
            'disk_io': round(np.random.uniform(5, 50), 2),
            'net_usage': round(np.random.uniform(20, 100), 2)
        })

server_logs_df = pd.DataFrame(server_logs)
server_logs_path = os.path.join(folder_path, "server_logs.csv")
server_logs_df.to_csv(server_logs_path, index=False)

# 2️⃣ helpdesk_tickets.csv
issues = ['VPN not working', 'Email access issue', 'Slow internet', 'System crash', 'Software install required']
departments = ['HR', 'IT', 'Finance', 'Sales', 'Marketing']
priorities = ['Low', 'Medium', 'High']

helpdesk_tickets = []

for i in range(1, 101):
    helpdesk_tickets.append({
        'ticket_id': 10000 + i,
        'timestamp': datetime(2024, 6, 1, random.randint(0, 23), random.randint(0, 59)),
        'issue': random.choice(issues),
        'department': random.choice(departments),
        'priority': random.choice(priorities),
        'resolved': random.choice(['Yes', 'No'])
    })

helpdesk_df = pd.DataFrame(helpdesk_tickets)
helpdesk_path = os.path.join(folder_path, "helpdesk_tickets.csv")
helpdesk_df.to_csv(helpdesk_path, index=False)

# 3️⃣ cost_report.csv
cost_report = []

for server in servers:
    for month in ['2024-04', '2024-05', '2024-06']:
        cost_report.append({
            'month': month,
            'server_id': server,
            'service': random.choice(['EC2 Instance', 'RDS', 'S3 Storage', 'Elastic Load Balancer']),
            'cost': round(np.random.uniform(80, 200), 2)
        })

cost_df = pd.DataFrame(cost_report)
cost_path = os.path.join(folder_path, "cost_report.csv")
cost_df.to_csv(cost_path, index=False)

server_logs_path, helpdesk_path, cost_path
