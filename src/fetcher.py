import feedparser
import yfinance as yf
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

def fetch_news(theme: str) -> list[dict]:
    """
    Fetch news from Google News RSS for a given theme.
    Returns up to 10 articles from the last 24 hours.
    """
    logger.info(f"Fetching news for theme: {theme}")
    # URL encode happens implicitly in requests, but feedparser handles the URL string directly.
    # Safe simple string concatenation is acceptable here for feedparser URL.
    url = f"https://news.google.com/rss/search?q={theme}&hl=ja&gl=JP&ceid=JP:ja"
    
    feed = feedparser.parse(url)
    
    articles = []
    now = datetime.now()
    
    for entry in feed.entries:
        if len(articles) >= 10:
            break
            
        # Parse published date if available
        pub_date = None
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            pub_date = datetime(*entry.published_parsed[:6])
            
        # Optional: strictly filter by last 24 hours if pub_date exists
        if pub_date and (now - pub_date) > timedelta(days=1):
            continue
            
        articles.append({
            "title": entry.title,
            "url": entry.link,
            "summary": getattr(entry, 'summary', '')
        })
        
    logger.info(f"Fetched {len(articles)} news articles.")
    return articles

def fetch_stock_prices(tickers: list[str]) -> list[dict]:
    """
    Fetch stock prices for a list of tickers.
    Returns closing price, change, percent change, and volume.
    """
    logger.info(f"Fetching stock prices for tickers: {tickers}")
    stock_data = []
    
    for ticker in tickers:
        try:
            ticker_obj = yf.Ticker(ticker)
            # Use '1mo' and get last 2 valid days to calculate change properly
            hist = ticker_obj.history(period="5d")
            
            if len(hist) < 2:
                logger.warning(f"Not enough historical data for ticker: {ticker}")
                continue
                
            last_close = hist['Close'].iloc[-1]
            prev_close = hist['Close'].iloc[-2]
            volume = hist['Volume'].iloc[-1]
            
            change = last_close - prev_close
            change_percent = (change / prev_close) * 100
            
            stock_data.append({
                "ticker": ticker,
                "close": round(last_close, 2),
                "change": round(change, 2),
                "change_percent": round(change_percent, 2),
                "volume": int(volume)
            })
        except Exception as e:
            logger.error(f"Failed to fetch data for {ticker}: {e}")
            
    logger.info(f"Fetched stock data for {len(stock_data)} tickers.")
    return stock_data
