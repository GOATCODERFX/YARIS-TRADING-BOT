
"""
YARIS Trading Bot
Main controller for the automated trading system.

This development version connects to MT5, scans enabled
markets and analyses signals. It does NOT execute orders.
"""

import time

from core.markets_selector import MarketSelector
from core.markets_scanner import MarketScanner
from core.strategy import StrategyEngine
from core.risk_manager import RiskManager
from core.trade_manager import TradeManager
from mt5.mt5_connector import MT5Connector


class YARIS:

    def __init__(self):
        self.mt5 = MT5Connector()

        self.market_selector = MarketSelector()
        self.market_scanner = MarketScanner(self.mt5)
        self.strategy = StrategyEngine()
        self.risk_manager = RiskManager(max_positions=5)
        self.trade_manager = TradeManager(
            self.mt5,
            max_positions=5
        )

        self.running = False

    def start(self):

        print("=" * 40)
        print("       YARIS TRADING BOT")
        print("       Automated Trading Engine")
        print("=" * 40)

        print("Initializing YARIS components...")

        if not self.mt5.connect():
            print("MT5 connection failed.")
            print("Check your MT5 terminal and account.")
            return

        print("MT5 connected successfully.")

        try:
            enabled_markets = (
                self.market_selector.get_enabled_markets()
            )

            selected_markets = (
                self.market_selector.select_markets(
                    enabled_markets
                )
            )

            if not selected_markets:
                print("No enabled markets found.")
                return

            symbols = [
                market["symbol"]
                for market in selected_markets
            ]

            print("Enabled markets:")

            for market in selected_markets:
                print(
                    f"- {market['name']}: "
                    f"{market['symbol']}"
                )

            self.running = True

            while self.running:

                print("\nYARIS scanning markets...")

                market_data = self.market_scanner.scan(
                    symbols
                )

                if not market_data:
                    print("No market data available.")
                    time.sleep(60)
                    continue

                signals = self.strategy.analyze_all(
                    market_data
                )

                for symbol, signal in signals.items():

                    signal_value = getattr(
                        signal,
                        "value",
                        signal
                    )

                    print(
                        f"{symbol}: {signal_value}"
                    )

                    if signal_value == "WAIT":
                        continue

                    print(
                        f"{symbol}: Signal detected. "
                        "Order execution remains disabled."
                    )

                print(
                    "YARIS scan complete. "
                    "Next scan in 60 seconds."
                )

                time.sleep(60)

        except KeyboardInterrupt:
            print("\nYARIS stopped by user.")

        except Exception as error:
            print(f"YARIS error: {error}")

        finally:
            self.running = False
            self.mt5.disconnect()
            print("YARIS disconnected from MT5.")

    def stop(self):
        self.running = False
        print("YARIS stop requested.")


if __name__ == "__main__":
    bot = YARIS()
    bot.start()
