from logger import build_logger
from config import (
    API_URL,
    CACHE_FILE,
    CACHE_EXPIRY,
    SUPPORTED_CURRENCIES,
    API_TIMEOUT,
    API_MAX_RETRIES,
    API_RETRY_DELAY,
)
from converters.api import ExchangeRateApi
from converters.cache import FileRateCache
from converters.currency_converter import CurrencyConverter
from converters.rate_service import RateService

def main():
    logger = build_logger()

    api_client = ExchangeRateApi(
        api_url=API_URL,
        timeout=API_TIMEOUT,
        max_retries=API_MAX_RETRIES,
        retry_delay=API_RETRY_DELAY,
        logger=logger,
    )

    cache = FileRateCache(
        cache_file=CACHE_FILE,
        cache_expiry=CACHE_EXPIRY,
    )

    rate_service = RateService(
        api_client=api_client,
        cache=cache,
        logger=logger,
    )

    converter = CurrencyConverter(rate_service, logger)

    try:
        amount = float(input("Enter amount in USD:"))

        for currency in SUPPORTED_CURRENCIES:
            result = converter.convert(amount, currency)
            print(f"{amount} USD to {currency}: {result:.2f}")

    except ValueError as error:
        logger.error(error)
        print(error)

    except RuntimeError as error:
        logger.error(error)
        print(error)

if __name__ == "__main__":
    main()