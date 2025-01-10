
from typing import List, Dict, Any, Literal, Union
import requests
import json
from typing import List, Dict, Any, Literal, Union
from dataclasses import dataclass
from pprint import pprint

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
    def allTokens(self, network:Union[int, str] = 1):
       pass
   
    @get("prices")
    def getSwap(self,
                  destToken: str, 
                  srcToken: str,
                  amount: int = 1000, 
                  side: Literal["BUY", "SELL"] = "BUY", 
                  network: Union[int, str] = '1', 
                  slippage: Union[int, str] = '1'):
        pass


if __name__ == "__main__":
    client = RealClient()
    input_mint  = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
    output_mint = "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB"
    amount = 500
    quote = client.getSwap(input_mint, output_mint. amount)
