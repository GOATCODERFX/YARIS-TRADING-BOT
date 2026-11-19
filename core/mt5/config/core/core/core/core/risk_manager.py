
"""
YARIS Trading Bot
Risk management and account protection.
"""


class RiskManager:
    def __init__(
        self,
        max_positions=5,
        risk_per_trade=0.01,
        max_daily_trades=5,
        max_daily_loss=0.03
    ):
        self.max_positions = max_positions
        self.risk_per_trade = risk_per_trade
        self.max_daily_trades = max_daily_trades
        self.max_daily_loss = max_daily_loss

    def can_trade(
        self,
        open_positions,
        daily_trades,
        signal,
        daily_loss_pct=0.0
    ):
        """
        Checks whether a new trade is allowed.
        Returns (approved, reason).
        """

        signal_value = getattr(signal, "value", signal)

        if signal_value == "WAIT":
            return False, "No valid trading signal."

        if signal_value not in ("BUY", "SELL"):
            return False, "Invalid trading signal."

        if open_positions >= self.max_positions:
            return False, "Maximum open positions reached."

        if daily_trades >= self.max_daily_trades:
            return False, "Daily trade limit reached."

        if daily_loss_pct >= self.max_daily_loss:
            return False, "Daily loss limit reached."

        return True, "Trade approved by risk checks."

    def calculate_risk_amount(self, balance):
        """
        Calculates the maximum money to risk on a trade.
        Actual lot sizing must also consider the stop-loss
        distance and the broker's symbol specifications.
        """

        if balance <= 0:
            raise ValueError("Account balance must be positive.")

        return balance * self.risk_per_trade
