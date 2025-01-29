from pprint import pprint

testing_modules = [
    # <--тестирование API биржи-->#
    # 'parasvap.client',
    'jupiter.clent',

    # <--тестирование сервиса-->#
]

if 'parasvap.client' in testing_modules:
    from api.exchanges.paraswap import *

    client = RealClient()
    input_mint = "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599"
    # input_mint = "0x55cD6469F597452B5A7536e2CD98fDE4c1247ee4"
    output_mint = "0xdac17f958d2ee523a2206206994597c13d831ec7"
    amount = 500
    quote = client.getSwap(output_mint, input_mint,  amount)
    # quote = client.getSwapData(output_mint, input_mint,  amount)
    pprint(quote)

if 'jupiter.clent' in testing_modules:
    from api.exchanges.jupiter import *

    client = RealClient()
    input_mint = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
    # input_mint = "0x55cD6469F597452B5A7536e2CD98fDE4c1247ee4"
    output_mint = "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB"
    amount = 500
    quote = client.getSwapData(output_mint, input_mint,  amount)
    pprint(quote)


# import api.exchanges.paraswap
