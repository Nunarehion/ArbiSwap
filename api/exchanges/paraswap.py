import aiohttp
from urllib.parse import urlparse, parse_qs
from typing import Literal, Union

from api.services.proxy import ProxyData
from logger import logger as log


class AsyncClient:
    proxy: ProxyData
    def __init__(self, base_url: str = 'https://api.paraswap.io/', proxy = None):
        self.proxy = proxy
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
            async with session.get(url, params=params, proxy=self.proxy.proxyUrl()) as response:
                log.info(str(response.url))
                data = await response.json()
                parsed_url = urlparse(str(response.url))
                query_params = parse_qs(parsed_url.query)
                data["info"] = {
                    'url': str(response.url),
                    'status': response.status,
                    'headers': dict(response.headers),
                    'query_params': query_params,
                }
                return data

    async def get_swap(self, *args, **kwargs):
        data = (await self.get_swap_data(*args, **kwargs))
        swap_data = data['priceRoute']
        dest_usd = float(swap_data['destUSD'])
        dest_decimals = swap_data['destDecimals']
        amount = float(swap_data['destAmount']) / 10**dest_decimals

        return {"amount": amount, "destUSD": dest_usd, **data}
