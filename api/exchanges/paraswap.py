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

    def getSwapData(self, srcToken: str, destToken: str, amount: float, srcDecimals: int = 6, destDecimals: int = 18, side: Literal["BUY", "SELL"] = "SELL", network: Union[int, str] = 8453, slippage: Union[int, str] = 0.5):
        url = f"{self.base_url}prices"
        params = {
            'srcToken': srcToken,
            'srcDecimals': str(srcDecimals),
            'destToken': destToken,
            'destDecimals': str(destDecimals),
            'amount': str(float(amount) * (10**srcDecimals if side == "SELL" else 10**destDecimals)),
            'network': str(network),
            'side': str(side)
        }

        response = self.session.get(url, params=params)
        # response.raise_for_status()
        print(response.url)

        return response.json()

    def getSwap(self, *args, **kwargs):
        swapData = self.getSwapData(
            *args, **kwargs)['priceRoute']
        srcUSD = float(swapData['srcUSD'])
        destUSD = float(swapData['destUSD'])
        difference = srcUSD - destUSD
        destDecimals = swapData['destDecimals']
        amount = float(swapData['destAmount']) / 10**destDecimals
        swapData = swapData['bestRoute'][0]['swaps'][0]

        swapData = swapData['swapExchanges'][0]
        gas = float(swapData['data']['gasUSD'])

        return {"amount": amount, "gas": difference, "destUSD": destUSD}
