
"""
YARIS Market Selector

Loads, validates and maps configured markets
to their broker symbols.
"""

import json
from pathlib import Path


class MarketSelector:

    def __init__(self, config_path="config/markets.json"):
        self.config_path = Path(config_path)
        self.markets = self._load_markets()

    def _load_markets(self):

        if not self.config_path.is_file():
            raise FileNotFoundError(
                f"Market configuration not found: {self.config_path}"
            )

        with self.config_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            raise ValueError("Configuration must be a JSON object.")

        markets = data.get("markets")

        if not isinstance(markets, dict):
            raise ValueError("'markets' must be a JSON object.")

        for name, settings in markets.items():

            if not isinstance(settings, dict):
                raise ValueError(f"Invalid settings for {name}.")

            if not isinstance(settings.get("enabled", False), bool):
                raise ValueError(f"Invalid enabled setting for {name}.")

            if not isinstance(settings.get("symbol"), str):
                raise ValueError(f"Missing broker symbol for {name}.")

            if not settings["symbol"].strip():
                raise ValueError(f"Empty broker symbol for {name}.")

        return markets

    def get_available_markets(self):
        return list(self.markets.keys())

    def get_enabled_markets(self):
        return [
            name for name, settings in self.markets.items()
            if settings.get("enabled", False)
        ]

    def get_broker_symbol(self, market_name):
        """Translate logical market name into broker symbol."""

        if market_name not in self.markets:
            raise ValueError(f"Unknown market: {market_name}")

        settings = self.markets[market_name]

        if not settings.get("enabled", False):
            raise ValueError(f"Market is disabled: {market_name}")

        return settings["symbol"]

    def select_markets(self, selected_markets):

        if isinstance(selected_markets, str):
            raise ValueError("Provide a list of market names.")

        selected = list(selected_markets)

        if len(selected) != len(set(selected)):
            raise ValueError("Duplicate selections are not allowed.")

        available = set(self.get_available_markets())
        enabled = set(self.get_enabled_markets())

        invalid = set(selected) - available
        if invalid:
            raise ValueError(f"Unknown markets: {sorted(invalid)}")

        disabled = set(selected) - enabled
        if disabled:
            raise ValueError(f"Disabled markets: {sorted(disabled)}")

        return [
            {
                "name": name,
                "symbol": self.get_broker_symbol(name)
            }
            for name in selected
        ]
