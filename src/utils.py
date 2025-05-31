import yaml
from datetime import datetime
import pytz

def load_config(config_path='config/config.yaml'):
    """加载配置文件"""
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def is_market_open():
    """检查美股市场是否开市"""
    ny_tz = pytz.timezone('America/New_York')
    ny_time = datetime.now(ny_tz)
    
    # 检查是否为工作日
    if ny_time.weekday() >= 5:  # 5是周六，6是周日
        return False
    
    # 检查是否在交易时间内（9:30 - 16:00）
    market_start = ny_time.replace(hour=9, minute=30, second=0, microsecond=0)
    market_end = ny_time.replace(hour=16, minute=0, second=0, microsecond=0)
    
    return market_start <= ny_time <= market_end

def format_price_change(change, percentage_change):
    """格式化价格变动信息"""
    return f"${change:.2f} ({percentage_change:.2f}%)" 