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


class Service:
    def __init__(self,
                 tokens=[
                     Coin(
                         symbol='USDC',
                         exchanges={
                             'Paraswap': Exchange(name='Paraswap', token='0x55cD6469F597452B5A7536e2CD98fDE4c1247ee4'),
                             'Jupiter': Exchange(name='Jupiter', token='9se6kma7LeGcQWyRBNcYzyxZPE3r9t9qWZ8SnjnN3jJ7')
                         }),
                     Coin(
                         symbol='LUNA',
                         exchanges={
                             'Paraswap': Exchange(name='Paraswap', token='0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913'),
                             'Jupiter': Exchange(name='Jupiter', token='EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v')
                         }),

                 ],
                 amount=500, mode="SELL"):

        self.input_mint = tokens[1]
        self.input_amount = amount
        self.output_mint = tokens[0]
        self.jupiterClient = jupiter.RealClient()
        self.paraswapClient = paraswap.RealClient()

    def get_data(self, client, base):
        print(self.input_mint.exchanges[base].token,
              self.output_mint.exchanges[base].token,
              self.input_amount)
        return client.getSwap(self.input_mint.exchanges[base].token, self.output_mint.exchanges[base].token, self.input_amount)

    def get_data_jupiter(self):
        data = self.get_data(self.jupiterClient, base="Jupiter")
        return data

    def get_data_paraswap(self):
        data = self.get_data(self.paraswapClient, base="Paraswap")
        return data

    def calc_amountCompare(self):
        pprint(self.get_data_jupiter())
        pprint(self.get_data_paraswap())

    def calc_spred():
        pass
