"""This is a plugin to use Auto-GPT with AlpacaTrader."""
from typing import Any, Dict, List, Optional, Tuple, TypeVar, TypedDict
from auto_gpt_plugin_template import AutoGPTPluginTemplate

import pandas as pd
import numpy as np
import requests
import os
# import alpaca
# from alpaca.trading.client import TradingClient
# from alpaca.trading.requests import MarketOrderRequest
# from alpaca.trading.enums import OrderSide, TimeInForce
# from alpaca.trading.models import Position
# from datetime import datetime

# api_key = os.environ.get('APCA_API_KEY_ID')
# api_secret = os.environ.get('APCA_API_SECRET_KEY') 
# isPaper= bool(os.environ.get('IS_PAPER') )
# trading_client =  TradingClient(api_key, api_secret,paper=True)

trading_client=None

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
        )
        return prompt
# ______________________________________________________________________________________________________________________

    def close_trade(self,symbol):
        # positions = trading_client.get_all_positions()
        # for position in positions:
        #     if position.symbol == symbol:
        #         if position.side == 'long':
        #             trading_client.submit_order(
        #                 symbol=symbol,
        #                 qty=position.qty,
        #                 side='sell',
        #                 type='market',
        #                 time_in_force='gtc'
        #             )
        #         elif position.side == 'short':
        #             trading_client.submit_order(
        #                 symbol=symbol,
        #                 qty=position.qty,
        #                 side='buy',
        #                 type='market',
        #                 time_in_force='gtc'
        #             )
        print("close trade")

    def close_all_trades(self):
        # trading_client.cancel_orders()
        print("cancel orders")

    def get_account_information(self):
        # return trading_client.get_account()
        print("acct")
        return "acct"

    def get_positions(self):
        # def pos_to_json(pos):
        #     res = { "asset_id": str(pos.asset_id), "symbol": pos.symbol, "avg_entry_price": pos.avg_entry_price, "qty": pos.qty, "market_value": pos.market_value, "cost_basis": pos.cost_basis, "unrealized_pl": pos.unrealized_pl, "unrealized_plpc": pos.unrealized_plpc, "unrealized_intraday_pl": pos.unrealized_intraday_pl, "unrealized_intraday_plpc": pos.unrealized_intraday_plpc, "current_price": pos.current_price, "lastday_price": pos.lastday_price, "change_today": pos.change_today, "asset_marginable": pos.asset_marginable }
        #     return res
        # positions = trading_client.get_all_positions()
        # formatted_positions = [pos_to_json(position) for position in positions]
        # return formatted_positions
        return "get position"
    def place_trade(self,symbol, qty, side, order_type, time_in_force):
        # order_data = MarketOrderRequest(
        #     symbol=symbol,
        #     qty=qty,
        #     side=side,
        #     time_in_force=time_in_force
        # )
        # order=trading_client.submit_order(order_data)
        # print(order)
        print("place trade")

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

