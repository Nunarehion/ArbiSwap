import aiohttp
import asyncio
from typing import List, Dict, Any, Literal, Union
from dataclasses import dataclass
import logging as log


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
            'amount': f"{float(amount) * (10**srcDecimals if side == 'SELL' else 10**destDecimals):.0f}",
            'network': str(network),
            'side': str(side)
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                log.info(response.url)
                return await response.json()

    async def get_swap(self, *args, **kwargs):
        swap_data = (await self.get_swap_data(*args, **kwargs))['priceRoute']
        dest_usd = float(swap_data['destUSD'])
        dest_decimals = swap_data['destDecimals']
        amount = float(swap_data['destAmount']) / 10**dest_decimals

        return {"amount": amount, "destUSD": dest_usd}
