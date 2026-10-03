"""
YARIS MT5 Connector
Connects YARIS to MetaTrader 5.
"""

import MetaTrader5 as mt5


class MT5Connector:
    def __init__(self):
        self.connected = False

    def connect(self):
        """Connect YARIS to MetaTrader 5."""
        if not mt5.initialize():
            print("YARIS: MT5 connection failed.")
            self.connected = False
            return False

        self.connected = True
        print("YARIS: MT5 connected.")
        return True

    def disconnect(self):
        """Disconnect from MetaTrader 5."""
        if self.connected:
            mt5.shutdown()
            self.connected = False
            print("YARIS: MT5 disconnected.")

    def is_connected(self):
        """Return current MT5 connection status."""
        return self.connected
