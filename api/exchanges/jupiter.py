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
        return response.json()

    def getSwap(self, inputMint: str, outputMint: str, amount: int):
        swap_data = self.__get_quote(inputMint, outputMint, amount)
        return swap_data.get('routePlan', {})
