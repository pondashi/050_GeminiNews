import pytest
from src.ai_summarizer import summarize_data

def test_summarize_data(mocker):
    mock_client = mocker.MagicMock()
    mock_response = mocker.MagicMock()
    mock_response.text = "This is a summary."
    mock_client.models.generate_content.return_value = mock_response
    mocker.patch('src.ai_summarizer.client', mock_client)
    
    news = [{"title": "Test News", "url": "http://test", "summary": "..."}]
    stocks = [{"ticker": "TEST", "close": 100, "change": 5, "change_percent": 5, "volume": 1000}]
    
    result = summarize_data("テスト", news, stocks)
    
    assert result == "This is a summary."
    mock_client.models.generate_content.assert_called_once()
    
    # Verify the prompt contains the input data
    prompt_used = mock_client.models.generate_content.call_args.kwargs['contents']
    assert "Test News" in prompt_used
    assert "TEST" in prompt_used
    assert "テスト" in prompt_used

def test_summarize_data_empty(mocker):
    # If no data is provided
    result = summarize_data("テスト", [], [])
    assert "ありませんでした" in result
