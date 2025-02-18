import aiohttp

from api.services.proxy import ProxyData
from api.services.service import proxys
from logger import logger as log
from urllib.parse import urlparse, parse_qs
import logging


class AsyncClient:
    proxy: ProxyData
    def __init__(self, base_url: str = "https://quote-api.jup.ag/v6", proxy = None):
        # "https://ultra-api.jup.ag"
        # "https://quote-api.jup.ag/v6"
        self.base_url = base_url
        self.proxy = proxy

    async def get_swap_data(self, inputMint: str, outputMint: str, amount: int):
        # "/quote"
        # /order
        url = f"{self.base_url}/quote"
        params = {
            'inputMint': inputMint,
            'outputMint': outputMint,
            'amount': amount,
            "platformFeeBps": 10,
        }
        # &slippageBps=50&restrictIntermediateTokens=true&platformFeeBps=20'
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, proxy=self.proxy.proxyUrl()) as response:
                response.raise_for_status()
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
        swap_data = await self.get_swap_data(*args, **kwargs)
        return {
            "amount": f"{float(swap_data['otherAmountThreshold']) / 100:.2f}",
            "gas": swap_data["priceImpactPct"],
            "destUSD": swap_data["inAmount"]
        }


# async def main():
#     client = AsyncClient()
#     result = await client.get_swap("inputMintValue", "outputMintValue", 1000)
#     print(result)
