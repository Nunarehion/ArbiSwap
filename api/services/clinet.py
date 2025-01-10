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


class Client:
    def __init__(self,
                 tokens=[
                     Coin(
                         symbol='LUNA',
                         exchanges={
                             'Paraswap': Exchange(name='Paraswap', token='0x55cd6469f597452b5a7536e2cd98fde4c1247ee4'),
                             'Jupiter': Exchange(name='Jupiter', token='9se6kma7LeGcQWyRBNcYzyxZPE3r9t9qWZ8SnjnN3jJ7')
                         }),
                     Coin(
                         symbol='USDT',
                         exchanges={
                             'Paraswap': Exchange(name='Paraswap', token='0xdac17f958d2ee523a2206206994597c13d831ec7'),
                             'Jupiter': Exchange(name='Jupiter', token='Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB')
                         }),
                 ],
                 amount=500, mode="SELL"):

        self.input_mint = tokens[0]
        self.input_amount = amount
        self.output_mint = tokens[1]
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
        print(self.get_data_jupiter())
        print(self.get_data_paraswap())

    def calc_spred():
        pass


Client().calc_amountCompare()
