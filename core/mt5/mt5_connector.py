
"""
YARIS MT5 Connector
Secure connection and account verification.
"""

import MetaTrader5 as mt5


class MT5Connector:

    def __init__(self):
        self.connected = False

    def connect(self):
        """Connect to MT5 and verify account access."""

        if not mt5.initialize():
            print("YARIS: MT5 initialization failed.")
            print("MT5 error:", mt5.last_error())
            self.connected = False
            return False

        account = mt5.account_info()

        if account is None:
            print("YARIS: No authenticated MT5 account.")
            print("MT5 error:", mt5.last_error())
            mt5.shutdown()
            self.connected = False
            return False

        self.connected = True

        print("YARIS: MT5 connected successfully.")
        print("Account login:", account.login)
        print("Broker server:", account.server)
        print("Account balance:", account.balance)

        return True

    def get_account_info(self):
        """Return account information if connected."""

        if not self.is_connected():
            return None

        return mt5.account_info()

    def is_connected(self):
        """Check MT5 connection and account availability."""

        if not self.connected:
            return False

        if mt5.terminal_info() is None:
            self.connected = False
            return False

        if mt5.account_info() is None:
            self.connected = False
            return False

        return True

    def disconnect(self):
        """Safely disconnect from MT5."""

        if self.connected:
            mt5.shutdown()
            self.connected = False
            print("YARIS: MT5 disconnected.")
