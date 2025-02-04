import aiohttp
import asyncio
from dataclasses import dataclass
from typing import Optional, List, Union, Protocol


class AsyncClient:
    def __init__(self, base_url: str = "https://quote-api.jup.ag/v6"):
        self.base_url = base_url

    async def get_swap_data(self, input_mint: str, output_mint: str, amount: int):
        url = f"{self.base_url}/quote"
        params = {
            'inputMint': input_mint,
            'outputMint': output_mint,
            'amount': amount
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                print(response.url)
                response.raise_for_status()
                data = await response.json()
                return data

    async def get_swap(self, *args, **kwargs):
        swap_data = await self.get_swap_data(*args, **kwargs)
        print(
            f">>>>>>>>>>>> {float(swap_data['otherAmountThreshold']) / 100:.2f}")
        print(f">>>>>>>>>>>> {float(swap_data['otherAmountThreshold']) / 100}")
        return {
            "amount": f"{float(swap_data['otherAmountThreshold']) / 100:.2f}",
            "gas": swap_data["priceImpactPct"],
            "destUSD": swap_data["inAmount"]
        }


# async def main():
#     client = AsyncClient()
#     result = await client.get_swap("inputMintValue", "outputMintValue", 1000)
#     print(result)
