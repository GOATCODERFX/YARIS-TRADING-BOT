"""
YARIS Trading Bot
Main controller for the automated trading system.
"""

from core.market_selector import MarketSelector
from core.market_scanner import MarketScanner
from core.strategy import StrategyEngine
from core.risk_manager import RiskManager
from core.trade_manager import TradeManager
from mt5.mt5_connector import MT5Connector


class YARIS:

    def __init__(self):

        # MT5 connection
        self.mt5 = MT5Connector()

        # YARIS modules
        self.market_selector = MarketSelector()
        self.scanner = MarketScanner(self.mt5)
        self.strategy = StrategyEngine()
        self.risk_manager = RiskManager()
        self.trade_manager = TradeManager(self.mt5)

        # Bot state
        self.running = False
        self.selected_markets = []

    def start(self, selected_markets):

        """Start YARIS with selected markets."""

        if self.running:
            print("YARIS: Already running.")
            return False

        if not selected_markets:
            print("YARIS: No markets selected.")
            return False

        try:
            self.selected_markets = (
                self.market_selector.select_markets(
                    selected_markets
                )
            )

        except ValueError as error:
            print(f"YARIS: {error}")
            return False

        # Connect to MT5
        if not self.mt5.connect():
            print("YARIS: MT5 connection failed.")
            return False

        self.running = True

        print()
        print("================================")
        print("        YARIS STARTED")
        print("================================")

        print("Selected markets:")

        for market in self.selected_markets:
            print(f" - {market}")

        print()
        print("YARIS: Market scanner ready.")
        print("YARIS: Strategy engine ready.")
        print("YARIS: Risk manager ready.")
        print("YARIS: Trade manager ready.")
        print("YARIS: Live trading is currently OFF.")
        print("================================")

        return True

    def scan(self):

        """Scan the selected markets."""

        if not self.running:
            print("YARIS: Bot is not running.")
            return []

        symbols = []

        for market in self.selected_markets:

            market_data = (
                self.market_selector.markets[market]
            )

            symbols.append(
                market_data["symbol"]
            )

        results = self.scanner.scan(symbols)

        return results

    def stop(self):

        """Stop YARIS safely."""

        if not self.running:
            print("YARIS: Already stopped.")
            return

        self.running = False

        self.mt5.disconnect()

        print("================================")
        print("        YARIS STOPPED")
        print("================================")

    def status(self):

        """Display YARIS status."""

        status = "RUNNING" if self.running else "STOPPED"

        print(f"YARIS STATUS: {status}")

        if self.selected_markets:

            print("Markets:")

            for market in self.selected_markets:
                print(f" - {market}")
