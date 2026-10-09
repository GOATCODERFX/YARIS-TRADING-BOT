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
    self.market_selector = MarketSelector()
    self.market_scanner = MarketScanner()
    self.strategy = StrategyEngine()
    self.risk_manager = RiskManager()
    self.trade_manager = TradeManager()
    self.mt5 = MT5Connector()

def start(self):
    print("YARIS Trading Bot")
    print("Initializing automated trading system...")

    if not self.mt5.connect():
        print("MT5 connection failed. Check your MT5 setup.")
        return

    print("MT5 connected successfully.")

    try:
        while True:
            market = self.market_selector.select_market()

            if not market:
                print("No market selected. Waiting...")
                continue

            market_data = self.market_scanner.scan(market)

            if market_data is None:
                print(f"No market data available for {market}.")
                continue

            signal = self.strategy.analyze(market_data)

            if signal:
                approved = self.risk_manager.approve_trade(
                    market, signal, market_data
                )

                if approved:
                    self.trade_manager.execute_trade(
                        market, signal, market_data
                    )

    except KeyboardInterrupt:
        print("YARIS stopped by user.")

    finally:
        self.mt5.disconnect()

if name == "main":
bot = YARIS()
bot.start()
