import os
import requests
import logging

logger = logging.getLogger("engipilot")

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")


def send_slack_notification(message: str) -> bool:
    """
    Sends a message to Slack via webhook. Fails silently (logs the failure)
    so that Slack being down never breaks the core automation flow.
    """
    if not SLACK_WEBHOOK_URL:
        logger.info("Slack notification skipped — SLACK_WEBHOOK_URL not configured")
        return False

    try:
        response = requests.post(
            SLACK_WEBHOOK_URL,
            json={"text": message},
            timeout=5,
        )
        response.raise_for_status()
        logger.info(f"Slack notification sent: {message[:80]}...")
        return True
    except Exception as e:
        logger.info(f"Slack notification failed (non-blocking): {e}")
        return False