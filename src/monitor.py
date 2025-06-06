import websocket
import json
import time
from datetime import datetime
import sys
import os
import threading
from queue import Queue
import ssl
import requests

from utils import load_config, is_market_open, format_price_change
from alert import AlertManager

class StockMonitor:
    def __init__(self):
        """初始化股票监控器"""
        self.config = load_config()
        self.alert_manager = AlertManager(self.config['settings']['sound_file'])
        
        # 优先从环境变量读取API密钥
        self.api_key = os.environ.get('FINNHUB_API_KEY') or self.config['settings'].get('finnhub_api_key')
        if not self.api_key:
            print("错误: 请设置FINNHUB_API_KEY环境变量或在config.yaml中设置finnhub_api_key")
            sys.exit(1)
        
        self.prices = {}
        self.price_queue = Queue()
        self.ws = None
        self.symbols = []
        self.index_symbols = []
        
        # 区分普通股票和指数
        for stock in self.config['stocks']:
            if stock['type'] == 'index':
                self.index_symbols.append(stock['symbol'])
            else:
                self.symbols.append(stock['symbol'])
                
        self.alerts = {stock['symbol']: stock['alerts'] for stock in self.config['stocks']}
        
        # 启动WebSocket连接（用于普通股票）
        if self.symbols:
            self.start_websocket()
        
        # 启动价格处理线程
        self.price_processor = threading.Thread(target=self.process_price_updates)
        self.price_processor.daemon = True
        self.price_processor.start()
        
        # 启动指数监控线程
        if self.index_symbols:
            self.index_monitor = threading.Thread(target=self.monitor_indices)
            self.index_monitor.daemon = True
            self.index_monitor.start()

    def get_index_price(self, symbol):
        """通过REST API获取指数价格"""
        try:
            url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={self.api_key}"
            response = requests.get(url)
            data = response.json()
            
            if 'c' in data and 't' in data:  # 'c'是当前价格，'t'是时间戳
                current_time = datetime.now().timestamp()
                data_time = data['t']  # Finnhub返回的时间戳
                delay = current_time - data_time
                
                print(f"\n数据延迟情况:")
                print(f"当前时间: {datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"数据时间: {datetime.fromtimestamp(data_time).strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"延迟时间: {delay:.2f} 秒")
                
                return float(data['c'])
            return None
        except Exception as e:
            print(f"\n获取指数 {symbol} 价格时出错: {e}")
            return None

    def monitor_indices(self):
        """监控指数价格"""
        while True:
            if is_market_open():
                for symbol in self.index_symbols:
                    price = self.get_index_price(symbol)
                    if price is not None:
                        self.price_queue.put((symbol, price))
            time.sleep(self.config['settings']['interval'])  # 使用配置的间隔时间

    def on_message(self, ws, message):
        """处理WebSocket消息"""
        data = json.loads(message)
        print(f"\n收到消息: {data}")
        
        if data['type'] == 'ping':
            print("收到心跳包...")
            return
            
        if data['type'] == 'error':
            print(f"错误: {data['msg']}")
            return
            
        if data['type'] == 'trade':
            symbol = data['data'][0]['s']
            price = float(data['data'][0]['p'])
            self.price_queue.put((symbol, price))

    def on_error(self, ws, error):
        """处理WebSocket错误"""
        print(f"\n*** WebSocket错误 ***")
        print(f"错误信息: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        """处理WebSocket连接关闭"""
        print(f"\n*** WebSocket连接关闭 ***")
        print(f"状态码: {close_status_code}")
        print(f"关闭信息: {close_msg}")
        time.sleep(5)  # 等待5秒后重连
        self.start_websocket()

    def on_open(self, ws):
        """处理WebSocket连接打开"""
        print("\n*** WebSocket连接已建立 ***")
        # 订阅所有股票
        for symbol in self.symbols:
            subscribe_message = json.dumps({'type': 'subscribe', 'symbol': symbol})
            print(f"订阅股票: {symbol}")
            print(f"发送订阅消息: {subscribe_message}")
            ws.send(subscribe_message)

    def start_websocket(self):
        """启动WebSocket连接"""
        print("\n开始建立WebSocket连接...")
        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp(
            f"wss://ws.finnhub.io?token={self.api_key}",
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
            on_open=self.on_open
        )
        
        # 禁用SSL证书验证
        ws_thread = threading.Thread(
            target=lambda: self.ws.run_forever(
                sslopt={"cert_reqs": ssl.CERT_NONE}
            )
        )
        ws_thread.daemon = True
        ws_thread.start()
        print("WebSocket线程已启动")

    def process_price_updates(self):
        """处理价格更新"""
        while True:
            symbol, current_price = self.price_queue.get()
            
            if symbol in self.prices:
                previous_price = self.prices[symbol]
                price_change = current_price - previous_price
                percentage_change = (price_change / previous_price) * 100

                # 获取警报阈值
                alerts = self.alerts[symbol]
                price_threshold = alerts['price_change']
                pct_threshold = alerts['percentage_change']

                # 格式化时间
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # 打印详细信息
                print("\n" + "="*60)
                print(f"时间: {current_time}")
                if not is_market_open():
                    print("*** 注意：当前为非交易时间，数据可能不是实时的 ***")
                print(f"股票: {symbol}")
                print(f"当前价格: ${current_price:.2f}")
                print(f"价格变动: {format_price_change(price_change, percentage_change)}")
                print(f"监控阈值:")
                print(f"  - 价格变动: ${price_threshold} (当前: ${abs(price_change):.2f})")
                print(f"  - 百分比变动: {pct_threshold}% (当前: {abs(percentage_change):.2f}%)")

                # 检查是否触发警报条件
                if (abs(price_change) >= alerts['price_change'] or 
                    abs(percentage_change) >= alerts['percentage_change']):
                    print("\n*** 触发警报! ***")
                    self.alert_manager.trigger_alert(
                        symbol, current_price, price_change, percentage_change
                    )
                print("="*60)

            self.prices[symbol] = current_price

    def run(self):
        """运行监控器"""
        print("启动股票监控系统...")
        print(f"\n监控配置:")
        for stock in self.config['stocks']:
            symbol = stock['symbol']
            print(f"{'指数' if stock['type'] == 'index' else '股票'}: {symbol}")
            print(f"  价格变动警报: ${self.alerts[symbol]['price_change']}")
            print(f"  百分比变动警报: {self.alerts[symbol]['percentage_change']}%")

        # 检查市场状态
        if not is_market_open():
            print("\n*** 提示：美股市场当前未开市 ***")
            print("美股交易时间：周一至周五")
            print("美东时间：9:30 - 16:00")
            print("北京时间：21:30 - 次日4:00")
            print("\n系统将继续运行，但在非交易时间可能收不到价格更新")
            print("建议在交易时间运行程序以获取实时数据")

        print("\n开始监控...\n")

        try:
            while True:
                time.sleep(1)
                # 每分钟检查一次市场状态
                if int(time.time()) % 60 == 0:
                    if not is_market_open():
                        print("\n市场处于非交易时间，等待市场开市...")
                    time.sleep(1)  # 防止重复打印
        except KeyboardInterrupt:
            print("\n正在关闭监控系统...")
            if self.ws:
                self.ws.close()

def main():
    """主程序入口"""
    monitor = StockMonitor()
    monitor.run()

if __name__ == "__main__":
    main() 