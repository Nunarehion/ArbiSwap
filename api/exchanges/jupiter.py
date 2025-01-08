from dataclasses import dataclass
from typing import Optional, List, Union
from requests import Session
from dataclass_rest import get
from dataclass_rest.http.requests import RequestsClient
from pprint import pprint

@dataclass
class SwapInfo:
    ammKey: str
    label: str
    inputMint: str
    outputMint: str
    inAmount: str
    outAmount: str
    feeAmount: str
    feeMint: str

@dataclass
class RoutePlan:
    swapInfo: SwapInfo
    percent: float

@dataclass
class QuoteResponse:
    inputMint: str
    inAmount: str
    outputMint: str
    outAmount: str
    otherAmountThreshold: str
    swapMode: str
    slippageBps: int
    platformFee: Optional[str]
    priceImpactPct: str
    routePlan: List[RoutePlan]
    scoreReport: Optional[str]
    contextSlot: int
    timeTaken: float


class RealClient(RequestsClient):
    def __init__(self):
        super().__init__("https://quote-api.jup.ag/v6", Session())

    @get("quote")
    def __get_quote(self, inputMint: str, outputMint: str, amount: int) -> QuoteResponse:
       pass
       
    def get_quote(self, inputMint: str, outputMint: str, amount: int):
       return self.__get_quote(inputMint, outputMint, amount).routePlan

if __name__ == "__main__":
    client = RealClient()
    input_mint = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
    output_mint = "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB"
    amount = 50
    quote = client.get_quote(inputMint=input_mint, outputMint=output_mint, amount=amount)
    pprint(quote)