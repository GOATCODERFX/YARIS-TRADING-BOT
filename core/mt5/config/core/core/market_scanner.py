
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
        """Get the latest bid/ask price for a broker symbol."""

        if not self.connector.is_connected():
            print("YARIS: MT5 is not connected.")
            return None

        info = mt5.symbol_info(symbol)

        if info is None:
            print(f"YARIS: Symbol {symbol} is unavailable.")
            print(f"MT5 error: {mt5.last_error()}")
            return None

        if not info.visible:
            if not mt5.symbol_select(symbol, True):
                print(f"YARIS: Could not select {symbol}.")
                print(f"MT5 error: {mt5.last_error()}")
                return None

        tick = mt5.symbol_info_tick(symbol)

        if tick is None:
            print(f"YARIS: No market data for {symbol}.")
            print(f"MT5 error: {mt5.last_error()}")
            return None

        if tick.bid <= 0 or tick.ask <= 0:
            print(f"YARIS: Invalid bid/ask for {symbol}.")
            return None

        return {
            "symbol": symbol,
            "bid": tick.bid,
            "ask": tick.ask,
            "time": tick.time
        }

    def scan(self, symbols):
        """Scan all configured broker symbols."""

        results = []

        for symbol in symbols:
            price = self.get_price(symbol)

            if price is not None:
                results.append(price)

        return results
