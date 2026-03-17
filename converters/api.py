import time
import logging
import requests

from converters.interfaces import RateProvider

class ExchangeRateApi(RateProvider):
    def __init__(self, api_url, timeout=5, max_retries=3, retry_delay=2, logger=None):
        self.api_url = api_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.logger = logger or logging.getLogger(__name__)

    def fetch_rates(self) -> dict:
        last_error = None

        for attempt in range(1, self.max_retries + 1):
            try:
                self.logger.info(f"Fetching exchange rates (attempt {attempt})")

                response = requests.get(self.api_url, timeout=self.timeout)
                response.raise_for_status()

                data = response.json()
                return data["rates"]

            except (requests.RequestException, KeyError, ValueError, TypeError) as error:
                last_error = error
                self.logger.warning(f"Request failed: {error}")

                if attempt < self.max_retries:
                    self.logger.info(f"Retrying in {self.retry_delay} seconds")
                    time.sleep(self.retry_delay)

        self.logger.error("Max retries reached. Unable to fetch rates.")
        raise RuntimeError("Unable to fetch exchange rates.") from last_error