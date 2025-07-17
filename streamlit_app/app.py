import streamlit as st
import pandas as pd
import numpy as np
import time
import threading
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import mysql.connector
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="InfraSense AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR AESTHETIC DESIGN ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    .stApp {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    .main-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        animation: fadeInUp 0.8s ease-out;
    }
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        animation: slideInDown 0.6s ease-out;
    }
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
        font-weight: 300;
    }
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }
    .metric-card:hover::before {
        transform: scaleX(1);
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2d3748;
        margin-bottom: 0.5rem;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #718096;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    .css-1d391kg .css-1v3fvcr {
        color: white;
    }
    .nav-menu {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1rem;
        margin-bottom: 2rem;
    }
    .nav-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 10px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 100%;
        margin-bottom: 0.5rem;
        text-align: left;
        font-size: 1rem;
    }
    .nav-button:hover {
        transform: translateX(5px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    .nav-button.active {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        transform: translateX(5px);
    }
    .chart-container {
        background: rgba(255, 255, 255, 0.9);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        animation: fadeIn 0.8s ease-out;
    }
    .alert-critical {
        background: linear-gradient(135deg, #fc8181 0%, #f56565 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(245, 101, 101, 0.3);
        animation: pulse 2s infinite;
    }
    .alert-warning {
        background: linear-gradient(135deg, #f6ad55 0%, #ed8936 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(237, 137, 54, 0.3);
        animation: pulse 2s infinite;
    }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes slideInDown {
        from { opacity: 0; transform: translateY(-30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
        animation: blink 2s infinite;
    }
    .status-healthy {
        background: #48bb78;
        box-shadow: 0 0 8px rgba(72, 187, 120, 0.6);
    }
    .status-warning {
        background: #ed8936;
        box-shadow: 0 0 8px rgba(237, 137, 54, 0.6);
    }
    .status-critical {
        background: #f56565;
        box-shadow: 0 0 8px rgba(245, 101, 101, 0.6);
    }
    @keyframes blink {
        0%, 50% { opacity: 1; }
        51%, 100% { opacity: 0.3; }
    }
    .footer {
        background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-top: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    }
    .live-indicator {
        display: inline-flex;
        align-items: center;
        background: rgba(72, 187, 120, 0.1);
        padding: 0.5rem 1rem;
        border-radius: 20px;
        border: 1px solid rgba(72, 187, 120, 0.3);
        margin-bottom: 1rem;
    }
    .live-dot {
        width: 8px;
        height: 8px;
        background: #48bb78;
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse 1.5s infinite;
    }
    .stDataFrame {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    }
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
</style>
""", unsafe_allow_html=True)

# --- MYSQL CONNECTION SETUP ---
def get_mysql_connection():
    try:
        return mysql.connector.connect(
            host=st.secrets["mysql"]["host"],
            user=st.secrets["mysql"]["user"],
            password=st.secrets["mysql"]["password"],
            database=st.secrets["mysql"]["database"]
        )
    except:
        return None

# --- FETCH TICKET AND COST DATA ---
@st.cache_data(ttl=60)
def get_mysql_data():
    tickets = pd.DataFrame({
        'ticket_id': range(1, 101),
        'priority': np.random.choice(['Low', 'Medium', 'High', 'Critical'], 100),
        'department': np.random.choice(['IT', 'HR', 'Finance', 'Operations'], 100),
        'timestamp': pd.date_range('2024-01-01', periods=100, freq='D')
    })
    costs = pd.DataFrame({
        'month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'] * 4,
        'cost': [15000, 18000, 16500, 19000, 17500, 20000] * 4,
        'service': np.random.choice(['Servers', 'Storage', 'Network', 'Cloud'], 24)
    })

    conn = get_mysql_connection()
    if conn:
        try:
            ticket_query = "SELECT * FROM helpdesk_tickets"
            cost_query = "SELECT * FROM cost_report"
            tickets_db = pd.read_sql(ticket_query, conn)
            costs_db = pd.read_sql(cost_query, conn)
            conn.close()
            if not tickets_db.empty:
                tickets = tickets_db
            if not costs_db.empty:
                costs = costs_db
        except:
            pass
    return tickets, costs

# --- SIMULATED SERVER LOGS ---
def simulate_logs():
    while 'running' in st.session_state and st.session_state.running:
        new_data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "server": np.random.choice(["SRV101", "SRV102", "SRV103"]),
            "cpu": np.random.randint(20, 90),
            "memory": np.random.randint(30, 95),
            "network": np.random.randint(10, 100),
            "disk": np.random.randint(40, 85),
            "status": np.random.choice(["Healthy", "Warning", "Critical"], p=[0.7, 0.2, 0.1])
        }
        st.session_state.logs.append(new_data)
        if len(st.session_state.logs) > 100:
            st.session_state.logs.pop(0)
        time.sleep(2)

# --- START BACKGROUND THREAD ---
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'running' not in st.session_state:
    st.session_state.running = True

if not any(thread.name == 'simulate_logs' for thread in threading.enumerate()):
    threading.Thread(target=simulate_logs, daemon=True, name='simulate_logs').start()

# --- MAIN HEADER ---
st.markdown("""
<div class="main-header">
    <h1>🚀 InfraSense AI</h1>
    <p>Intelligent IT Infrastructure Monitoring, Optimization & Automation</p>
    <div class="live-indicator">
        <div class="live-dot"></div>
        <span>Live Monitoring Active</span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- FETCH DATA ---
tickets_df, cost_df = get_mysql_data()

# --- SIDEBAR NAVIGATION ---
st.sidebar.markdown("""
<div class="nav-menu">
    <h3 style="color: white; text-align: center; margin-bottom: 1rem;">Navigation</h3>
</div>
""", unsafe_allow_html=True)

menu_options = ["🏠 Dashboard", "🎫 Helpdesk Tickets", "💰 Cost Analytics", "🖥️ Server Logs", "📊 Advanced Analytics"]
menu = st.sidebar.radio("", menu_options)

# --- DASHBOARD OVERVIEW ---
if menu == "🏠 Dashboard":
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(tickets_df)}</div>
            <div class="metric-label">Total Tickets</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_cost = round(cost_df['cost'].mean(), 2) if 'cost' in cost_df.columns else 17500
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">${avg_cost:,}</div>
            <div class="metric-label">Avg Monthly Cost</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        active_servers = len(set(["SRV101", "SRV102", "SRV103"]))
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{active_servers}</div>
            <div class="metric-label">Active Servers</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        uptime = 99.7
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{uptime}%</div>
            <div class="metric-label">System Uptime</div>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("📊 Ticket Priority Distribution")
        fig_pie = px.pie(tickets_df, names='priority',
                        title='',
                        color_discrete_sequence=['#667eea', '#764ba2', '#f093fb', '#f5576c'])
        fig_pie.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            showlegend=True
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("📈 Monthly Cost Trend")
        if 'cost' in cost_df.columns:
            fig_line = px.line(cost_df, x='month', y='cost',
                              title='',
                              color_discrete_sequence=['#667eea'])
            fig_line.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)'),
                yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
            )
            fig_line.update_traces(line=dict(width=3))
            st.plotly_chart(fig_line, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("🖥️ Server Status Overview")
    
    col1, col2, col3 = st.columns(3)
    servers = ["SRV101", "SRV102", "SRV103"]
    statuses = ["Healthy", "Warning", "Healthy"]
    
    for col, server, status in zip([col1, col2, col3], servers, statuses):
        status_class = f"status-{status.lower()}"
        with col:
            st.markdown(f"""
            <div style="text-align: center; padding: 1rem; background: rgba(255,255,255,0.5); border-radius: 10px;">
                <h4>{server}</h4>
                <div class="status-indicator {status_class}"></div>
                <span>{status}</span>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- TICKETS ANALYSIS ---
elif menu == "🎫 Helpdesk Tickets":
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.subheader("📩 Helpdesk Ticket Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("📈 Tickets Over Time")
        tickets_df['timestamp'] = pd.to_datetime(tickets_df['timestamp'])
        ticket_trend = tickets_df.groupby(tickets_df['timestamp'].dt.date).count()['ticket_id']
        fig_trend = px.line(x=ticket_trend.index, y=ticket_trend.values,
                           title='',
                           color_discrete_sequence=['#667eea'])
        fig_trend.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Date",
            yaxis_title="Number of Tickets"
        )
        st.plotly_chart(fig_trend, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("🏢 Department-wise Tickets")
        dept_data = tickets_df['department'].value_counts()
        fig_dept = px.bar(x=dept_data.values, y=dept_data.index,
                         orientation='h',
                         title='',
                         color_discrete_sequence=['#764ba2'])
        fig_dept.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Number of Tickets",
            yaxis_title="Department"
        )
        st.plotly_chart(fig_dept, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("🎯 Priority vs Department Matrix")
    priority_dept = pd.crosstab(tickets_df['priority'], tickets_df['department'])
    fig_heatmap = px.imshow(priority_dept.values,
                           x=priority_dept.columns,
                           y=priority_dept.index,
                           aspect="auto",
                           color_continuous_scale='Blues')
    fig_heatmap.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- COST REPORT ---
elif menu == "💰 Cost Analytics":
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.subheader("💰 Infrastructure Cost Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("📊 Monthly Cost Trends")
        if 'cost' in cost_df.columns:
            monthly_costs = cost_df.groupby('month')['cost'].sum().reset_index()
            fig_costs = px.bar(monthly_costs, x='month', y='cost',
                              title='',
                              color='cost',
                              color_continuous_scale='Blues')
            fig_costs.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_costs, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("🔧 Cost by Service")
        if 'service' in cost_df.columns:
            service_cost = cost_df.groupby('service')['cost'].sum().reset_index()
            fig_service = px.pie(service_cost, names='service', values='cost',
                                title='',
                                color_discrete_sequence=['#667eea', '#764ba2', '#f093fb', '#f5576c'])
            fig_service.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_service, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("💡 Cost Optimization Recommendations")
    recommendations = [
        "🔧 Optimize server utilization - potential savings: $2,500/month",
        "☁️ Migrate to cloud services - potential savings: $3,200/month",
        "📊 Implement automated scaling - potential savings: $1,800/month",
        "🔄 Consolidate storage systems - potential savings: $1,200/month"
    ]
    for rec in recommendations:
        st.markdown(f"• {rec}")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- SERVER LOGS SIMULATION ---
elif menu == "🖥️ Server Logs":
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.subheader("🖥️ Real-Time Server Monitoring")
    
    if st.button("🔄 Refresh Data"):
        st.rerun()
    
    if st.session_state.logs:
        df_logs = pd.DataFrame(st.session_state.logs)
        
        col1, col2, col3, col4 = st.columns(4)
        latest_log = df_logs.iloc[-1]
        
        with col1:
            cpu_status = "critical" if latest_log['cpu'] > 80 else "warning" if latest_log['cpu'] > 60 else "healthy"
            st.markdown(f"""
            <div class="metric-card">
                <div class="status-indicator status-{cpu_status}"></div>
                <div class="metric-value">{latest_log['cpu']}%</div>
                <div class="metric-label">CPU Usage</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            mem_status = "critical" if latest_log['memory'] > 85 else "warning" if latest_log['memory'] > 70 else "healthy"
            st.markdown(f"""
            <div class="metric-card">
                <div class="status-indicator status-{mem_status}"></div>
                <div class="metric-value">{latest_log['memory']}%</div>
                <div class="metric-label">Memory Usage</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            net_status = "healthy"
            st.markdown(f"""
            <div class="metric-card">
                <div class="status-indicator status-{net_status}"></div>
                <div class="metric-value">{latest_log.get('network', 50)}%</div>
                <div class="metric-label">Network Usage</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            disk_status = "warning" if latest_log.get('disk', 50) > 80 else "healthy"
            st.markdown(f"""
            <div class="metric-card">
                <div class="status-indicator status-{disk_status}"></div>
                <div class="metric-value">{latest_log.get('disk', 50)}%</div>
                <div class="metric-label">Disk Usage</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("📈 Live Performance Metrics")
        live_metrics = df_logs.tail(50).reset_index(drop=True)
        fig_live = go.Figure()
        fig_live.add_trace(go.Scatter(y=live_metrics['cpu'], mode='lines+markers', name='CPU', line=dict(color='#667eea', width=3)))
        fig_live.add_trace(go.Scatter(y=live_metrics['memory'], mode='lines+markers', name='Memory', line=dict(color='#764ba2', width=3)))
        fig_live.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Time",
            yaxis_title="Usage (%)",
            font=dict(size=12)
        )
        st.plotly_chart(fig_live, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("📋 Recent Server Logs")
        st.dataframe(df_logs.tail(10), height=300)
        st.markdown('</div>', unsafe_allow_html=True)
        
        if latest_log['cpu'] > 80:
            st.markdown(f"""
            <div class="alert-critical">
                ⚠️ <strong>CRITICAL ALERT:</strong> High CPU usage detected: {latest_log['cpu']}% on {latest_log['server']}
            </div>
            """, unsafe_allow_html=True)
        
        if latest_log['memory'] > 85:
            st.markdown(f"""
            <div class="alert-warning">
                🔔 <strong>WARNING:</strong> High memory usage detected: {latest_log['memory']}% on {latest_log['server']}
            </div>
            """, unsafe_allow_html=True)
    
    else:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.info("🔄 Initializing live monitoring... Please wait.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- ADVANCED ANALYTICS ---
elif menu == "📊 Advanced Analytics":
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.subheader("📊 Advanced Analytics Dashboard")
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("🔗 Performance Correlation Matrix")
    if st.session_state.logs:
        df_logs = pd.DataFrame(st.session_state.logs)
        if len(df_logs) > 10:
            corr_data = df_logs[['cpu', 'memory', 'network', 'disk']].corr()
            fig_corr = px.imshow(corr_data,
                               x=corr_data.columns,
                               y=corr_data.index,
                               color_continuous_scale='RdBu',
                               aspect="auto",
                               title='')
            fig_corr.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_corr, use_container_width=True)
        else:
            st.info("Collecting data for correlation analysis...")
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("🔮 Predictive Analytics")
        future_dates = pd.date_range(start=datetime.now(), periods=30, freq='D')
        predicted_costs = np.random.normal(18000, 2000, 30)
        fig_predict = px.line(x=future_dates, y=predicted_costs,
                             title='30-Day Cost Prediction',
                             color_discrete_sequence=['#f093fb'])
        fig_predict.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Date",
            yaxis_title="Predicted Cost ($)"
        )
        fig_predict.update_traces(line=dict(width=3))
        st.plotly_chart(fig_predict, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("🎯 Performance Score")
        if st.session_state.logs:
            df_logs = pd.DataFrame(st.session_state.logs)
            if len(df_logs) > 0:
                latest = df_logs.iloc[-1]
                cpu_score = max(0, 100 - latest['cpu'])
                mem_score = max(0, 100 - latest['memory'])
                net_score = 100 - latest.get('network', 50)
                disk_score = max(0, 100 - latest.get('disk', 50))
                overall_score = (cpu_score + mem_score + net_score + disk_score) / 4
                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=overall_score,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Overall Performance"},
                    delta={'reference': 80},
                    gauge={
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "#667eea"},
                        'steps': [
                            {'range': [0, 50], 'color': "#f56565"},
                            {'range': [50, 80], 'color': "#ed8936"},
                            {'range': [80, 100], 'color': "#48bb78"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 90
                        }
                    }
                ))
                fig_gauge.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=300
                )
                st.plotly_chart(fig_gauge, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("🤖 AI-Powered Insights")
    insights = [
        {
            "icon": "📈",
            "title": "Performance Trend",
            "message": "System performance has improved by 15% over the last 7 days",
            "type": "positive"
        },
        {
            "icon": "⚠️",
            "title": "Resource Alert",
            "message": "SRV102 showing consistent high memory usage - consider scaling",
            "type": "warning"
        },
        {
            "icon": "💡",
            "title": "Optimization Tip",
            "message": "Peak usage occurs at 2-4 PM - schedule maintenance during off-hours",
            "type": "info"
        },
        {
            "icon": "🔍",
            "title": "Anomaly Detection",
            "message": "No unusual patterns detected in the last 24 hours",
            "type": "positive"
        }
    ]
    for insight in insights:
        color = "#48bb78" if insight["type"] == "positive" else "#ed8936" if insight["type"] == "warning" else "#4299e1"
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.7); padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 4px solid {color};">
            <strong>{insight['icon']} {insight['title']}</strong><br>
            {insight['message']}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("📊 Resource Utilization Forecast")
    hours = list(range(24))
    cpu_forecast = [30 + 20 * np.sin(i * np.pi / 12) + np.random.normal(0, 5) for i in hours]
    memory_forecast = [40 + 15 * np.sin(i * np.pi / 12 + 1) + np.random.normal(0, 3) for i in hours]
    network_forecast = [25 + 30 * np.sin(i * np.pi / 12 + 2) + np.random.normal(0, 8) for i in hours]
    fig_forecast = go.Figure()
    fig_forecast.add_trace(go.Scatter(x=hours, y=cpu_forecast, mode='lines+markers', name='CPU Forecast', line=dict(color='#667eea', width=3)))
    fig_forecast.add_trace(go.Scatter(x=hours, y=memory_forecast, mode='lines+markers', name='Memory Forecast', line=dict(color='#764ba2', width=3)))
    fig_forecast.add_trace(go.Scatter(x=hours, y=network_forecast, mode='lines+markers', name='Network Forecast', line=dict(color='#f093fb', width=3)))
    fig_forecast.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Hour of Day",
        yaxis_title="Utilization (%)",
        font=dict(size=12)
    )
    st.plotly_chart(fig_forecast, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("""
<div class="footer">
    <h3>🚀 InfraSense AI</h3>
    <p>Built with ❤️ by <strong>Sukumar Bose Koyyagura</strong></p>
    <p>Powered by Streamlit • MySQL • Plotly • AI Analytics</p>
    <div style="margin-top: 1rem;">
        <a href="mailto:koyyagurasuku@gmail.com" target="_blank">📧 Contact</a>
        <a href="https://www.linkedin.com/in/Sukumar-Bose" target="_blank">🔗 LinkedIn</a>
        <a href="https://github.com/sukumar0508" target="_blank">📊 GitHub</a>
    </div>
</div>
""", unsafe_allow_html=True)

# --- AUTO-REFRESH SCRIPT ---
st.markdown("""
<script>
    setTimeout(function(){
        window.location.reload();
    }, 30000);
</script>
""", unsafe_allow_html=True)