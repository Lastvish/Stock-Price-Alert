from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class PricePoint:
    def __init__(self, price: float, timestamp: datetime):
        self.price = price
        self.timestamp = timestamp

class PriceMovementValidator:
    def __init__(self, config: dict):
        """
        Initialize the price movement validator with configuration.
        
        Args:
            config: Dictionary containing trigger conditions configuration
        """
        self.window_size = timedelta(minutes=config['time_window_minutes'])
        self.min_data_points = config['min_data_points']
        self.price_thresholds = config['price_movement']
        self.cool_down_minutes = config['debounce']['cool_down_minutes']
        
        self.price_windows: Dict[str, List[PricePoint]] = {}
        self.last_alerts: Dict[str, datetime] = {}

    def _is_in_cooldown(self, symbol: str, current_time: datetime) -> bool:
        """Check if the symbol is still in cooldown period."""
        if symbol not in self.last_alerts:
            return False
        
        elapsed = current_time - self.last_alerts[symbol]
        return elapsed < timedelta(minutes=self.cool_down_minutes)

    def _clean_old_data_points(self, symbol: str, current_time: datetime):
        """Remove data points outside the time window."""
        if symbol not in self.price_windows:
            return
        
        cutoff_time = current_time - self.window_size
        self.price_windows[symbol] = [
            point for point in self.price_windows[symbol]
            if point.timestamp >= cutoff_time
        ]

    def add_price_point(self, symbol: str, price: float, timestamp: datetime):
        """
        Add a new price point for the given symbol.
        
        Args:
            symbol: Stock symbol
            price: Current price
            timestamp: Time of the price update
        """
        if symbol not in self.price_windows:
            self.price_windows[symbol] = []
        
        # Clean old data points
        self._clean_old_data_points(symbol, timestamp)
        
        # Add new data point
        self.price_windows[symbol].append(PricePoint(price, timestamp))
        
        # Keep only necessary data points
        max_points = max(100, self.min_data_points * 2)  # Arbitrary limit to prevent memory issues
        if len(self.price_windows[symbol]) > max_points:
            self.price_windows[symbol] = self.price_windows[symbol][-max_points:]

    def get_price_movement(self, symbol: str) -> Optional[dict]:
        """
        Calculate price movement for the given symbol.
        
        Returns:
            Dictionary containing price movement details or None if insufficient data
        """
        if symbol not in self.price_windows:
            return None
        
        window = self.price_windows[symbol]
        if len(window) < self.min_data_points:
            return None
        
        base_price = window[0].price
        current_price = window[-1].price
        
        abs_change = current_price - base_price
        pct_change = (abs_change / base_price) * 100
        
        return {
            'base_price': base_price,
            'current_price': current_price,
            'absolute_change': abs_change,
            'percentage_change': pct_change,
            'start_time': window[0].timestamp,
            'end_time': window[-1].timestamp
        }

    def should_trigger_news_search(self, symbol: str, current_time: datetime, is_index: bool = False) -> Optional[dict]:
        """
        Check if news search should be triggered for the symbol.
        
        Args:
            symbol: Stock symbol
            current_time: Current timestamp
            is_index: Whether the symbol is a market index
            
        Returns:
            Dictionary containing trigger details if should trigger, None otherwise
        """
        # Check cooldown period
        if self._is_in_cooldown(symbol, current_time):
            return None
        
        movement = self.get_price_movement(symbol)
        if not movement:
            return None
        
        pct_change = movement['percentage_change']
        
        # 根据是否为指数选择不同的百分比阈值
        pct_thresholds = (
            self.price_thresholds['percentage']['index']
            if is_index
            else self.price_thresholds['percentage']['stock']
        )
        
        # 只检查百分比变动
        if (pct_change >= pct_thresholds['up'] or 
            pct_change <= pct_thresholds['down']):
            self.last_alerts[symbol] = current_time
            movement['trigger_type'] = {
                'percentage': True
            }
            logger.info(f"News search triggered for {symbol}. Movement: {movement}")
            return movement
            
        return None 