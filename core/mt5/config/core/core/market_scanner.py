
"""
YARIS Market Scanner

Reads live prices and historical candlestick
data from MetaTrader 5.
Does NOT place trades.
"""

import MetaTrader5 as mt5


class MarketScanner:

    def __init__(self, connector):
        self.connector = connector

    def get_price(self, symbol):
        """Retrieve the latest bid and ask."""

        if not self.connector.is_connected():
            print("YARIS: MT5 is not connected.")
            return None

        info = mt5.symbol_info(symbol)

        if info is None:
            print(f"YARIS: Symbol unavailable: {symbol}")
            return None

        if not info.visible:
            if not mt5.symbol_select(symbol, True):
                print(f"YARIS: Cannot select {symbol}.")
                return None

        tick = mt5.symbol_info_tick(symbol)

        if tick is None or tick.bid <= 0 or tick.ask <= 0:
            print(f"YARIS: Invalid price for {symbol}.")
            return None

        return {
            "symbol": symbol,
            "bid": tick.bid,
            "ask": tick.ask,
            "time": tick.time
        }

    def get_candles(
        self,
        symbol,
        timeframe=mt5.TIMEFRAME_M15,
        bars=200
    ):
        """Retrieve historical OHLC candlestick data."""

        if not self.connector.is_connected():
            return None

        if bars < 50 or bars > 1000:
            raise ValueError("Bars must be between 50 and 1000.")

        rates = mt5.copy_rates_from_pos(
            symbol,
            timeframe,
            0,
            bars
        )

        if rates is None or len(rates) < 50:
            print(f"YARIS: Insufficient candle data for {symbol}.")
            print("MT5 error:", mt5.last_error())
            return None

        candles = []

        for rate in rates:
            candles.append({
                "time": int(rate["time"]),
                "open": float(rate["open"]),
                "high": float(rate["high"]),
                "low": float(rate["low"]),
                "close": float(rate["close"]),
                "tick_volume": int(rate["tick_volume"])
            })

        return candles

    def scan(
        self,
        symbols,
        timeframe=mt5.TIMEFRAME_M15,
        bars=200
    ):
        """Scan multiple symbols and retrieve their candles."""

        results = []

        for symbol in symbols:

            price = self.get_price(symbol)

            if price is None:
                continue

            candles = self.get_candles(
                symbol,
                timeframe,
                bars
            )

            if candles is None:
                continue

            results.append({
                **price,
                "candles": candles
            })

        return results
