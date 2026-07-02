import pytest
from src.fetcher import fetch_news, fetch_stock_prices
from datetime import datetime, timedelta
import pandas as pd

def test_fetch_news(mocker):
    # Mock feedparser.parse
    mock_feed = mocker.MagicMock()
    mock_entry1 = mocker.MagicMock()
    mock_entry1.title = "News 1"
    mock_entry1.link = "http://example.com/1"
    mock_entry1.summary = "Summary 1"
    mock_entry1.published_parsed = datetime.now().timetuple()
    
    # Old entry to check filtering (if implemented)
    mock_entry2 = mocker.MagicMock()
    mock_entry2.title = "News 2"
    mock_entry2.link = "http://example.com/2"
    mock_entry2.summary = "Summary 2"
    mock_entry2.published_parsed = (datetime.now() - timedelta(days=2)).timetuple()
    
    mock_feed.entries = [mock_entry1, mock_entry2]
    
    mocker.patch('feedparser.parse', return_value=mock_feed)
    
    results = fetch_news("test")
    
    # Assuming we filter out older than 24 hours
    assert len(results) == 1
    assert results[0]['title'] == "News 1"
    assert results[0]['url'] == "http://example.com/1"
    assert results[0]['summary'] == "Summary 1"

def test_fetch_stock_prices(mocker):
    # Mock yfinance Ticker
    mock_ticker_obj = mocker.MagicMock()
    
    # Create fake pandas dataframe for history
    dates = pd.date_range(end=datetime.today(), periods=2)
    fake_hist = pd.DataFrame({
        'Close': [100.0, 105.0],
        'Volume': [1000, 2000]
    }, index=dates)
    
    mock_ticker_obj.history.return_value = fake_hist
    mocker.patch('yfinance.Ticker', return_value=mock_ticker_obj)
    
    results = fetch_stock_prices(["TEST"])
    
    assert len(results) == 1
    assert results[0]['ticker'] == "TEST"
    assert results[0]['close'] == 105.0
    assert results[0]['change'] == 5.0
    assert results[0]['change_percent'] == 5.0
    assert results[0]['volume'] == 2000
