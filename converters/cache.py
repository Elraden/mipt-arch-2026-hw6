import json
import os
import time

from converters.interfaces import RateCache

class FileRateCache(RateCache):
    def __init__(self, cache_file="exchange_rates.json", cache_expiry=3600):
        self.cache_file = cache_file
        self.cache_expiry = cache_expiry

    def load_rates(self):
        if not os.path.exists(self.cache_file):
            return None

        try:
            with open(self.cache_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            if time.time() - data["timestamp"] < self.cache_expiry:
                return data["rates"]

        except (OSError, KeyError, ValueError, TypeError):
            return None

        return None

    def save_rates(self, rates):
        try:
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(
                    {"timestamp": time.time(), "rates": rates},
                    f,
                    ensure_ascii=False,
                    indent=2,
                )
        except OSError:
            pass