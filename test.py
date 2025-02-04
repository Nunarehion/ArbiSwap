import asyncio
from pprint import pprint

testing_modules = [
    # <--тестирование API биржи-->#
    # 'paraswap.client',
    'jupiter.client',

    # # <--тестирование сервиса-->#
    'service'
]
tokens = {
    "luna (base)": "0x55cD6469F597452B5A7536e2CD98fDE4c1247ee4",
    "luna (eth)": "0x416cdaf616a82d7dd46e0dbf36e7d6fe412bc40e",
    "luna (jupiter)": "9se6kma7LeGcQWyRBNcYzyxZPE3r9t9qWZ8SnjnN3jJ7",

    "usdc (base)": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
    "usdc (eth)": '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48',
    "usdc (jupiter)": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",


    'wbtc (eth)': "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599",
    "wbtc (jupiter)": "3NZ9JMVBmGAqocybic2c7LQCJScmgsAZ6vQqTDzcqmJh",

    "goat (jupiter)": "CzLSujWBLFsSjncfkh59rUFqvafWcY5tzedWJSuypump"
}


async def run_paraswap_tests():
    from api.exchanges.paraswap import AsyncClient
    print("paraswap.client")

    client = AsyncClient()
    testes = {
        'usdc => luna': {
            'srcToken': tokens['usdc (base)'],
            'destToken': tokens['luna (base)'],
            "amount": 500,
        },
        # 'usdc => luna (sell)': {
        #     'srcToken': tokens['usdc (base)'],
        #     'destToken': tokens['luna (base)'],
        #     "amount": 500,
        #     "side": "BUY"
        # },
        'luna => usdc': {
            'srcToken': tokens['luna (base)'],
            'srcDecimals': 18,
            'destToken': tokens['usdc (base)'],
            'destDecimals': 6,
            "amount": 21900.66,
        },
        # 'luna => usdc (buy)': {
        #     'srcToken': tokens['luna (base)'],
        #     'srcDecimals': 18,
        #     'destToken': tokens['usdc (base)'],
        #     'destDecimals': 6,
        #     "amount": 21900,
        #     "side": "BUY"
        # },

        # '(eth) usdc => luna': {
        #     'srcToken': tokens['usdc (eth)'],
        #     'destToken': tokens['luna (eth)'],
        #     "amount": 500,
        #     "network": 1,
        # },
        # 'usdc => wbtc': {
        #     'srcToken': tokens['usdc (eth)'],
        #     'destToken': tokens['wbtc (eth)'],
        #     "amount": 500,
        #     "network": 1,
        #     "destDecimals": 6
        # },
    }

    for key in testes:
        print(f"[[ {key} ]]")
        price = await client.get_swap(**testes[key])
        pprint(price)
        print("____________________________________" + "\n")


async def run_jupiter_tests():
    from api.exchanges.jupiter import AsyncClient
    print('jupiter.client')

    client = AsyncClient()
    testes = {
        '(jupiter) usdc => luna': {
            'inputMint': tokens['usdc (jupiter)'],
            'outputMint': tokens['luna (jupiter)'],
            "amount": 500,
        },
        '(jupiter) usdc => goat': {
            'inputMint': tokens['usdc (jupiter)'],
            'outputMint': tokens['goat (jupiter)'],
            "amount": 500,
        },
    }

    for key in testes:
        print(f"[[ {key} ]]")
        price = await client.get_swap(**testes[key])
        pprint(price)
        print("____________________________________" + "\n")


async def run_service_tests():
    from api.services.service import Service
    print('test service')

    service = Service()
    result = await service.calc_amount_compare()
    pprint(result)


async def main():
    if 'paraswap.client' in testing_modules:
        await run_paraswap_tests()

    if 'jupiter.client' in testing_modules:
        await run_jupiter_tests()

    if 'service' in testing_modules:
        await run_service_tests()


if __name__ == "__main__":
    asyncio.run(main())
