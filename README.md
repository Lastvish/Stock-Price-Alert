# Stock Price Alert System

一个基于 Finnhub API 的美股实时监控系统，支持股票和指数的实时价格监控及自定义警报。

## 功能特点

- 实时监控个股价格（使用 WebSocket）
- 定期监控指数数据（使用 REST API）
- 自定义价格变动阈值警报
- 自定义百分比变动阈值警报
- 支持自定义警报音效
- 完整的市场状态检查
- 错误处理和自动重连机制

## 技术实现

- 使用 Finnhub WebSocket API 实时监控股票价格
- 使用 Finnhub REST API 监控指数数据
- 支持配置文件自定义监控参数
- 内置市场交易时间检查
- 完整的错误处理机制

## 安装说明

1. 克隆仓库：
```bash
git clone https://github.com/Lastvish/Stock-Price-Alert.git
cd Stock-Price-Alert
```

2. 创建并激活虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 配置：
- 复制配置文件模板：
```bash
cp config/config.example.yaml config/config.yaml
```
- 编辑 `config/config.yaml`，设置您的 Finnhub API key 和监控参数

## 配置说明

配置文件（config.yaml）包含以下主要参数：

- `api_key`: Finnhub API 密钥
- `symbols`: 需要监控的股票代码列表
- `indices`: 需要监控的指数列表
- `thresholds`:
  - `price`: 价格变动阈值（美元）
  - `percentage`: 百分比变动阈值
- `update_interval`: 数据更新间隔（秒）
- `sound`: 警报音效设置

## 使用方法

1. 确保已正确配置 `config.yaml`
2. 运行程序：
```bash
python src/monitor.py
```

## 注意事项

- 请确保您有有效的 Finnhub API key
- 建议在美股交易时间运行程序
- 请注意 Finnhub API 的使用限制
- 建议根据自己的需求调整警报阈值

## 许可证

MIT License

## 作者

Lastvish

## 贡献

欢迎提交 Issue 和 Pull Request！ 
