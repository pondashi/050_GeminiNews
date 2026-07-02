import logging
import sys
from src import config
from src.fetcher import fetch_news, fetch_stock_prices
from src.ai_summarizer import summarize_data
from src.notifier import send_notification

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting Daily Summary Bot...")
    
    try:
        # Validate configuration
        config.validate_config()
        
        theme = config.TARGET_THEME
        tickers_str = config.TARGET_TICKERS
        tickers = [t.strip() for t in tickers_str.split(',')] if tickers_str else []
        
        # 1. Fetch Data
        news = fetch_news(theme)
        stocks = fetch_stock_prices(tickers)
        
        # 2. Summarize Data
        summary = summarize_data(theme, news, stocks)
        
        # 3. Send Notification
        send_notification(summary)
        
        logger.info("Daily Summary Bot finished successfully.")
        
    except Exception as e:
        logger.exception("An error occurred during execution.")
        # Attempt to notify about the error if possible
        try:
            error_msg = f"⚠️ Daily Summary Bot Error:\n```\n{str(e)}\n```"
            send_notification(error_msg)
        except Exception as notify_err:
            logger.error(f"Failed to send error notification: {notify_err}")
        
        sys.exit(1)

if __name__ == "__main__":
    main()
