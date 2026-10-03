"""
YARIS Trade Manager

Handles trade planning and position management.
Live order execution will be enabled only after
the strategy and risk systems have been tested.
"""


class TradeManager:

    def __init__(self, mt5_connector):
        self.mt5 = mt5_connector
        self.live_trading_enabled = False

    def create_trade_plan(
        self,
        symbol,
        direction,
        entry,
        stop_loss,
        take_profit
    ):
        """Create a trade plan without sending an order."""

        return {
            "symbol": symbol,
            "direction": direction,
            "entry": entry,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "status": "PLANNED"
        }

    def execute(self, trade_plan):
        """
        Execute a trade only when live trading has
        explicitly been enabled.
        """

        if not self.live_trading_enabled:
            print(
                "YARIS: LIVE TRADING DISABLED. "
                "Trade plan was not sent to MT5."
            )
            return False

        # Actual MT5 order execution will be added
        # after testing and validation.
        print(
            f"YARIS: Execution requested for "
            f"{trade_plan['symbol']}"
        )

        return False

    def enable_live_trading(self):
        """Enable live execution after testing."""

        self.live_trading_enabled = True
        print("YARIS: LIVE TRADING ENABLED.")

    def disable_live_trading(self):
        """Disable live execution."""

        self.live_trading_enabled = False
        print("YARIS: LIVE TRADING DISABLED.")
