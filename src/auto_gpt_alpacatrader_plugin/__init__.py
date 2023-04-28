"""This is a plugin to use Auto-GPT with AlpacaTrader."""
from typing import Any, Dict, List, Optional, Tuple, TypeVar, TypedDict
from auto_gpt_plugin_template import AutoGPTPluginTemplate
import alpaca_trade_api as tradeapi
import pandas as pd
import numpy as np
from ta import add_all_ta_features
from ta.trend import ADXIndicator, SMAIndicator, EMAIndicator, MACD
from ta.momentum import RSIIndicator, StochasticOscillator, TSIIndicator, MFIIndicator
from ta.volatility import AverageTrueRange
from ta.volume import VolumeWeightedAveragePrice
# AlpacaTrader
import requests
import os

from alpaca_trade_api import REST

api_key = os.environ.get('APCA_API_KEY_ID')
api_secret = os.environ.get('APCA_API_SECRET_KEY') 
base_url = os.environ.get('APCA_API_BASE_URL') 

api = REST(api_key, api_secret, base_url, api_version='v2')


PromptGenerator = TypeVar("PromptGenerator")

class Message(TypedDict):
    role: str
    content: str


class AutoGPTAlpacaTraderPlugin(AutoGPTPluginTemplate):
    """
    This is a plugin to use Auto-GPT with AlpacaTrader.
    """

    def __init__(self):
        super().__init__()
        self._name = "Auto-GPT-AlpacaTrader"
        self._version = "0.1.0"
        self._description = "This is a plugin for Auto-GPT-AlpacaTrader."

    def post_prompt(self, prompt: PromptGenerator) -> PromptGenerator:
        prompt.add_command(
            "Fetch Candlesticks",
            "fetch_candlesticks",
            {
                "symbol": "<symbol>",
                "timeframe": "<timeframe>"
            },
            self.fetch_candlesticks
        ),
        prompt.add_command(
            "Close All Trades",
            "close_all_trades",
            {},
            self.close_all_trades
        ),
        prompt.add_command(
            "Get Account Information",
            "get_account_information",
            {},
            self.get_account_information
        ),
        prompt.add_command(
            "Get Positions",
            "get_positions",
            {},
            self.get_positions
        ),
        prompt.add_command(
            "Place Trade",
            "place_trade",
            {
                "symbol": "<symbol>",
                "volume": "<volume>",
                "signal": "<signal>"
            },
            self.place_trade
        ),
        prompt.add_command(
            "Money Flow Index",
            "money_flow_index",
            {
                "symbol": "<symbol>",
                "timeframe": "<timeframe>"
            },
            self.money_flow_index
        ),
        prompt.add_command(
            "RSI",
            "rsi",
            {
                "symbol": "<symbol>",
                "timeframe": "<timeframe>",
            },
            self.rsi
        ),
        prompt.add_command(
            "Volume",
            "volume",
            {
                "symbol": "<symbol>",
                "timeframe": "<timeframe>",
            },
            self.volume
        ),
        prompt.add_command(
            "Simple Moving Average",
            "sma",
            {
                "symbol": "<symbol>",
                "timeframe": "<timeframe>",
                "period": "<period>",
            },
            self.sma
        ),
        prompt.add_command(
            "Exponential Moving Average",
            "ema",
            {
                "symbol": "<symbol>",
                "timeframe": "<timeframe>",
                "period": "<period>",
            },
            self.ema
        ),
        prompt.add_command(
            "MACD",
            "macd",
            {
                "symbol": "<symbol>",
                "timeframe": "<timeframe>",
                "period_fast": "<period_fast>",
                "period_slow": "<period_slow>",
                "period_signal": "<period_signal>",
            },
            self.macd
        ),
        prompt.add_command(
            "Moving Average of Oscillator (OsMA)",
            "osma",
            {
                "symbol": "<symbol>",
                "timeframe": "<timeframe>",
                "period_fast": "<period_fast>",
                "period_slow": "<period_slow>",
                "period_signal": "<period_signal>",
            },
            self.osma
        ),
        prompt.add_command(
            "Weighted Moving Average",
            "wma",
            {
                "symbol": "<symbol>",
                "timeframe": "<timeframe>",
                "period": "<period>",

            },
            self.wma
        ),
        prompt.add_command(
            "Moving Average Envelope",
            "mae",
            {
                "symbol": "<symbol>",
                "timeframe": "<timeframe>",
                "period": "<period>",
                "percentage": "<period>",
            },
            self.mae
        ),
        prompt.add_command(
            "Bollinger Bands",
            "bollinger_bands",
            {
                "symbol": "<symbol>",
                "timeframe": "<timeframe>",
                "period": "<period>",
                "deviation": "<deviation>",
            },
            self.bollinger_bands
        ), prompt.add_command(
            "Fibonacci Retracement",
            "fib_retracements",
            {
                "symbol": "<symbol>",
                "timeframe": "<timeframe>",
                "high": "<high>",
                "low": "<low>",
            },
            self.fib_retracements
        ),
        return prompt
# ______________________________________________________________________________________________________________________
    def fetch_candlesticks(self,symbol, timeframe, start, end, limit=1000):
        return api.get_barset(symbol, timeframe, limit=limit, start=start, end=end).df[symbol]

    def close_trade(self,symbol):
        positions = api.list_positions()
        for position in positions:
            if position.symbol == symbol:
                if position.side == 'long':
                    api.submit_order(
                        symbol=symbol,
                        qty=position.qty,
                        side='sell',
                        type='market',
                        time_in_force='gtc'
                    )
                elif position.side == 'short':
                    api.submit_order(
                        symbol=symbol,
                        qty=position.qty,
                        side='buy',
                        type='market',
                        time_in_force='gtc'
                    )

    def close_all_trades(self):
        positions = api.list_positions()
        for position in positions:
            close_trade(position.symbol)

    def get_account_information(self):
        return api.get_account()

    def get_positions(self):
        return api.list_positions()

    def place_trade(self,symbol, qty, side, order_type, time_in_force):
        api.submit_order(
            symbol=symbol,
            qty=qty,
            side=side,
            type=order_type,
            time_in_force=time_in_force
        )

    def _prepare_data(self,symbol, timeframe, start, end):
        data = fetch_candlesticks(symbol, timeframe, start, end)
        data = add_all_ta_features(data, open="open", high="high", low="low", close="close", volume="volume")
        return data

    # Technical indicators
    def rsi(self,symbol, timeframe, start, end, period=14):
        data = _prepare_data(symbol, timeframe, start, end)
        rsi_indicator = RSIIndicator(data['close'], window=period)
        return rsi_indicator.rsi()

    def money_flow_index(self,symbol, timeframe, start, end, period=14):
        data = _prepare_data(symbol, timeframe, start, end)
        mfi_indicator = MFIIndicator(data['high'], data['low'], data['close'], data['volume'], window=period)
        return mfi_indicator.money_flow_index()

    def volume(self,symbol, timeframe, start, end):
        data = fetch_candlesticks(symbol, timeframe, start, end)
        return data['volume']

    def sma(self,symbol, timeframe, start, end, period=14):
        data = _prepare_data(symbol, timeframe, start, end)
        sma_indicator = SMAIndicator(data['close'], window=period)
        return sma_indicator.sma_indicator()

    def ema(self,symbol, timeframe, start, end, period=14):
        data = _prepare_data(symbol, timeframe, start, end)
        ema_indicator = EMAIndicator(data['close'], window=period)
        return ema_indicator.ema_indicator()

    def macd(self,symbol, timeframe, start, end, period_slow=26, period_fast=12, period_sign=9):
        data = _prepare_data(symbol, timeframe, start, end)
        macd_indicator = MACD(data['close'], n_slow=period_slow, n_fast=period_fast, n_sign=period_sign)
        return macd_indicator.macd(), macd_indicator.macd_signal(), macd_indicator.macd_diff()



    def wma(self,symbol, timeframe, start, end, period=14):
        data = _prepare_data(symbol, timeframe, start, end)
        vwap = VolumeWeightedAveragePrice(data['high'], data['low'], data['close'], data['volume'], window=period)
        return vwap.volume_weighted_average_price()

    def adx(self,symbol, timeframe, start, end, n=14):
        data = _prepare_data(symbol, timeframe, start, end)
        adx_indicator = ADXIndicator(data['high'], data['low'], data['close'], window=n)
        return adx_indicator.adx()

    def adi(self,symbol, timeframe, start, end, n=14):
        data = _prepare_data(symbol, timeframe, start, end)
        atr = AverageTrueRange(data['high'], data['low'], data['close'], window=n)
        return atr.average_true_range()

    def fib_retracements(self,symbol, timeframe, start, end):
        data = fetch_candlesticks(symbol, timeframe, start, end)
        high = data['high'].max()
        low = data['low'].min()
        levels = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1]
        retracements = [(high - low) * level for level in levels]
        return [(high - r, level) for r, level in zip(retracements, levels)]

    def stochastic_oscillator(self,symbol, timeframe, start, end, n=14):
        data = _prepare_data(symbol, timeframe, start, end)
        stoch = StochasticOscillator(data['high'], data['low'], data['close'], window=n)
        return stoch.stoch(), stoch.stoch_signal()

    def tsi(self,symbol, timeframe, start, end, r=25, s=13):
        data = _prepare_data(symbol, timeframe, start, end)
        tsi_indicator = TSIIndicator(data['close'], r, s)
        return tsi_indicator.tsi()

    def get_stock_of_the_day(self):
        assets = api.list_assets(status='active', asset_class='us_equity')
        symbols = [asset.symbol for asset in assets]
        return np.random.choice(symbols)
# ______________________________________________________________________________________________________________________
    def handle_chat_completion(
        self, messages: List[Message], model: str, temperature: float, max_tokens: int
    ) -> str:
        """This method is called when the chat completion is done.
        Args:
            messages (List[Message]): The messages.
            model (str): The model name.
            temperature (float): The temperature.
            max_tokens (int): The max tokens.
        Returns:
            str: The resulting response.
        """
        pass
    
    def can_handle_post_prompt(self) -> bool:
        """This method is called to check that the plugin can
        handle the post_prompt method.
        Returns:
            bool: True if the plugin can handle the post_prompt method."""
        return True

    def can_handle_on_response(self) -> bool:
        """This method is called to check that the plugin can
        handle the on_response method.
        Returns:
            bool: True if the plugin can handle the on_response method."""
        return False

    def on_response(self, response: str, *args, **kwargs) -> str:
        """This method is called when a response is received from the model."""
        pass

    def can_handle_on_planning(self) -> bool:
        """This method is called to check that the plugin can
        handle the on_planning method.
        Returns:
            bool: True if the plugin can handle the on_planning method."""
        return False

    def on_planning(
        self, prompt: PromptGenerator, messages: List[Message]
    ) -> Optional[str]:
        """This method is called before the planning chat completion is done.
        Args:
            prompt (PromptGenerator): The prompt generator.
            messages (List[str]): The list of messages.
        """
        pass

    def can_handle_post_planning(self) -> bool:
        """This method is called to check that the plugin can
        handle the post_planning method.
        Returns:
            bool: True if the plugin can handle the post_planning method."""
        return False

    def post_planning(self, response: str) -> str:
        """This method is called after the planning chat completion is done.
        Args:
            response (str): The response.
        Returns:
            str: The resulting response.
        """
        pass

    def can_handle_pre_instruction(self) -> bool:
        """This method is called to check that the plugin can
        handle the pre_instruction method.
        Returns:
            bool: True if the plugin can handle the pre_instruction method."""
        return False

    def pre_instruction(self, messages: List[Message]) -> List[Message]:
        """This method is called before the instruction chat is done.
        Args:
            messages (List[Message]): The list of context messages.
        Returns:
            List[Message]: The resulting list of messages.
        """
        pass

    def can_handle_on_instruction(self) -> bool:
        """This method is called to check that the plugin can
        handle the on_instruction method.
        Returns:
            bool: True if the plugin can handle the on_instruction method."""
        return False

    def on_instruction(self, messages: List[Message]) -> Optional[str]:
        """This method is called when the instruction chat is done.
        Args:
            messages (List[Message]): The list of context messages.
        Returns:
            Optional[str]: The resulting message.
        """
        pass

    def can_handle_post_instruction(self) -> bool:
        """This method is called to check that the plugin can
        handle the post_instruction method.
        Returns:
            bool: True if the plugin can handle the post_instruction method."""
        return False

    def post_instruction(self, response: str) -> str:
        """This method is called after the instruction chat is done.
        Args:
            response (str): The response.
        Returns:
            str: The resulting response.
        """
        pass

    def can_handle_pre_command(self) -> bool:
        """This method is called to check that the plugin can
        handle the pre_command method.
        Returns:
            bool: True if the plugin can handle the pre_command method."""
        return False

    def pre_command(
        self, command_name: str, arguments: Dict[str, Any]
    ) -> Tuple[str, Dict[str, Any]]:
        """This method is called before the command is executed.
        Args:
            command_name (str): The command name.
            arguments (Dict[str, Any]): The arguments.
        Returns:
            Tuple[str, Dict[str, Any]]: The command name and the arguments.
        """
        pass

    def can_handle_post_command(self) -> bool:
        """This method is called to check that the plugin can
        handle the post_command method.
        Returns:
            bool: True if the plugin can handle the post_command method."""
        return False

    def post_command(self, command_name: str, response: str) -> str:
        """This method is called after the command is executed.
        Args:
            command_name (str): The command name.
            response (str): The response.
        Returns:
            str: The resulting response.
        """
        pass

    def can_handle_chat_completion(
        self, messages: Dict[Any, Any], model: str, temperature: float, max_tokens: int
    ) -> bool:
        """This method is called to check that the plugin can
          handle the chat_completion method.
        Args:
            messages (List[Message]): The messages.
            model (str): The model name.
            temperature (float): The temperature.
            max_tokens (int): The max tokens.
          Returns:
              bool: True if the plugin can handle the chat_completion method."""
        return False

# maunal te
# ______________________________________________________________________________________________________________________

# trader = AutoGPTAlpacaTraderPlugin()
# print(trader)

# print(trader.get_positions())