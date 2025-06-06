import aiohttp
import logging
import os
from datetime import datetime, timedelta
from typing import List, Optional

logger = logging.getLogger(__name__)

class NewsSearcher:
    def __init__(self, config: dict):
        """
        Initialize the news searcher with configuration.
        
        Args:
            config: Dictionary containing DeepSeek API configuration
        """
        # 优先从环境变量读取API密钥
        self.api_key = os.environ.get('DEEPSEEK_API_KEY') or config.get('api_key')
        if not self.api_key:
            raise ValueError("请设置DEEPSEEK_API_KEY环境变量或在配置中设置api_key")
            
        self.base_url = "https://api.deepseek.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
    async def search_news(self, symbol: str, company_name: Optional[str] = None, is_index: bool = False) -> List[dict]:
        """
        Search for breaking news about the given stock symbol using DeepSeek's chat API.
        
        Args:
            symbol: Stock symbol
            company_name: Company name (optional)
            is_index: Whether the symbol is a market index
            
        Returns:
            List of news articles
        """
        try:
            # 构建搜索提示词
            system_message = (
                "You are a financial news analyst specializing in real-time market analysis. "
                "Your task is to search and analyze breaking news about financial markets "
                "and stocks. Please provide a concise summary of the most relevant and "
                "recent news, focusing on market-moving events that happened in the last 10 minutes."
            )
            
            if is_index:
                # 指数的提示词，关注整体市场动向
                user_message = (
                    f"Please analyze and summarize the most important breaking news in the last 10 minutes "
                    f"that could explain the current movement in {symbol}. "
                    f"Focus on broad market news, including:\n"
                    f"1. Major economic events or data releases\n"
                    f"2. Global market trends and developments\n"
                    f"3. Political or policy changes affecting markets\n"
                    f"4. Significant sector-wide movements\n"
                    f"Format your response as a list of news items, each with a title, source, "
                    f"time, and brief summary. Only include factual, market-relevant information "
                    f"that could explain sudden market movements."
                )
            else:
                # 个股的提示词，关注公司和行业新闻
                user_message = (
                    f"Please analyze and summarize the most important breaking news in the last 10 minutes "
                    f"for {symbol} stock{f' ({company_name})' if company_name else ''}. "
                    f"Focus on:\n"
                    f"1. Company-specific news and announcements\n"
                    f"2. Industry-related developments\n"
                    f"3. Competitor activities that might affect the company\n"
                    f"4. Regulatory changes impacting the company or industry\n"
                    f"Format your response as a list of news items, each with a title, source, "
                    f"time, and brief summary. Only include factual, market-relevant information "
                    f"that could explain sudden stock price movements."
                )
            
            # 准备请求参数
            data = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                "temperature": 0.3,  # 保持输出的一致性
                "max_tokens": 1000
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.base_url,
                    headers=self.headers,
                    json=data
                ) as response:
                    if response.status != 200:
                        logger.error(f"Failed to fetch news. Status: {response.status}")
                        return []
                    
                    result = await response.json()
                    return self._process_news_results(result)
                    
        except Exception as e:
            logger.error(f"Error searching news for {symbol}: {str(e)}")
            return []
    
    def _process_news_results(self, data: dict) -> List[dict]:
        """Process and format the news search results."""
        try:
            # 从API响应中提取文本内容
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            if not content:
                return []
            
            # 解析文本内容为结构化的新闻列表
            # 这里假设AI返回的是格式化的文本，我们需要解析它
            articles = []
            current_article = {}
            
            for line in content.split("\n"):
                line = line.strip()
                if not line:
                    continue
                    
                if line.startswith("Title:") or line.startswith("1.") or line.startswith("2."):
                    # 如果已经有一个文章在处理中，保存它
                    if current_article:
                        articles.append(current_article.copy())
                        current_article = {}
                    
                    # 提取标题
                    title = line.split(":", 1)[-1].strip().strip('"')
                    current_article["title"] = title
                    
                elif "Source:" in line:
                    parts = line.split("Source:", 1)
                    current_article["source"] = parts[1].split("|")[0].strip()
                    if "Time:" in line:
                        current_article["published_at"] = line.split("Time:", 1)[1].strip()
                        
                elif "Summary:" in line:
                    current_article["summary"] = line.split("Summary:", 1)[1].strip()
            
            # 添加最后一个文章
            if current_article:
                articles.append(current_article)
            
            return articles
            
        except Exception as e:
            logger.error(f"Error processing news results: {str(e)}")
            return []
    
    def format_news_alert(self, symbol: str, articles: List[dict], price_movement: dict) -> str:
        """Format news alert message with price movement and articles."""
        if not articles:
            return f"[ALERT] {symbol} price movement detected but no relevant news found."
        
        # 构建价格变动信息
        price_info = (
            f"[PRICE ALERT] {symbol}: ${price_movement['current_price']:.2f} "
            f"({price_movement['percentage_change']:+.1f}%)"
        )
        
        # 构建新闻信息
        news_info = [f"[NEWS UPDATE] Found {len(articles)} relevant news:"]
        for i, article in enumerate(articles, 1):
            news_info.extend([
                f"{i}. \"{article['title']}\"",
                f"   Source: {article['source']} | Time: {article['published_at']}",
                f"   Summary: {article['summary'][:200]}..."
            ])
        
        return "\n".join([price_info, ""] + news_info) 