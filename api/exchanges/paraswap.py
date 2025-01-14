
from typing import List, Dict, Any, Literal, Union
import requests
import json
from typing import List, Dict, Any, Literal, Union
from dataclasses import dataclass


from requests import Session
from dataclass_rest.http.requests import RequestsClient
from dataclass_rest import get


@dataclass
class TokenData:
    address: str
    decimals: int
    img: str
    network: int
    symbol: str


@dataclass
class Pool:
    address: str
    direction: bool
    fee: int


@dataclass
class SwapData:
    factory: str
    feeFactor: int
    gasUSD: str
    initCode: str
    path: List[str]
    pools: List[Pool]
    router: str


@dataclass
class SwapExchange:
    data: SwapData
    destAmount: str
    exchange: str
    percent: int
    poolAddresses: List[str]
    srcAmount: str


@dataclass
class BestRoute:
    percent: int
    swaps: List[SwapExchange]


@dataclass
class PriceRoute:
    bestRoute: List[BestRoute]
    blockNumber: int
    contractAddress: str
    contractMethod: str
    destAmount: str
    destDecimals: int
    destToken: str
    destUSD: str
    gasCost: str
    gasCostUSD: str
    hmac: str
    maxImpactReached: bool
    network: int
    partner: str
    partnerFee: int
    side: str
    srcAmount: str
    srcDecimals: int
    srcToken: str
    srcUSD: str
    tokenTransferProxy: str
    version: str


@dataclass
class PriceResponse:
    priceRoute: PriceRoute


class RealClient(RequestsClient):
    def __init__(self):
        super().__init__('https://api.paraswap.io/', Session())

    @get("tokens/{network}")
    def allTokens(self, network: Union[int, str] = 1):
        pass

    @get("prices")
    def __getSwap(self,
                  destToken: str,
                  srcToken: str,
                  amount: int = 1000,
                  srcDecimals: int = 6,
                  destDecimals: int = 18,
                  side: Literal["BUY", "SELL"] = "BAY",
                  network: Union[int, str] = '1',
                  slippage: Union[int, str] = '0.5'):
        pass

    def getSwap(self,  destToken: str, srcToken: str, amount: int = 1000, srcDecimals: int = 6, destDecimals: int = 18, side: Literal["BUY", "SELL"] = "SELL", network: Union[int, str] = '1', slippage: Union[int, str] = '0.5'):
        amount *= 10**18
        return self.__getSwap(destToken, srcToken, amount, srcDecimals, destDecimals, side, network, slippage)


if __name__ == "__api.exchanges.paraswap":
    from pprint import pprint
    client = RealClient()
    input_mint = "0x55cd6469f597452b5a7536e2cd98fde4c1247ee4"
    output_mint = "0xdac17f958d2ee523a2206206994597c13d831ec7"
    amount = 500
    quote = client.getSwap(input_mint, output_mint, amount)
    pprint(quote)
