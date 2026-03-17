import logging
from converters.interfaces import RateSource

class CurrencyConverter:
    def __init__(self, rate_service: RateSource, logger=None):
        self.rate_service = rate_service
        self.logger = logger or logging.getLogger(__name__)

    def convert(self, amount: float, target_currency: str) -> float:
        if amount < 0:
            raise ValueError("Amount cannot be negative.")

        rates = self.rate_service.get_rates()

        if target_currency not in rates:
            raise ValueError(f"Currency {target_currency} not found.")

        result = amount * rates[target_currency]
        self.logger.info(f"Converted {amount} USD to {target_currency}: {result}")
        return result