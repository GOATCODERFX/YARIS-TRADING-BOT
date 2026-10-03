"""
YARIS Strategy Engine

Analyzes market data and produces a signal.
This module does NOT place trades.
"""

from enum import Enum


class Signal(Enum):
    BUY = "BUY"
    SELL = "SELL"
    WAIT = "WAIT"


class StrategyEngine:

    def analyze(self, market_data):
        """
        Analyze one market.

        Strategy rules will be added here after
        the market-data and risk layers are tested.
        """

        if not market_data:
            return Signal.WAIT

        # Safety default:
        # YARIS does not trade until a validated
        # strategy condition is implemented.
        return Signal.WAIT

    def analyze_all(self, markets):
        """Analyze multiple markets."""

        results = {}

        for market in markets:
            results[market["symbol"]] = self.analyze(market)

        return results
