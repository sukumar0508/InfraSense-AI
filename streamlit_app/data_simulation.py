import random
from datetime import datetime

def get_fake_logs():
    servers = ['SRV001', 'SRV002', 'SRV003']
    server = random.choice(servers)
    cpu = random.randint(20, 95)         # simulate CPU usage
    memory = random.randint(30, 90)      # simulate memory usage

    return {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'server_id': server,
        'cpu': cpu,
        'memory': memory
    }
