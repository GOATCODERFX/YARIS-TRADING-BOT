"""
YARIS Risk Manager

Controls basic trading-risk rules before an order
can be considered for execution.
"""


class RiskManager:

    def __init__(
        self,
        max_positions=1,
        risk_per_trade=0.01,
        max_daily_trades=5
    ):
        self.max_positions = max_positions
        self.risk_per_trade = risk_per_trade
        self.max_daily_trades = max_daily_trades

    def can_trade(
        self,
        open_positions,
        daily_trades,
        signal
    ):
        """Check whether a new trade is permitted."""

        if signal == "WAIT":
            return False, "No valid signal."

        if open_positions >= self.max_positions:
            return False, "Maximum open positions reached."

        if daily_trades >= self.max_daily_trades:
            return False, "Daily trade limit reached."

        return True, "Risk checks passed."

    def calculate_risk_amount(self, account_balance):
        """Calculate the maximum planned risk amount."""

        if account_balance <= 0:
            return 0

        return account_balance * self.risk_per_trade
