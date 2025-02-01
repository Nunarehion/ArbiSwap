from dataclasses import dataclass
from typing import (Optional, List, Union, Protocol)

import requests


class RealClient:
    def __init__(self, base_url: str = "https://quote-api.jup.ag/v6"):
        self.base_url = base_url
        self.session = requests.Session()

    def getSwapData(self, inputMint: str, outputMint: str, amount: int):
        url = f"{self.base_url}/quote"
        params = {
            'inputMint': inputMint,
            'outputMint': outputMint,
            'amount': amount
        }
        response = self.session.get(url, params=params)

        response.raise_for_status()
        print(1)
        print(response.url)
        return response.json()

    def getSwap(self, *args, **kwargs):
        swap_data = self.getSwapData(*args, **kwargs)
        return {"amount": swap_data["outAmount"], "gas": swap_data["priceImpactPct"], "destUSD": swap_data["inAmount"]}
