from pprint import pprint

testing_modules = [
    # <--тестирование API биржи-->#
    # 'parasvap.client',
    # 'jupiter.clent',

    # <--тестирование сервиса-->#
    'service',
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

if 'parasvap.client' in testing_modules:
    from api.exchanges.paraswap import RealClient
    testes = {
        'usdc => luna': {
            'srcToken': tokens['usdc (base)'],
            'destToken': tokens['luna (base)'],
            "amount": 500,
        },
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
        client = RealClient()
        quote = client.getSwapData(**testes[key])
        price = client.getSwap(**testes[key])
        pprint(quote)
        pprint(price)


if 'jupiter.clent' in testing_modules:
    from api.exchanges.jupiter import RealClient
    testes = {
        '(jupiter) usdc => luna': {
            'inputMint': tokens['usdc (jupiter)'],
            'outputMint': tokens['luna (jupiter)'],
            "amount": 500,
        },
        # '(jupiter) usdc => goat': {
        #     'inputMint': tokens['usdc (jupiter)'],
        #     'outputMint': tokens['goat (jupiter)'],
        #     "amount": 1,
        # },
    }

    for key in testes:
        print(f"[[ {key} ]]")
        client = RealClient()
        quote = client.getSwapData(**testes[key])
        price = client.getSwap(**testes[key])
        pprint(quote)
        pprint(price)

    client = RealClient()
    input_mint = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"  # USDC
    # input_mint = "0x55cD6469F597452B5A7536e2CD98fDE4c1247ee4"
    output_mint = "9se6kma7LeGcQWyRBNcYzyxZPE3r9t9qWZ8SnjnN3jJ7"  # luna
    amount = 1
    quote = client.getSwapData(input_mint, output_mint,  amount)
    price = client.getSwap(input_mint, output_mint,  amount)
    pprint(quote)
    print(price)

if 'service' in testing_modules:
    from api.services.service import Service
    Service().calc_amountCompare()
