import logging
from converters.interfaces import RateProvider, RateCache, RateSource

class RateService(RateSource):
    def __init__(
        self,
        api_client: RateProvider,
        cache: RateCache | None = None,
        logger=None,
    ):
        self.api_client = api_client
        self.cache = cache
        self.logger = logger or logging.getLogger(__name__)

    def get_rates(self) -> dict:
        if self.cache is not None:
            cached_rates = self.cache.load_rates()
            if cached_rates is not None:
                self.logger.info("Rates loaded from cache.")
                return cached_rates

        self.logger.info("Fetching rates from API.")
        rates = self.api_client.fetch_rates()

        if self.cache is not None:
            self.cache.save_rates(rates)
            self.logger.info("Rates saved to cache.")

        return rates