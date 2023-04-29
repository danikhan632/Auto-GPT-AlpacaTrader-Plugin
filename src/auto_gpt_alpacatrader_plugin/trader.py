import os
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.models import Position
from datetime import datetime

 
class Trader():
    """
    This is a plugin to use Auto-GPT with AlpacaTrader.
    """

    def __init__(self):
        self.trading_client =  TradingClient(os.environ.get('APCA_API_KEY_ID'), os.environ.get('APCA_API_SECRET_KEY')  ,paper=bool(os.environ.get('IS_PAPER', 'True')))

    def close_trade(self,symbol):
        positions = self.trading_client.get_all_positions()
        for position in positions:
            if position.symbol == symbol:
                if position.side == 'long':
                    self.trading_client.submit_order(
                        symbol=symbol,
                        qty=position.qty,
                        side='sell',
                        type='market',
                        time_in_force='gtc'
                    )
                elif position.side == 'short':
                    self.trading_client.submit_order(
                        symbol=symbol,
                        qty=position.qty,
                        side='buy',
                        type='market',
                        time_in_force='gtc'
                    )
        print("close trade")

    def close_all_trades(self):
        self.trading_client.cancel_orders()
        print("cancel orders")

    def get_account_information(self):
        return self.trading_client.get_account()
        # print("acct")
        # return "acct"

    def get_positions(self):
        def pos_to_json(pos):
            res = { "asset_id": str(pos.asset_id), "symbol": pos.symbol, "avg_entry_price": pos.avg_entry_price, "qty": pos.qty, "market_value": pos.market_value, "cost_basis": pos.cost_basis, "unrealized_pl": pos.unrealized_pl, "unrealized_plpc": pos.unrealized_plpc, "unrealized_intraday_pl": pos.unrealized_intraday_pl, "unrealized_intraday_plpc": pos.unrealized_intraday_plpc, "current_price": pos.current_price, "lastday_price": pos.lastday_price, "change_today": pos.change_today, "asset_marginable": pos.asset_marginable }
            return res
        positions = self.trading_client.get_all_positions()
        formatted_positions = [pos_to_json(position) for position in positions]
        return formatted_positions
        # return "get position"

    def place_trade(self,symbol, qty, side, order_type, time_in_force):
        order_data =  alpaca.trading.requests.MarketOrderRequest(
            symbol=symbol,
            qty=qty,
            side=side,
            time_in_force=time_in_force
        )
        order=self.trading_client.submit_order(order_data)
        print(order)
        print("place trade")