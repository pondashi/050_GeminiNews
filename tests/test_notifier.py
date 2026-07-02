import pytest
import responses
from src.notifier import send_notification
from src import config

@responses.activate
def test_send_notification_discord(mocker):
    # Set config for Discord
    mocker.patch.object(config, 'WEBHOOK_URL', 'https://discord.com/api/webhooks/test')
    
    responses.add(
        responses.POST,
        'https://discord.com/api/webhooks/test',
        json={"success": True},
        status=200
    )
    
    # Should not raise
    send_notification("Test summary")
    
    assert len(responses.calls) == 1
    assert b'{"content": "Test summary"}' in responses.calls[0].request.body

@responses.activate
def test_send_notification_slack(mocker):
    # Set config for Slack (doesn't contain discord.com)
    mocker.patch.object(config, 'WEBHOOK_URL', 'https://hooks.slack.com/services/test')
    
    responses.add(
        responses.POST,
        'https://hooks.slack.com/services/test',
        body="ok",
        status=200
    )
    
    send_notification("Test summary")
    
    assert len(responses.calls) == 1
    assert b'{"text": "Test summary"}' in responses.calls[0].request.body

@responses.activate
def test_send_notification_error(mocker):
    mocker.patch.object(config, 'WEBHOOK_URL', 'https://discord.com/api/webhooks/test')
    
    responses.add(
        responses.POST,
        'https://discord.com/api/webhooks/test',
        body="error",
        status=500
    )
    
    import requests
    with pytest.raises(requests.exceptions.HTTPError):
        send_notification("Test summary")
