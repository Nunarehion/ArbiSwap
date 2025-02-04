import os
from api.exchanges import jupiter, paraswap
from dataclasses import dataclass
from typing import Dict


@dataclass
class Exchange:
    name: str
    token: str


@dataclass
class Coin:
    symbol: str
    exchanges: Dict[str, Exchange]

#  Coin(
#      symbol='LUNA',
#      exchanges={
#          'Paraswap': Exchange(name='Paraswap', token='0x55cd6469f597452b5a7536e2cd98fde4c1247ee4'),
#          'Jupiter': Exchange(name='Jupiter', token='9se6kma7LeGcQWyRBNcYzyxZPE3r9t9qWZ8SnjnN3jJ7')
#      }),


@dataclass
class ClientResult:
    coins: list[Coin]
    amount: float
    jupiter_LUNA: float
    paraswap_USDC: float
    paraswap_LUNA: float
    jupiter_USDC: float
    difference: float
    spread_jupiter: float
    spread_paraswap: float


class Service:
    def __init__(self,
                 tokens=[
                     Coin(
                         symbol='USDC',
                         exchanges={
                             'paraswap': Exchange(name='Paraswap', token='0x55cD6469F597452B5A7536e2CD98fDE4c1247ee4'),
                             'jupiter': Exchange(name='Jupiter', token='9se6kma7LeGcQWyRBNcYzyxZPE3r9t9qWZ8SnjnN3jJ7')
                         }),
                     Coin(
                         symbol='LUNA',
                         exchanges={
                             'paraswap': Exchange(name='Paraswap', token='0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913'),
                             'jupiter': Exchange(name='Jupiter', token='EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v')
                         }),
                 ],
                 amount=500, mode="SELL"):
        self.input_mint = tokens[1]
        self.amount = amount
        self.output_mint = tokens[0]
        self.jupiterClient = jupiter.AsyncClient()
        self.paraswapClient = paraswap.AsyncClient()

    async def calc_amount_compare(self):
        # luna
        jupiter_LUNA_response = await self.jupiterClient.get_swap(
            self.input_mint.exchanges["jupiter"].token,
            self.output_mint.exchanges["jupiter"].token,
            self.amount
        )
        jupiter_LUNA = jupiter_LUNA_response["amount"]

        # usdC
        paraswap_USDC_response = await self.paraswapClient.get_swap(
            self.output_mint.exchanges["paraswap"].token,
            self.input_mint.exchanges["paraswap"].token,
            jupiter_LUNA,
            srcDecimals=18,
            destDecimals=6
        )
        paraswap_USDC = paraswap_USDC_response["amount"]

        # luna
        paraswap_LUNA_response = await self.paraswapClient.get_swap(
            self.input_mint.exchanges["paraswap"].token,
            self.output_mint.exchanges["paraswap"].token,
            self.amount,
        )
        paraswap_LUNA = paraswap_LUNA_response["amount"]

        # usdC
        jupiter_USDC_response = await self.jupiterClient.get_swap(
            self.output_mint.exchanges["jupiter"].token,
            self.input_mint.exchanges["jupiter"].token,
            int(paraswap_LUNA) * 100
        )
        jupiter_USDC = float(jupiter_USDC_response["amount"]) * 100

        return ClientResult(
            coins=[self.output_mint, self.input_mint],
            amount=self.amount,
            jupiter_LUNA=jupiter_LUNA,
            paraswap_USDC=paraswap_USDC,
            paraswap_LUNA=paraswap_LUNA,
            jupiter_USDC=jupiter_USDC,
            difference=self.calc_difference(paraswap_USDC, jupiter_USDC),
            spread_jupiter=self.calc_spread(self.amount, jupiter_USDC),
            spread_paraswap=self.calc_spread(self.amount, paraswap_USDC),
        )

    def calc_difference(self, price_bye, price_sell):
        return price_bye - price_sell

    def calc_spread(self, price_bye: float, price_sell: float):
        return abs(price_bye - price_sell) / price_bye * 100
