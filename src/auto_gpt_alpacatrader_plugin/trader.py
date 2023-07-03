import os,json,re
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce, OrderType
from alpaca.trading.models import Position
import requests
from collections import deque

from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
from dateutil.relativedelta import relativedelta, MO
import pytz
from datapackage import Package
import threading
import time
from datetime import datetime, timedelta

import yfinance as yf

class Trader():
    """
    This is a plugin to use Auto-GPT with AlpacaTrader.
    """

    def __init__(self, experiment=False):
        self.trading_client =  TradingClient(
            os.environ.get('APCA_API_KEY_ID'), 
            os.environ.get('APCA_API_SECRET_KEY'),
            paper=bool(os.environ.get('APCA_PAPER',True))
        )

        self.current_prices = {}
        self.previous_prices = {}
        self.price_changes = {}
        self.top_movers = {}
        self.alerts={}
        self.threads = []
        self.idea=1
        self.update = False
        self.update_info = ""
        self.active = experiment
        self.price_history = {}
        if experiment==True:
            threading.Thread(target=self.check_price_changes).start()

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





    def get_positions(self):
        def pos_to_json(pos):
            res = { "asset_id": str(pos.asset_id), "symbol": pos.symbol, "avg_entry_price": pos.avg_entry_price, "qty": pos.qty, "market_value": pos.market_value, "cost_basis": pos.cost_basis, "unrealized_pl": pos.unrealized_pl, "unrealized_plpc": pos.unrealized_plpc, "unrealized_intraday_pl": pos.unrealized_intraday_pl, "unrealized_intraday_plpc": pos.unrealized_intraday_plpc, "current_price": pos.current_price, "lastday_price": pos.lastday_price, "change_today": pos.change_today, "asset_marginable": pos.asset_marginable }
            return res
        positions = self.trading_client.get_all_positions()
        formatted_positions = [pos_to_json(position) for position in positions]
        for position in formatted_positions:
            self.monitor(position['symbol'])
        return formatted_positions


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


    def get_positions_info(self):
        pass
    def get_watchlist(self):
        pass
    def add_to_watchlist(self):
        pass


    def get_market_sentiment(self):
        msg=""
        tickers=["SPY", "DOW", "QQQ"]
        for ticker in tickers:
            msg += ticker+":\n"
            sym=yf.Ticker(ticker).info
            msg += 'previousClose: '+str(sym['previousClose'])+"\n"
            msg += 'open '+str(sym['open'])+"\n"
            msg += 'dayLow '+str(sym['dayLow'])+"\n"
            msg += 'dayHigh '+str(sym['dayHigh'])+"\nNews:\n"
            msg +=self.get_sym_news(symbol=ticker)
        return msg

    def get_sym_news(self,symbol):
        msg=""
        news=yf.Ticker(symbol).news[:5]
        for article in news:
            publish_time = datetime.fromtimestamp(article['providerPublishTime'])
            title = article['title']
            publish_hour = publish_time.strftime("%m-%d %H:%M")
            msg += f"{title} ({publish_hour})\n"
        msg += "\n"
        return msg
    
    
    def get_large_movers(self):
        # url = "https://www.tradingview.com/markets/stocks-usa/market-movers-large-cap/"
        # response = requests.get(url)
        # soup = BeautifulSoup(response.content, "html.parser")
        # text_content = soup.get_text().replace("\n", "")
        # text_content = re.sub(r'\S*@\S*\s?', '', text_content)  
        # text_content = re.sub(r'http\S+|www.\S+', '', text_content)  
        # text_content = re.sub(r'@\S+', '', text_content)  
        # text_content = text_content[1237:].replace("\t", "")
        # text_content = text_content[:5000]
        return ['MSFT',' GOOG',' AMZN',' NVDA',' TSLA',' BRK.A',' META',' V',' UNH',' LLY',' XOM',' JPM',' WMT',' JNJ',' MA',' AVGO',' PG',' ORCL',' HD',' CVX',' MRK',' KO',' PEP',' COST',' ABBV',' BAC',' ADBE',' MCD',' CSCO',' PFE',' ACN',' CRM',' TMO',' NFLX',' AMD',' ABT',' LIN',' DHR',' CMCSA',' NKE',' TMUS',' DIS',' TXN',' WFC',' UPS',' VZ',' PM',' NEE',' MS',' RTX',' INTC']


    def get_ideas(self):
        url = "https://www.tradingview.com/markets/stocks-usa/ideas/page-"+str(self.idea)+"/"  
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        text_content = soup.get_text().replace("\n", "")
        text_content = re.sub(r'\S*@\S*\s?', '', text_content)  
        text_content = re.sub(r'http\S+|www.\S+', '', text_content)  
        text_content = re.sub(r'@\S+', '', text_content)  
        text_content=text_content[852:].replace("\t", "")
        text_content=text_content[:-1085]
        self.idea+=1
        return text_content




    def monitor(self, symbol):
        def _monitor(symbol):
            previous_close = None
            while True:
                ticker = yf.Ticker(symbol)
                today_data = ticker.history(period='1d')
                if len(today_data['Close']) > 0:
                    current_close = today_data['Close'][0]
                    if previous_close is not None:
                        self.price_changes[symbol] = ((current_close - previous_close) / previous_close) * 100
                    self.current_prices[symbol] = current_close
                    previous_close = current_close
                    self.price_history.setdefault(symbol, deque(maxlen=100)).append((current_close, datetime.now()))
                time.sleep(10)

        thread = threading.Thread(target=_monitor, args=(symbol,))
        thread.start()
        self.threads.append(thread)

    def check_price_changes(self):
        while self.active:  # Checks self.active in each iteration
            for symbol, history in self.price_history.items():
                now = datetime.now()
                five_minutes_ago = now - timedelta(minutes=5)
                recent_prices = [price for price, timestamp in history if five_minutes_ago <= timestamp <= now]
                if len(recent_prices) >= 2 and abs(recent_prices[-1] - recent_prices[0]) > 0.5:
                    self.monitor(symbol)
                    self.update = True
                    self.update_info += f"Stock {symbol} has moved by more than 0.5 points in the past 5 minutes.\n"
            time.sleep(25)  # Check every minute

    def get_current_price(self, symbol):
        price = self.current_prices.get(symbol)
        return round(price, 2) if price is not None else None

    def get_day_percent_change(self, symbol):
        change = self.price_changes.get(symbol)
        return round(change, 2) if change is not None else None




    def is_market_open(self) -> bool:
        HOLIDAYS = [
            datetime(datetime.now().year, 1, 1),  # New Year's Day
            datetime(datetime.now().year, 7, 4),  # Independence Day
            datetime(datetime.now().year, 12, 25),  # Christmas Day
            datetime(datetime.now().year, 1, 1) + relativedelta(weekday=MO(+3)),  # Martin Luther King, Jr. Day
            datetime(datetime.now().year, 2, 1) + relativedelta(weekday=MO(+3)),  # Washington's Birthday
            datetime(datetime.now().year, 5, 31) + relativedelta(weekday=MO(-1)),  # Memorial Day
            datetime(datetime.now().year, 9, 1) + relativedelta(weekday=MO(+1)),  # Labor Day
            datetime(datetime.now().year, 11, 1) + relativedelta(weekday=MO(+4)),  # Thanksgiving Day
            datetime(datetime.now().year, 6, 19)  # Juneteenth National Independence Day
        ]

        for i in range(len(HOLIDAYS)):
            if HOLIDAYS[i].weekday() == 5:  # if holiday falls on Saturday
                HOLIDAYS[i] -= relativedelta(days=+1)
            elif HOLIDAYS[i].weekday() == 6:  # if holiday falls on Sunday
                HOLIDAYS[i] += relativedelta(days=+1)
        market_open_time = datetime.now(pytz.timezone('US/Eastern')).replace(hour=9, minute=30, second=0)
        market_close_time = datetime.now(pytz.timezone('US/Eastern')).replace(hour=16, minute=0, second=0)
        current_time = datetime.now(pytz.timezone('US/Eastern'))
        if market_open_time <= current_time <= market_close_time:
            if current_time.weekday() < 5:  # 0 = Monday, 1 = Tuesday, ..., 4 = Friday
                if current_time.date() not in [d.date() for d in HOLIDAYS]:
                    return True

        return False

    def __del__(self):
        self.active = False  # Set flag to False to stop threads
        for thread in self.threads:  # Wait for all threads to finish
            thread.join()
