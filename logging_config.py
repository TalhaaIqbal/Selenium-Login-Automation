import sys
import logging
import os
import requests

from dotenv import load_dotenv


load_dotenv()


LOG_FORMAT = "%(levelname)s - %(funcName)s - %(message)s"


class SlackHandler(logging.Handler):
    def __init__(self, webhook_url: str, level: int = logging.WARNING):
        super().__init__(level)
        self.webhook_url = webhook_url

    def emit(self, record: logging.LogRecord):
        try:
            message = self.format(record)

            payload = {
                "text": f"*[{record.levelname}]* `{record.name}`\n`{record.pathname}`\n`{message}`"
            }

            response = requests.post(
                self.webhook_url,
                json=payload,
                timeout=5
            )

            response.raise_for_status()

        except Exception:
            self.handleError(record)


slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL")

handlers = [
    logging.StreamHandler(sys.stdout)
]

if slack_webhook_url:
    handlers.append(
        SlackHandler(
            slack_webhook_url,
            logging.WARNING
        )
    )


logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=handlers
)


logger = logging.getLogger("Scraper")


__all__ = [
    "logger",
    "slack_webhook_url"
]