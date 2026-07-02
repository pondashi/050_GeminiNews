import requests
import logging
from . import config

logger = logging.getLogger(__name__)

def send_notification(summary: str):
    """
    Send the summary to a webhook (Discord or Slack).
    """
    webhook_url = config.WEBHOOK_URL
    if not webhook_url:
        logger.error("Webhook URL is not configured.")
        raise ValueError("Webhook URL is not configured.")

    logger.info("Sending notification via Webhook.")

    # Determine payload format based on URL
    if "discord.com" in webhook_url:
        payload = {"content": summary}
    else:
        # Default to Slack format
        payload = {"text": summary}

    response = requests.post(webhook_url, json=payload, timeout=10)
    
    try:
        response.raise_for_status()
        logger.info("Notification sent successfully.")
    except requests.exceptions.HTTPError as e:
        logger.error(f"Failed to send notification: {e}\nResponse: {response.text}")
        raise
