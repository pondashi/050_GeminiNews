import pytest
from src import main
import sys

def test_main_success(mocker):
    # Mock config validation
    mocker.patch('src.config.validate_config')
    mocker.patch('src.config.TARGET_THEME', 'test_theme')
    mocker.patch('src.config.TARGET_TICKERS', 'TEST1,TEST2')
    
    # Mock data
    mock_news = [{"title": "t", "url": "u", "summary": "s"}]
    mock_stocks = [{"ticker": "TEST1", "close": 100, "change": 0, "change_percent": 0, "volume": 100}]
    mock_summary = "Mock summary text"
    
    # Patch dependencies
    mock_fetch_news = mocker.patch('src.main.fetch_news', return_value=mock_news)
    mock_fetch_stocks = mocker.patch('src.main.fetch_stock_prices', return_value=mock_stocks)
    mock_summarize = mocker.patch('src.main.summarize_data', return_value=mock_summary)
    mock_send = mocker.patch('src.main.send_notification')
    
    main.main()
    
    # Verify calls
    mock_fetch_news.assert_called_once_with('test_theme')
    mock_fetch_stocks.assert_called_once_with(['TEST1', 'TEST2'])
    mock_summarize.assert_called_once_with('test_theme', mock_news, mock_stocks)
    mock_send.assert_called_once_with(mock_summary)

def test_main_failure(mocker):
    # Mock config validation
    mocker.patch('src.config.validate_config')
    mocker.patch('src.config.TARGET_THEME', 'test_theme')
    mocker.patch('src.config.TARGET_TICKERS', 'TEST1')
    
    # Make fetch_news raise an exception
    mocker.patch('src.main.fetch_news', side_effect=Exception("Fetch error"))
    mock_send = mocker.patch('src.main.send_notification')
    
    # The main function catches exceptions and calls sys.exit(1)
    with pytest.raises(SystemExit) as e:
        main.main()
    
    assert e.value.code == 1
    
    # Verify error notification was sent
    mock_send.assert_called_once()
    assert "Daily Summary Bot Error" in mock_send.call_args[0][0]
    assert "Fetch error" in mock_send.call_args[0][0]
