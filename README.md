# 股票实时监控系统

这是一个基于 Python 的股票实时监控系统，可以同时监控股票和指数的价格变动。

## 功能特点

- 支持实时监控股票价格（通过 WebSocket）
- 支持监控指数价格（通过 REST API）
- 可自定义价格变动警报阈值
- 可自定义百分比变动警报阈值
- 支持自定义警报音效
- 自动检测市场开闭市状态

## 安装步骤

1. 克隆仓库：
```bash
git clone [你的仓库URL]
cd stock-monitor
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
```bash
cp config/config.example.yaml config/config.yaml
```
然后编辑 `config/config.yaml`，填入您的 Finnhub API key。

## 使用方法

1. 获取 Finnhub API key：
   - 访问 https://finnhub.io/
   - 注册账号并获取免费的 API key

2. 配置监控的股票：
   - 编辑 `config/config.yaml`
   - 可以添加/修改要监控的股票和指数
   - 可以调整警报阈值

3. 运行程序：
```bash
python src/monitor.py
```

## 配置说明

配置文件 `config/config.yaml` 包含以下设置：

- `stocks`: 要监控的股票列表
  - `symbol`: 股票代码
  - `type`: 类型（stock/index）
  - `alerts`: 警报设置
    - `price_change`: 价格变动阈值
    - `percentage_change`: 百分比变动阈值

- `settings`: 全局设置
  - `interval`: 监控间隔（秒）
  - `sound_file`: 警报音效文件
  - `finnhub_api_key`: API key

## 注意事项

- 美股交易时间：
  - 美东时间：9:30 - 16:00
  - 北京时间：21:30 - 次日4:00
  - 周一至周五（节假日除外）

- API 限制：
  - 免费版每分钟最多 60 次 API 调用
  - WebSocket 连接无调用限制

## 许可证

MIT 