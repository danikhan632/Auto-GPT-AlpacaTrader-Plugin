import os
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce, OrderType
from alpaca.trading.models import Position
from datetime import datetime

 
class Trader():
    """
    This is a plugin to use Auto-GPT with AlpacaTrader.
    """

    def __init__(self):
        self.trading_client =  TradingClient(
        os.environ.get('APCA_API_KEY_ID'), 
        os.environ.get('APCA_API_SECRET_KEY'),
        paper=bool(os.environ.get('APCA_PAPER',True)))

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

    def place_trade(self, symbol, quantity, side, order_type, time_in_force):
        side = side.lower()
        order_type = order_type.lower()
        time_in_force = time_in_force.lower()

        side_mapping = {'buy': OrderSide.BUY, 'sell': OrderSide.SELL}
        order_type_mapping = {'market': OrderType.MARKET, 'limit': OrderType.LIMIT, 'stop': OrderType.STOP,
                            'stop_limit': OrderType.STOP_LIMIT, 'trailing_stop': OrderType.TRAILING_STOP}
        time_in_force_mapping = {'day': TimeInForce.DAY, 'gtc': TimeInForce.GTC, 'opg': TimeInForce.OPG,
                                'cls': TimeInForce.CLS, 'ioc': TimeInForce.IOC, 'fok': TimeInForce.FOK}
        if side not in side_mapping:
            return {"error": "invalid order, side must be buy or sell"}
        if order_type not in order_type_mapping:
            return {"error": "invalid order, order type must be market, limit, stop, stop_limit or trailing_stop"}
        if time_in_force not in time_in_force_mapping:
            return {"error": "invalid order, time in force must be day, gtc, opg, cls, ioc, or fok"}

        side_req, order_type_req, time_in_force_req = side_mapping[side], order_type_mapping[order_type], time_in_force_mapping[time_in_force]




        order_data = MarketOrderRequest(
            symbol=symbol,
            qty=float(quantity),
            side=side_req,
            type=order_type_req,
            time_in_force=time_in_force
        )
        order=self.trading_client.submit_order(order_data)
        return str(order)


    def get_allowed_stocks(self):
        return {"allowed_stocks_to_trade":['AAPL', 'TSLA', 'NVDA', 'PEP', 'AVGO', 'AZN', 'CSCO', 'ASML', 'ADBE', 'TXN', 'AMGN', 'QCOM', 'INTC', 'SBUX', 'AMD', 'REGN', 'MDLZ', 'VRTX', 'ISRG', 'PDD', 'ADI', 'ABNB', 'CHTR', 'AMAT', 'MU', 'KDP', 'TEAM', 'MNST', 'ORLY', 'LRCX', 'SNPS', 'ADSK', 'CDNS', 'CTAS', 'FTNT', 'BIIB', 'WDAY', 'DXCM', 'KLAC', 'LULU', 'NXPI', 'CRWD', 'BIDU', 'ILMN', 'MRVL', 'CTSH', 'ODFL', 'ROST', 'IDXX', 'CPRT', 'FAST', 'DDOG', 'SGEN', 'ZS', 'VRSN', 'ANSS', 'ALGN', 'SWKS', 'DOCU', 'OKTA', 'ZM', 'MSFT', 'GOOG', 'GOOGL', 'AMZN', 'META', 'COST', 'NFLX', 'INTU', 'BKNG', 'ATVI', 'MAR', 'NTES', 'PAYX', 'EA', 'MCHP', 'DLTR', 'EBAY', 'MTCH', 'SPLK']}

