def cpu_alert_level(df):
    alerts = []
    high_cpu = df[df['cpu'] > 85]
    for _, row in high_cpu.iterrows():
        alerts.append(f"🚨 High CPU Alert | Server: {row['server_id']} | CPU: {row['cpu']}%")
    return alerts
