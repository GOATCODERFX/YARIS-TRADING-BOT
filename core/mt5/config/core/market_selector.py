"""
YARIS Market Selector

Controls which markets YARIS is allowed to scan.
"""

import json
from pathlib import Path


class MarketSelector:
    def __init__(self, config_path="config/markets.json"):
        self.config_path = Path(config_path)
        self.markets = self._load_markets()

    def _load_markets(self):
        with open(self.config_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        return data.get("markets", {})

    def get_available_markets(self):
        """Return all configured YARIS markets."""
        return list(self.markets.keys())

    def get_enabled_markets(self):
        """Return markets currently enabled."""
        return [
            name
            for name, data in self.markets.items()
            if data.get("enabled", False)
        ]

    def select_markets(self, selected_markets):
        """
        Select the markets YARIS is allowed to trade.
        """
        available = set(self.get_available_markets())

        invalid = set(selected_markets) - available

        if invalid:
            raise ValueError(
                f"Unknown YARIS markets: {', '.join(invalid)}"
            )

        return list(selected_markets)
