
"""
YARIS Trading Bot
Trade planning and position management.

Order execution remains disabled during development
and testing. No live orders can be sent by this version.
"""


class TradeManager:

    def __init__(self, mt5_connector, max_positions=5):
        self.mt5 = mt5_connector
        self.max_positions = max_positions
        self.live_trading_enabled = False
        self.trade_history = []

    def create_trade_plan(
        self,
        symbol,
        direction,
        entry,
        stop_loss,
        take_profit
    ):
        """Validate and create a trade plan."""

        if not symbol:
            raise ValueError("A trading symbol is required.")

        if direction not in ("BUY", "SELL"):
            raise ValueError("Direction must be BUY or SELL.")

        values = (entry, stop_loss, take_profit)

        if any(
            not isinstance(value, (int, float))
            or isinstance(value, bool)
            for value in values
        ):
            raise ValueError("Prices must be numeric.")

        if any(value <= 0 for value in values):
            raise ValueError("Prices must be positive.")

        if direction == "BUY":
            if not stop_loss < entry < take_profit:
                raise ValueError(
                    "BUY requires stop loss < entry < take profit."
                )

        if direction == "SELL":
            if not take_profit < entry < stop_loss:
                raise ValueError(
                    "SELL requires take profit < entry < stop loss."
                )

        return {
            "symbol": symbol,
            "direction": direction,
            "entry": float(entry),
            "stop_loss": float(stop_loss),
            "take_profit": float(take_profit),
            "status": "PLANNED"
        }

    def execute(self, trade_plan):
        """
        Execution is deliberately blocked.
        This version cannot send MT5 orders.
        """

        print(
            "YARIS: ORDER EXECUTION BLOCKED. "
            "Testing and validation are still required."
        )

        return False

    def get_open_positions(self):
        """Return current broker positions when connected."""

        if not self.mt5 or not self.mt5.is_connected():
            return []

        return self.mt5.get_open_positions()

    def can_open_position(self):
        """Check the maximum simultaneous position limit."""

        positions = self.get_open_positions()

        return len(positions) < self.max_positions

    def get_trade_history(self):
        """Return recorded trade history."""

        return list(self.trade_history)

    def disable_live_trading(self):
        """Keep order execution disabled."""

        self.live_trading_enabled = False
        print("YARIS: LIVE TRADING DISABLED.")
