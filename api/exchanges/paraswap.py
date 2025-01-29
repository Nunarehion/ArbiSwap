from typing import List, Dict, Any, Literal, Union
import requests


from dataclasses import dataclass


class RealClient:
    def __init__(self, base_url: str = 'https://api.paraswap.io/'):
        self.base_url = base_url
        self.session = requests.Session()

    def allTokens(self, network: Union[int, str] = 1):
        url = f"{self.base_url}tokens/{network}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def getSwapData(self, destToken: str, srcToken: str, amount: int, srcDecimals: int = 10**6, destDecimals: int = 10**6, side: Literal["BUY", "SELL"] = "BUY", network: Union[int, str] = 1, slippage: Union[int, str] = 0.5):
        url = f"{self.base_url}prices"

        params = {
            'destToken': destToken,
            'srcToken': srcToken,
            'amount': str(amount * srcDecimals),
            'network': str(network),
            'slippage': str(slippage),
            'side': side,
        }
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def getSwap(self, *args):
        swapData = self.getSwapData(
            *args)['priceRoute']
        srcUSD = float(swapData['srcUSD'])
        destUSD = float(swapData['destUSD'])
        difference = srcUSD - destUSD

        swapData = swapData['bestRoute'][0]['swaps'][0]
        decimals = swapData['srcDecimals']
        swapData = swapData['swapExchanges'][0]
        gas = float(swapData['data']['gasUSD'])
        amount = float(swapData['srcAmount']) / 10**decimals
        return {"amount": amount, "gas": difference}
