"""
YARIS Market Selector

Controls which markets YARIS is allowed to scan.
"""

import json
from pathlib import Path

class MarketSelector:
def init(self, config_path="config/markets.json"):
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
        raise ValueError("Market configuration must be a JSON object.")

    markets = data.get("markets", {})

    if not isinstance(markets, dict):
        raise ValueError("'markets' must be a JSON object.")

    for name, settings in markets.items():
        if not isinstance(settings, dict):
            raise ValueError(f"Invalid settings for market: {name}")

        if "enabled" in settings and not isinstance(
            settings["enabled"], bool
        ):
            raise ValueError(
                f"'enabled' must be true or false for market: {name}"
            )

    return markets

def get_available_markets(self):
    """Return all configured market names."""
    return list(self.markets.keys())

def get_enabled_markets(self):
    """Return only markets enabled in the configuration."""
    return [
        name
        for name, settings in self.markets.items()
        if settings.get("enabled", False) is True
    ]

def select_markets(self, selected_markets):
    """Validate and return selected, enabled markets."""
    if isinstance(selected_markets, str):
        raise ValueError("Provide a list of market names, not a string.")

    selected = list(selected_markets)
    available = set(self.get_available_markets())
    enabled = set(self.get_enabled_markets())

    invalid = set(selected) - available
    if invalid:
        raise ValueError(
            f"Unknown YARIS markets: {', '.join(sorted(invalid))}"
        )

    disabled = set(selected) - enabled
    if disabled:
        raise ValueError(
            f"These markets are disabled in config: "
            f"{', '.join(sorted(disabled))}"
        )

    if len(selected) != len(set(selected)):
        raise ValueError("Duplicate market selections are not allowed.")

    return selected
