import logging as log
from api.exchanges import jupiter, paraswap
from dataclasses import dataclass
from typing import Dict
from logger import logger as log


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
    paraswap_difference: float
    jupiter_USDC: float
    jupiter_difference: float
    spread_jupiter: float
    spread_paraswap: float


@dataclass
class ClientResult:
    logs: dict
    coins: list[Coin]
    amount: float
    usdc: float
    luna: float
    difference: float
    spread: float


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

    async def fetch_jupiter_data(self, input_token, output_token, amount, **kwargs):
        try:
            return await self.jupiterClient.get_swap_data(input_token, output_token, amount, **kwargs)
        except Exception as e:
            log.error(f"Error fetching data from Jupiter: {e}")
            return None

    async def fetch_paraswap_data(self, input_token, output_token, amount, **kwargs):
        try:
            return await self.paraswapClient.get_swap(input_token, output_token, amount, **kwargs)
        except Exception as e:
            log.error(f"Error fetching data from Paraswap: {e}")
            return None

    async def calc_jupiter_amount(self):
        # Получаем данные о свопе из Jupiter
        log.debug("[GET AMOUNT FROM JUPITER]")
        jupiter_response = await self.fetch_jupiter_data(
            self.input_mint.exchanges["jupiter"].token,
            self.output_mint.exchanges["jupiter"].token,
            self.amount
        )
        if jupiter_response is None:
            return None

        luna = float(jupiter_response["otherAmountThreshold"]) / 100

        # Получаем данные о свопе из Paraswap
        paraswap_response = await self.fetch_paraswap_data(
            self.output_mint.exchanges["paraswap"].token,
            self.input_mint.exchanges["paraswap"].token,
            luna,
            srcDecimals=18
        )
        if paraswap_response is None:
            return None

        usdc = paraswap_response["amount"]
        logs = {}
        logs["message"] = "[JUPITER 500USDC -> JUPITER GET LUNA -> PARASWAP GET USDC ]"
        logs["GET AMOUNT FROM JUPITER"] = {}
        logs["GET AMOUNT FROM JUPITER"]["paraswap_response"] = paraswap_response
        logs["GET AMOUNT FROM JUPITER"]["jupiter_response"] = jupiter_response
        return ClientResult(
            logs=logs,
            coins=[self.output_mint, self.input_mint],
            amount=500,
            usdc=usdc,
            luna=luna,
            difference=self.amount - usdc,
            spread=self.calc_spread(self.amount, usdc)
        )

    async def calc_paraswap_amount(self):
        try:
            # Получаем данные о свопе из Paraswap
            paraswap_response = await self.fetch_paraswap_data(
                self.input_mint.exchanges["paraswap"].token,
                self.output_mint.exchanges["paraswap"].token,
                self.amount
            )
            if paraswap_response is None:
                return None

            luna = paraswap_response["amount"]

            # Получаем данные о свопе из Jupiter
            jupiter_response = await self.fetch_jupiter_data(
                self.output_mint.exchanges["jupiter"].token,
                self.input_mint.exchanges["jupiter"].token,
                int(luna) * 100
            )
            if jupiter_response is None:
                return None

            usdc = float(jupiter_response["otherAmountThreshold"])
            logs = {}
            logs["message"] = "[PARASWAP 500USDC -> PARASWAP GET LUNA -> JUPITER GET USDC ]"
            logs["GET AMOUNT FROM PARASWAP"] = {}
            logs["GET AMOUNT FROM PARASWAP"]["paraswap_response"] = paraswap_response
            logs["GET AMOUNT FROM PARASWAP"]["jupiter_response"] = jupiter_response

            return ClientResult(
                logs=logs,
                coins=[self.output_mint, self.input_mint],
                amount=500,
                usdc=usdc,
                luna=luna,
                difference=self.amount - usdc,
                spread=self.calc_spread(self.amount, usdc)
            )
        except Exception as e:
            log.error(f"Error in calc_paraswap_amount: {e}")
            return None

    def calc_difference(self, price_bye, price_sell):
        return price_bye - price_sell

    def calc_spread(self, price_bye: float, price_sell: float):
        return abs(price_bye - price_sell) / price_bye * 100
