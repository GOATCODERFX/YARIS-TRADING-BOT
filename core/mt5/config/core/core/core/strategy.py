
"""
YARIS Strategy Engine

Analyzes historical market candles.
Does NOT place trades.
"""

from enum import Enum


class Signal(Enum):
    BUY = "BUY"
    SELL = "SELL"
    WAIT = "WAIT"


class StrategyEngine:

    def __init__(self, min_candles=50):
        self.min_candles = min_candles

    def analyze(self, market_data):
        """Validate market data before strategy analysis."""

        if not isinstance(market_data, dict):
            return Signal.WAIT

        candles = market_data.get("candles")

        if not isinstance(candles, list):
            return Signal.WAIT

        if len(candles) < self.min_candles:
            return Signal.WAIT

        for candle in candles:
            required = ("open", "high", "low", "close")

            if not isinstance(candle, dict):
                return Signal.WAIT

            if not all(key in candle for key in required):
                return Signal.WAIT

            try:
                o, h, l, c = (
                    float(candle[key]) for key in required
                )
            except (TypeError, ValueError):
                return Signal.WAIT

            if not all(map(lambda x: x > 0 and x < float("inf"), [o, h, l, c])):
                return Signal.WAIT

            if h < max(o, c) or l > min(o, c) or h < l:
                return Signal.WAIT

        # Entry rules will be implemented and validated
        # after market-data and risk integration.

        return Signal.WAIT

    def analyze_all(self, markets):
        """Analyze multiple market-data dictionaries."""

        results = {}

        for market in markets:

            if not isinstance(market, dict):
                continue

            symbol = market.get("symbol")

            if not symbol:
                continue

            results[symbol] = self.analyze(market)

        return results
