"""
YARIS Trading Bot
Main controller for the YARIS automated trading system.
"""

from core.market_selector import MarketSelector
from mt5.mt5_connector import MT5Connector


class YARIS:
    def __init__(self):
        self.mt5 = MT5Connector()
        self.market_selector = MarketSelector()

        self.running = False
        self.selected_markets = []

    def start(self, selected_markets):
        """Start YARIS with the markets selected by the user."""

        if self.running:
            print("YARIS is already running.")
            return False

        if not selected_markets:
            print("YARIS: No markets selected.")
            return False

        try:
            self.selected_markets = (
                self.market_selector.select_markets(selected_markets)
            )
        except ValueError as error:
            print(f"YARIS: {error}")
            return False

        if not self.mt5.connect():
            print("YARIS: Cannot start without MT5.")
            return False

        self.running = True

        print("================================")
        print("        YARIS STARTED")
        print("================================")

        print("Selected markets:")

        for market in self.selected_markets:
            print(f" - {market}")

        print("================================")
        print("YARIS is now scanning.")
        print("================================")

        return True

    def stop(self):
        """Stop YARIS safely."""

        if not self.running:
            print("YARIS is already stopped.")
            return

        self.running = False
        self.mt5.disconnect()

        print("================================")
        print("        YARIS STOPPED")
        print("================================")

    def status(self):
        """Display the current YARIS status."""

        status = "RUNNING" if self.running else "STOPPED"

        print(f"YARIS STATUS: {status}")

        if self.selected_markets:
            print("Markets:")

            for market in self.selected_markets:
                print(f" - {market}")
