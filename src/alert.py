import os
import subprocess
from datetime import datetime

class AlertManager:
    def __init__(self, sound_file):
        """初始化警报管理器"""
        self.sound_file = sound_file
        self._validate_sound_file()

    def _validate_sound_file(self):
        """验证声音文件是否存在"""
        if not os.path.exists(self.sound_file):
            raise FileNotFoundError(f"警报音文件未找到: {self.sound_file}")

    def _play_sound(self):
        """使用系统命令播放声音"""
        try:
            subprocess.run(['afplay', self.sound_file], check=True)
        except subprocess.CalledProcessError as e:
            print(f"播放警报音失败: {e}")
        except FileNotFoundError:
            print("警告: 在此系统上找不到 afplay 命令")

    def trigger_alert(self, stock_symbol, current_price, price_change, percentage_change):
        """触发警报"""
        # 播放声音
        self._play_sound()

        # 打印警报信息
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        alert_message = (
            f"\n警报时间: {timestamp}\n"
            f"股票: {stock_symbol}\n"
            f"当前价格: ${current_price:.2f}\n"
            f"价格变动: ${price_change:.2f}\n"
            f"百分比变动: {percentage_change:.2f}%\n"
        )
        print("\n" + "="*50)
        print(alert_message)
        print("="*50) 