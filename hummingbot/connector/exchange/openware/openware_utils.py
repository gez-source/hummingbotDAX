import datetime
from datetime import timezone

import re
from typing import (
    Optional,
    Tuple)

from hummingbot.client.config.config_var import ConfigVar
from hummingbot.client.config.config_methods import using_exchange


CENTRALIZED = True
EXAMPLE_PAIR = "ETH-USD"
DEFAULT_FEES = [0.001, 0.001]

KEYS = {
    "openware_api_key":
        ConfigVar(key="openware_api_key",
                  prompt="Enter your Openware API key >>> ",
                  required_if=using_exchange("openware"),
                  is_secure=True,
                  is_connect_key=True),
    "openware_api_secret":
        ConfigVar(key="openware_api_secret",
                  prompt="Enter your Openware API secret >>> ",
                  required_if=using_exchange("openware"),
                  is_secure=True,
                  is_connect_key=True),
    "openware_api_url":
        ConfigVar(key="openware_api_url",
                  prompt="Enter your Openware API URL >>> ",
                  required_if=using_exchange("openware"), 
                  is_secure=False,
                  is_connect_key=True),
    "openware_ranger_url":
        ConfigVar(key="openware_ranger_url",
                  prompt="Enter your Openware WebSockets API URL >>> ",
                  required_if=using_exchange("openware"),
                  is_secure=False,
                  is_connect_key=True),
}

def split_trading_pair(trading_pair: str) -> Optional[Tuple[str, str]]:
#    return trading_pair.replace('usdc', ''), 'usdc'
    try:
        tpstring = global_config_map.get("trading_pair_splitter").value.lower()
        #print("tpstring:!!!!!!!", tpstring)
        #tpstring = "ETH|EUR|USD".lower()
        trading_pair_splitter = re.compile(rf"^(\w+)({tpstring})$")
        m = trading_pair_splitter.match(trading_pair.lower())
        return m.group(1), m.group(2)
    except Exception as e:
        print("ERROR: Trading pair could not be split")
        return None


def convert_from_exchange_trading_pair(exchange_trading_pair: str) -> Optional[str]:
    if split_trading_pair(exchange_trading_pair) is None:
        return None
    # Openware does not split BASEQUOTE (BTCUSDT)
    base_asset, quote_asset = split_trading_pair(exchange_trading_pair)
    return f"{base_asset.upper()}-{quote_asset.upper()}"

def convert_to_exchange_trading_pair(hb_trading_pair: str) -> str:
    # Openware does not split BASEQUOTE (BTCUSDT)
    return hb_trading_pair.replace("-", "").lower()

def DateTimeToUnixTimestamp(strDate):
    # Converts a datetime with a timezone to a unix timestamp. 
    # e.g. 2021-08-09T12:14:47+02:00 is converted to 1628504087.0
    d2 = datetime.datetime.fromisoformat(strDate)
    d1 = datetime.datetime(1970, 1, 1).replace(tzinfo=datetime.timezone.utc)
    diff = d2 - d1
    timestamp = diff.total_seconds()
    return timestamp