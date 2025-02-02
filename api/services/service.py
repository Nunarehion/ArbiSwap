import os
from api.exchanges import jupiter, paraswap
from dataclasses import dataclass
from typing import Dict
from pprint import pprint


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
class ClinentResult:
    coins: list[Coin]
    amount: float
    paraswap_amount: float
    jupiter_amount: float
    spred: float


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
        self.jupiterClient = jupiter.RealClient()
        self.paraswapClient = paraswap.RealClient()

    def calc_amountCompare(self):
        jupiter_amount = self.jupiterClient.getSwap(
            self.input_mint.exchanges["jupiter"].token,
            self.output_mint.exchanges["jupiter"].token,
            self.amount)["amount"]

        paraswap_amount = self.paraswapClient.getSwap(
            self.output_mint.exchanges["paraswap"].token,
            self.input_mint.exchanges["paraswap"].token,
            jupiter_amount,
            srcDecimals=18,
            destDecimals=6
        )["amount"]

        return ClinentResult(
            coins=[self.output_mint, self.input_mint],
            amount=self.amount,
            jupiter_amount=jupiter_amount,
            paraswap_amount=paraswap_amount,
            spred=self.calc_spred(self.amount, paraswap_amount)
        )

    def calc_spred(self, price_bye: float, price_buy: float):
        return price_bye/price_buy
