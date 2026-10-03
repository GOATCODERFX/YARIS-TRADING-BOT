"""
YARIS Market Scanner

Reads live market information from MetaTrader 5.
This module does NOT place trades.
"""

import MetaTrader5 as mt5


class MarketScanner:

    def __init__(self, connector):
        self.connector = connector

    def get_price(self, symbol):
        """Get the latest bid/ask price for a symbol."""

        if not self.connector.is_connected():
            print("YARIS: MT5 is not connected.")
            return None

        tick = mt5.symbol_info_tick(symbol)

        if tick is None:
            print(f"YARIS: No market data for {symbol}.")
            return None

        return {
            "symbol": symbol,
            "bid": tick.bid,
            "ask": tick.ask,
            "time": tick.time
        }

    def scan(self, symbols):
        """Scan the selected symbols."""

        results = []

        for symbol in symbols:
            price = self.get_price(symbol)

            if price is not None:
                results.append(price)

        return results
