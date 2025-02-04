import aiohttp
import asyncio
from typing import List, Dict, Any, Literal, Union
from dataclasses import dataclass


class AsyncClient:
    def __init__(self, base_url: str = 'https://api.paraswap.io/'):
        self.base_url = base_url

    async def all_tokens(self, network: Union[int, str] = 1):
        url = f"{self.base_url}tokens/{network}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.json()

    async def get_swap_data(self, srcToken: str, destToken: str, amount: float, srcDecimals: int = 6, destDecimals: int = 18, side: Literal["BUY", "SELL"] = "SELL", network: Union[int, str] = 8453, slippage: Union[int, str] = 0.5):
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

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                print(response.url)
                return await response.json()

    async def get_swap(self, *args, **kwargs):
        swap_data = (await self.get_swap_data(*args, **kwargs))['priceRoute']
        src_usd = float(swap_data['srcUSD'])
        dest_usd = float(swap_data['destUSD'])
        difference = src_usd - dest_usd
        dest_decimals = swap_data['destDecimals']
        amount = float(swap_data['destAmount']) / 10**dest_decimals
        swap_data = swap_data['bestRoute'][0]['swaps'][0]
        swap_data = swap_data['swapExchanges'][0]
        gas = float(swap_data['data']['gasUSD'])

        return {"amount": amount, "gas": difference, "destUSD": dest_usd}

# Example usage
# async def main():
#     client = AsyncClient()
#     tokens = await client.all_tokens()
#     print(tokens)

#     swap_result = await client.get_swap("srcTokenValue", "destTokenValue", 100.0)
#     print(swap_result)

# # To run the example
# if __name__ == "__main__":
#     asyncio.run(main())
