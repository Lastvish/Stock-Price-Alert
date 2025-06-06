# Stock Price Alert System

A real-time US stock monitoring system based on Finnhub API, supporting real-time price monitoring and custom alerts for stocks and indices.

## Features

- Real-time stock price monitoring (using WebSocket)
- Periodic index data monitoring (using REST API)
- Custom price change threshold alerts
- Custom percentage change threshold alerts
- Support for custom alert sounds
- Complete market status checking
- Error handling and automatic reconnection mechanism
- AI-powered news search and analysis (using DeepSeek API)

## Technical Implementation

- Uses Finnhub WebSocket API for real-time stock price monitoring
- Uses Finnhub REST API for index data monitoring
- Uses DeepSeek API for intelligent news search and analysis
- Supports custom monitoring parameters via configuration file
- Built-in market trading hours check
- Comprehensive error handling mechanism

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Lastvish/Stock-Price-Alert.git
cd Stock-Price-Alert
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configuration:
- Copy the configuration file template:
```bash
cp config/config.example.yaml config/config.yaml
```
- Set up your API keys (推荐使用环境变量):
```bash
# Finnhub API密钥
export FINNHUB_API_KEY="your_finnhub_api_key"

# DeepSeek API密钥 (如果启用新闻搜索功能)
export DEEPSEEK_API_KEY="your_deepseek_api_key"
```
- 或者在 `config/config.yaml` 中设置API密钥和监控参数

## Configuration Guide

配置文件 (config.yaml) 包含以下主要参数：

- API密钥设置 (推荐使用环境变量):
  - `FINNHUB_API_KEY`: Finnhub API密钥
  - `DEEPSEEK_API_KEY`: DeepSeek API密钥 (用于新闻搜索)
- 监控设置:
  - `symbols`: 要监控的股票列表
  - `indices`: 要监控的指数列表
  - `thresholds`:
    - `price`: 价格变动阈值 (美元)
    - `percentage`: 百分比变动阈值
  - `update_interval`: 数据更新间隔 (秒)
  - `sound`: 警报声音设置
- 新闻搜索设置:
  - `news_alert`:
    - `enabled`: 是否启用新闻搜索功能
    - `trigger_conditions`: 触发条件配置
      - `time_window_minutes`: 监控时间窗口（分钟）
      - `min_data_points`: 最小数据点数量
      - `price_movement`: 价格变动阈值
      - `debounce`: 防抖动设置
    - `search_settings`: 新闻搜索设置
      - `time_window_hours`: 搜索最近多少小时的新闻
      - `max_results`: 每次返回的最大新闻数量
      - `min_relevance_score`: 最小相关度分数

## Usage

1. 确保已设置API密钥（环境变量或配置文件）
2. 运行程序:
```bash
python src/monitor.py
```

## Important Notes

- 确保您有有效的 Finnhub API 密钥
- 推荐使用环境变量来存储API密钥，这样更安全
- 建议在美国市场交易时间运行程序
- 注意 Finnhub API 的使用限制
- 根据需要调整警报阈值

## News Search Feature

新闻搜索功能使用 DeepSeek API 来分析和解释股票价格变动的原因：

1. **触发条件**：
   - 当股票价格在指定时间窗口内发生显著变动
   - 需要满足最小数据点数量要求，避免价格抖动
   - 支持绝对价格变动和百分比变动阈值

2. **新闻分析**：
   - 使用 AI 分析最近的相关新闻
   - 识别可能导致价格变动的关键事件
   - 提供新闻摘要和相关度评分

3. **防抖动机制**：
   - 对同一股票的新闻搜索有冷却时间
   - 避免频繁触发和重复通知

4. **通知内容**：
   - 价格变动信息
   - 相关新闻标题和摘要
   - 新闻来源和发布时间
   - AI 分析的相关性说明

## Security Notes

- 不要在代码或配置文件中直接存储API密钥
- 不要将包含API密钥的文件提交到版本控制系统
- 使用环境变量来管理敏感信息
- 定期更换API密钥以提高安全性

## License

MIT License

## Author

Lastvish

## Contributing

欢迎提交 Issue 和 Pull Request！
